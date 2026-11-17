package cn.wanyiwige.minego;

import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.fml.ModLoadingContext;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.config.ModConfig;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

@Mod(WansMinegoExpansion.MOD_ID)
public final class WansMinegoExpansion {
    public static final String MOD_ID = "wans_minego_expansion";

    public WansMinegoExpansion() {
        SoulStoneItems.ITEMS.register(FMLJavaModLoadingContext.get().getModEventBus());
        SoulStoneCreativeTab.TABS.register(FMLJavaModLoadingContext.get().getModEventBus());
        BossSoulEffects.EFFECTS.register(FMLJavaModLoadingContext.get().getModEventBus());
        BossSoulEntities.ENTITIES.register(FMLJavaModLoadingContext.get().getModEventBus());
        FMLJavaModLoadingContext.get().getModEventBus().addListener(BossSoulEntities::attributes);
        ModLoadingContext.get().registerConfig(ModConfig.Type.COMMON, SoulStoneConfig.SPEC);
        ModLoadingContext.get().registerConfig(ModConfig.Type.SERVER, BossSoulConfig.SPEC, "wans_minego_expansion-boss-souls.toml");
        ModLoadingContext.get().registerConfig(ModConfig.Type.SERVER, BiomeSoulConfig.SPEC, "wans_minego_expansion-biome-souls.toml");
        ModLoadingContext.get().registerConfig(ModConfig.Type.SERVER, MaterialSoulConfig.SPEC, "wans_minego_expansion-material-souls.toml");
        ModLoadingContext.get().registerConfig(ModConfig.Type.SERVER, EpochSoulConfig.SPEC, "wans_minego_expansion-epoch-souls.toml");
        MinecraftForge.EVENT_BUS.register(SoulStoneEvents.class);
        if (SoulDependencies.loaded("foolish")) MinecraftForge.EVENT_BUS.register(BossSoulEvents.class);
        if (SoulDependencies.loaded("foolish")) MinecraftForge.EVENT_BUS.register(BiomeSoulEvents.class);
        if (SoulDependencies.loaded("foolish")) MinecraftForge.EVENT_BUS.register(MaterialSoulEvents.class);
        if (SoulDependencies.loaded("splendour_ablaze_epoch")) MinecraftForge.EVENT_BUS.register(EpochSoulEvents.class);
    }
}
