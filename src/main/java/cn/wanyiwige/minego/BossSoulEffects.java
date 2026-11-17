package cn.wanyiwige.minego;

import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public final class BossSoulEffects {
    public static final DeferredRegister<MobEffect> EFFECTS = DeferredRegister.create(ForgeRegistries.MOB_EFFECTS, WansMinegoExpansion.MOD_ID);
    public static final RegistryObject<MobEffect> TIME_SLOW = movement("time_slow", "timewelder.shift", -1, 0x6688cf);
    public static final RegistryObject<MobEffect> TIME_SPEED = movement("time_speed", "timewelder.shift", 1, 0x9ae9ff);
    public static final RegistryObject<MobEffect> STORM_SPEED = movement("storm_speed", "thunderbird.speed", 1, 0xffdd66);
    public static final RegistryObject<MobEffect> ROOTED = EFFECTS.register("soul_rooted", () -> new MobEffect(MobEffectCategory.HARMFUL, 0x9dc990) {}
            .addAttributeModifier(Attributes.MOVEMENT_SPEED, "7deed3ad-4842-4091-8421-b57b1e392014", -1, AttributeModifier.Operation.MULTIPLY_TOTAL));
    public static final RegistryObject<MobEffect> CRYSTAL_SLOW = movement("crystal_slow", "crystal.boss_slow", -1, 0xb88aea);
    public static final RegistryObject<MobEffect> FLORA_SLOW = movement("flora_slow", "flora.boss_slow", -1, 0xdc94bb);
    public static final RegistryObject<MobEffect> CORROSION = EFFECTS.register("soul_corrosion", () -> new MobEffect(MobEffectCategory.HARMFUL, 0xa8bd56) {
        @Override public double getAttributeModifierValue(int amplifier, AttributeModifier modifier) {
            return -Math.min(1, BossSoulConfig.value("varmint.armor_loss"));
        }
    }.addAttributeModifier(Attributes.ARMOR, "2ec08304-bb1c-46dc-a023-5e7dd532dc2c", 0, AttributeModifier.Operation.MULTIPLY_TOTAL));

    private static RegistryObject<MobEffect> movement(String name, String key, int sign, int color) {
        String uuid = java.util.UUID.nameUUIDFromBytes((WansMinegoExpansion.MOD_ID + ":" + name)
                .getBytes(java.nio.charset.StandardCharsets.UTF_8)).toString();
        return EFFECTS.register(name, () -> new MobEffect(sign > 0 ? MobEffectCategory.BENEFICIAL : MobEffectCategory.HARMFUL, color) {
            @Override public double getAttributeModifierValue(int amplifier, AttributeModifier modifier) {
                return sign * Math.min(1, BossSoulConfig.value(key));
            }
        }.addAttributeModifier(Attributes.MOVEMENT_SPEED, uuid, 0, AttributeModifier.Operation.MULTIPLY_TOTAL));
    }
    private BossSoulEffects() {}
}
