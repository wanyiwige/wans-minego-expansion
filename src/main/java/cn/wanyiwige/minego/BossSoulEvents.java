package cn.wanyiwige.minego;

import java.util.*;
import cn.wanyiwige.minego.BossSoulStoneItem.Kind;
import io.redspace.ironsspellbooks.api.events.SpellOnCastEvent;
import io.redspace.ironsspellbooks.api.magic.MagicData;
import io.redspace.ironsspellbooks.damage.SpellDamageSource;
import io.redspace.ironsspellbooks.entity.mobs.IMagicSummon;
import io.redspace.ironsspellbooks.network.SyncManaPacket;
import io.redspace.ironsspellbooks.setup.PacketDistributor;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.damagesource.*;
import net.minecraft.world.effect.*;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.living.*;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.eventbus.api.*;

public final class BossSoulEvents {
    private static final TagKey<DamageType> SECONDARY = TagKey.create(Registries.DAMAGE_TYPE, id("secondary"));
    private static final TagKey<EntityType<?>> BOSSES = TagKey.create(Registries.ENTITY_TYPE, new ResourceLocation("forge", "bosses"));
    private static final Map<UUID, State> STATES = new HashMap<>();
    private static class State {
        final Map<String, Long> cooldowns = new HashMap<>();
        long combat, riposte, healWindow; float healed;
        Refund refund;
    }
    private record Refund(long due, float before, float cost) {}
    private static State state(Player p) { return STATES.computeIfAbsent(p.getUUID(), k -> new State()); }
    private static ResourceLocation id(String key) { return new ResourceLocation(WansMinegoExpansion.MOD_ID, key); }
    private static double v(String key) { return BossSoulConfig.value(key); }
    private static long now(LivingEntity e) { return e.level().getGameTime(); }
    private static boolean ready(Player p, String key) { return now(p) >= state(p).cooldowns.getOrDefault(key, 0L); }
    private static void cool(Player p, String key, String duration) { state(p).cooldowns.put(key, now(p) + BossSoulConfig.ticks(duration)); }
    private static boolean roll(Player p, String key) { return p.getRandom().nextFloat() < BossSoulConfig.chance(key); }
    public static boolean secondary(DamageSource source) { return source.is(SECONDARY); }
    private static boolean magic(DamageSource source, String school) {
        return source.is(TagKey.create(Registries.DAMAGE_TYPE, new ResourceLocation("irons_spellbooks", school + "_magic")))
                || school.equals("tainted") && source.is(net.minecraft.resources.ResourceKey.create(Registries.DAMAGE_TYPE,
                    new ResourceLocation("bielgg_spells", "tainted_magic")));
    }
    private static boolean direct(DamageSource source) {
        return !secondary(source) && source.getEntity() instanceof Player
                && (source instanceof SpellDamageSource || source.getDirectEntity() == source.getEntity()
                    || source.getDirectEntity() instanceof net.minecraft.world.entity.projectile.Projectile)
                && (!source.is(DamageTypeTags.IS_FIRE) || source instanceof SpellDamageSource)
                && !source.is(DamageTypes.THORNS);
    }
    public static boolean enemy(Player owner, LivingEntity target) {
        if (target == null || target == owner || !target.isAlive() || target.isSpectator() || owner.isAlliedTo(target) || target.isAlliedTo(owner)) return false;
        if (target instanceof TamableAnimal pet && owner.getUUID().equals(pet.getOwnerUUID())) return false;
        if (target instanceof IMagicSummon summon && summon.getSummoner() != null
                && (summon.getSummoner() == owner || owner.isAlliedTo(summon.getSummoner()))) return false;
        if (target instanceof Player other && !owner.canHarmPlayer(other)) return false;
        return true;
    }
    private static Player summoner(Entity entity) {
        if (entity instanceof IMagicSummon summon && summon.getSummoner() instanceof Player p) return p;
        if (entity instanceof TamableAnimal pet && pet.getOwner() instanceof Player p) return p;
        return null;
    }
    private static List<LivingEntity> nearby(Player p, LivingEntity target, double range) {
        var list = p.level().getEntitiesOfClass(LivingEntity.class, target.getBoundingBox().inflate(range),
                e -> e != target && enemy(p, e) && (e instanceof net.minecraft.world.entity.monster.Enemy
                    || e.getType().is(BOSSES) || e instanceof Mob mob && mob.getTarget() == p
                    || e instanceof Player && p.getLastHurtMob() == e)
                    && e.distanceToSqr(target) <= range * range && target.hasLineOfSight(e));
        list.sort(Comparator.comparingDouble(target::distanceToSqr)); return list;
    }
    public static DamageSource source(ServerPlayer owner, String kind, Entity direct) {
        var holder = owner.level().registryAccess().registryOrThrow(Registries.DAMAGE_TYPE)
                .getHolderOrThrow(net.minecraft.resources.ResourceKey.create(Registries.DAMAGE_TYPE, id(kind)));
        return new DamageSource(holder, direct, owner);
    }
    private static void hit(ServerPlayer p, LivingEntity target, float amount, String kind) {
        if (amount > 0 && enemy(p, target)) target.hurt(source(p, kind, p), amount);
    }
    private static void effect(LivingEntity target, MobEffect effect, int ticks) {
        var instance = new MobEffectInstance(effect, ticks, 0);
        if (target.canBeAffected(instance)) target.addEffect(instance);
    }
    private static void line(ServerLevel level, Vec3 from, Vec3 to, boolean electric) {
        int count = Math.min(48, Math.max(3, (int)(from.distanceTo(to) * 6)));
        for (int i=0;i<=count;i++) {
            var pos = from.lerp(to, i/(double)count);
            level.sendParticles(electric ? ParticleTypes.ELECTRIC_SPARK : ParticleTypes.ENCHANT, pos.x, pos.y, pos.z, 1, .025, .025, .025, 0);
        }
    }

    @SubscribeEvent(priority = EventPriority.LOW)
    public static void hurt(LivingHurtEvent event) {
        if (event.getEntity().level().isClientSide || secondary(event.getSource())) return;
        var target = event.getEntity(); var src = event.getSource(); float amount = event.getAmount();
        var summonOwner = summoner(src.getEntity());
        if (summonOwner != null && BossSoulStoneItem.equipped(summonOwner).contains(Kind.SCARLANT_QUEEN) && enemy(summonOwner, target))
            amount *= 1 + v("queen.summon_bonus");
        if (src.getEntity() instanceof ServerPlayer p && direct(src) && enemy(p, target)) {
            var a = BossSoulStoneItem.equipped(p);
            if (a.contains(Kind.PYRE) && target.isOnFire()) amount *= 1 + v(magic(src,"fire") ? "pyre.fire_spell_bonus" : "pyre.burning_bonus");
            if (a.contains(Kind.THRASHER) && p.isInWater()) amount *= 1 + v("thrasher.water_bonus");
            if (a.contains(Kind.VARMINT_KING) && target.hasEffect(MobEffects.POISON) && (magic(src,"nature") || magic(src,"tainted"))) amount *= 1 + v("varmint.spell_bonus");
            if (a.contains(Kind.WENDIGRUDGE)) {
                double hp = p.getHealth()/p.getMaxHealth(), start=v("wraith.start_hp"), peak=v("wraith.peak_hp");
                amount *= 1 + BossSoulMath.lowHealthBonus(hp,start,peak,v("wraith.bonus"));
            }
            if (a.contains(Kind.ASTRALIS) && now(p) < state(p).riposte) amount *= 1 + v("star.riposte_bonus");
        }
        if (target instanceof ServerPlayer p) {
            var a = BossSoulStoneItem.equipped(p);
            if (a.contains(Kind.PYRE) && src.is(DamageTypeTags.IS_FIRE)) amount *= 1 - Math.min(1,v("pyre.fire_reduction"));
            if (a.contains(Kind.ASTRALIS) && src.getEntity() instanceof LivingEntity attacker && enemy(p, attacker)
                    && ready(p,"parry") && roll(p,"star.parry_chance")) {
                amount *= 1 - Math.min(1,v("star.parry_reduction")); cool(p,"parry","star.parry_cooldown");
                state(p).riposte=now(p)+BossSoulConfig.ticks("star.riposte_seconds");
                ((ServerLevel)p.level()).sendParticles(ParticleTypes.END_ROD,p.getX(),p.getY()+1,p.getZ(),16,.6,.6,.6,.05);
            }
        }
        event.setAmount(Math.max(0,amount));
    }

    @SubscribeEvent(priority = EventPriority.LOWEST)
    public static void damage(LivingDamageEvent event) {
        if (event.getEntity().level().isClientSide || secondary(event.getSource()) || event.getAmount()<=0) return;
        LivingEntity target=event.getEntity(); var src=event.getSource(); float actual=BossSoulMath.effectiveDamage(target.getHealth(),event.getAmount());
        if (target instanceof ServerPlayer defender) {
            state(defender).combat=now(defender)+BossSoulConfig.ticks("common.combat_seconds");
            if (BossSoulStoneItem.equipped(defender).contains(Kind.SACILIC_ABOMINATION)
                    && src.getEntity() instanceof LivingEntity attacker && enemy(defender,attacker)
                    && defender.distanceToSqr(attacker)<=Math.pow(v("crystal.reflect_range"),2) && ready(defender,"reflect")) {
                cool(defender,"reflect","crystal.reflect_cooldown");
                hit(defender,attacker,(float)Math.min(v("crystal.reflect_cap"),v("crystal.reflect_flat")+actual*v("crystal.reflect_ratio")),"soul_crystal");
                line((ServerLevel)defender.level(),defender.getEyePosition(),attacker.getEyePosition(),false);
            }
        }
        if (!(src.getEntity() instanceof ServerPlayer p) || !direct(src) || !enemy(p,target)) return;
        var a=BossSoulStoneItem.equipped(p); if(a.isEmpty()) return;
        State s=state(p); s.combat=now(p)+BossSoulConfig.ticks("common.combat_seconds");
        // Healing budget is independent of the general proc gate and includes every original valid hit.
        if (a.contains(Kind.TERRORFLORA)) {
            if (now(p)-s.healWindow>=20) {s.healWindow=now(p);s.healed=0;}
            float heal=BossSoulMath.healing(actual,v("flora.heal_ratio"),v("flora.heal_per_second"),s.healed);
            if(heal>0){s.healed+=heal;p.heal(heal);}
        }
        if(!ready(p,"proc"))return; cool(p,"proc","common.proc_gate");
        boolean spell=src instanceof SpellDamageSource;
        boolean boss=target.getType().is(BOSSES) || !target.canChangeDimensions();
        String targetKey=target.getUUID().toString();
        if(a.contains(Kind.PYRE) && ready(p,"ignite:"+targetKey)){
            cool(p,"ignite:"+targetKey,"pyre.hit_gate_seconds");
            if(roll(p,"pyre.ignite_chance"))target.setSecondsOnFire((int)v("pyre.ignite_seconds"));
        }
        if(a.contains(Kind.TIMEWELDER) && ready(p,"time") && roll(p,spell?"timewelder.spell_chance":"timewelder.chance")){
            cool(p,"time","timewelder.cooldown");effect(target,BossSoulEffects.TIME_SLOW.get(),BossSoulConfig.ticks("timewelder.duration"));
            effect(p,BossSoulEffects.TIME_SPEED.get(),BossSoulConfig.ticks("timewelder.duration"));
        }
        if(a.contains(Kind.THRASHER) && ready(p,"splash")){
            var others=nearby(p,target,v("thrasher.radius"));
            if(!others.isEmpty()) {cool(p,"splash","thrasher.cooldown");
                others.stream().limit((long)v("thrasher.targets")).forEach(e->{hit(p,e,(float)(actual*v(spell?"thrasher.spell_ratio":"thrasher.splash_ratio")),"soul_splash");
                    ((ServerLevel)p.level()).sendParticles(ParticleTypes.SPLASH,e.getX(),e.getY()+.5,e.getZ(),12,.4,.3,.4,.05);});}
        }
        if(a.contains(Kind.SACILIC_ABOMINATION) && ready(p,"stagger") && roll(p,"crystal.stagger_chance")){
            cool(p,"stagger","crystal.stagger_cooldown");effect(target,boss?BossSoulEffects.CRYSTAL_SLOW.get():BossSoulEffects.ROOTED.get(),BossSoulConfig.ticks("crystal.stagger_seconds"));
        }
        if(a.contains(Kind.VARMINT_KING)) {
            boolean poisoned=target.hasEffect(MobEffects.POISON);
            effect(target,MobEffects.POISON,BossSoulConfig.ticks("varmint.poison_seconds"));
            if(poisoned && ready(p,"corrode:"+targetKey)) {cool(p,"corrode:"+targetKey,"varmint.hit_gate");
                if(roll(p,"varmint.corrosion_chance"))effect(target,BossSoulEffects.CORROSION.get(),BossSoulConfig.ticks("varmint.corrosion_seconds"));}
        }
        if(a.contains(Kind.THUNDERBIRD) && ready(p,"storm") && (magic(src,"lightning") || roll(p,"thunderbird.chance"))) {
            var others=nearby(p,target,v("thunderbird.radius"));
            if(!others.isEmpty()){cool(p,"storm","thunderbird.cooldown");LivingEntity from=target;
                for(int i=0;i<Math.min(2,others.size());i++){var e=others.get(i);line((ServerLevel)p.level(),from.getEyePosition(),e.getEyePosition(),true);
                    hit(p,e,(float)Math.min(v("thunderbird.damage_cap"),actual*v(i==0?"thunderbird.first_ratio":"thunderbird.second_ratio")),"soul_lightning");from=e;}
                effect(p,BossSoulEffects.STORM_SPEED.get(),BossSoulConfig.ticks("thunderbird.speed_seconds"));}
        }
        if(a.contains(Kind.SCARLANT_QUEEN) && ready(p,"queen") && roll(p,spell?"queen.spell_chance":"queen.chance")) {
            long count=p.level().getEntitiesOfClass(SoulAntEntity.class,p.getBoundingBox().inflate(64),e->e.getSummoner()==p).size();
            if(count<v("queen.max_ants")){var ant=BossSoulEntities.ANT.get().create(p.level());
                if(ant!=null){ant.moveTo(target.getX()+1,target.getY(),target.getZ(),0,0);
                    if(p.level().noCollision(ant)){ant.configure(p,target);p.level().addFreshEntity(ant);cool(p,"queen","queen.cooldown");}}}
        }
        if(a.contains(Kind.TERRORFLORA) && ready(p,"root") && roll(p,magic(src,"nature")?"flora.nature_chance":"flora.chance")){
            cool(p,"root","flora.cooldown");effect(target,boss?BossSoulEffects.FLORA_SLOW.get():BossSoulEffects.ROOTED.get(),BossSoulConfig.ticks("flora.root_seconds"));
        }
        if(a.contains(Kind.WENDIGRUDGE) && ready(p,"wraith") && roll(p,"wraith.chance")){
            cool(p,"wraith","wraith.cooldown");SoulBoltEntity.launch(p,target,(float)Math.min(v("wraith.damage_cap"),actual*v("wraith.ratio")),false);
        }
        if(a.contains(Kind.ASTRALIS) && ready(p,"star") && roll(p,spell?"star.spell_chance":"star.chance")){
            cool(p,"star","star.cooldown");SoulBoltEntity.launch(p,target,(float)Math.min(v("star.damage_cap"),actual*v("star.ratio")),true);
        }
        // Expire per-target gates, retaining active cooldowns across equipment swaps.
        if(s.cooldowns.size()>256)s.cooldowns.entrySet().removeIf(e->e.getValue()<now(p));
    }

    @SubscribeEvent(priority=EventPriority.LOWEST)
    public static void cast(SpellOnCastEvent event){
        if(!(event.getEntity() instanceof ServerPlayer p) || p.isCreative() || !event.getCastSource().consumesMana()
                || !BossSoulStoneItem.equipped(p).contains(Kind.TIMEWELDER) || event.getManaCost()<=0
                || MagicData.getPlayerMagicData(p).getPlayerRecasts().hasRecastForSpell(event.getSpellId())
                || !ready(p,"refund") || state(p).refund!=null || !roll(p,"timewelder.refund_chance"))return;
        state(p).refund=new Refund(now(p)+1,MagicData.getPlayerMagicData(p).getMana(),event.getManaCost());
    }
    @SubscribeEvent
    public static void tick(TickEvent.PlayerTickEvent event){
        if(event.phase!=TickEvent.Phase.END || !(event.player instanceof ServerPlayer p))return;
        State s=STATES.get(p.getUUID());if(s==null)return;
        if(s.refund!=null && now(p)>=s.refund.due){
            var r=s.refund;s.refund=null;var data=MagicData.getPlayerMagicData(p);
            float paid=BossSoulMath.paidMana(r.cost,r.before,data.getMana());
            if(paid>0 && BossSoulStoneItem.equipped(p).contains(Kind.TIMEWELDER)){
                data.addMana((float)Math.min(v("timewelder.refund_cap"),paid*v("timewelder.refund_ratio")));
                cool(p,"refund","timewelder.refund_cooldown");PacketDistributor.sendToPlayer(p,new SyncManaPacket(data));}
        }
        if(p.isAlive() && s.combat>now(p) && p.getHealth()<p.getMaxHealth()*v("wraith.start_hp")
                && ready(p,"regen") && BossSoulStoneItem.equipped(p).contains(Kind.WENDIGRUDGE)){
            cool(p,"regen","wraith.heal_interval");p.heal((float)Math.min(v("wraith.heal"),p.getMaxHealth()*v("wraith.start_hp")-p.getHealth()));}
    }
    @SubscribeEvent public static void logout(PlayerEvent.PlayerLoggedOutEvent event){STATES.remove(event.getEntity().getUUID());}
    private BossSoulEvents(){}
}
