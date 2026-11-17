package cn.wanyiwige.minego;

import com.google.common.collect.LinkedHashMultimap;
import com.google.common.collect.Multimap;
import java.util.*;
import javax.annotation.Nullable;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraft.world.item.*;
import net.minecraft.world.level.Level;
import top.theillusivec4.curios.api.CuriosApi;
import top.theillusivec4.curios.api.SlotContext;
import top.theillusivec4.curios.api.type.capability.ICurioItem;

public final class MaterialSoulStoneItem extends Item implements ICurioItem {
    public enum Kind {
        SACILITE("sacilite", BiomeSoulStoneItem.Kind.BLOOM), THUNDERSTONE("thunderstone", BiomeSoulStoneItem.Kind.STORM),
        CORROSIVE("corrosive", BiomeSoulStoneItem.Kind.WASTE), BLUNT("blunt", null), INFERNAL("infernal", null),
        KEEPSTEEL("keepsteel", null), AMBER("amber", BiomeSoulStoneItem.Kind.TIME), SLIDE("slide", null),
        PARASITIC("parasitic", null), SOULCOAT("soulcoat", null);
        private final String key;
        final BiomeSoulStoneItem.Kind inherited;
        Kind(String key, BiomeSoulStoneItem.Kind inherited) { this.key = key; this.inherited = inherited; }
        public String key() { return key; }
        public String id() { return "foolish_" + key + "_material_soul_stone"; }
    }
    private final Kind kind;
    public MaterialSoulStoneItem(Kind kind) { super(new Properties().stacksTo(1).fireResistant()); this.kind = kind; }
    public static EnumSet<Kind> equipped(LivingEntity entity) {
        var result=EnumSet.noneOf(Kind.class);
        CuriosApi.getCuriosHelper().findCurios(entity,stack -> stack.getItem() instanceof MaterialSoulStoneItem)
                .forEach(slot -> result.add(((MaterialSoulStoneItem)slot.stack().getItem()).kind));
        return result;
    }
    @Override public boolean canEquip(SlotContext slot, ItemStack stack) {
        return !equipped(slot.entity()).contains(kind) && (kind.inherited == null
                || !BiomeSoulStoneItem.equipped(slot.entity()).contains(kind.inherited));
    }
    @Override public Multimap<Attribute, AttributeModifier> getAttributeModifiers(SlotContext slot, UUID uuid, ItemStack stack) {
        Multimap<Attribute, AttributeModifier> result=LinkedHashMultimap.create();
        switch(kind) {
            case BLUNT -> { add(result,Attributes.ARMOR,uuid,MaterialSoulConfig.v("blunt.armor")); add(result,Attributes.KNOCKBACK_RESISTANCE,uuid,MaterialSoulConfig.v("blunt.knockback")); }
            case KEEPSTEEL -> { add(result,Attributes.ARMOR,uuid,MaterialSoulConfig.v("steel.armor")); add(result,Attributes.ARMOR_TOUGHNESS,uuid,MaterialSoulConfig.v("steel.toughness")); }
            case AMBER -> result.put(Attributes.MOVEMENT_SPEED,new AttributeModifier(uuid,"wan_material_amber",BiomeSoulConfig.v("time.move_speed"),AttributeModifier.Operation.MULTIPLY_BASE));
            default -> {}
        }
        return result;
    }
    private static void add(Multimap<Attribute,AttributeModifier> result,Attribute attribute,UUID uuid,double value) {
        result.put(attribute,new AttributeModifier(uuid,"wan_material_soul",value,AttributeModifier.Operation.ADDITION));
    }
    @Override public void appendHoverText(ItemStack stack,@Nullable Level level,List<Component> tooltip,TooltipFlag flag) {
        String keys=switch(kind) {
            case SACILITE -> "biome:bloom.mining% biome:bloom.cooldown biome:bloom.damage_ratio% biome:bloom.damage_cap";
            case THUNDERSTONE -> "thunder.hits biome:storm.damage_ratio% biome:storm.damage_cap biome:storm.cooldown";
            case CORROSIVE -> "biome:waste.duration_reduction% biome:waste.chance% biome:waste.corrosion_seconds biome:waste.cooldown";
            case BLUNT -> "blunt.armor blunt.knockback%";
            case INFERNAL -> "infernal.burn_reduction% infernal.burning_bonus%";
            case KEEPSTEEL -> "steel.armor steel.toughness steel.low_health% steel.low_knockback%";
            case AMBER -> "biome:time.move_speed% biome:time.mining% biome:time.escape_seconds biome:time.escape_cooldown";
            case SLIDE -> "slide.ramp_seconds slide.max_speed%";
            case PARASITIC -> "parasite.regen_seconds parasite.cooldown";
            case SOULCOAT -> "soulcoat.ratio% soulcoat.damage_cap soulcoat.cooldown soulcoat.range";
        };
        var stats=Arrays.stream(keys.split(" ")).map(key -> {
            boolean percent=key.endsWith("%");String raw=key.replace("%","");
            double value=raw.startsWith("biome:")?BiomeSoulConfig.v(raw.substring(6)):MaterialSoulConfig.v(raw);
            return (Object)java.math.BigDecimal.valueOf(value*(percent?100:1)).stripTrailingZeros().toPlainString();
        }).toArray();
        SoulTooltip.add(tooltip,Component.translatable("tooltip.wans_minego_expansion.material."+kind.key,stats));
        SoulTooltip.add(tooltip,Component.translatable("tooltip.wans_minego_expansion.material.rules"));
    }
}
