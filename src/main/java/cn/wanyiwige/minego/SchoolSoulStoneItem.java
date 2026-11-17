package cn.wanyiwige.minego;

import com.google.common.collect.LinkedHashMultimap;
import com.google.common.collect.Multimap;
import io.redspace.ironsspellbooks.api.registry.AttributeRegistry;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraftforge.registries.ForgeRegistries;
import top.theillusivec4.curios.api.CuriosApi;
import top.theillusivec4.curios.api.SlotContext;
import top.theillusivec4.curios.api.type.capability.ICurioItem;

import javax.annotation.Nullable;
import java.util.List;
import java.util.UUID;

public final class SchoolSoulStoneItem extends Item implements ICurioItem {
    public enum School {
        SYMMETRY("iss_magicfromtheeast:symmetry_spell_power"),
        SPIRIT("iss_magicfromtheeast:spirit_spell_power"),
        INSECT("entomology_spell:insect_spell_power"),
        DREAM("dreammagic:dream_spell_power"),
        WIND("wind_spellbooks:wind_spell_power"),
        ANNIHILATION("legendary_spellbooks:annihilation_spell_power"),
        SHADOW("bielgg_spells:shadow_spell_power"),
        UNSTABLE("bielgg_spells:unstable_spell_power"),
        RELICRON("bielgg_spells:relicron_spell_power"),
        INFINITY("bielgg_spells:infinity_spell_power"),
        TAINTED("bielgg_spells:tainted_spell_power"),
        TRAILBLAZER_ARCANA("astralrail_cube:trailblazer_arcana_damage_boost"),
        FUSION("iss_csw:fusion_spell_power"),
        ARS_NOUVEAU("ars_nouveau_spellbooks:ars_nouveau_spell_power"),
        ABYSSAL("cataclysm_spellbooks:abyssal_spell_power"),
        TECHNOMANCY("cataclysm_spellbooks:technomancy_spell_power"),
        ESOTERIC("esoteric_spell:esoteric_spell_power"),
        GLUTTONY("farmers_spell:gluttony_spell_power"),
        GLINTSTONE("iss_elden_ring:glintstone_spell_power"),
        GLUTTON("bigeater_magic:glutton_spell_power"),
        SMITHING("iron_spell_smithing_template_addon:smithing_spell_power"),
        CURSE("cursespells:curse_spell_power"),
        TIME("irons_chronomancy:time_spell_power"),
        ECHO("echo_spellbooks:echo_spell_power"),
        EXO("roacw:exo_spell_power"),
        MAGNETIC("alex_caves_spellsbook:magnetic_spell_power"),
        CANDY("alex_caves_spellsbook:candy_spell_power"),
        CLOUD("alex_caves_spellsbook:cloud_spell_power"),
        TOXIC("alex_caves_spellsbook:toxic_spell_power"),
        ASTRAL("kubejs:astral_spell_power"),
        TRAVELLER("kubejs:traveller_spell_power"),
        HAZEN_COSMIC("alex_caves_spellsbook:hazen_cosmic_spell_power"),
        HAZEN_RADIANCE("alex_caves_spellsbook:hazen_radiance_spell_power"),
        HAZEN_SHADOW("alex_caves_spellsbook:hazen_shadow_spell_power"),
        HAZEN_HYDRO("alex_caves_spellsbook:hazen_hydro_spell_power");

        private final ResourceLocation powerId;

        School(String powerId) { this.powerId = new ResourceLocation(powerId); }

        public String[] dependencies() {
            return switch (this) {
                case SHADOW -> new String[]{"bielgg_spells", "roaring"};
                case RELICRON -> new String[]{"bielgg_spells", "eeeabsmobs"};
                case INFINITY -> new String[]{"bielgg_spells", "avaritia"};
                case TAINTED -> new String[]{"bielgg_spells", "witherstormmod"};
                // These schools use the kubejs namespace but are registered by the Java mod.
                case ASTRAL, TRAVELLER -> new String[]{"alex_caves_spellsbook"};
                default -> new String[]{powerId.getNamespace()};
            };
        }

        public boolean available() {
            if (!SoulDependencies.loaded(dependencies())) return false;
            // Older releases of the provider do not contain the full migrated school set.
            return switch (this) {
                case MAGNETIC, CANDY, CLOUD, TOXIC, ASTRAL, TRAVELLER,
                        HAZEN_COSMIC, HAZEN_RADIANCE, HAZEN_SHADOW, HAZEN_HYDRO ->
                        SoulDependencies.atLeast("alex_caves_spellsbook", "1.2.2");
                default -> true;
            };
        }
    }

    private final School school;

    public SchoolSoulStoneItem(School school) {
        super(new Item.Properties().stacksTo(1).fireResistant());
        this.school = school;
    }

    @Override
    public Multimap<Attribute, AttributeModifier> getAttributeModifiers(SlotContext slotContext, UUID uuid, ItemStack stack) {
        Multimap<Attribute, AttributeModifier> modifiers = LinkedHashMultimap.create();
        Attribute power = ForgeRegistries.ATTRIBUTES.getValue(school.powerId);
        double powerAmount = school == School.SYMMETRY ? SoulStoneConfig.SYMMETRY_POWER.get()
                : school == School.SPIRIT ? SoulStoneConfig.SPIRIT_POWER.get() : SoulStoneConfig.ADDED_POWER.get();
        if (power != null) {
            modifiers.put(power, new AttributeModifier(uuid, "wan_minego_school_power", powerAmount,
                    school == School.TRAILBLAZER_ARCANA || school == School.ASTRAL
                            ? AttributeModifier.Operation.ADDITION : AttributeModifier.Operation.MULTIPLY_BASE));
        }
        modifiers.put(AttributeRegistry.MAX_MANA.get(), new AttributeModifier(uuid, "wan_minego_max_mana",
                SoulStoneConfig.MAX_MANA.get(), AttributeModifier.Operation.ADDITION));
        if (school == School.SYMMETRY) {
            modifiers.put(AttributeRegistry.SPELL_RESIST.get(), new AttributeModifier(uuid,
                    "wan_minego_spell_resist", SoulStoneConfig.SYMMETRY_RESIST.get(),
                    AttributeModifier.Operation.MULTIPLY_BASE));
        }
        if (school == School.RELICRON) {
            modifiers.put(AttributeRegistry.SPELL_RESIST.get(), new AttributeModifier(uuid,
                    "wan_minego_relicron_resist", SoulStoneConfig.RELICRON_RESIST.get(),
                    AttributeModifier.Operation.MULTIPLY_BASE));
        }
        Attribute secondary = switch (school) {
            case TRAILBLAZER_ARCANA, ABYSSAL, HAZEN_RADIANCE -> AttributeRegistry.SPELL_RESIST.get();
            case FUSION, GLINTSTONE, ASTRAL -> AttributeRegistry.MANA_REGEN.get();
            case ARS_NOUVEAU, HAZEN_COSMIC -> AttributeRegistry.SUMMON_DAMAGE.get();
            case TECHNOMANCY, TIME -> AttributeRegistry.COOLDOWN_REDUCTION.get();
            case ESOTERIC, HAZEN_SHADOW -> AttributeRegistry.CAST_TIME_REDUCTION.get();
            case GLUTTONY, GLUTTON, CANDY -> Attributes.MAX_HEALTH;
            case SMITHING -> Attributes.ARMOR;
            case EXO -> Attributes.ARMOR_TOUGHNESS;
            case MAGNETIC -> Attributes.KNOCKBACK_RESISTANCE;
            case CLOUD, TRAVELLER -> Attributes.MOVEMENT_SPEED;
            case HAZEN_HYDRO -> net.minecraftforge.common.ForgeMod.SWIM_SPEED.get();
            default -> null;
        };
        if (secondary != null) {
            boolean health = school == School.GLUTTONY || school == School.GLUTTON || school == School.CANDY;
            boolean flat = health || school == School.SMITHING || school == School.EXO || school == School.MAGNETIC;
            double amount = health || school == School.SMITHING ? 2.0 : school == School.EXO ? 1.0
                    : school == School.MAGNETIC || school == School.HAZEN_HYDRO ? 0.10 : 0.05;
            modifiers.put(secondary, new AttributeModifier(uuid, "wan_minego_school_specialty",
                    amount, flat ? AttributeModifier.Operation.ADDITION : AttributeModifier.Operation.MULTIPLY_BASE));
        }
        return modifiers;
    }

    @Override
    public boolean canEquip(SlotContext slotContext, ItemStack stack) {
        for (String masterId : List.of("soul_of_iron_spell", "soul_of_inolia")) {
            Item combined = ForgeRegistries.ITEMS.getValue(new ResourceLocation("mine_fargo", masterId));
            if (combined != null && CuriosApi.getCuriosHelper().findFirstCurio(slotContext.entity(), combined).isPresent()) {
                return false;
            }
        }
        return CuriosApi.getCuriosHelper().findFirstCurio(slotContext.entity(), this).isEmpty();
    }

    @Override
    public void appendHoverText(ItemStack stack, @Nullable Level level, List<Component> tooltip, TooltipFlag flag) {
        if (school == School.SYMMETRY) {
            SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion.symmetry_sect_soul_stone",
                    percent(SoulStoneConfig.SYMMETRY_POWER.get()), SoulStoneConfig.MAX_MANA.get().intValue(),
                    percent(SoulStoneConfig.SYMMETRY_DAMAGE.get()), percent(SoulStoneConfig.SYMMETRY_RESIST.get())));
        } else if (school == School.SPIRIT) {
            SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion.spirit_sect_soul_stone",
                    percent(SoulStoneConfig.SPIRIT_POWER.get()), SoulStoneConfig.MAX_MANA.get().intValue(),
                    SoulStoneConfig.SPIRIT_BURN_SECONDS.get(), percent(SoulStoneConfig.SPIRIT_HEAL.get())));
        } else {
            SoulTooltip.add(tooltip, Component.translatable(school == School.TRAILBLAZER_ARCANA
                            ? "tooltip.wans_minego_expansion.trailblazer_base"
                            : "tooltip.wans_minego_expansion.school_power",
                    percent(SoulStoneConfig.ADDED_POWER.get()), SoulStoneConfig.MAX_MANA.get().intValue()));
            SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion." + school.name().toLowerCase()));
        }
        super.appendHoverText(stack, level, tooltip, flag);
    }

    private static int percent(double ratio) { return (int) Math.round(ratio * 100); }
}
