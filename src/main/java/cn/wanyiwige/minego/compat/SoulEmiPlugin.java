package cn.wanyiwige.minego.compat;

import cn.wanyiwige.minego.SoulStoneItems;
import dev.emi.emi.api.*;
import dev.emi.emi.api.recipe.EmiInfoRecipe;
import dev.emi.emi.api.stack.*;
import java.util.List;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.fml.ModList;

@EmiEntrypoint
public final class SoulEmiPlugin implements EmiPlugin {
    @Override public void register(EmiRegistry registry) {
        if (SoulStoneItems.ATTUNED != null && SoulStoneItems.ATTUNED.isPresent()) {
            registry.setDefaultComparison(SoulStoneItems.ATTUNED.get(),
                    Comparison.compareData(stack -> SoulAcquisitionInfo.subtype(stack.getItemStack())));
            for (var variant : SoulAcquisitionInfo.variants()) registry.addEmiStack(EmiStack.of(variant));
        }
        // With JEI present, JEMI imports the same information pages. Do not duplicate them.
        if (!ModList.get().isLoaded("jei")) for (var page : SoulAcquisitionInfo.pages()) {
            List<EmiIngredient> targets = page.stacks().stream().<EmiIngredient>map(EmiStack::of).toList();
            registry.addRecipe(new EmiInfoRecipe(targets, page.text(),
                    new ResourceLocation("wans_minego_expansion", "info/" + page.id())));
        }
    }
}
