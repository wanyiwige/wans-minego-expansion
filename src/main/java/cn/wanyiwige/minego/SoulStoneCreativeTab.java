package cn.wanyiwige.minego;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

public final class SoulStoneCreativeTab {
    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, WansMinegoExpansion.MOD_ID);

    public static final RegistryObject<CreativeModeTab> SOUL_STONES = TABS.register("soul_stones",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.wans_minego_expansion.soul_stones"))
                    .icon(() -> SoulStoneItems.ITEMS.getEntries().stream().filter(RegistryObject::isPresent).findFirst().map(item -> new ItemStack(item.get())).orElse(new ItemStack(net.minecraft.world.item.Items.AMETHYST_SHARD)))
                    .displayItems((parameters, output) -> {
                        SoulStoneItems.ITEMS.getEntries().stream().filter(RegistryObject::isPresent)
                                .filter(item -> item != SoulStoneItems.ATTUNED).forEach(item -> output.accept(item.get()));
                        if (SoulStoneItems.ATTUNED != null && SoulStoneItems.ATTUNED.isPresent())
                            for (var kind : BiomeSoulStoneItem.Kind.values())
                                if (kind != BiomeSoulStoneItem.Kind.OTHERWORLD) output.accept(AttunedSoulStoneItem.attuned(kind));
                    })
                    .build());

    private SoulStoneCreativeTab() {}
}
