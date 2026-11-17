package cn.wanyiwige.minego;

import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraftforge.common.ForgeConfigSpec;

public final class BiomeSoulConfig {
    private static final ForgeConfigSpec.Builder B = new ForgeConfigSpec.Builder();
    private static final Map<String, ForgeConfigSpec.DoubleValue> VALUES = new LinkedHashMap<>();
    public static final ForgeConfigSpec SPEC;
    static {
        define("bloom.mining", .15, 1); define("bloom.cooldown", 6, 300);
        define("bloom.damage_ratio", .20, 2); define("bloom.damage_cap", 8, 100);
        define("storm.charge_seconds", 6, 300); define("storm.damage_ratio", .25, 2);
        define("storm.damage_cap", 10, 100); define("storm.cooldown", 3, 300);
        define("time.move_speed", .05, 1); define("time.mining", .10, 1);
        define("time.escape_seconds", 2, 30); define("time.escape_cooldown", 8, 300);
        define("scarlet.chance", .15, 1); define("scarlet.cooldown", 10, 300);
        define("scarlet.life_seconds", 8, 60); define("scarlet.health", 10, 100);
        define("scarlet.attack", 2, 30); define("scarlet.max_summons", 2, 4);
        define("waste.chance", .20, 1); define("waste.cooldown", 4, 300);
        define("waste.corrosion_seconds", 3, 30); define("waste.duration_reduction", .40, .9);
        define("mire.swim_speed", .20, 1); define("mire.heal", 1, 10);
        define("mire.heal_interval", 8, 300);
        define("growth.radius", 4, 12); define("growth.max_targets", 4, 12);
        define("growth.slow_seconds", 2, 10); define("growth.cooldown", 10, 300);
        define("growth.heal", 1, 10);
        define("ash.burn_reduction", .40, .9); define("ash.burning_bonus", .08, 1);
        define("ash.radius", 3, 12); define("ash.max_targets", 3, 12);
        define("ash.damage", 2, 30); define("ash.cooldown", 8, 300);
        define("common.biome_multiplier", 1.5, 2); define("common.hit_gate", .5, 10);
        SPEC = B.build();
    }
    private static void define(String key, double value, double max) {
        VALUES.put(key, B.defineInRange(key, value, 0, max));
    }
    public static double v(String key) {
        var value = VALUES.get(key);
        return SPEC.isLoaded() ? value.get() : value.getDefault();
    }
    public static int ticks(String key) { return Math.max(1, (int)Math.round(v(key) * 20)); }
    public static String number(String key, boolean percent) {
        return java.math.BigDecimal.valueOf(v(key) * (percent ? 100 : 1)).stripTrailingZeros().toPlainString();
    }
    private BiomeSoulConfig() {}
}
