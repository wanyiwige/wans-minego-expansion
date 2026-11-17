package cn.wanyiwige.minego;

import java.util.*;
import cn.wanyiwige.minego.BiomeSoulStoneItem.Kind;
import io.redspace.ironsspellbooks.damage.SpellDamageSource;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.*;
import net.minecraft.world.effect.*;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.living.*;
import net.minecraftforge.event.entity.player.*;
import net.minecraftforge.eventbus.api.*;
import net.minecraftforge.registries.ForgeRegistries;

/** Server-authoritative biome rewards. Secondary damage never feeds back into procs. */
public final class BiomeSoulEvents {
    private static final Map<UUID, State> STATES = new HashMap<>();
    private static class State {
        final Map<String, Long> cooldowns = new HashMap<>();
        double charge; int fire, corrosion; long combat;
    }
    private static State state(ServerPlayer p) { return STATES.computeIfAbsent(p.getUUID(), key -> new State()); }
    private static long now(ServerPlayer p) { return p.server.overworld().getGameTime(); }
    private static boolean ready(ServerPlayer p, String key) { return now(p) >= state(p).cooldowns.getOrDefault(key, 0L); }
    private static void cool(ServerPlayer p, String key, String config) { state(p).cooldowns.put(key, now(p) + BiomeSoulConfig.ticks(config)); }
    public static boolean matching(LivingEntity entity, Kind kind) {
        return entity.level().getBiome(entity.blockPosition()).unwrapKey().map(key -> kind.matches(key.location())).orElse(false);
    }
    private static double boost(ServerPlayer p, Kind kind) { return nativeBonus(p, kind) ? BiomeSoulConfig.v("common.biome_multiplier") : 1; }
    private static boolean nativeBonus(LivingEntity p, Kind kind) { return matching(p,kind) && BiomeSoulStoneItem.nativeEquipped(p).contains(kind); }
    private static boolean direct(DamageSource source) {
        return !BossSoulEvents.secondary(source) && source.getEntity() instanceof ServerPlayer
                && (source instanceof SpellDamageSource || source.getDirectEntity() == source.getEntity()
                    || source.getDirectEntity() instanceof net.minecraft.world.entity.projectile.Projectile)
                && (!source.is(DamageTypeTags.IS_FIRE) || source instanceof SpellDamageSource)
                && !source.is(DamageTypes.THORNS);
    }
    private static void particles(ServerPlayer p, net.minecraft.core.particles.ParticleOptions type, int count) {
        ((ServerLevel)p.level()).sendParticles(type, p.getX(), p.getY() + .8, p.getZ(), count, .5, .4, .5, .025);
    }
    private static List<LivingEntity> hostileNearby(ServerPlayer p, double radius, int max) {
        var list = p.level().getEntitiesOfClass(LivingEntity.class, p.getBoundingBox().inflate(radius),
                target -> BossSoulEvents.enemy(p, target) && p.distanceToSqr(target) <= radius * radius
                        && p.hasLineOfSight(target) && (target instanceof Enemy
                        || target instanceof Mob mob && mob.getTarget() == p || p.getLastHurtMob() == target));
        list.sort(Comparator.comparingDouble(p::distanceToSqr));
        return list.subList(0, Math.min(max, list.size()));
    }
    @SubscribeEvent public static void attune(PlayerInteractEvent.RightClickBlock event) {
        if (!event.getEntity().isShiftKeyDown() || !ForgeRegistries.ITEMS.getKey(event.getItemStack().getItem())
                .equals(new ResourceLocation("mine_fargo", "empty_soul_stone"))) return;
        var biome = event.getLevel().getBiome(event.getEntity().blockPosition()).unwrapKey();
        Kind kind = biome.map(key -> Kind.forBiome(key.location())).orElse(null);
        if (kind == null) return;
        // Both sides cancel block interaction; inventory mutation occurs once on the server.
        event.setCanceled(true); event.setCancellationResult(InteractionResult.sidedSuccess(event.getLevel().isClientSide));
        if (!(event.getEntity() instanceof ServerPlayer p)) return;
        if (!p.getAbilities().instabuild) event.getItemStack().shrink(1);
        ItemStack result = AttunedSoulStoneItem.attuned(kind);
        if (!p.getInventory().add(result)) p.drop(result, false);
        p.displayClientMessage(net.minecraft.network.chat.Component.translatable("message.wans_minego_expansion.attuned",
                net.minecraft.network.chat.Component.translatable("item.wans_minego_expansion." + kind.id())), true);
        particles(p, ParticleTypes.ENCHANT, 20);
    }
    @SubscribeEvent public static void mining(PlayerEvent.BreakSpeed event) {
        var p = event.getEntity(); var abilities = BiomeSoulStoneItem.equipped(p);
        double bonus = 0;
        if (abilities.contains(Kind.BLOOM)) bonus += BiomeSoulConfig.v("bloom.mining") * (nativeBonus(p, Kind.BLOOM) ? BiomeSoulConfig.v("common.biome_multiplier") : 1);
        if (abilities.contains(Kind.TIME)) bonus += BiomeSoulConfig.v("time.mining") * (nativeBonus(p, Kind.TIME) ? BiomeSoulConfig.v("common.biome_multiplier") : 1);
        if (bonus > 0) event.setNewSpeed((float)(event.getNewSpeed() * (1 + bonus)));
    }
    @SubscribeEvent(priority = EventPriority.LOW) public static void hurt(LivingHurtEvent event) {
        if (event.getEntity().level().isClientSide || BossSoulEvents.secondary(event.getSource())) return;
        if (event.getSource().getEntity() instanceof ServerPlayer p && direct(event.getSource()) && p.isOnFire()
                && BiomeSoulStoneItem.equipped(p).contains(Kind.ASH) && BossSoulEvents.enemy(p, event.getEntity()))
            event.setAmount((float)(event.getAmount() * (1 + BiomeSoulConfig.v("ash.burning_bonus") * boost(p, Kind.ASH))));
    }
    @SubscribeEvent(priority = EventPriority.LOWEST) public static void damage(LivingDamageEvent event) {
        if (event.getEntity().level().isClientSide || BossSoulEvents.secondary(event.getSource()) || event.getAmount() <= 0) return;
        LivingEntity target = event.getEntity();
        if (target instanceof ServerPlayer p) {
            var abilities = BiomeSoulStoneItem.equipped(p);
            if (!abilities.isEmpty()) state(p).combat = now(p) + 100;
            if (abilities.contains(Kind.TIME) && ready(p, "escape")) {
                cool(p, "escape", "time.escape_cooldown");
                p.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, (int)(BiomeSoulConfig.ticks("time.escape_seconds") * boost(p, Kind.TIME)), 0));
            }
        }
        if (!(event.getSource().getEntity() instanceof ServerPlayer p) || !direct(event.getSource()) || !BossSoulEvents.enemy(p, target)) return;
        var abilities = BiomeSoulStoneItem.equipped(p); if (abilities.isEmpty()) return;
        State s = state(p); s.combat = now(p) + 100;
        if (!ready(p, "hit")) return; cool(p, "hit", "common.hit_gate");
        float actual = BossSoulMath.effectiveDamage(target.getHealth(), event.getAmount());
        if (abilities.contains(Kind.BLOOM) && ready(p, "crystal") && p.distanceToSqr(target) <= 24 * 24 && p.hasLineOfSight(target)) {
            cool(p, "crystal", "bloom.cooldown");
            float amount = (float)Math.min(BiomeSoulConfig.v("bloom.damage_cap"), actual * BiomeSoulConfig.v("bloom.damage_ratio") * boost(p, Kind.BLOOM));
            SoulBoltEntity.launchCrystal(p, target, amount);
        }
        if (MaterialSoulStoneItem.equipped(p).contains(MaterialSoulStoneItem.Kind.THUNDERSTONE))
            s.charge = Math.min(1, s.charge + 1 / Math.max(1,MaterialSoulConfig.v("thunder.hits")));
        if (abilities.contains(Kind.STORM) && s.charge >= 1 && ready(p, "electric")) {
            s.charge = 0; cool(p, "electric", "storm.cooldown");
            float amount = (float)Math.min(BiomeSoulConfig.v("storm.damage_cap"), actual * BiomeSoulConfig.v("storm.damage_ratio") * boost(p, Kind.STORM));
            target.hurt(BossSoulEvents.source(p, "soul_lightning", p), amount);
            ((ServerLevel)p.level()).sendParticles(ParticleTypes.ELECTRIC_SPARK, target.getX(), target.getY() + 1, target.getZ(), 20, .3, .5, .3, .06);
        }
        if (abilities.contains(Kind.WASTE) && ready(p, "corrode")
                && p.getRandom().nextFloat() < Math.min(1, BiomeSoulConfig.v("waste.chance") * boost(p, Kind.WASTE))) {
            var corrosion = ForgeRegistries.MOB_EFFECTS.getValue(new ResourceLocation("foolish", "corrosion"));
            if (corrosion != null) {
                cool(p, "corrode", "waste.cooldown");
                var effect = new MobEffectInstance(corrosion, BiomeSoulConfig.ticks("waste.corrosion_seconds"), 0);
                if (target.canBeAffected(effect)) target.addEffect(effect);
            }
        }
        if (abilities.contains(Kind.SCARLET) && ready(p, "ant")
                && p.getRandom().nextFloat() < Math.min(1, BiomeSoulConfig.v("scarlet.chance") * boost(p, Kind.SCARLET))
                && p.distanceToSqr(target) <= 24 * 24 && p.hasLineOfSight(target)) {
            int cap = (int)BiomeSoulConfig.v("scarlet.max_summons");
            long count = p.level().getEntitiesOfClass(SoulAntEntity.class, p.getBoundingBox().inflate(64), ant -> p.getUUID().equals(ant.ownerUUID())).size();
            if (count < cap) {
                var ant = BossSoulEntities.ANT.get().create(p.level());
                if (ant != null) {
                    ant.moveTo(p.getX() + 1, p.getY(), p.getZ(), 0, 0);
                    if (p.level().noCollision(ant)) { ant.configureBiome(p, target); p.level().addFreshEntity(ant); cool(p, "ant", "scarlet.cooldown"); }
                }
            }
        }
    }
    @SubscribeEvent public static void tick(TickEvent.PlayerTickEvent event) {
        if (event.phase != TickEvent.Phase.END || !(event.player instanceof ServerPlayer p)) return;
        var abilities = BiomeSoulStoneItem.equipped(p); State s = STATES.get(p.getUUID());
        if (abilities.isEmpty()) { if (s != null) { s.charge = 0; s.fire = 0; s.corrosion = 0; s.combat = 0; } return; }
        s = state(p); if (!p.isAlive()) { s.charge = 0; s.combat = 0; return; }
        if (BiomeSoulStoneItem.nativeEquipped(p).contains(Kind.STORM) && p.isSprinting()) {
            s.charge = Math.min(1, s.charge + boost(p, Kind.STORM) * (p.isInWaterRainOrBubble() ? 1.5 : 1) / BiomeSoulConfig.ticks("storm.charge_seconds"));
            if (p.tickCount % 20 == 0 && s.charge >= 1) particles(p, ParticleTypes.ELECTRIC_SPARK, 3);
        } else if (!abilities.contains(Kind.STORM)) s.charge = 0;
        if (abilities.contains(Kind.ASH)) {
            int fire = Math.max(0, p.getRemainingFireTicks());
            if (fire > s.fire) p.setRemainingFireTicks((int)(fire * (1 - Math.min(.9, BiomeSoulConfig.v("ash.burn_reduction") * boost(p, Kind.ASH)))));
            s.fire = Math.max(0, p.getRemainingFireTicks());
        } else s.fire = 0;
        if (abilities.contains(Kind.WASTE)) {
            var corrosion = ForgeRegistries.MOB_EFFECTS.getValue(new ResourceLocation("foolish", "corrosion"));
            var instance = corrosion == null ? null : p.getEffect(corrosion);
            if (instance != null && !instance.isInfiniteDuration() && instance.getDuration() > s.corrosion) {
                int duration = Math.max(1, (int)(instance.getDuration() * (1 - Math.min(.9, BiomeSoulConfig.v("waste.duration_reduction") * boost(p, Kind.WASTE)))));
                var shortened = new MobEffectInstance(corrosion, duration, instance.getAmplifier(), instance.isAmbient(), instance.isVisible(), instance.showIcon());
                p.removeEffect(corrosion); p.addEffect(shortened); instance = p.getEffect(corrosion);
            }
            s.corrosion = instance == null ? 0 : instance.getDuration();
        } else s.corrosion = 0;
        if (p.tickCount % 20 != 0) return;
        if (abilities.contains(Kind.MIRE) && p.isInWaterRainOrBubble() && ready(p, "mire")) {
            cool(p, "mire", "mire.heal_interval"); p.heal((float)(BiomeSoulConfig.v("mire.heal") * boost(p, Kind.MIRE)));
        }
        if (s.combat > now(p) && abilities.contains(Kind.GROWTH) && ready(p, "pollen")) {
            var targets = hostileNearby(p, BiomeSoulConfig.v("growth.radius"), (int)BiomeSoulConfig.v("growth.max_targets"));
            if (!targets.isEmpty()) {
                cool(p, "pollen", "growth.cooldown");
                for (var target : targets) target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN,
                        (int)(BiomeSoulConfig.ticks("growth.slow_seconds") * boost(p, Kind.GROWTH)), 0));
                p.heal((float)(BiomeSoulConfig.v("growth.heal") * boost(p, Kind.GROWTH))); particles(p, ParticleTypes.SPORE_BLOSSOM_AIR, 24);
            }
        }
        if (abilities.contains(Kind.ASH) && p.isOnFire() && ready(p, "embers")) {
            var targets = hostileNearby(p, BiomeSoulConfig.v("ash.radius"), (int)BiomeSoulConfig.v("ash.max_targets"));
            if (!targets.isEmpty()) {
                cool(p, "embers", "ash.cooldown");
                for (var target : targets) target.hurt(BossSoulEvents.source(p, "soul_ember", p), (float)(BiomeSoulConfig.v("ash.damage") * boost(p, Kind.ASH)));
                particles(p, ParticleTypes.FLAME, 16);
            }
        }
    }
    @SubscribeEvent public static void logout(PlayerEvent.PlayerLoggedOutEvent event) { STATES.remove(event.getEntity().getUUID()); }
    private BiomeSoulEvents() {}
}
