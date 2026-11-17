package cn.wanyiwige.minego;

import java.util.List;
import javax.annotation.Nullable;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.*;
import net.minecraft.world.level.Level;

/** Recipe ingredient only; attunement cannot be equipped or overwritten. */
public final class AttunedSoulStoneItem extends Item {
    public static final String TAG = "FoolishBiomeSoul";
    public AttunedSoulStoneItem() { super(new Properties().stacksTo(1).fireResistant()); }
    public static ItemStack attuned(BiomeSoulStoneItem.Kind kind) {
        var stack = new ItemStack(SoulStoneItems.ATTUNED.get());
        stack.getOrCreateTag().putString(TAG, kind.key()); return stack;
    }
    @Override public Component getName(ItemStack stack) {
        var kind = stack.hasTag() ? BiomeSoulStoneItem.Kind.fromKey(stack.getTag().getString(TAG)) : null;
        return kind == null ? super.getName(stack) : Component.translatable("item.wans_minego_expansion.attuned_named",
                Component.translatable("item.wans_minego_expansion." + kind.id()));
    }
    @Override public void appendHoverText(ItemStack stack, @Nullable Level level, List<Component> tooltip, TooltipFlag flag) {
        SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion.attuned"));
    }
}
