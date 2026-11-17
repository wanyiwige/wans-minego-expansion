package cn.wanyiwige.minego;

import java.util.*;
import cn.wanyiwige.minego.MaterialSoulStoneItem.Kind;
import io.redspace.ironsspellbooks.damage.SpellDamageSource;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.damagesource.*;
import net.minecraft.world.effect.*;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.living.*;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.eventbus.api.*;

public final class MaterialSoulEvents {
    private static final UUID SLIDE=UUID.fromString("4bd2b143-8b8b-4256-af84-3f17433da326");
    private static final UUID STEEL=UUID.fromString("58093258-d262-46b0-a3c5-c1ab39502892");
    private static final Map<UUID,State> STATES=new HashMap<>();
    private static class State { final Map<String,Long> cooldowns=new HashMap<>(); int sprint,fire; }
    private static State state(ServerPlayer p){return STATES.computeIfAbsent(p.getUUID(),key->new State());}
    private static long now(ServerPlayer p){return p.server.overworld().getGameTime();}
    private static boolean ready(ServerPlayer p,String key){return now(p)>=state(p).cooldowns.getOrDefault(key,0L);}
    private static void cool(ServerPlayer p,String key,String config){state(p).cooldowns.put(key,now(p)+MaterialSoulConfig.ticks(config));}
    private static boolean direct(DamageSource source){
        return !BossSoulEvents.secondary(source) && source.getEntity() instanceof ServerPlayer
            && (source instanceof SpellDamageSource || source.getDirectEntity()==source.getEntity()
                || source.getDirectEntity() instanceof net.minecraft.world.entity.projectile.Projectile)
            && (!source.is(DamageTypeTags.IS_FIRE) || source instanceof SpellDamageSource) && !source.is(DamageTypes.THORNS);
    }
    @SubscribeEvent(priority=EventPriority.LOW) public static void hurt(LivingHurtEvent event){
        if(event.getEntity().level().isClientSide || BossSoulEvents.secondary(event.getSource()))return;
        if(event.getSource().getEntity() instanceof ServerPlayer p && direct(event.getSource()) && p.isOnFire()
                && MaterialSoulStoneItem.equipped(p).contains(Kind.INFERNAL)
                && !BiomeSoulStoneItem.equipped(p).contains(BiomeSoulStoneItem.Kind.ASH) && BossSoulEvents.enemy(p,event.getEntity()))
            event.setAmount((float)(event.getAmount()*(1+MaterialSoulConfig.v("infernal.burning_bonus"))));
    }
    @SubscribeEvent(priority=EventPriority.LOWEST) public static void damage(LivingDamageEvent event){
        if(event.getEntity().level().isClientSide || BossSoulEvents.secondary(event.getSource()) || event.getAmount()<=0)return;
        if(event.getEntity() instanceof ServerPlayer p && MaterialSoulStoneItem.equipped(p).contains(Kind.SOULCOAT)
                && event.getSource().getEntity() instanceof LivingEntity attacker && BossSoulEvents.enemy(p,attacker)
                && p.distanceToSqr(attacker)<=Math.pow(MaterialSoulConfig.v("soulcoat.range"),2) && p.hasLineOfSight(attacker) && ready(p,"ward")){
            cool(p,"ward","soulcoat.cooldown");
            SoulBoltEntity.launchWard(p,attacker,(float)Math.min(MaterialSoulConfig.v("soulcoat.damage_cap"),
                BossSoulMath.effectiveDamage(p.getHealth(),event.getAmount())*MaterialSoulConfig.v("soulcoat.ratio")));
        }
        if(event.getSource().getEntity() instanceof ServerPlayer p && direct(event.getSource()) && BossSoulEvents.enemy(p,event.getEntity())
                && MaterialSoulStoneItem.equipped(p).contains(Kind.PARASITIC) && ready(p,"regen")){
            cool(p,"regen","parasite.cooldown");
            p.addEffect(new MobEffectInstance(MobEffects.REGENERATION,MaterialSoulConfig.ticks("parasite.regen_seconds"),0));
        }
    }
    private static void transientModifier(ServerPlayer p,Attribute attribute,UUID id,double value,AttributeModifier.Operation operation){
        var instance=p.getAttribute(attribute);if(instance==null)return;
        var old=instance.getModifier(id);
        if(old!=null && Math.abs(old.getAmount()-value)<.000001)return;
        instance.removeModifier(id);
        if(value>0)instance.addTransientModifier(new AttributeModifier(id,"wan_material_conditional",value,operation));
    }
    @SubscribeEvent public static void tick(TickEvent.PlayerTickEvent event){
        if(event.phase!=TickEvent.Phase.END || !(event.player instanceof ServerPlayer p))return;
        var equipped=MaterialSoulStoneItem.equipped(p);State s=STATES.get(p.getUUID());
        if(equipped.isEmpty() && s==null)return;
        s=state(p);
        if(p.isAlive() && equipped.contains(Kind.SLIDE) && p.isSprinting())s.sprint=Math.min(MaterialSoulConfig.ticks("slide.ramp_seconds"),s.sprint+1);
        else s.sprint=0;
        // Immediate reset on stopping/unequipping; updates are otherwise quantized to once a second.
        if(s.sprint==0 || p.tickCount%20==0)transientModifier(p,Attributes.MOVEMENT_SPEED,SLIDE,
            MaterialSoulConfig.v("slide.max_speed")*s.sprint/MaterialSoulConfig.ticks("slide.ramp_seconds"),AttributeModifier.Operation.MULTIPLY_BASE);
        double steel=p.isAlive() && equipped.contains(Kind.KEEPSTEEL) && p.getHealth()<p.getMaxHealth()*MaterialSoulConfig.v("steel.low_health")
                ?MaterialSoulConfig.v("steel.low_knockback"):0;
        transientModifier(p,Attributes.KNOCKBACK_RESISTANCE,STEEL,steel,AttributeModifier.Operation.ADDITION);
        if(equipped.contains(Kind.INFERNAL) && !BiomeSoulStoneItem.equipped(p).contains(BiomeSoulStoneItem.Kind.ASH)){
            int fire=Math.max(0,p.getRemainingFireTicks());
            if(fire>s.fire)p.setRemainingFireTicks((int)(fire*(1-MaterialSoulConfig.v("infernal.burn_reduction"))));
            s.fire=Math.max(0,p.getRemainingFireTicks());
        }else s.fire=0;
    }
    @SubscribeEvent public static void logout(PlayerEvent.PlayerLoggedOutEvent event){STATES.remove(event.getEntity().getUUID());}
    private MaterialSoulEvents(){}
}
