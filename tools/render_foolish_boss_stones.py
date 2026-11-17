"""Extend the accepted soul-stone renderer with ten strictly 18x18 boss sprites.

New PNGs only; no registration, recipe, build or deployment changes.
All facets and glyphs are painted on the same grid before nearest-neighbor export.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont, ImageChops
from render_scroll_style_stones import render, colors, ROOT, TEXTURES

ART = ROOT / "art/foolish-boss-stones-v1"
NATIVE = ART / "native-18px"
LARGE = ART / "preview-1260px"


def rgb(value):
    return tuple(bytes.fromhex(value.removeprefix("#")))


def stone(name, theme, palette, disk, rune, glyph):
    assert len(glyph) == 8 and all(len(row) == 8 for row in glyph)
    assert set("".join(glyph)) <= set(".OI")
    return dict(name=name, theme=theme, palette=colors(*palette.split()),
                disk=tuple(map(rgb, disk.split())), rune=tuple(map(rgb, rune.split())),
                glyph=tuple(glyph))


STONES = {
    "pyre": stone("焚堆", "白炽火焰",
        "180e14 382329 623028 963b26 c34f23 e9742f ffa749 ffda86 fff5c5",
        "2d1720 371c23", "f67c23 fff0ac",
        ["....O...", "...OO...", ".O.OOO..", ".OOOOO..", "OOOIIOO.", "OOIIIIO.", ".OIIIO..", "..OOO..."]),
    "timewelder": stone("时铸者", "时之沙漏",
        "0d122b 1e2850 2e447b 405d9c 587fbe 799fd5 a6c5e9 d4e7f7 f3faff",
        "141e3b 1b2749", "86b7ee e1f9ff",
        ["OOOOOOOO", ".OIIIIO.", "..OIIO..", "...OO...", "...OO...", "..OIIO..", ".OIIIIO.", "OOOOOOOO"]),
    "thrasher": stone("鞭打者", "泥潭怒潮",
        "0c201f 1a3c37 285950 397b68 53a58a 79c5a6 a3dfbe d4f2dd f1fff1",
        "102d2d 173838", "62c4bb d9fff0",
        ["....OOO.", "...OIIOO", "..OI...O", ".OI.....", "OOI..OO.", "OII.OIIO", ".OOOOOO.", "..OOOO.."]),
    "sacilic_abomination": stone("紫晶突变体", "三叉紫晶",
        "180e2c 33214e 513273 704895 9561bc b681d9 d3a8ee ebd2ff fbf0ff",
        "211238 2b1947", "9b68e7 edd8ff",
        ["...II...", "..OIIO..", "O.OIIO.O", "IOOIIOOI", "IOOIIOOI", "IOOIIOOI", ".OOOOOO.", "..OOOO.."]),
    "varmint_king": stone("害兽王", "腐蚀兽颅",
        "162016 2b3820 46532a 627132 849b3c aec94f d2e579 ebf6b3 f9ffda",
        "20291c 2a3520", "b8d553 f0ffb7",
        ["O......O", "OOOOOOOO", ".OIIIIO.", "OO.OO.OO", "OO.OO.OO", ".OO..OO.", "..OII.O.", "..OOOO.."]),
    "thunderbird": stone("雷鸟", "雷霆电闪",
        "0b172c 1c3251 2c5175 377b9d 4fa5c3 75cbdc a4e8ed d6faf6 f5ffff",
        "14273c 1b3449", "f5c552 fff7c3",
        ["....OOO.", "...OII..", "..OII...", ".OII....", "OOOOOOO.", "...IIO..", "..IIO...", ".OO....."]),
    "scarlant_queen": stone("猩红女王", "猩红王冠",
        "260e1c 49152a 73213b 9b2c4e c53e65 e86283 f48fab fbc4d3 fff0e6",
        "391224 46172d", "eab652 fff0ba",
        ["O..II..O", "OO.II.OO", "OIOIIOIO", "OIIIIIIO", "OIIIIIIO", "OOOOOOOO", ".IIIIII.", ".OOOOOO."]),
    "terrorflora": stone("怖蕈", "花印与孢子",
        "201224 41213f 63355b 854c70 a86888 c48aa5 dfaec5 f3d4e4 fff3fa",
        "291b33 33213d", "d976ad fce2ae",
        ["..OOOO..", ".O.II.O.", "O.OIIO.O", "OII..IIO", "OII..IIO", "O.OIIO.O", ".O.II.O.", "..OOOO.."]),
    "wendigrudge": stone("怀恨巨灵", "角颅怨灵",
        "142021 293b3a 405753 5b7469 7c9785 a6ba9f cbd8bd e6eed9 f9fff0",
        "15272b 1c3235", "a9dbca edffe7",
        ["O......O", "OO....OO", ".OOOOOO.", ".OI..IO.", ".OI..IO.", "..OOOO..", "..O..O..", "...OO..."]),
    "astralis": stone("阿斯塔瑞斯·堕落之星", "粉金星刃",
        "201323 492638 764343 a57553 d8a76e eeca94 f2debb fbeed7 fffff0",
        "301c38 3b2345", "ec9aca fff1a1",
        ["...II...", "...II...", ".OOIIOO.", "OOIIIIOO", ".OOIIOO.", "...II...", "..OII.O.", "...OO..."]),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    for folder in (ART, NATIVE, LARGE, TEXTURES):
        folder.mkdir(parents=True, exist_ok=True)
    existing = {p: digest(p) for p in TEXTURES.glob("*.png")
                if not p.name.startswith("foolish_")}
    font_path = Path("C:/Windows/Fonts/msyh.ttc")
    font = ImageFont.truetype(str(font_path), 19) if font_path.exists() else ImageFont.load_default()
    small_font = ImageFont.truetype(str(font_path), 14) if font_path.exists() else ImageFont.load_default()
    preview = Image.new("RGBA", (1500, 680), (24, 26, 33, 255))
    draw = ImageDraw.Draw(preview)
    manifests = []
    expected_alpha = None
    for i, (boss, info) in enumerate(STONES.items()):
        filename = f"foolish_{boss}_soul_stone.png"
        sprite = render(info)
        assert sprite.size == (18, 18) and sprite.mode == "RGBA"
        alpha_values = set(sprite.getchannel("A").tobytes())
        assert alpha_values == {0, 255}, alpha_values
        if expected_alpha is None:
            expected_alpha = sprite.getchannel("A")
        else:
            assert ImageChops.difference(expected_alpha, sprite.getchannel("A")).getbbox() is None
        native_path = NATIVE / filename
        texture_path = TEXTURES / filename
        sprite.save(native_path)
        sprite.save(texture_path)
        large = sprite.resize((1260, 1260), Image.Resampling.NEAREST)
        large.save(LARGE / filename)
        # Each 70x70 preview block is exactly one native pixel, including center runes.
        for y in range(18):
            for x in range(18):
                block = large.crop((x*70, y*70, (x+1)*70, (y+1)*70))
                assert block.getcolors(2) == [(4900, sprite.getpixel((x, y)))]
        px, py = (i % 5) * 300, (i // 5) * 340
        tile = sprite.resize((252, 252), Image.Resampling.NEAREST)
        preview.alpha_composite(tile, (px+24, py+12))
        label = f"{i+1:02d}  {info['name']}"
        draw.text((px+150, py+275), label, font=font, fill=(235, 238, 245), anchor="mt")
        draw.text((px+150, py+309), info['theme'], font=small_font, fill=(151, 165, 183), anchor="mt")
        manifests.append(dict(boss=boss, name=info['name'], theme=info['theme'],
            file=filename, native_size=[18,18], preview_size=[1260,1260],
            alpha="binary 0/255", sha256=digest(native_path),
            glyph=info['glyph'], palette=info['palette']))
    assert len(manifests) == 10
    assert all(digest(p) == value for p, value in existing.items()), "Existing school texture changed"
    preview.save(ART / "foolish-boss-stones-preview.png")
    (ART / "manifest.json").write_text(json.dumps(dict(
        renderer="render_foolish_boss_stones.py; accepted 18x18 family renderer",
        stones=manifests, preserved_school_textures=len(existing)), ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (ART / "README.md").write_text(
        "# Foolish BOSS魂石贴图\n\n"
        "共10张，采用已有魂石的宝石轮廓、左上高光和8×8中心符纹。\n"
        "原生贴图统一18×18 RGBA，透明度仅0/255。外圈、符纹、高光均共用同一像素网格。\n\n"
        "- native-18px：原生PNG，与源码textures/item内同名文件一致。\n"
        "- preview-1260px：70倍最近邻放大，便于检查；不是额外细节。\n"
        "- foolish-boss-stones-preview.png：带中文名称的十张总览。\n"
        "- manifest.json：对应Boss、配色、符纹及哈希。\n\n"
        "仅新增贴图，未注册新物品、修改旧学派贴图、构建或部署JAR。\n"
        "绘制方式：复用现有Python像素绘制脚本；前次AI生成图不作为最终资产。\n",
        encoding="utf-8")
    print(f"Saved 10 RGBA textures; shared 18x18 grid and silhouette verified; {len(existing)} existing textures unchanged.")
    print(ART / "foolish-boss-stones-preview.png")


if __name__ == "__main__":
    main()
