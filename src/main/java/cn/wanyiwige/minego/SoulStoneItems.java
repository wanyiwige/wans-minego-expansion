package cn.wanyiwige.minego;

import net.minecraft.world.item.Item;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;
import org.slf4j.Logger;
import com.mojang.logging.LogUtils;

public final class SoulStoneItems {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, WansMinegoExpansion.MOD_ID);
    private static final Logger LOGGER = LogUtils.getLogger();
    public static final RegistryObject<Item> SYMMETRY = stone("symmetry_sect_soul_stone", SchoolSoulStoneItem.School.SYMMETRY);
    public static final RegistryObject<Item> SPIRIT = stone("spirit_sect_soul_stone", SchoolSoulStoneItem.School.SPIRIT);
    public static final RegistryObject<Item> INSECT = stone("insect_soul_stone", SchoolSoulStoneItem.School.INSECT);
    public static final RegistryObject<Item> DREAM = stone("dream_soul_stone", SchoolSoulStoneItem.School.DREAM);
    public static final RegistryObject<Item> WIND = stone("wind_soul_stone", SchoolSoulStoneItem.School.WIND);
    public static final RegistryObject<Item> ANNIHILATION = stone("annihilation_soul_stone", SchoolSoulStoneItem.School.ANNIHILATION);
    public static final RegistryObject<Item> SHADOW = stone("shadow_soul_stone", SchoolSoulStoneItem.School.SHADOW);
    public static final RegistryObject<Item> UNSTABLE = stone("unstable_soul_stone", SchoolSoulStoneItem.School.UNSTABLE);
    public static final RegistryObject<Item> RELICRON = stone("relicron_soul_stone", SchoolSoulStoneItem.School.RELICRON);
    public static final RegistryObject<Item> INFINITY = stone("infinity_soul_stone", SchoolSoulStoneItem.School.INFINITY);
    public static final RegistryObject<Item> TAINTED = stone("tainted_soul_stone", SchoolSoulStoneItem.School.TAINTED);
    public static final RegistryObject<Item> TRAILBLAZER_ARCANA = stone("trailblazer_arcana_soul_stone", SchoolSoulStoneItem.School.TRAILBLAZER_ARCANA);
    public static final RegistryObject<Item> FUSION = stone("fusion_soul_stone", SchoolSoulStoneItem.School.FUSION);
    public static final RegistryObject<Item> ARS_NOUVEAU = stone("ars_nouveau_soul_stone", SchoolSoulStoneItem.School.ARS_NOUVEAU);
    public static final RegistryObject<Item> ABYSSAL = stone("abyssal_soul_stone", SchoolSoulStoneItem.School.ABYSSAL);
    public static final RegistryObject<Item> TECHNOMANCY = stone("technomancy_soul_stone", SchoolSoulStoneItem.School.TECHNOMANCY);
    public static final RegistryObject<Item> ESOTERIC = stone("esoteric_soul_stone", SchoolSoulStoneItem.School.ESOTERIC);
    public static final RegistryObject<Item> GLUTTONY = stone("gluttony_soul_stone", SchoolSoulStoneItem.School.GLUTTONY);
    public static final RegistryObject<Item> GLINTSTONE = stone("glintstone_soul_stone", SchoolSoulStoneItem.School.GLINTSTONE);
    public static final RegistryObject<Item> GLUTTON = stone("glutton_soul_stone", SchoolSoulStoneItem.School.GLUTTON);
    public static final RegistryObject<Item> SMITHING = stone("smithing_soul_stone", SchoolSoulStoneItem.School.SMITHING);
    public static final RegistryObject<Item> CURSE = stone("curse_soul_stone", SchoolSoulStoneItem.School.CURSE);
    public static final RegistryObject<Item> TIME = stone("time_soul_stone", SchoolSoulStoneItem.School.TIME);
    public static final RegistryObject<Item> ECHO = stone("echo_soul_stone", SchoolSoulStoneItem.School.ECHO);
    public static final RegistryObject<Item> EXO = stone("exo_soul_stone", SchoolSoulStoneItem.School.EXO);
    public static final RegistryObject<Item> MAGNETIC = stone("magnetic_school_soul_stone", SchoolSoulStoneItem.School.MAGNETIC);
    public static final RegistryObject<Item> CANDY = stone("candy_school_soul_stone", SchoolSoulStoneItem.School.CANDY);
    public static final RegistryObject<Item> CLOUD = stone("cloud_school_soul_stone", SchoolSoulStoneItem.School.CLOUD);
    public static final RegistryObject<Item> TOXIC = stone("toxic_school_soul_stone", SchoolSoulStoneItem.School.TOXIC);
    public static final RegistryObject<Item> ASTRAL = stone("astral_soul_stone", SchoolSoulStoneItem.School.ASTRAL);
    public static final RegistryObject<Item> TRAVELLER = stone("traveller_soul_stone", SchoolSoulStoneItem.School.TRAVELLER);
    public static final RegistryObject<Item> HAZEN_COSMIC = stone("hazen_cosmic_soul_stone", SchoolSoulStoneItem.School.HAZEN_COSMIC);
    public static final RegistryObject<Item> HAZEN_RADIANCE = stone("hazen_radiance_soul_stone", SchoolSoulStoneItem.School.HAZEN_RADIANCE);
    public static final RegistryObject<Item> HAZEN_SHADOW = stone("hazen_shadow_soul_stone", SchoolSoulStoneItem.School.HAZEN_SHADOW);
    public static final RegistryObject<Item> HAZEN_HYDRO = stone("hazen_hydro_soul_stone", SchoolSoulStoneItem.School.HAZEN_HYDRO);

    public static final java.util.Map<BossSoulStoneItem.Kind, RegistryObject<Item>> BOSS = registerBosses();
    public static final RegistryObject<Item> ATTUNED = SoulDependencies.loaded("foolish")
            ? ITEMS.register("foolish_attuned_soul_stone", AttunedSoulStoneItem::new) : null;
    public static final java.util.Map<BiomeSoulStoneItem.Kind, RegistryObject<Item>> BIOME = registerBiomes();
    public static final java.util.Map<MaterialSoulStoneItem.Kind, RegistryObject<Item>> MATERIAL = registerMaterials();
    public static final java.util.Map<EpochSoulStoneItem.Kind, RegistryObject<Item>> EPOCH = registerEpoch();
    public static final java.util.Map<String, RegistryObject<Item>> EPOCH_PROOFS = registerEpochProofs();

    private static java.util.Map<EpochSoulStoneItem.Kind, RegistryObject<Item>> registerEpoch() {
        var result = new java.util.EnumMap<EpochSoulStoneItem.Kind, RegistryObject<Item>>(EpochSoulStoneItem.Kind.class);
        if (SoulDependencies.loaded("splendour_ablaze_epoch")) for (var kind : EpochSoulStoneItem.Kind.values())
            result.put(kind, ITEMS.register(kind.id(), () -> new EpochSoulStoneItem(kind)));
        return java.util.Collections.unmodifiableMap(result);
    }

    private static java.util.Map<String, RegistryObject<Item>> registerEpochProofs() {
        var result = new java.util.LinkedHashMap<String, RegistryObject<Item>>();
        if (SoulDependencies.loaded("splendour_ablaze_epoch")) for (String key : new String[]{"cauldron", "tiger", "rusted", "explorer", "complete"})
            result.put(key, ITEMS.register("epoch_" + key + "_proof", () -> new Item(new Item.Properties().fireResistant())));
        return java.util.Collections.unmodifiableMap(result);
    }

    private static java.util.Map<MaterialSoulStoneItem.Kind, RegistryObject<Item>> registerMaterials() {
        var result = new java.util.EnumMap<MaterialSoulStoneItem.Kind, RegistryObject<Item>>(MaterialSoulStoneItem.Kind.class);
        if (SoulDependencies.loaded("foolish")) for (var kind : MaterialSoulStoneItem.Kind.values())
            result.put(kind, ITEMS.register(kind.id(), () -> new MaterialSoulStoneItem(kind)));
        return java.util.Collections.unmodifiableMap(result);
    }

    private static java.util.Map<BiomeSoulStoneItem.Kind, RegistryObject<Item>> registerBiomes() {
        var result = new java.util.EnumMap<BiomeSoulStoneItem.Kind, RegistryObject<Item>>(BiomeSoulStoneItem.Kind.class);
        if (SoulDependencies.loaded("foolish")) for (var kind : BiomeSoulStoneItem.Kind.values())
            result.put(kind, ITEMS.register(kind.id(), () -> new BiomeSoulStoneItem(kind)));
        return java.util.Collections.unmodifiableMap(result);
    }

    private static java.util.Map<BossSoulStoneItem.Kind, RegistryObject<Item>> registerBosses() {
        var result = new java.util.EnumMap<BossSoulStoneItem.Kind, RegistryObject<Item>>(BossSoulStoneItem.Kind.class);
        if (SoulDependencies.loaded("foolish")) {
            for (var kind : BossSoulStoneItem.Kind.values()) {
                result.put(kind, ITEMS.register(kind.id(), () -> new BossSoulStoneItem(kind)));
            }
        } else {
            LOGGER.info("Foolish absent: skipping all 12 Foolish soul stones");
        }
        return java.util.Collections.unmodifiableMap(result);
    }

    private static RegistryObject<Item> stone(String name, SchoolSoulStoneItem.School school) {
        if (!school.available()) {
            LOGGER.info("Skipping soul stone {}: requires {}", name, java.util.Arrays.toString(school.dependencies()));
            return null;
        }
        return ITEMS.register(name, () -> new SchoolSoulStoneItem(school));
    }

    private SoulStoneItems() {}
}
