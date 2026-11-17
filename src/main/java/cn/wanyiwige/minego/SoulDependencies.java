package cn.wanyiwige.minego;

import java.util.Arrays;
import java.util.function.Predicate;
import net.minecraftforge.fml.ModList;

/** Registration and recipe generation use the same requirements. */
public final class SoulDependencies {
    public static boolean loaded(String... mods) {
        return satisfied(ModList.get()::isLoaded, mods);
    }

    public static boolean satisfied(Predicate<String> loaded, String... mods) {
        return Arrays.stream(mods).allMatch(loaded);
    }

    public static boolean atLeast(String mod, String minimumVersion) {
        return ModList.get().getModContainerById(mod)
                .map(container -> container.getModInfo().getVersion().compareTo(
                        new org.apache.maven.artifact.versioning.DefaultArtifactVersion(minimumVersion)) >= 0)
                .orElse(false);
    }

    private SoulDependencies() {}
}
