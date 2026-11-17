package cn.wanyiwige.minego;

import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraftforge.common.ForgeConfigSpec;

public final class BossSoulConfig {
    private static final ForgeConfigSpec.Builder BUILDER = new ForgeConfigSpec.Builder();
    private static final Map<String, ForgeConfigSpec.DoubleValue> VALUES = new LinkedHashMap<>();
    public static final ForgeConfigSpec SPEC;
    static {
        define("pyre.ignite_chance", .30); define("pyre.ignite_seconds", 6);
        define("pyre.hit_gate_seconds", .5); define("pyre.burning_bonus", .10);
        define("pyre.fire_spell_bonus", .15); define("pyre.fire_reduction", .15);
        define("timewelder.move_speed", .08); define("timewelder.chance", .20);
        define("timewelder.spell_chance", .30); define("timewelder.cooldown", 6);
        define("timewelder.duration", 2); define("timewelder.shift", .15);
        define("timewelder.refund_chance", .20); define("timewelder.refund_ratio", .15);
        define("timewelder.refund_cap", 10); define("timewelder.refund_cooldown", 8);
        define("thrasher.swim_speed", .20); define("thrasher.water_bonus", .10);
        define("thrasher.splash_ratio", .20); define("thrasher.spell_ratio", .25);
        define("thrasher.cooldown", 3); define("thrasher.radius", 3); define("thrasher.targets", 3);
        define("crystal.toughness", 3); define("crystal.reflect_flat", 5);
        define("crystal.reflect_ratio", .20); define("crystal.reflect_cap", 40);
        define("crystal.reflect_cooldown", 2); define("crystal.reflect_range", 16);
        define("crystal.stagger_chance", .20); define("crystal.stagger_cooldown", 8);
        define("crystal.stagger_seconds", .75); define("crystal.boss_slow", .05);
        define("varmint.poison_seconds", 6); define("varmint.corrosion_chance", .25);
        define("varmint.corrosion_seconds", 6); define("varmint.armor_loss", .15);
        define("varmint.hit_gate", 1); define("varmint.spell_bonus", .08);
        define("thunderbird.chance", .25); define("thunderbird.cooldown", 2);
        define("thunderbird.radius", 6); define("thunderbird.first_ratio", .25);
        define("thunderbird.second_ratio", .15); define("thunderbird.damage_cap", 40);
        define("thunderbird.speed", .10); define("thunderbird.speed_seconds", 3);
        define("queen.summon_bonus", .10); define("queen.chance", .20);
        define("queen.spell_chance", .30); define("queen.cooldown", 6);
        define("queen.max_ants", 2); define("queen.life_seconds", 12);
        define("queen.health", 18); define("queen.attack", 3);
        define("flora.chance", .20); define("flora.nature_chance", .30);
        define("flora.root_seconds", 1); define("flora.boss_slow", .05);
        define("flora.cooldown", 6); define("flora.heal_ratio", .03); define("flora.heal_per_second", 2);
        define("wraith.start_hp", .50); define("wraith.peak_hp", .20);
        define("wraith.bonus", .15); define("wraith.heal", 1); define("wraith.heal_interval", 2);
        define("wraith.chance", .20); define("wraith.ratio", .30);
        define("wraith.damage_cap", 60); define("wraith.cooldown", 4);
        define("star.chance", .25); define("star.spell_chance", .35);
        define("star.ratio", .35); define("star.damage_cap", 80); define("star.cooldown", 3);
        define("star.parry_chance", .10); define("star.parry_reduction", .50);
        define("star.parry_cooldown", 12); define("star.riposte_bonus", .10); define("star.riposte_seconds", 2);
        define("common.proc_gate", .25); define("common.projectile_range", 24);
        define("common.combat_seconds", 10);
        SPEC = BUILDER.build();
    }
    private static void define(String key, double value) {
        VALUES.put(key, BUILDER.defineInRange(key, value, 0.0, 10000.0));
    }
    public static double value(String key) { return SPEC.isLoaded() ? VALUES.get(key).get() : VALUES.get(key).getDefault(); }
    public static int ticks(String key) { return Math.max(1, (int)Math.round(value(key) * 20)); }
    public static float chance(String key) { return (float)Math.min(1, value(key)); }
    private BossSoulConfig() {}
}
