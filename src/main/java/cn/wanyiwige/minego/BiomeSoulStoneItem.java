package cn.wanyiwige.minego;

import com.google.common.collect.LinkedHashMultimap;
import com.google.common.collect.Multimap;
import java.util.EnumSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import javax.annotation.Nullable;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraft.world.item.*;
import net.minecraft.world.level.Level;
import net.minecraftforge.common.ForgeMod;
import top.theillusivec4.curios.api.CuriosApi;
import top.theillusivec4.curios.api.SlotContext;
import top.theillusivec4.curios.api.type.capability.ICurioItem;

public final class BiomeSoulStoneItem extends Item implements ICurioItem {
    public enum Kind {
        BLOOM("bloom", "sacilite_bloom", "sacilite_cavern"),
        STORM("storm", "storm_jungle"), TIME("time", "sands_of_time"),
        SCARLET("scarlet", "scarlet_fields"), WASTE("waste", "wasteland", "irradiated_undergrowth"),
        MIRE("mire", "miserable_mire"), GROWTH("growth", "overgrowth"),
        ASH("ash", "ashen_woods", "volcanic_valley", "emberlight_valley"),
        OTHERWORLD("otherworld");
        final String key;
        final Set<String> biomes;
        Kind(String key, String... biomes) { this.key = key; this.biomes = Set.of(biomes); }
        public String key() { return key; }
        public Set<String> biomePaths() { return biomes; }
        public String id() { return this == OTHERWORLD ? "soul_of_otherworld" : "foolish_" + key + "_biome_soul_stone"; }
        public EnumSet<Kind> abilities() { return this == OTHERWORLD ? EnumSet.range(BLOOM, ASH) : EnumSet.of(this); }
        public boolean matches(ResourceLocation biome) { return biome.getNamespace().equals("foolish") && biomes.contains(biome.getPath()); }
        public static Kind forBiome(ResourceLocation biome) {
            for (var kind : values()) if (kind.matches(biome)) return kind;
            return null;
        }
        public static Kind fromKey(String key) {
            for (var kind : values()) if (kind != OTHERWORLD && kind.key.equals(key)) return kind;
            return null;
        }
    }
    private final Kind kind;
    public BiomeSoulStoneItem(Kind kind) { super(new Properties().stacksTo(1).fireResistant()); this.kind = kind; }
    public Kind kind() { return kind; }
    public static EnumSet<Kind> equipped(LivingEntity entity) {
        var result = nativeEquipped(entity);
        for (var material : MaterialSoulStoneItem.equipped(entity)) if (material.inherited != null) result.add(material.inherited);
        return result;
    }
    public static EnumSet<Kind> nativeEquipped(LivingEntity entity) {
        var result = EnumSet.noneOf(Kind.class);
        CuriosApi.getCuriosHelper().findCurios(entity, stack -> stack.getItem() instanceof BiomeSoulStoneItem)
                .forEach(slot -> result.addAll(((BiomeSoulStoneItem)slot.stack().getItem()).kind.abilities()));
        return result;
    }
    @Override public boolean canEquip(SlotContext slot, ItemStack stack) {
        var existing = equipped(slot.entity()); existing.retainAll(kind.abilities()); return existing.isEmpty();
    }
    @Override public Multimap<Attribute, AttributeModifier> getAttributeModifiers(SlotContext slot, UUID uuid, ItemStack stack) {
        Multimap<Attribute, AttributeModifier> result = LinkedHashMultimap.create();
        if (kind.abilities().contains(Kind.TIME)) result.put(Attributes.MOVEMENT_SPEED,
                new AttributeModifier(uuid, "wan_biome_time", BiomeSoulConfig.v("time.move_speed"), AttributeModifier.Operation.MULTIPLY_BASE));
        if (kind.abilities().contains(Kind.MIRE)) result.put(ForgeMod.SWIM_SPEED.get(),
                new AttributeModifier(uuid, "wan_biome_mire", BiomeSoulConfig.v("mire.swim_speed"), AttributeModifier.Operation.MULTIPLY_BASE));
        return result;
    }
    @Override public void appendHoverText(ItemStack stack, @Nullable Level level, List<Component> tooltip, TooltipFlag flag) {
        for (var ability : kind.abilities()) {
            SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion.biome." + ability.key, stats(ability)));
            SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion.biome.region." + ability.key));
        }
        SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion.biome.rules",
                BiomeSoulConfig.number("common.biome_multiplier", false)));
    }
    private static Object[] stats(Kind kind) {
        String keys = switch (kind) {
            case BLOOM -> "bloom.mining% bloom.cooldown bloom.damage_ratio% bloom.damage_cap";
            case STORM -> "storm.charge_seconds storm.damage_ratio% storm.damage_cap storm.cooldown";
            case TIME -> "time.move_speed% time.mining% time.escape_seconds time.escape_cooldown";
            case SCARLET -> "scarlet.chance% scarlet.cooldown scarlet.max_summons scarlet.life_seconds scarlet.health scarlet.attack";
            case WASTE -> "waste.duration_reduction% waste.chance% waste.corrosion_seconds waste.cooldown";
            case MIRE -> "mire.swim_speed% mire.heal_interval mire.heal";
            case GROWTH -> "growth.cooldown growth.radius growth.max_targets growth.slow_seconds growth.heal";
            case ASH -> "ash.burn_reduction% ash.burning_bonus% ash.cooldown ash.radius ash.max_targets ash.damage";
            default -> "";
        };
        return java.util.Arrays.stream(keys.split(" ")).map(key -> (Object)BiomeSoulConfig.number(
                key.replace("%", ""), key.endsWith("%"))).toArray();
    }
}
