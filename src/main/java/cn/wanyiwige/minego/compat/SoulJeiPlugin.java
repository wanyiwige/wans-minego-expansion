package cn.wanyiwige.minego.compat;

import cn.wanyiwige.minego.SoulStoneItems;
import mezz.jei.api.*;
import mezz.jei.api.ingredients.subtypes.IIngredientSubtypeInterpreter;
import mezz.jei.api.registration.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;

@JeiPlugin
public final class SoulJeiPlugin implements IModPlugin {
    @Override public ResourceLocation getPluginUid() {
        return new ResourceLocation("wans_minego_expansion", "soul_acquisition");
    }
    @Override public void registerItemSubtypes(ISubtypeRegistration registration) {
        if (SoulStoneItems.ATTUNED != null && SoulStoneItems.ATTUNED.isPresent())
            registration.registerSubtypeInterpreter(SoulStoneItems.ATTUNED.get(),
                    (IIngredientSubtypeInterpreter<ItemStack>) (stack, context) -> SoulAcquisitionInfo.subtype(stack));
    }
    @Override public void registerExtraIngredients(IExtraIngredientRegistration registration) {
        registration.addExtraItemStacks(SoulAcquisitionInfo.variants());
    }
    @Override public void registerRecipes(IRecipeRegistration registration) {
        for (var page : SoulAcquisitionInfo.pages()) registration.addItemStackInfo(page.stacks(),
                page.text().toArray(net.minecraft.network.chat.Component[]::new));
    }
}
