package cn.wanyiwige.minego;

import java.util.*;
import net.minecraftforge.common.ForgeConfigSpec;

public final class MaterialSoulConfig {
    private static final ForgeConfigSpec.Builder B=new ForgeConfigSpec.Builder();
    private static final Map<String,ForgeConfigSpec.DoubleValue> VALUES=new LinkedHashMap<>();
    public static final ForgeConfigSpec SPEC;
    static {
        define("blunt.armor",3,30); define("blunt.knockback",.10,1);
        define("thunder.hits",4,30);
        define("infernal.burn_reduction",.30,.9); define("infernal.burning_bonus",.05,1);
        define("steel.armor",2,30); define("steel.toughness",2,30);
        define("steel.low_health",.35,1); define("steel.low_knockback",.25,1);
        define("slide.ramp_seconds",4,30); define("slide.max_speed",.25,1);
        define("parasite.regen_seconds",3,30); define("parasite.cooldown",6,300);
        define("soulcoat.ratio",.20,2); define("soulcoat.damage_cap",8,100);
        define("soulcoat.cooldown",6,300); define("soulcoat.range",16,32);
        define("common.hit_gate",.5,10); SPEC=B.build();
    }
    private static void define(String key,double value,double max){VALUES.put(key,B.defineInRange(key,value,0,max));}
    public static double v(String key){var value=VALUES.get(key);return SPEC.isLoaded()?value.get():value.getDefault();}
    public static int ticks(String key){return Math.max(1,(int)Math.round(v(key)*20));}
    private MaterialSoulConfig(){}
}
