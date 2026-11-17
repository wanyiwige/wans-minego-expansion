package cn.wanyiwige.minego;

import java.util.List;
import net.minecraft.network.chat.Component;

/** Expand explicit localized line breaks after translation and placeholder substitution. */
public final class SoulTooltip {
    public static void add(List<Component> tooltip, Component formatted) {
        for (String line : formatted.getString().split("\\R")) {
            if (!line.isBlank()) tooltip.add(Component.literal(line).withStyle(formatted.getStyle()));
        }
    }
    private SoulTooltip() {}
}
