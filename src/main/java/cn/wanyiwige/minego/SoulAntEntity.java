package cn.wanyiwige.minego;

import io.redspace.ironsspellbooks.entity.mobs.IMagicSummon;
import java.util.UUID;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.level.Level;
import net.minecraft.resources.ResourceLocation;

/** A genuinely owned, short-lived summon; never a wild Foolish monster. */
public final class SoulAntEntity extends PathfinderMob implements IMagicSummon {
    private UUID ownerUUID;
    private int life;
    private boolean biomeSummon;
    public SoulAntEntity(EntityType<? extends PathfinderMob> type, Level level) { super(type, level); xpReward = 0; }
    public static AttributeSupplier.Builder attributes() {
        return createMobAttributes().add(Attributes.MAX_HEALTH, 18).add(Attributes.ATTACK_DAMAGE, 3)
                .add(Attributes.MOVEMENT_SPEED, .32).add(Attributes.FOLLOW_RANGE, 24);
    }
    @Override protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(1, new MeleeAttackGoal(this, 1.15, true));
    }
    public void configure(ServerPlayer owner, LivingEntity target) {
        ownerUUID = owner.getUUID(); life = BossSoulConfig.ticks("queen.life_seconds");
        getAttribute(Attributes.MAX_HEALTH).setBaseValue(BossSoulConfig.value("queen.health"));
        getAttribute(Attributes.ATTACK_DAMAGE).setBaseValue(BossSoulConfig.value("queen.attack"));
        setHealth(getMaxHealth()); setTarget(target); setPersistenceRequired();
    }
    public UUID ownerUUID() { return ownerUUID; }
    public void configureBiome(ServerPlayer owner, LivingEntity target) {
        ownerUUID = owner.getUUID(); biomeSummon = true;
        life = BiomeSoulConfig.ticks("scarlet.life_seconds");
        getAttribute(Attributes.MAX_HEALTH).setBaseValue(BiomeSoulConfig.v("scarlet.health"));
        getAttribute(Attributes.ATTACK_DAMAGE).setBaseValue(BiomeSoulConfig.v("scarlet.attack"));
        setHealth(getMaxHealth()); setTarget(target); setPersistenceRequired();
    }
    @Override public Entity getSummoner() {
        return level() instanceof ServerLevel server && ownerUUID != null ? server.getEntity(ownerUUID) : null;
    }
    @Override public void onUnSummon() { discard(); }
    @Override public boolean isAlliedTo(Entity other) {
        Entity owner = getSummoner();
        return other == owner || (owner != null && (owner.isAlliedTo(other)
                || other instanceof IMagicSummon summon && summon.getSummoner() == owner)) || super.isAlliedTo(other);
    }
    @Override public boolean hurt(DamageSource source, float amount) {
        return source.getEntity() != null && isAlliedTo(source.getEntity()) ? false : super.hurt(source, amount);
    }
    @Override public void tick() {
        super.tick();
        if (level().isClientSide) return;
        Entity entity = getSummoner();
        if (!(entity instanceof ServerPlayer owner) || !owner.isAlive() || --life <= 0
                || (biomeSummon ? !BiomeSoulStoneItem.equipped(owner).contains(BiomeSoulStoneItem.Kind.SCARLET)
                    : !BossSoulStoneItem.equipped(owner).contains(BossSoulStoneItem.Kind.SCARLANT_QUEEN))
                || distanceToSqr(owner) > 64 * 64) { discard(); return; }
        if (!BossSoulEvents.enemy(owner, getTarget())) setTarget(null);
        if (getTarget() == null) {
            LivingEntity ordered = owner.getLastHurtMob();
            if (!BossSoulEvents.enemy(owner, ordered)) ordered = owner.getLastHurtByMob();
            if (BossSoulEvents.enemy(owner, ordered) && distanceToSqr(ordered) <= 24 * 24) setTarget(ordered);
        }
        if (getTarget() == null && distanceToSqr(owner) > 9) getNavigation().moveTo(owner, 1.1);
    }
    @Override public boolean doHurtTarget(Entity target) {
        Entity owner = getSummoner();
        return owner instanceof ServerPlayer player && target instanceof LivingEntity victim
                && BossSoulEvents.enemy(player, victim) && super.doHurtTarget(target);
    }
    @Override protected ResourceLocation getDefaultLootTable() { return new ResourceLocation("minecraft:empty"); }
    @Override protected void dropCustomDeathLoot(DamageSource source, int looting, boolean recentlyHit) {}
    @Override public boolean shouldDropExperience() { return false; }
    @Override public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag); if (ownerUUID != null) tag.putUUID("SoulOwner", ownerUUID); tag.putInt("SoulLife", life); tag.putBoolean("BiomeSummon", biomeSummon);
    }
    @Override public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag); ownerUUID = tag.hasUUID("SoulOwner") ? tag.getUUID("SoulOwner") : null;
        life = tag.getInt("SoulLife");
        biomeSummon = tag.getBoolean("BiomeSummon");
    }
}
