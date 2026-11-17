package cn.wanyiwige.minego;

import java.util.*;
import cn.wanyiwige.minego.EpochSoulStoneItem.Kind;
import io.redspace.ironsspellbooks.api.events.SpellOnCastEvent;
import io.redspace.ironsspellbooks.api.magic.MagicData;
import io.redspace.ironsspellbooks.api.registry.AttributeRegistry;
import io.redspace.ironsspellbooks.damage.SpellDamageSource;
import io.redspace.ironsspellbooks.entity.mobs.IMagicSummon;
import io.redspace.ironsspellbooks.network.SyncManaPacket;
import io.redspace.ironsspellbooks.setup.PacketDistributor;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.*;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.*;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.living.*;
import net.minecraftforge.event.entity.player.*;
import net.minecraftforge.eventbus.api.*;
import net.minecraftforge.registries.ForgeRegistries;

public final class EpochSoulEvents {
    private static final Map<UUID,State> STATES = new HashMap<>();
    private static final UUID TOUGH = UUID.fromString("9e9c1eda-b22f-42f4-b384-0c8ac34883d1");
    private static final UUID REGEN = UUID.fromString("e0b5d36c-b010-4f1b-a662-2e03008a6612");
    private static final UUID WARD = UUID.fromString("57b9c367-33df-492e-8a39-bd301960d633");
    private static final UUID BRACE = UUID.fromString("1e82ae26-00ae-4ad2-9d29-d818172a7149");
    private static final String[] BIOMES = {"descenjadeshoal","speclumeforest","bambusmulberrywetland","grazingmoonfield",
            "craneplumeocean","battlefieldwasteland","archaicfadetimberland","splendourablazehills"};
    public static java.util.List<String> progressBiomes() { return java.util.List.of(BIOMES); }
    private static class State {
        final Map<String,Long> cd = new HashMap<>();
        final Map<UUID,Long> poisoned = new HashMap<>();
        final List<Burst> bursts = new ArrayList<>();
        int pressure, magnet, fire, glyphs, bell, formation, visitTicks;
        long tough, xp, riposte, ranged, ghost, creditUntil;
        boolean ownsInvisibility;
        float credit;
        Payment payment;
        String visit = "";
    }
    private record Payment(long due, float before, int cost, boolean fire, EnumSet<Kind> abilities) {}
    private record Burst(long due, UUID target, ResourceLocation dimension, Kind ability, float damage) {}
    private static State state(ServerPlayer p) { return STATES.computeIfAbsent(p.getUUID(), id -> new State()); }
    private static long now(ServerPlayer p) { return p.server.overworld().getGameTime(); }
    private static double v(String key) { return EpochSoulConfig.v(key); }
    private static boolean ready(ServerPlayer p,String key) { return now(p) >= state(p).cd.getOrDefault(key,0L); }
    private static void cool(ServerPlayer p,String key,String config) { state(p).cd.put(key,now(p)+EpochSoulConfig.ticks(config)); }
    private static boolean proc(ServerPlayer p,String key,String config) {
        if (!ready(p,"shared") || !ready(p,key)) return false;
        cool(p,"shared","common.shared_gate"); cool(p,key,config); return true;
    }
    private static boolean direct(DamageSource src) {
        return !BossSoulEvents.secondary(src) && src.getEntity() instanceof ServerPlayer
                && (src instanceof SpellDamageSource || src.getDirectEntity() == src.getEntity() || src.getDirectEntity() instanceof Projectile)
                && (!src.is(DamageTypeTags.IS_FIRE) || src instanceof SpellDamageSource)
                && !src.is(net.minecraft.world.damagesource.DamageTypes.THORNS);
    }
    private static Player owner(Entity e) {
        if (e instanceof Player p) return p;
        if (e instanceof IMagicSummon s && s.getSummoner() instanceof Player p) return p;
        if (e instanceof TamableAnimal t && t.getOwner() instanceof Player p) return p;
        return null;
    }
    private static boolean ownSummon(ServerPlayer p,LivingEntity e) { return e != p && owner(e) == p; }
    private static boolean inRange(ServerPlayer p,LivingEntity e) {
        return p.distanceToSqr(e) <= v("common.range")*v("common.range") && p.hasLineOfSight(e);
    }
    private static void effect(LivingEntity e,MobEffect effect,int duration,int amplifier) {
        var instance=new MobEffectInstance(effect,duration,amplifier);
        if (e.canBeAffected(instance)) e.addEffect(instance);
    }
    private static void queue(ServerPlayer p,LivingEntity target,Kind kind,double damage) {
        state(p).bursts.add(new Burst(now(p)+1,target.getUUID(),p.level().dimension().location(),kind,
                (float)Math.min(v("common.cap"),Math.max(0,damage))));
    }
    private static void clearGhost(ServerPlayer p,State s) {
        var invis=p.getEffect(MobEffects.INVISIBILITY);
        if(s.ownsInvisibility && invis!=null && !invis.isInfiniteDuration() && invis.getAmplifier()==0
                && invis.getDuration()<=Math.max(0,s.ghost-now(p))+1) p.removeEffect(MobEffects.INVISIBILITY);
        s.ownsInvisibility=false;s.ghost=0;
    }
    @SubscribeEvent(priority=EventPriority.LOW)
    public static void hurt(LivingHurtEvent event) {
        if(event.getEntity().level().isClientSide || BossSoulEvents.secondary(event.getSource()))return;
        if(event.getEntity() instanceof ServerPlayer p && event.getSource().is(DamageTypeTags.IS_FIRE)
                && EpochSoulStoneItem.equipped(p).contains(Kind.ZHENYAN))
            event.setAmount((float)(event.getAmount()*(1-Math.min(1,v("fire.reduction")))));
        if(event.getSource().getEntity() instanceof ServerPlayer p && direct(event.getSource()) && BossSoulEvents.enemy(p,event.getEntity())) {
            State s=state(p);clearGhost(p,s);
            if(EpochSoulStoneItem.equipped(p).contains(Kind.BRONZE) && s.riposte>now(p)) {
                event.setAmount((float)(event.getAmount()*(1+v("bronze.bonus"))));s.riposte=0;
            }
        }
    }
    @SubscribeEvent(priority=EventPriority.LOWEST)
    public static void block(ShieldBlockEvent event) {
        if(event.getEntity() instanceof ServerPlayer p && event.getBlockedDamage()>0 && EpochSoulStoneItem.equipped(p).contains(Kind.BRONZE))
            state(p).riposte=now(p)+EpochSoulConfig.ticks("bronze.window");
    }
    @SubscribeEvent(priority=EventPriority.LOWEST)
    public static void damage(LivingDamageEvent event) {
        if(event.getEntity().level().isClientSide || event.getAmount()<=0 || BossSoulEvents.secondary(event.getSource()))return;
        var target=event.getEntity();var src=event.getSource();
        if(target instanceof ServerPlayer p) {
            var a=EpochSoulStoneItem.equipped(p);State s=state(p);
            boolean hostile=src.getEntity() instanceof LivingEntity e && BossSoulEvents.enemy(p,e);
            if(hostile && a.contains(Kind.FANGZUN) && ready(p,"defense_hit")) {
                cool(p,"defense_hit","common.hit_gate");s.pressure=Math.min(EpochSoulConfig.count("fang.hits"),s.pressure+1);
                if(s.pressure>=EpochSoulConfig.count("fang.hits") && inRange(p,(LivingEntity)src.getEntity()) && proc(p,"fang","fang.cooldown")) {
                    s.pressure=0;queue(p,(LivingEntity)src.getEntity(),Kind.FANGZUN,v("fang.damage"));
                }
            }
            if(hostile && a.contains(Kind.GHOST_JADE) && ready(p,"ghost")) {
                cool(p,"ghost","ghost.cooldown");s.ghost=now(p)+EpochSoulConfig.ticks("ghost.duration");
                if(!p.hasEffect(MobEffects.INVISIBILITY)){effect(p,MobEffects.INVISIBILITY,EpochSoulConfig.ticks("ghost.duration"),0);s.ownsInvisibility=true;}
                effect(p,MobEffects.MOVEMENT_SPEED,EpochSoulConfig.ticks("ghost.duration"),0);
                if(src.getEntity() instanceof Mob mob && mob.getTarget()==p)mob.setTarget(null);
            }
            if(a.contains(Kind.TALISMAN) && ready(p,"talisman")) {
                int mode=EpochSoulStoneItem.mode(p,Kind.TALISMAN);
                if(mode==0 && src.is(DamageTypeTags.IS_FIRE)) {
                    cool(p,"talisman","talisman.cooldown");p.clearFire();effect(p,MobEffects.FIRE_RESISTANCE,EpochSoulConfig.ticks("talisman.duration"),0);
                } else if(mode==3 && hostile && p.distanceToSqr(src.getEntity())<=9) {
                    cool(p,"talisman","talisman.cooldown");effect((LivingEntity)src.getEntity(),MobEffects.MOVEMENT_SLOWDOWN,EpochSoulConfig.ticks("talisman.duration"),1);
                }
            }
        }
        if(!(src.getEntity() instanceof ServerPlayer p) || !direct(src) || !BossSoulEvents.enemy(p,target))return;
        var a=EpochSoulStoneItem.equipped(p);if(a.isEmpty())return;State s=state(p);
        if(a.contains(Kind.DAMASCENE) && src.getDirectEntity()==p) s.tough=now(p)+EpochSoulConfig.ticks("damascene.duration");
        if(a.contains(Kind.GENERAL) && ready(p,"general")) formation(p,target,s);
        if(!ready(p,"hit"))return;cool(p,"hit","common.hit_gate");
        if(a.contains(Kind.CANGYAO))s.magnet=Math.min(EpochSoulConfig.count("magnet.hits"),s.magnet+1);
        if(a.contains(Kind.GOLDENHOU) && target.isOnFire())s.bell=Math.min(EpochSoulConfig.count("hou.hits"),s.bell+1);
        if(!inRange(p,target))return;
        if(a.contains(Kind.CANGYAO) && s.magnet>=EpochSoulConfig.count("magnet.hits") && proc(p,"magnet","magnet.cooldown")) {
            s.magnet=0;queue(p,target,Kind.CANGYAO,v("magnet.damage"));
        } else if(a.contains(Kind.ZIXU) && proc(p,"zixu","zixu.cooldown")) {
            effect(target,MobEffects.POISON,EpochSoulConfig.ticks("zixu.poison"),0);
            effect(target,MobEffects.MOVEMENT_SLOWDOWN,EpochSoulConfig.ticks("zixu.poison"),0);
            if(target.hasEffect(MobEffects.POISON))s.poisoned.put(target.getUUID(),now(p)+EpochSoulConfig.ticks("zixu.poison"));
        } else if(a.contains(Kind.ZHENYAN) && s.fire>=EpochSoulConfig.count("fire.casts") && proc(p,"fire","fire.cooldown")) {
            s.fire=0;queue(p,target,Kind.ZHENYAN,v("fire.damage"));
        } else if(a.contains(Kind.TYPE) && src instanceof SpellDamageSource && s.glyphs>=EpochSoulConfig.count("type.casts") && proc(p,"type","type.cooldown")) {
            s.glyphs=0;queue(p,target,Kind.TYPE,v("type.damage"));
        } else if(a.contains(Kind.GOLDENHOU) && s.bell>=EpochSoulConfig.count("hou.hits") && proc(p,"hou","hou.cooldown")) {
            s.bell=0;queue(p,target,Kind.GOLDENHOU,v("hou.damage"));
        } else if(a.contains(Kind.TIGER) && s.ranged>now(p) && (src instanceof SpellDamageSource || src.getDirectEntity() instanceof Projectile)
                && proc(p,"tiger","tiger.cooldown")) {
            s.ranged=0;queue(p,target,Kind.TIGER,v("tiger.damage"));
        }
    }
    private static void formation(ServerPlayer p,LivingEntity target,State s) {
        var summons=p.level().getEntitiesOfClass(Mob.class,p.getBoundingBox().inflate(v("general.range")),
                e -> ownSummon(p,e) && e.isAlive() && p.distanceToSqr(e)<=v("general.range")*v("general.range"));
        summons.sort(Comparator.comparingDouble(p::distanceToSqr));
        if(summons.isEmpty())return;cool(p,"general","general.cooldown");
        MobEffect buff=switch(s.formation++%3){case 0 -> MobEffects.MOVEMENT_SPEED;case 1 -> MobEffects.DAMAGE_BOOST;default -> MobEffects.DAMAGE_RESISTANCE;};
        for(var mob:summons.stream().limit(EpochSoulConfig.count("general.limit")).toList()) {
            effect(mob,buff,EpochSoulConfig.ticks("general.duration"),0);
            if(mob.hasLineOfSight(target))mob.setTarget(target);
        }
    }
    @SubscribeEvent(priority=EventPriority.LOWEST)
    public static void cast(SpellOnCastEvent event) {
        if(!(event.getEntity() instanceof ServerPlayer p))return;
        State s=STATES.get(p.getUUID());if(s!=null)clearGhost(p,s);
        var a=EpochSoulStoneItem.equipped(p);
        if(a.isEmpty() || p.isCreative() || event.getManaCost()<=0 || !event.getCastSource().consumesMana()
                || MagicData.getPlayerMagicData(p).getPlayerRecasts().hasRecastForSpell(event.getSpellId()))return;
        s=state(p);if(s.payment!=null)return;
        s.payment=new Payment(now(p)+1,MagicData.getPlayerMagicData(p).getMana(),event.getManaCost(),
                event.getSchoolType().getId().equals(new ResourceLocation("irons_spellbooks","fire")),a);
    }
    private static void settle(ServerPlayer p,State s,EnumSet<Kind> a) {
        var r=s.payment;s.payment=null;var data=MagicData.getPlayerMagicData(p);
        float paid=BossSoulMath.paidMana(r.cost,r.before,data.getMana());if(paid<=0)return;
        var eligible=r.abilities.clone();eligible.retainAll(a);
        if(eligible.contains(Kind.TYPE))s.glyphs=Math.min(EpochSoulConfig.count("type.casts"),s.glyphs+1);
        if(eligible.contains(Kind.TIGER))s.ranged=now(p)+EpochSoulConfig.ticks("tiger.window");
        if(r.fire && eligible.contains(Kind.ZHENYAN))s.fire=Math.min(EpochSoulConfig.count("fire.casts"),s.fire+1);
        float refund=0;
        if(r.fire && eligible.contains(Kind.PYROTEMPER) && ready(p,"pyro")) {
            cool(p,"pyro","pyro.cooldown");refund=(float)Math.min(v("pyro.refund_cap"),paid*Math.min(1,v("pyro.refund_ratio")));mana(p,refund);
        }
        if(eligible.contains(Kind.ZIXU)) {
            // Only the unrefunded observed payment becomes a short-lived, consumable credit.
            if(s.creditUntil<=now(p))s.credit=0;
            s.credit=Math.min((float)v("zixu.refund_cap"),s.credit+(paid-refund)*(float)Math.min(1,v("zixu.refund_ratio")));
            s.creditUntil=now(p)+400;
        }
    }
    private static void mana(ServerPlayer p,float amount) {
        if(amount<=0)return;var data=MagicData.getPlayerMagicData(p);data.addMana(amount);
        PacketDistributor.sendToPlayer(p,new SyncManaPacket(data));
    }
    private static void burst(ServerPlayer p,Burst b,EnumSet<Kind> a) {
        if(!a.contains(b.ability) || !p.level().dimension().location().equals(b.dimension))return;
        var entity=((ServerLevel)p.level()).getEntity(b.target);
        if(!(entity instanceof LivingEntity target) || !BossSoulEvents.enemy(p,target) || !inRange(p,target))return;
        ((ServerLevel)p.level()).sendParticles(b.ability==Kind.ZHENYAN || b.ability==Kind.GOLDENHOU ? ParticleTypes.FLAME : ParticleTypes.ENCHANT,
                target.getX(),target.getY()+.8,target.getZ(),12,.3,.4,.3,.02);
        if(b.ability==Kind.CANGYAO) {
            // Small velocity nudge; never teleport the target or override its existing movement.
            Vec3 delta=p.position().subtract(target.position());
            if(delta.lengthSqr()>1){Vec3 push=delta.normalize().scale(Math.min(.6,v("magnet.pull")));target.push(push.x,.05,push.z);target.hurtMarked=true;}
            var magnetic=ForgeRegistries.MOB_EFFECTS.getValue(new ResourceLocation("alexscaves","magnetizing"));
            if(magnetic!=null)effect(target,magnetic,40,0);
        }
        if(b.ability==Kind.FANGZUN || b.ability==Kind.TYPE)effect(target,MobEffects.MOVEMENT_SLOWDOWN,EpochSoulConfig.ticks("fang.slow"),0);
        if(b.ability==Kind.ZHENYAN || b.ability==Kind.GOLDENHOU)target.setSecondsOnFire(EpochSoulConfig.count("hou.burn"));
        var victims=new ArrayList<LivingEntity>();victims.add(target);
        if(b.ability==Kind.GOLDENHOU) {
            var nearby=p.level().getEntitiesOfClass(LivingEntity.class,target.getBoundingBox().inflate(v("hou.radius")),
                    e -> e!=target && BossSoulEvents.enemy(p,e) && (e instanceof net.minecraft.world.entity.monster.Enemy || e instanceof Mob mob && mob.getTarget()==p)
                            && target.distanceToSqr(e)<=v("hou.radius")*v("hou.radius") && p.hasLineOfSight(e));
            nearby.sort(Comparator.comparingDouble(target::distanceToSqr));
            victims.addAll(nearby.stream().limit(Math.max(0,EpochSoulConfig.count("hou.targets")-1)).toList());
        }
        float split=b.damage/victims.size();
        for(var victim:victims) {
            if(b.ability==Kind.GOLDENHOU) {victim.setSecondsOnFire(EpochSoulConfig.count("hou.burn"));effect(victim,MobEffects.WEAKNESS,40,0);}
            victim.hurt(BossSoulEvents.source(p,b.ability==Kind.ZHENYAN || b.ability==Kind.GOLDENHOU ? "epoch_fire" : "epoch_echo",p),split);
        }
    }
    private static void modifier(ServerPlayer p,Attribute attr,UUID id,double value,boolean multiply) {
        var instance=p.getAttribute(attr);if(instance==null)return;var old=instance.getModifier(id);
        if(old!=null && Math.abs(old.getAmount()-value)<.000001)return;
        instance.removeModifier(id);if(value>0)instance.addTransientModifier(new AttributeModifier(id,"wan_epoch_conditional",value,
                multiply?AttributeModifier.Operation.MULTIPLY_BASE:AttributeModifier.Operation.ADDITION));
    }
    @SubscribeEvent public static void tick(TickEvent.PlayerTickEvent event) {
        if(event.phase!=TickEvent.Phase.END || !(event.player instanceof ServerPlayer p))return;
        var a=EpochSoulStoneItem.equipped(p);State s=STATES.get(p.getUUID());
        if(s==null && a.isEmpty() && p.tickCount%20!=0)return;s=state(p);
        // Cancel all stored charges as soon as their source ability is removed.
        if(!a.contains(Kind.FANGZUN))s.pressure=0;if(!a.contains(Kind.CANGYAO))s.magnet=0;
        if(!a.contains(Kind.ZHENYAN))s.fire=0;if(!a.contains(Kind.TYPE))s.glyphs=0;
        if(!a.contains(Kind.GOLDENHOU))s.bell=0;if(!a.contains(Kind.TIGER))s.ranged=0;
        if(!a.contains(Kind.BRONZE))s.riposte=0;
        if(!a.contains(Kind.DAMASCENE))s.tough=0;if(!a.contains(Kind.CLASSICS))s.xp=0;
        if(!a.contains(Kind.ZIXU)){s.credit=0;s.poisoned.clear();}
        else if(s.creditUntil<=now(p))s.credit=0;
        if(!a.contains(Kind.GHOST_JADE) || !p.isAlive())clearGhost(p,s);
        if(!p.isAlive()){s.payment=null;s.bursts.clear();s.credit=0;}
        if(s.payment!=null && now(p)>=s.payment.due)settle(p,s,a);
        var iterator=s.bursts.iterator();
        while(iterator.hasNext()){var b=iterator.next();if(b.due<=now(p)){iterator.remove();if(p.isAlive())burst(p,b,a);}}
        modifier(p,Attributes.ARMOR_TOUGHNESS,TOUGH,p.isAlive() && a.contains(Kind.DAMASCENE) && now(p)<s.tough?v("damascene.toughness"):0,false);
        modifier(p,AttributeRegistry.MANA_REGEN.get(),REGEN,p.isAlive() && a.contains(Kind.CLASSICS) && now(p)<s.xp?v("classics.regen"):0,true);
        int mode=EpochSoulStoneItem.mode(p,Kind.EXPLORER);
        modifier(p,AttributeRegistry.SPELL_RESIST.get(),WARD,p.isAlive() && a.contains(Kind.EXPLORER) && mode==0 && p.level().isNight()?v("explorer.night_resist"):0,true);
        modifier(p,Attributes.KNOCKBACK_RESISTANCE,BRACE,p.isAlive() && a.contains(Kind.EXPLORER) && mode==3?.10:0,false);
        if(p.isAlive() && a.contains(Kind.TALISMAN) && ready(p,"talisman")) {
            int ward=EpochSoulStoneItem.mode(p,Kind.TALISMAN);
            if(ward==1 && p.isUnderWater()) {cool(p,"talisman","talisman.cooldown");p.setAirSupply(p.getMaxAirSupply());effect(p,MobEffects.WATER_BREATHING,EpochSoulConfig.ticks("talisman.duration"),0);}
            if(ward==2 && p.fallDistance>3 && p.getDeltaMovement().y<0) {cool(p,"talisman","talisman.cooldown");effect(p,MobEffects.SLOW_FALLING,EpochSoulConfig.ticks("talisman.duration"),0);}
        }
        if(p.tickCount%20==0 && p.isAlive()) {
            if(a.contains(Kind.EXPLORER)) {
                if(mode==0 && p.level().isNight())effect(p,MobEffects.NIGHT_VISION,EpochSoulConfig.ticks("explorer.duration"),0);
                if(mode==2 && p.isInWater()){effect(p,MobEffects.WATER_BREATHING,EpochSoulConfig.ticks("explorer.duration"),0);effect(p,MobEffects.DOLPHINS_GRACE,EpochSoulConfig.ticks("explorer.duration"),0);}
            }
            if(a.contains(Kind.RUSTED) || a.contains(Kind.EXPLORER) && mode==3)shortenHaze(p,s);
            explore(p,s);
            s.poisoned.entrySet().removeIf(e -> e.getValue()<now(p));
            s.cd.entrySet().removeIf(e -> e.getValue()<now(p)-1200);
        }
    }
    private static void shortenHaze(ServerPlayer p,State s) {
        var haze=ForgeRegistries.MOB_EFFECTS.getValue(new ResourceLocation("splendour_ablaze_epoch","haze"));
        if(haze==null)return;var instance=p.getEffect(haze);if(instance==null)return;
        // At most once per application/refresh: an absolute expiry prevents repeated exponential shortening.
        long expiry=now(p)+instance.getDuration();long seen=s.cd.getOrDefault("haze_expiry",0L);
        if(!instance.isInfiniteDuration() && expiry>seen+20) {
            int ticks=Math.max(1,(int)(instance.getDuration()*(1-Math.min(.8,v("rusted.haze_reduction")))));
            p.removeEffect(haze);effect(p,haze,ticks,instance.getAmplifier());s.cd.put("haze_expiry",now(p)+ticks);
        }
    }
    @SubscribeEvent public static void mining(PlayerEvent.BreakSpeed event) {
        if(EpochSoulStoneItem.equipped(event.getEntity()).contains(Kind.EXPLORER) && EpochSoulStoneItem.mode(event.getEntity(),Kind.EXPLORER)==1)
            event.setNewSpeed(event.getNewSpeed()*1.10f);
    }
    @SubscribeEvent(priority=EventPriority.LOWEST) public static void experience(PlayerXpEvent.XpChange event) {
        if(event.getAmount()>0 && event.getEntity() instanceof ServerPlayer p && EpochSoulStoneItem.equipped(p).contains(Kind.CLASSICS))
            state(p).xp=now(p)+EpochSoulConfig.ticks("classics.duration");
    }
    @SubscribeEvent(priority=EventPriority.LOWEST) public static void droppedExperience(LivingExperienceDropEvent event) {
        if(event.getAttackingPlayer() instanceof ServerPlayer p && EpochSoulStoneItem.equipped(p).contains(Kind.CAULDRON) && event.getDroppedExperience()>0)
            event.setDroppedExperience(event.getDroppedExperience()+(int)Math.min(v("cauldron.xp_cap"),Math.floor(event.getDroppedExperience()*v("cauldron.xp_ratio"))));
    }
    @SubscribeEvent(priority=EventPriority.LOWEST) public static void death(LivingDeathEvent event) {
        if(!(owner(event.getSource().getEntity()) instanceof ServerPlayer p))return;
        var target=event.getEntity();State s=STATES.get(p.getUUID());
        if(target==p || p.isAlliedTo(target) || target.isAlliedTo(p) || owner(target)==p)return;
        if(s!=null && EpochSoulStoneItem.equipped(p).contains(Kind.ZIXU) && s.poisoned.getOrDefault(target.getUUID(),0L)>=now(p)
                && target.hasEffect(MobEffects.POISON) && s.creditUntil>now(p)) {
            mana(p,s.credit);s.credit=0;s.poisoned.remove(target.getUUID());
        }
        ResourceLocation id=ForgeRegistries.ENTITY_TYPES.getKey(target.getType());
        if(id==null || !id.getNamespace().equals("splendour_ablaze_epoch"))return;
        String route=switch(id.getPath()){case "cauldronbeast" -> "cauldron";case "firearmtigerguard" -> "tiger";
            case "rustedancestors","rustrelics","rusthound" -> "rusted";default -> "";};
        if(route.isEmpty())return;
        CompoundTag progress=progress(p);int count=progress.getInt(route)+1;
        if(count>=EpochSoulConfig.count("progress.kills")){count=0;give(p,new ItemStack(SoulStoneItems.EPOCH_PROOFS.get(route).get()));}
        progress.putInt(route,count);
    }
    private static CompoundTag progress(ServerPlayer p) {
        CompoundTag data=p.getPersistentData();
        if(!data.contains(Player.PERSISTED_NBT_TAG))data.put(Player.PERSISTED_NBT_TAG,new CompoundTag());
        var persisted=data.getCompound(Player.PERSISTED_NBT_TAG);
        if(!persisted.contains("EpochProgress"))persisted.put("EpochProgress",new CompoundTag());
        return persisted.getCompound("EpochProgress");
    }
    private static void explore(ServerPlayer p,State s) {
        var biome=p.level().getBiome(p.blockPosition()).unwrapKey().map(k -> k.location()).orElse(null);
        if(biome==null || !biome.getNamespace().equals("splendour_ablaze_epoch") || !Arrays.asList(BIOMES).contains(biome.getPath())) {
            s.visit="";s.visitTicks=0;return;
        }
        if(!s.visit.equals(biome.getPath())){s.visit=biome.getPath();s.visitTicks=0;}
        s.visitTicks+=20;if(s.visitTicks<EpochSoulConfig.ticks("progress.visit_seconds"))return;
        var progress=progress(p);int index=Arrays.asList(BIOMES).indexOf(s.visit);
        int before=progress.getInt("visited"),visited=before | (1<<index);progress.putInt("visited",visited);
        int cycleBefore=progress.getInt("cycle"),cycle=cycleBefore | (1<<index);progress.putInt("cycle",cycle);
        if(cycleBefore!=cycle) {
            give(p,new ItemStack(SoulStoneItems.EPOCH_PROOFS.get("explorer").get()));
            p.displayClientMessage(net.minecraft.network.chat.Component.translatable("message.wans_minego_expansion.epoch.visit",Integer.bitCount(visited),8),true);
        }
        if(cycle==255) {
            progress.putInt("cycle",0);s.visitTicks=0;give(p,new ItemStack(SoulStoneItems.EPOCH_PROOFS.get("complete").get()));
        }
    }
    private static void give(ServerPlayer p,ItemStack stack) { if(!p.addItem(stack))p.drop(stack,false); }
    @SubscribeEvent public static void logout(PlayerEvent.PlayerLoggedOutEvent event) {STATES.remove(event.getEntity().getUUID());}
    @SubscribeEvent public static void clone(PlayerEvent.Clone event) {
        STATES.remove(event.getEntity().getUUID());
        var original=event.getOriginal().getPersistentData();
        if(original.contains(Player.PERSISTED_NBT_TAG))event.getEntity().getPersistentData().put(Player.PERSISTED_NBT_TAG,original.getCompound(Player.PERSISTED_NBT_TAG).copy());
    }
    private EpochSoulEvents() {}
}
