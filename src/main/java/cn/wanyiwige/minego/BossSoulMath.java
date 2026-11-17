package cn.wanyiwige.minego;

/** Pure settlement boundaries, independent of Minecraft entity lifecycle. */
public final class BossSoulMath {
    public static float effectiveDamage(float health, float damage) { return Math.max(0, Math.min(health, damage)); }
    public static double lowHealthBonus(double healthRatio, double start, double peak, double cap) {
        return cap * Math.max(0, Math.min(1, (start-healthRatio)/Math.max(.001,start-peak)));
    }
    public static float healing(float damage, double ratio, double cap, float alreadyHealed) {
        return (float)Math.max(0,Math.min(damage*ratio,Math.max(0,cap-alreadyHealed)));
    }
    public static float paidMana(float cost, float before, float after) { return Math.max(0, Math.min(cost, before-after)); }
    private BossSoulMath() {}
}
