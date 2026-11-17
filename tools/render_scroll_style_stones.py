"""Render school stones in the accepted 18x18 scroll-inspired pixel style.

The silhouette and facet lighting come from the user's teal reference image.
Each palette follows that school's spell scroll in the installed add-on JAR.
Central runes are drawn on the same 18x18 grid as the rim and facets.
This script only changes PNG source assets and art previews; it never builds a mod.
"""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw
from soul_stone_lighting import soften_axis, clarify_upper_right, clarify_upper_left

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Image.open(ROOT / "art" / "reference-teal-soul-stone.png").convert("RGBA")
TEXTURES = ROOT / "src/main/resources/assets/wans_minego_expansion/textures/item"
ART = ROOT / "art"
NATIVE = ART / "stones-18px"
LEVELS = (0, 40, 70, 100, 130, 160, 190, 220, 255)


def colors(*hexes: str) -> tuple[tuple[int, int, int], ...]:
    assert len(hexes) == len(LEVELS)
    return tuple(tuple(bytes.fromhex(c.lstrip("#"))) for c in hexes)


STONES = {
    "annihilation": {
        "palette": colors("#031403", "#003000", "#005102", "#007505", "#499b27", "#51a22d", "#53c728", "#79ea5a", "#fffeb9"),
        "disk": ((7, 34, 8), (10, 43, 10)), "rune": ((121, 234, 90), (255, 254, 185)), "full_disk": True,
        "glyph": ("...OO...", "...II...", "..OIIO..", "OOIIIIOO", "OOIIIIOO", "..OIIO..", "...II...", "...OO..."),
    },
    "trailblazer_arcana": {
        "palette": colors("#100e15", "#382d29", "#634527", "#916433", "#bc8a43", "#ddb367", "#f4d892", "#ffeaba", "#fff8e0"),
        "disk": ((39, 30, 34), (49, 36, 39)), "rune": ((250, 215, 124), (255, 246, 191)), "full_disk": True,
        "glyph": ("...II...", "..IIII..", ".OIIIIO.", "O.OIIO.O", "..OIIO..", ".OOOOOO.", ".OI..IO.", "OO....OO"),
    },
    "fusion": {
        "palette": colors("#061625", "#17374d", "#2c5876", "#4482a8", "#67aed0", "#9ed3e8", "#c9eaf6", "#e6f9ff", "#ffffff"),
        "disk": ((16, 45, 69), (21, 56, 82)), "rune": ((71, 176, 221), (217, 248, 255)),
        "glyph": ("O......I", ".O....I.", "..O..I..", "...OI...", "...IO...", "..I..O..", ".I....O.", "I......O"),
    },
    "ars_nouveau": {
        "palette": colors("#120b22", "#2d1552", "#4d2176", "#732d97", "#a038bb", "#c35ad6", "#e189ec", "#f2c5f7", "#fff1ba"),
        "disk": ((29, 12, 54), (43, 18, 69)), "rune": ((244, 185, 51), (255, 240, 123)),
        "glyph": ("...OO...", "..O..O..", ".O.II.O.", "O.IIII.O", "O.IIII.O", ".O.II.O.", "..O..O..", "...OO..."),
    },
    "abyssal": {
        "palette": colors("#0c0920", "#1e143b", "#33255b", "#493477", "#624b9c", "#7d64b9", "#9d86d2", "#bdace8", "#e2d9ff"),
        "disk": ((21, 13, 44), (30, 19, 59)), "rune": ((133, 99, 238), (205, 189, 255)),
        "glyph": ("..OOOO..", ".O....O.", "O......O", "O..II..O", "O..II..O", "O......O", ".O....O.", "..OOOO.."),
    },
    "technomancy": {
        "palette": colors("#0b0e15", "#242a32", "#453131", "#863327", "#c04122", "#e95e24", "#ff9730", "#ffca5f", "#fff5bc"),
        "disk": ((28, 29, 39), (38, 37, 44)), "rune": ((255, 127, 38), (255, 214, 92)),
        "glyph": ("....O..O", "...OI..I", "...OI..I", "...OIIIO", "...OIIO.", "..OIIO..", ".OIIO...", ".OOO...."),
    },
    "esoteric": {
        "palette": colors("#0f1016", "#2b2d34", "#484b50", "#68666a", "#918d87", "#bab4aa", "#d3d0c9", "#e9e7df", "#fff4d0"),
        "disk": ((37, 37, 43), (48, 45, 47)), "rune": ((225, 153, 26), (255, 214, 91)),
        "glyph": ("...OO...", "..O..O..", ".O....O.", "O..II..O", "OOO..OOO", ".O....O.", "..OOOO..", "...OO..."),
    },
    "gluttony": {
        "palette": colors("#1d0a20", "#4c103d", "#861043", "#b91a54", "#e53a58", "#f76641", "#ff9b32", "#ffcc55", "#ffef8b"),
        "disk": ((69, 13, 43), (83, 17, 48)), "rune": ((255, 166, 42), (255, 238, 128)),
        "glyph": ("O.O.O...", "O.O.O...", "OOOOO...", "..O.....", "..O..II.", "..O..II.", "..O..II.", "..O...I."),
    },
    "glintstone": {
        "palette": colors("#061e28", "#153a47", "#205965", "#2f797d", "#42a19a", "#6cbcaf", "#97d6c7", "#c1ebde", "#f0fff8"),
        "disk": ((16, 55, 65), (20, 69, 77)), "rune": ((111, 215, 205), (227, 255, 239)),
        "glyph": ("...OO...", "..OOOO..", ".OOIIOO.", "OOIIIIOO", "OOIIIIOO", ".OOIIOO.", "..OOOO..", "...OO..."),
    },
    "glutton": {
        "palette": colors("#210d0b", "#4d2013", "#7e371d", "#ad4d23", "#d2692a", "#e98736", "#f5ac4b", "#ffd07b", "#fff0b2"),
        "disk": ((61, 27, 21), (75, 33, 23)), "rune": ((246, 165, 66), (255, 220, 129)),
        "glyph": ("O.O..O.O", "OOOOOOOO", ".O....O.", "..O..O..", "..O..O..", ".O....O.", ".OOOOOO.", "........"),
    },
}


def gradient(palette: tuple[tuple[int, int, int], ...], value: int) -> tuple[int, int, int]:
    for i in range(len(LEVELS) - 1):
        low, high = LEVELS[i : i + 2]
        if value <= high:
            t = max(0.0, min(1.0, (value - low) / (high - low)))
            return tuple(round(a * (1 - t) + b * t) for a, b in zip(palette[i], palette[i + 1]))
    return palette[-1]


def render(info: dict) -> Image.Image:
    sprite = Image.new("RGBA", (18, 18))
    for y in range(18):
        for x in range(18):
            r, g, b, a = SOURCE.getpixel((round((x + 0.5) * SOURCE.width / 18), round((y + 0.5) * SOURCE.height / 18)))
            if a < 128:
                continue
            value = round(0.2126 * r + 0.7152 * g + 0.0722 * b)
            sprite.putpixel((x, y), (*gradient(info["palette"], value), 255))
    for y in range(5, 13):
        for x in range(5, 13):
            if not info.get("full_disk") and x in (5, 12) and y in (5, 12):
                continue
            sprite.putpixel((x, y), (*info["disk"][(x + y) % 3 == 0], 255))
    for gy, row in enumerate(info["glyph"]):
        assert len(row) == 8, row
        for gx, mark in enumerate(row):
            if mark == "O":
                sprite.putpixel((gx + 5, gy + 5), (*info["rune"][0], 255))
            elif mark == "I":
                sprite.putpixel((gx + 5, gy + 5), (*info["rune"][1], 255))
    assert len(info["glyph"]) == 8
    return clarify_upper_left(clarify_upper_right(soften_axis(sprite)))


def main() -> None:
    NATIVE.mkdir(parents=True, exist_ok=True)
    TEXTURES.mkdir(parents=True, exist_ok=True)
    preview = Image.new("RGBA", (5 * 270, 2 * 294), (26, 26, 31, 255))
    draw = ImageDraw.Draw(preview)
    for index, (name, info) in enumerate(STONES.items()):
        sprite = render(info)
        sprite.save(NATIVE / f"{name}_soul_stone.png")
        large = sprite.resize((1260, 1260), Image.Resampling.NEAREST)
        sprite.save(TEXTURES / f"{name}_soul_stone.png")
        tile = sprite.resize((252, 252), Image.Resampling.NEAREST)
        x, y = (index % 5) * 270 + 9, (index // 5) * 294 + 8
        preview.alpha_composite(tile, (x, y))
        draw.text((x + 4, y + 258), name, fill=(245, 245, 245, 255))
    preview.save(ART / "new-school-stones-preview-v2.png")


if __name__ == "__main__":
    main()
