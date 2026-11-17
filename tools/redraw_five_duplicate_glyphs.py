"""Export five edited native glyph definitions; preserve every outer pixel."""
from pathlib import Path
import hashlib
import json
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont
from render_scroll_style_stones import ROOT, TEXTURES, STONES, render, colors
from create_material_souls import STONES as MATERIAL, rgb_list
from render_epoch_stones import STONES as EPOCH
from render_foolish_boss_stones import STONES as BOSS
from create_biome_souls import STONES as BIOME, item_id as biome_id
from unify_soul_stone_grid import LEGACY

OUT = ROOT / 'art/five-glyph-redraw-20261012'
BACKUP = ROOT / 'backups/20261012-123207-before-five-glyph-redraw'
ASSETS = ROOT / 'src/main/resources/assets/wans_minego_expansion'
TARGETS = [
    ('foolish_soulcoat_material_soul_stone', '魂裳魂石', '魂衣披风', 'epoch_ghost_jade_soul_stone'),
    ('foolish_thunderstone_material_soul_stone', '雷石魂石', '带电晶石', 'foolish_thunderbird_soul_stone'),
    ('technomancy_soul_stone', '械术学派魂石', '开口扳手', 'relicron_soul_stone'),
    ('epoch_explorer_soul_stone', '顶世界探索魂石', '菱框指南针', 'annihilation_soul_stone'),
    ('trailblazer_arcana_soul_stone', '开拓奥秘学派魂石', '轨道箭头', 'glintstone_soul_stone'),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect_glyphs():
    glyphs = {k + '_soul_stone': tuple(v['glyph']) for k, v in STONES.items()}
    glyphs.update({k + '_soul_stone': tuple(v[0]) for k, v in LEGACY.items()})
    glyphs.update({'foolish_' + k + '_soul_stone': tuple(v['glyph']) for k, v in BOSS.items()})
    glyphs.update({'epoch_' + k + '_soul_stone': tuple(v['glyph']) for k, v in EPOCH.items()})
    glyphs.update({biome_id(k): tuple(v[-1]) for k, v in BIOME.items()})
    glyphs.update({'foolish_' + k + '_material_soul_stone': tuple(v[-1]) for k, v in MATERIAL.items()})
    manifest = json.loads((ROOT / 'art/foolish-boss-stones-v1/manifest.json').read_text(encoding='utf-8'))
    glyphs.update({Path(v['file']).stem: tuple(v['glyph']) for v in manifest['composites']})
    return glyphs


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    inventory = json.loads((ROOT / 'audit/20261012-texture-duplicates/inventory.json').read_text(encoding='utf-8'))
    initial = {r['file']: r['sha256'] for r in inventory['items']}
    info = {k + '_soul_stone': v for k, v in STONES.items()}
    info.update({'epoch_' + k + '_soul_stone': v for k, v in EPOCH.items()})
    for k in ('soulcoat', 'thunderstone'):
        v = MATERIAL[k]
        info['foolish_' + k + '_material_soul_stone'] = {
            'palette': colors(*v[3].split()), 'disk': rgb_list(v[4]),
            'rune': rgb_list(v[5]), 'glyph': v[-1]}
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 20)
    small = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 16)
    sheet = Image.new('RGBA', (1050, 1500), (24, 26, 33, 255))
    d = ImageDraw.Draw(sheet)
    records = []
    for i, (stem, name, theme, partner) in enumerate(TARGETS):
        path = TEXTURES / (stem + '.png')
        old = Image.open(BACKUP / path.name).convert('RGBA')
        new = render(info[stem])
        assert new.size == old.size == (18, 18)
        assert new.getchannel('A').tobytes() == old.getchannel('A').tobytes()
        assert set(new.getchannel('A').tobytes()) == {0, 255}
        changed = []
        for y in range(18):
            for x in range(18):
                if new.getpixel((x, y)) != old.getpixel((x, y)):
                    assert 5 <= x < 13 and 5 <= y < 13, (stem, x, y)
                    changed.append([x, y])
        assert changed
        new.save(path)
        (OUT / 'native-18px').mkdir(exist_ok=True)
        (OUT / 'preview-1260px').mkdir(exist_ok=True)
        new.save(OUT / 'native-18px' / path.name)
        preview = new.resize((1260, 1260), Image.Resampling.NEAREST)
        # The center and rim each expand one native pixel into the same 70x70 block.
        for y in range(18):
            for x in range(18):
                assert preview.crop((x*70, y*70, (x+1)*70, (y+1)*70)).getcolors(2) == [(4900, new.getpixel((x, y)))]
        preview.save(OUT / 'preview-1260px' / path.name)
        y = i * 300
        d.text((22, y + 12), f'{i+1:02d} {name} · {theme}', font=font, fill='white')
        for col, (im, label) in enumerate(((Image.open(TEXTURES / (partner + '.png')).convert('RGBA'), '同组保留'), (old, '重绘前'), (new, '重绘后'))):
            x = col * 350 + 67
            sheet.alpha_composite(im.resize((216, 216), Image.Resampling.NEAREST), (x, y + 44))
            d.text((col * 350 + 175, y + 272), label, font=small, fill='white', anchor='mt')
        records.append({'id': stem, 'name': name, 'theme': theme, 'partner': partner,
                        'glyph': list(info[stem]['glyph']), 'before_sha256': sha(BACKUP / path.name),
                        'after_sha256': sha(path), 'changed_center_pixels': changed,
                        'outer_pixels_unchanged': True, 'alpha_unchanged': True,
                        'native_size': [18, 18], 'preview_pixel_block': [70, 70]})
    targets = {'textures/item/' + r['id'] + '.png' for r in records}
    changed_files = {rel for rel, h in initial.items() if sha(ASSETS / rel) != h}
    assert changed_files == targets, changed_files
    glyphs = collect_glyphs()
    assert len(glyphs) == 73
    by_pattern, by_shape = defaultdict(list), defaultdict(list)
    for stem, pattern in glyphs.items():
        by_pattern[pattern].append(stem)
        shape = tuple(''.join('.' if c == '.' else '#' for c in row) for row in pattern)
        by_shape[shape].append(stem)
    duplicate_patterns = [v for v in by_pattern.values() if len(v) > 1]
    duplicate_shapes = [v for v in by_shape.values() if len(v) > 1]
    assert not duplicate_patterns, duplicate_patterns
    assert not duplicate_shapes, duplicate_shapes
    sheet.save(OUT / 'before-after.png')
    (OUT / 'manifest.json').write_text(json.dumps({'backup': str(BACKUP), 'items': records,
        'textures_changed': 5, 'other_textures_unchanged': len(initial)-5,
        'stone_glyphs_checked': 73, 'duplicate_patterns': duplicate_patterns,
        'duplicate_shapes': duplicate_shapes, 'built': False, 'deployed': False}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    rows = ['# 五组魂石符号重绘', '', '只更新每组的一张魂石；原生 18×18，中央 8×8，内外像素使用同一网格。', '', '| 重绘魂石 | 新符号 | 同组保留 |', '| --- | --- | --- |']
    lang = json.loads((ASSETS / 'lang/zh_cn.json').read_text(encoding='utf-8'))
    for r in records:
        rows.append(f"| {r['name']} | {r['theme']} | {lang['item.wans_minego_expansion.' + r['partner']]} |")
    rows += ['', '校验：仅 5 张贴图改变，其他 84 张贴图不变；5 张外框、切面、配色及透明轮廓逐像素保持不变。', '73 张魂石的符号定义重新比较后，没有完全重复的符号或完全相同的符号占位轮廓。', '预览统一最近邻放大，每个源像素严格占 70×70 像素，中央与外框一致。', '', '已修改可编辑的图案定义与源码 PNG；尚未构建或部署，游戏安装的 JAR 保持原样。', '概念稿通过内置 imagegen 制作，正式贴图通过项目既有原生绘制器导出。', '', '设计提示词摘要：魂衣披风、带电晶石、开口扳手、菱框指南针、轨道箭头；简化双颜色像素符号，避免原来的脸形、闪电、齿环、实心十字与实心菱形。']
    (OUT / 'report.md').write_text('\n'.join(rows)+'\n', encoding='utf-8')
    print('PASS: 5 center-only redraws; 84 other textures unchanged; 73 distinct patterns and silhouettes; native 18px grid verified.')
    print(OUT / 'before-after.png')


if __name__ == '__main__':
    main()
