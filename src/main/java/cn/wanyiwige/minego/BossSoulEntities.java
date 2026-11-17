package cn.wanyiwige.minego;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraftforge.event.entity.EntityAttributeCreationEvent;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public final class BossSoulEntities {
    public static final DeferredRegister<EntityType<?>> ENTITIES = DeferredRegister.create(ForgeRegistries.ENTITY_TYPES, WansMinegoExpansion.MOD_ID);
    public static final RegistryObject<EntityType<SoulAntEntity>> ANT = SoulDependencies.loaded("foolish")
            ? ENTITIES.register("soul_ant", () -> EntityType.Builder.of(SoulAntEntity::new, MobCategory.CREATURE)
                .sized(.65f, .45f).clientTrackingRange(8).build("soul_ant")) : null;
    public static final RegistryObject<EntityType<SoulBoltEntity>> BOLT = SoulDependencies.loaded("foolish")
            ? ENTITIES.register("soul_bolt", () -> EntityType.Builder.<SoulBoltEntity>of(SoulBoltEntity::new, MobCategory.MISC)
                .sized(.25f, .25f).clientTrackingRange(8).updateInterval(1).build("soul_bolt")) : null;

    public static void attributes(EntityAttributeCreationEvent event) {
        if (ANT != null && ANT.isPresent()) event.put(ANT.get(), SoulAntEntity.attributes().build());
    }
    private BossSoulEntities() {}
}
