package cn.wanyiwige.minego;

import net.minecraftforge.common.ForgeConfigSpec;

public final class SoulStoneConfig {
    private static final ForgeConfigSpec.Builder BUILDER = new ForgeConfigSpec.Builder();

    public static final ForgeConfigSpec.DoubleValue MAX_MANA = value("max_mana", 60);
    public static final ForgeConfigSpec.DoubleValue ADDED_POWER = value("added_schools.spell_power", 0.10);
    public static final ForgeConfigSpec.DoubleValue RELICRON_RESIST = value("relicron.spell_resist", 0.05);
    public static final ForgeConfigSpec.DoubleValue SYMMETRY_POWER = value("symmetry.spell_power", 0.10);
    public static final ForgeConfigSpec.DoubleValue SYMMETRY_DAMAGE = value("symmetry.spell_damage", 0.05);
    public static final ForgeConfigSpec.DoubleValue SYMMETRY_RESIST = value("symmetry.spell_resist", 0.05);
    public static final ForgeConfigSpec.DoubleValue SPIRIT_POWER = value("spirit.spell_power", 0.10);
    public static final ForgeConfigSpec.DoubleValue SPIRIT_HEAL = value("spirit.heal_from_damage", 0.05);
    public static final ForgeConfigSpec.IntValue SPIRIT_BURN_SECONDS = BUILDER.defineInRange("spirit.soulburn_seconds", 3, 0, 60);
    public static final ForgeConfigSpec SPEC = BUILDER.build();

    private static ForgeConfigSpec.DoubleValue value(String name, double defaultValue) {
        return BUILDER.defineInRange(name, defaultValue, 0.0, 10000.0);
    }

    private SoulStoneConfig() {}
}
