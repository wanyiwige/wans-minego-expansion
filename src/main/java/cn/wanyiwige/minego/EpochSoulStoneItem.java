package cn.wanyiwige.minego;

import com.google.common.collect.LinkedHashMultimap;
import com.google.common.collect.Multimap;
import java.util.*;
import javax.annotation.Nullable;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.*;
import net.minecraft.world.level.Level;
import net.minecraftforge.registries.ForgeRegistries;
import top.theillusivec4.curios.api.CuriosApi;
import top.theillusivec4.curios.api.SlotContext;
import top.theillusivec4.curios.api.type.capability.ICurioItem;

/** SAE is optional: no class from that mod is linked by this integration. */
public final class EpochSoulStoneItem extends Item implements ICurioItem {
    public enum Kind {
        FANGZUN, CANGYAO, ZIXU, ZHENYAN, GOLDENHOU, GENERAL,
        MAGNETIC_STEEL, DAMASCENE, BRONZE, JADE, TALISMAN, TYPE,
        GHOST_JADE, PYROTEMPER, CLASSICS, CAULDRON, TIGER, RUSTED,
        EXPLORER, CELESTERRAL, FOUR_SOVEREIGNS, EPOCH;
        public String key() { return name().toLowerCase(Locale.ROOT); }
        public String id() { return "epoch_" + key() + "_soul_stone"; }
        public EnumSet<Kind> abilities() {
            return switch (this) {
                case CELESTERRAL -> EnumSet.of(MAGNETIC_STEEL, DAMASCENE, JADE, TALISMAN);
                case FOUR_SOVEREIGNS -> EnumSet.of(FANGZUN, CANGYAO, ZIXU, ZHENYAN);
                case EPOCH -> EnumSet.of(FANGZUN, CANGYAO, ZIXU, ZHENYAN, GOLDENHOU, GENERAL,
                        MAGNETIC_STEEL, DAMASCENE, JADE, TALISMAN, EXPLORER);
                default -> EnumSet.of(this);
            };
        }
    }
    public final Kind kind;
    public EpochSoulStoneItem(Kind kind) {
        super(new Properties().stacksTo(1).fireResistant().rarity(
                kind == Kind.EPOCH ? Rarity.EPIC : kind.ordinal() < 6 || kind == Kind.FOUR_SOVEREIGNS ? Rarity.RARE : Rarity.UNCOMMON));
        this.kind = kind;
    }
    public static List<ItemStack> stones(LivingEntity e) {
        return CuriosApi.getCuriosHelper().findCurios(e, s -> s.getItem() instanceof EpochSoulStoneItem)
                .stream().map(s -> s.stack()).toList();
    }
    public static EnumSet<Kind> equipped(LivingEntity e) {
        var result = EnumSet.noneOf(Kind.class);
        for (var s : stones(e)) result.addAll(((EpochSoulStoneItem)s.getItem()).kind.abilities());
        return result;
    }
    public static int mode(ItemStack s) { return Math.floorMod(s.hasTag() ? s.getTag().getInt("EpochMode") : 0, 4); }
    public static int mode(LivingEntity e, Kind ability) {
        for (var s : stones(e)) if (((EpochSoulStoneItem)s.getItem()).kind.abilities().contains(ability)) return mode(s);
        return 0;
    }
    @Override public boolean canEquip(SlotContext slot, ItemStack stack) {
        return Collections.disjoint(kind.abilities(), equipped(slot.entity()));
    }
    @Override public InteractionResultHolder<ItemStack> use(Level level, Player p, InteractionHand hand) {
        var stack = p.getItemInHand(hand);
        if (!p.isShiftKeyDown() || !(kind.abilities().contains(Kind.TALISMAN) || kind.abilities().contains(Kind.EXPLORER)))
            return InteractionResultHolder.pass(stack);
        if (!level.isClientSide) {
            int mode = (mode(stack) + 1) % 4;
            stack.getOrCreateTag().putInt("EpochMode", mode);
            p.displayClientMessage(Component.translatable("tooltip.wans_minego_expansion.epoch.mode." + mode), true);
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide);
    }
    @Override public Multimap<Attribute, AttributeModifier> getAttributeModifiers(SlotContext slot, UUID uuid, ItemStack stack) {
        Multimap<Attribute, AttributeModifier> out = LinkedHashMultimap.create();
        var a = kind.abilities();
        if (a.contains(Kind.MAGNETIC_STEEL)) {
            add(out, Attributes.ARMOR, uuid, EpochSoulConfig.v("steel.armor"), false);
            dynamic(out, "alex_caves_spellsbook:magnetic_spell_power", uuid, EpochSoulConfig.v("steel.power"));
        }
        if (a.contains(Kind.JADE)) dynamic(out, "iss_magicfromtheeast:symmetry_spell_power", uuid, EpochSoulConfig.v("jade.power"));
        if (a.contains(Kind.FANGZUN) || a.contains(Kind.JADE))
            dynamic(out, "irons_spellbooks:spell_resist", uuid,
                    (a.contains(Kind.FANGZUN) ? EpochSoulConfig.v("fang.resist") : 0) + (a.contains(Kind.JADE) ? EpochSoulConfig.v("jade.resist") : 0));
        if (a.contains(Kind.RUSTED)) add(out, Attributes.KNOCKBACK_RESISTANCE, uuid, EpochSoulConfig.v("rusted.knockback"), false);
        return out;
    }
    private static void dynamic(Multimap<Attribute,AttributeModifier> out, String key, UUID uuid, double value) {
        var attr = ForgeRegistries.ATTRIBUTES.getValue(new ResourceLocation(key));
        if (attr != null) add(out, attr, uuid, value, true);
    }
    private static void add(Multimap<Attribute,AttributeModifier> out, Attribute attr, UUID uuid, double value, boolean multiply) {
        out.put(attr, new AttributeModifier(uuid, "wan_epoch_soul", value,
                multiply ? AttributeModifier.Operation.MULTIPLY_BASE : AttributeModifier.Operation.ADDITION));
    }
    @Override public void appendHoverText(ItemStack stack, @Nullable Level level, List<Component> tooltip, TooltipFlag flag) {
        for (var ability : kind.abilities()) {
            Object[] values = EpochSoulConfig.tooltip(ability);
            SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion.epoch." + ability.key(), values));
        }
        if (kind.abilities().contains(Kind.TALISMAN) || kind.abilities().contains(Kind.EXPLORER)) {
            SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion.epoch.switch"));
            SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion.epoch.mode." + mode(stack)));
        }
        SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion.epoch.rules"));
    }
}
