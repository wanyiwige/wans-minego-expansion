import cn.wanyiwige.minego.BossSoulMath;
import cn.wanyiwige.minego.SoulDependencies;
import java.util.Set;

public final class BossSoulBoundaryCheck {
    static void equal(double expected,double actual) {
        if(Math.abs(expected-actual)>0.00001)throw new AssertionError(expected+" != "+actual);
    }
    public static void main(String[] args) {
        equal(6,BossSoulMath.effectiveDamage(6,500));
        equal(0,BossSoulMath.effectiveDamage(6,-1));
        equal(0,BossSoulMath.lowHealthBonus(.5,.5,.2,.15));
        equal(.075,BossSoulMath.lowHealthBonus(.35,.5,.2,.15));
        equal(.15,BossSoulMath.lowHealthBonus(.05,.5,.2,.15));
        float spent=0;
        for(int i=0;i<100;i++)spent+=BossSoulMath.healing(10,.03,2,spent);
        equal(2,spent);
        equal(.18,BossSoulMath.healing(BossSoulMath.effectiveDamage(6,500),.03,2,0));
        equal(0,BossSoulMath.healing(10,.03,2,3));
        equal(0,BossSoulMath.paidMana(100,200,220));
        equal(0,BossSoulMath.paidMana(100,200,200));
        equal(25,BossSoulMath.paidMana(100,200,175));
        equal(100,BossSoulMath.paidMana(100,200,0));
        Set<String> all=Set.of("bielgg_spells","roaring","foolish");
        if(!SoulDependencies.satisfied(all::contains,"bielgg_spells","roaring"))throw new AssertionError("all installed");
        if(SoulDependencies.satisfied(all::contains,"bielgg_spells","avaritia"))throw new AssertionError("partial dependency");
        if(SoulDependencies.satisfied(s->false,"foolish"))throw new AssertionError("absent dependency");
        System.out.println("15 boundary checks passed: overkill, shared healing cap, HP ramp, paid mana and optional dependencies.");
    }
}
