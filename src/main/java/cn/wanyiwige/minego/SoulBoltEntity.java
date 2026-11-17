package cn.wanyiwige.minego;

import java.util.UUID;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.protocol.Packet;
import net.minecraft.network.protocol.game.ClientGamePacketListener;
import net.minecraft.network.syncher.*;
import net.minecraft.server.level.*;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.phys.*;
import net.minecraftforge.network.NetworkHooks;

public final class SoulBoltEntity extends Projectile {
    private static final EntityDataAccessor<Boolean> STAR=SynchedEntityData.defineId(SoulBoltEntity.class,EntityDataSerializers.BOOLEAN);
    private static final EntityDataAccessor<Boolean> CRYSTAL=SynchedEntityData.defineId(SoulBoltEntity.class,EntityDataSerializers.BOOLEAN);
    private static final EntityDataAccessor<Boolean> WARD=SynchedEntityData.defineId(SoulBoltEntity.class,EntityDataSerializers.BOOLEAN);
    private UUID target; private float damage; private int age;
    public SoulBoltEntity(EntityType<? extends SoulBoltEntity> type,net.minecraft.world.level.Level level){super(type,level);setNoGravity(true);}
    @Override protected void defineSynchedData(){entityData.define(STAR,false);entityData.define(CRYSTAL,false);entityData.define(WARD,false);}
    public boolean star(){return entityData.get(STAR);}
    public boolean crystal(){return entityData.get(CRYSTAL);}
    public static void launchWard(ServerPlayer owner,LivingEntity target,float damage){
        if(damage<=0 || owner.distanceToSqr(target)>Math.pow(MaterialSoulConfig.v("soulcoat.range"),2))return;
        var bolt=BossSoulEntities.BOLT.get().create(owner.level());if(bolt==null)return;
        bolt.setOwner(owner);bolt.target=target.getUUID();bolt.damage=damage;bolt.entityData.set(WARD,true);
        bolt.setPos(owner.getEyePosition());owner.level().addFreshEntity(bolt);
    }
    public static void launchCrystal(ServerPlayer owner,LivingEntity target,float damage){
        if(damage<=0 || owner.distanceToSqr(target)>24*24)return;
        var bolt=BossSoulEntities.BOLT.get().create(owner.level());if(bolt==null)return;
        bolt.setOwner(owner);bolt.target=target.getUUID();bolt.damage=damage;bolt.entityData.set(CRYSTAL,true);
        bolt.setPos(owner.getEyePosition());owner.level().addFreshEntity(bolt);
    }
    public static void launch(ServerPlayer owner,LivingEntity target,float damage,boolean star){
        if(owner.distanceToSqr(target)>Math.pow(BossSoulConfig.value("common.projectile_range"),2))return;
        var bolt=BossSoulEntities.BOLT.get().create(owner.level());if(bolt==null)return;
        bolt.setOwner(owner);bolt.target=target.getUUID();bolt.damage=damage;bolt.entityData.set(STAR,star);
        bolt.setPos(owner.getEyePosition());owner.level().addFreshEntity(bolt);
    }
    @Override public void tick(){
        super.tick();if(level().isClientSide)return;
        if(!(getOwner() instanceof ServerPlayer p) || !p.isAlive() || ++age>60){discard();return;}
        if(crystal() && !BiomeSoulStoneItem.equipped(p).contains(BiomeSoulStoneItem.Kind.BLOOM)){discard();return;}
        if(entityData.get(WARD) && !MaterialSoulStoneItem.equipped(p).contains(MaterialSoulStoneItem.Kind.SOULCOAT)){discard();return;}
        Entity entity=target==null?null:((ServerLevel)level()).getEntity(target);
        if(!(entity instanceof LivingEntity victim) || !BossSoulEvents.enemy(p,victim)
                || p.distanceToSqr(victim)>Math.pow(BossSoulConfig.value("common.projectile_range"),2)){discard();return;}
        Vec3 destination=victim.getBoundingBox().getCenter(),from=position(),delta=destination.subtract(from);
        Vec3 next=from.add(delta.normalize().scale(Math.min(.8,delta.length())));
        var obstruction=level().clip(new net.minecraft.world.level.ClipContext(from,next,net.minecraft.world.level.ClipContext.Block.COLLIDER,net.minecraft.world.level.ClipContext.Fluid.NONE,this));
        if(obstruction.getType()!=HitResult.Type.MISS){discard();return;}
        ((ServerLevel)level()).sendParticles(crystal()?ParticleTypes.ENCHANT:star()?ParticleTypes.END_ROD:ParticleTypes.SOUL_FIRE_FLAME,from.x,from.y,from.z,2,.03,.03,.03,0);
        setDeltaMovement(next.subtract(from));setPos(next);
        if(delta.length()<1){victim.hurt(BossSoulEvents.source(p,crystal()?"soul_crystal":star()?"soul_star":"soul_wraith",this),damage);discard();}
    }
    @Override protected void addAdditionalSaveData(CompoundTag tag){super.addAdditionalSaveData(tag);if(target!=null)tag.putUUID("Target",target);tag.putFloat("Damage",damage);tag.putBoolean("Star",star());tag.putBoolean("Crystal",crystal());tag.putBoolean("Ward",entityData.get(WARD));tag.putInt("Age",age);}
    @Override protected void readAdditionalSaveData(CompoundTag tag){super.readAdditionalSaveData(tag);target=tag.hasUUID("Target")?tag.getUUID("Target"):null;damage=tag.getFloat("Damage");entityData.set(STAR,tag.getBoolean("Star"));entityData.set(CRYSTAL,tag.getBoolean("Crystal"));entityData.set(WARD,tag.getBoolean("Ward"));age=tag.getInt("Age");}
    @Override public Packet<ClientGamePacketListener> getAddEntityPacket(){return NetworkHooks.getEntitySpawningPacket(this);}
}
