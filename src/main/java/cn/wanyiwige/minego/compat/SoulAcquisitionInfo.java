package cn.wanyiwige.minego.compat;

import cn.wanyiwige.minego.*;
import java.util.*;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;

/** Display data shared by the optional viewers; does not create gameplay recipes. */
public final class SoulAcquisitionInfo {
    public record Page(String id, List<ItemStack> stacks, List<Component> text) {}
    public static String subtype(ItemStack stack) {
        return stack.hasTag() ? stack.getTag().getString(AttunedSoulStoneItem.TAG) : "";
    }
    public static List<ItemStack> variants() {
        if (SoulStoneItems.ATTUNED == null || !SoulStoneItems.ATTUNED.isPresent()) return List.of();
        return Arrays.stream(BiomeSoulStoneItem.Kind.values())
                .filter(k -> k != BiomeSoulStoneItem.Kind.OTHERWORLD).map(AttunedSoulStoneItem::attuned).toList();
    }
    private static Component biome(String namespace, String path) {
        return Component.translatable("biome." + namespace + "." + path);
    }
    public static List<Page> pages() {
        List<Page> result = new ArrayList<>();
        for (var variant : variants()) {
            var kind = BiomeSoulStoneItem.Kind.fromKey(subtype(variant));
            var regions = kind.biomePaths().stream().sorted().map(p -> biome("foolish", p)).toList();
            List<Component> text = new ArrayList<>();
            text.add(Component.translatable("info.wans_minego_expansion.attune"));
            text.add(Component.translatable("info.wans_minego_expansion.regions"));
            text.addAll(regions);
            text.add(Component.translatable("info.wans_minego_expansion.attune_result"));
            result.add(new Page("attune/" + kind.key(), List.of(variant,
                    new ItemStack(SoulStoneItems.BIOME.get(kind).get())), text));
        }
        for (var entry : SoulStoneItems.EPOCH_PROOFS.entrySet()) {
            List<Component> text = new ArrayList<>();
            String route = entry.getKey();
            if (route.equals("cauldron") || route.equals("tiger") || route.equals("rusted")) {
                text.add(Component.translatable("info.wans_minego_expansion.proof_kills", EpochSoulConfig.count("progress.kills")));
                var entities = switch (route) {
                    case "cauldron" -> List.of("cauldronbeast");
                    case "tiger" -> List.of("firearmtigerguard");
                    default -> List.of("rustedancestors", "rustrelics", "rusthound");
                };
                for (String entity : entities) text.add(Component.translatable("entity.splendour_ablaze_epoch." + entity));
                text.add(Component.translatable("info.wans_minego_expansion.proof_credit"));
            } else {
                text.add(Component.translatable("info.wans_minego_expansion.proof_" + route,
                        EpochSoulConfig.ticks("progress.visit_seconds") / 20.0));
                for (String region : EpochSoulEvents.progressBiomes()) text.add(biome("splendour_ablaze_epoch", region));
                text.add(Component.translatable("info.wans_minego_expansion.proof_cycle"));
            }
            text.add(Component.translatable("info.wans_minego_expansion.config"));
            result.add(new Page("proof/" + route, List.of(new ItemStack(entry.getValue().get())), text));
        }
        return result;
    }
    private SoulAcquisitionInfo() {}
}
