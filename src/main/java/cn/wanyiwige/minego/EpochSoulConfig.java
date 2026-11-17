package cn.wanyiwige.minego;

import java.util.*;
import net.minecraftforge.common.ForgeConfigSpec;

public final class EpochSoulConfig {
    private static final ForgeConfigSpec.Builder B = new ForgeConfigSpec.Builder();
    private static final Map<String,ForgeConfigSpec.DoubleValue> V = new LinkedHashMap<>();
    private static final Map<EpochSoulStoneItem.Kind,String[]> T = new EnumMap<>(EpochSoulStoneItem.Kind.class);
    public static final ForgeConfigSpec SPEC;
    static {
        d("common.hit_gate", .5); d("common.shared_gate", 1); d("common.range", 16); d("common.cap", 12);
        t(EpochSoulStoneItem.Kind.FANGZUN,"fang.resist",.05,"fang.hits",3,"fang.cooldown",8,"fang.damage",4,"fang.slow",1);
        t(EpochSoulStoneItem.Kind.CANGYAO,"magnet.hits",4,"magnet.cooldown",6,"magnet.damage",4,"magnet.pull",.35);
        t(EpochSoulStoneItem.Kind.ZIXU,"zixu.cooldown",8,"zixu.poison",3,"zixu.refund_ratio",.10,"zixu.refund_cap",6);
        t(EpochSoulStoneItem.Kind.ZHENYAN,"fire.casts",3,"fire.damage",8,"fire.cooldown",6,"fire.reduction",.10);
        t(EpochSoulStoneItem.Kind.GOLDENHOU,"hou.hits",3,"hou.cooldown",10,"hou.damage",4,"hou.radius",3,"hou.targets",3,"hou.burn",3);
        t(EpochSoulStoneItem.Kind.GENERAL,"general.cooldown",12,"general.duration",5,"general.range",16,"general.limit",8);
        t(EpochSoulStoneItem.Kind.MAGNETIC_STEEL,"steel.armor",2,"steel.power",.05);
        t(EpochSoulStoneItem.Kind.DAMASCENE,"damascene.toughness",2,"damascene.duration",3);
        t(EpochSoulStoneItem.Kind.BRONZE,"bronze.bonus",.15,"bronze.window",4);
        t(EpochSoulStoneItem.Kind.JADE,"jade.power",.05,"jade.resist",.05);
        t(EpochSoulStoneItem.Kind.TALISMAN,"talisman.cooldown",20,"talisman.duration",4);
        t(EpochSoulStoneItem.Kind.TYPE,"type.casts",6,"type.damage",5,"type.cooldown",8);
        t(EpochSoulStoneItem.Kind.GHOST_JADE,"ghost.cooldown",20,"ghost.duration",2);
        t(EpochSoulStoneItem.Kind.PYROTEMPER,"pyro.refund_ratio",.05,"pyro.refund_cap",4,"pyro.cooldown",6);
        t(EpochSoulStoneItem.Kind.CLASSICS,"classics.regen",.10,"classics.duration",5);
        t(EpochSoulStoneItem.Kind.CAULDRON,"cauldron.xp_ratio",.10,"cauldron.xp_cap",5);
        t(EpochSoulStoneItem.Kind.TIGER,"tiger.damage",3,"tiger.window",5,"tiger.cooldown",6);
        t(EpochSoulStoneItem.Kind.RUSTED,"rusted.knockback",.10,"rusted.haze_reduction",.25);
        t(EpochSoulStoneItem.Kind.EXPLORER,"explorer.duration",3,"explorer.night_resist",.03);
        d("progress.kills",3); d("progress.visit_seconds",5);
        SPEC = B.build();
    }
    private static void d(String key,double value) { V.put(key,B.defineInRange(key,value,0,10000)); }
    private static void t(EpochSoulStoneItem.Kind kind,Object... pairs) {
        var keys = new String[pairs.length/2];
        for (int i=0;i<keys.length;i++) { keys[i]=(String)pairs[i*2]; d(keys[i],((Number)pairs[i*2+1]).doubleValue()); }
        T.put(kind,keys);
    }
    public static double v(String key) { var value=V.get(key); return SPEC.isLoaded()?value.get():value.getDefault(); }
    public static int ticks(String key) { return Math.max(1,(int)Math.round(v(key)*20)); }
    public static int count(String key) { return Math.max(1,(int)Math.round(v(key))); }
    public static Object[] tooltip(EpochSoulStoneItem.Kind kind) {
        return Arrays.stream(T.getOrDefault(kind,new String[0])).map(key ->
                (Object)java.math.BigDecimal.valueOf(v(key) * (percent(key) ? 100 : 1)).stripTrailingZeros().toPlainString()).toArray();
    }
    private static boolean percent(String key) {
        return key.endsWith(".power") || key.endsWith(".resist") || key.endsWith(".bonus") || key.endsWith(".regen")
                || key.endsWith(".knockback") || key.endsWith("_ratio") || key.endsWith("_reduction") || key.endsWith(".reduction");
    }
    private EpochSoulConfig() {}
}
