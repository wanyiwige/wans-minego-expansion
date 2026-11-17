"""Add ten material/function stones using the established native pixel renderer."""
import json, zipfile
from PIL import Image, ImageDraw, ImageFont
from create_biome_souls import ROOT, RES, TEXTURES, MOD, write, sha, rgb_list, ZH, EN
from render_scroll_style_stones import render, colors
ART=ROOT/'art/foolish-material-stones-0.6.0'
STONES={
 'sacilite':('萦光魂石','Sacilite Soul Stone',['sacilite_shard','dull_sacilite_shard','azure_sacilite_lens','shining_sacilite_lens'],
 '150d2a 2d1c46 49306a 67478f 8861b2 a681ce c6a6e5 e4cff5 f9eeff','1e1432 291b43','bc93ea eee0ff',
 ['...II...','..OIIO..','.OIIIIO.','OIIIIIIO','.OIIIIO.','..OIIO..','...II...','...OO...']),
 'thunderstone':('雷石魂石','Thunderstone Soul Stone',['thunderstone','electrical_charge','thunderstone','electrical_charge'],
 '13182a 253349 3e526b 56758b 7995a7 99b3c0 bfd6dc deeef0 f7ffff','1c293e 27364b','e5cb63 fff0b2',
 ['O..OO..O','I.OIIO.I','..OIIO..','.OIIIIO.','.OIOIIO.','..OIIO..','I..II..I','O..OO..O']),
 'corrosive':('腐蚀魂石','Corrosive Soul Stone',['radium','toxic_waste','corroded_metal','waste_roots'],
 '212215 3c4023 586130 76833d 97a651 b7c578 d4dda6 ecf2ce fcffe6','2c301b 3a3e24','bbd47a f4fac5',
 ['...OO...','..OIIO..','..OIIO..','.OIIIIO.','OIIIIIIO','OIIII.IO','.OIIIIO.','..OOOO..']),
 'blunt':('钝金属魂石','Blunt Metal Soul Stone',['blunt_metal_ingot','blunt_metal','blunt_metal_ingot','blunt_metal'],
 '181d25 2d3743 47515e 636b75 848a92 a4a9ae c5c9cc e4e7e8 f8fafb','222c38 303a47','aebcc9 e9f2f9',
 ['OOOOOOOO','OIIIIIIO','OIIIIIIO','OIIIIIIO','.OIIIIO.','.OIIIIO.','..OIIO..','...OO...']),
 'infernal':('炽合金魂石','Infernal Alloy Soul Stone',['infernal_alloy_ingot','infernal_alloy_plate_item','scorchslate','minecraft:magma_block'],
 '271314 4b2927 754139 9a5c44 bb805a d5a477 e8c9a2 f7e4c9 fff7e5','39211d 482921','eda866 ffe8b5',
 ['OOOOOOOO','O......O','O..II..O','O.OIIO.O','O.OIIO.O','O..OO..O','OOOOOOOO','.IIIIII.']),
 'keepsteel':('固钢魂石','Keepsteel Soul Stone',['keepsteel_ingot','keepsteel_ingot','keepsteel_ingot','keepsteel_ingot'],
 '181727 302b42 4c455e 6b627b 8e839c b0a6be d1c9dc e9e4f0 fbf8ff','29233b 352e47','c0a6df e9dcfa',
 ['OO.OO.OO','II.II.II','OOOOOOOO','OIIOOIIO','OOOOOOOO','OIIOOIIO','OOOOOOOO','OOOOOOOO']),
 'amber':('琥珀魂石','Warp Amber Soul Stone',['warp_amber','timefruit','chronosand','timewood_planks'],
 '2b1820 4d2c32 74433f 9e6049 c5845b dda876 efcd9f fae5c8 fff8e8','3b242b 4b2b31','d9a8b6 ffdfa4',
 ['...OO...','..OIIO..','.OIIIIO.','OIIOOIIO','OIO..OIO','OIIOOIIO','.OIIIIO.','..OOOO..']),
 'slide':('滑行魂石','Skating Soul Stone',['enderskates_boots','ender_tire','chorus_leather','rotary_core'],
 '17142b 30294a 4b426c 6b5e8e 9080b2 b09dcc d0bfea eaddf7 fbf3ff','211c39 2b2548','c6b0e9 f3e3ff',
 ['..OO....','..II....','..II.OO.','..IIOIIO','..IIIII O'.replace(' ',''),'.OOOOOO.','OI....IO','.OO..OO.']),
 'parasitic':('寄生魂石','Parasitic Soul Stone',['parasitic_stinger','hyper_stinger','burn_stinger','minecraft:string'],
 '20141b 3c2530 5b3b49 805664 a87982 c69c9e e0bebd f2dedd fff2ec','2d1c28 3b2530','d79eb6 ffe2c2',
 ['..OOOO..','.OI..IO.','OI....IO','OI....IO','..OOOO..','...II...','...II...','...OO...']),
 'soulcoat':('魂裳魂石','Soulcoat Soul Stone',['soulsucker_fur','soul_coat_chestplate','minecraft:soul_sand','minecraft:soul_soil'],
 '10222b 203c49 315a67 467d85 65a1a6 8ac2c3 b4dcda d9efea f4fffa','17313e 203f4b','9bdaca e8fff4',
 ['..OOOO..','.OI..IO.','OOI..IOO','OII..IIO','.OI..IO.','.OI..IO.','OIIOOIIO','OOO..OOO']),
}
ZH_TEXT={
 'sacilite':ZH['bloom'], 'corrosive':ZH['waste'], 'amber':ZH['time'],
 'thunderstone':'雷石：每 %s 次有效命中蓄满电荷，释放一次电击。\n伤害为实际命中伤害的 %s%%，上限 %s HP，冷却 %s 秒。',
 'blunt':'钝金属：护甲 +%s，抗击退 +%s%%。',
 'infernal':'炽合金：新施加的燃烧持续时间缩短 %s%%。\n自身燃烧时攻击伤害 +%s%%。\n与灰烬魂石同时装备时，采用灰烬效果，不额外叠加。',
 'keepsteel':'固钢：护甲 +%s，护甲韧性 +%s。\n生命低于 %s%% 时，额外抗击退 +%s%%。',
 'slide':'滑行：持续疾跑 %s 秒逐渐获得最多 %s%% 移速。\n停止疾跑或卸下魂石后重置；不改变飞行能力。',
 'parasitic':'寄生：有效命中后获得 %s 秒生命恢复 I，冷却 %s 秒。',
 'soulcoat':'魂裳：受击后向攻击者释放追踪魂火。\n伤害为实际受击伤害的 %s%%，上限 %s HP。\n冷却 %s 秒，最大反击距离 %s 格。',
}
EN_TEXT={
 'sacilite':EN['bloom'],'corrosive':EN['waste'],'amber':EN['time'],
 'thunderstone':'Thunderstone: every %s valid hits, discharge for %s%%\nof effective hit damage, capped at %s HP; cooldown %s s.',
 'blunt':'Blunt Metal: +%s armor, +%s%% knockback resistance.',
 'infernal':'Infernal Alloy: new burn durations reduced by %s%%.\nWhile burning, +%s%% attack damage.\nAshen Soul Stone takes precedence; these effects do not stack.',
 'keepsteel':'Keepsteel: +%s armor, +%s armor toughness.\nBelow %s%% health, gain +%s%% knockback resistance.',
 'slide':'Skating: sprint for %s s to gradually gain up to %s%% movement speed.\nStopping or unequipping resets it; does not grant flight.',
 'parasitic':'Parasitic: valid hits grant Regeneration I for %s s; cooldown %s s.',
 'soulcoat':'Soulcoat: taking damage launches a seeking soulflame at the attacker.\nDamage is %s%% effective incoming damage, capped at %s HP.\nCooldown %s s; retaliation range %s blocks.',
}
def item_id(key):return f'foolish_{key}_material_soul_stone'
def full_id(value):return value if ':' in value else 'foolish:'+value
def main():
    ART.mkdir(parents=True,exist_ok=True)
    before={p.name:sha(p) for p in TEXTURES.glob('*.png') if not p.stem.endswith('_material_soul_stone')}
    with zipfile.ZipFile(ROOT.parent/'mods/foolish-1.3.0 patched.jar') as z:
        registry=z.read('net/mcreator/foolish/init/FoolishModItems.class')+z.read('net/mcreator/foolish/init/FoolishModBlocks.class')
        for info in STONES.values():
            for material in info[2]:assert ':' in material or material.encode() in registry,material
    sheet=Image.new('RGBA',(1400,1080),(24,26,33,255));draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
    records=[]
    for index,(key,info) in enumerate(STONES.items()):
        zh,en,materials,palette,disk,rune,glyph=info
        assert all(len(row)==8 for row in glyph),(key,glyph)
        sprite=render({'palette':colors(*palette.split()),'disk':rgb_list(disk),'rune':rgb_list(rune),'glyph':glyph})
        assert sprite.getchannel('A').tobytes()==Image.open(TEXTURES/'foolish_pyre_soul_stone.png').getchannel('A').tobytes()
        for folder in [TEXTURES,ART/'native-18px']:
            folder.mkdir(parents=True,exist_ok=True);sprite.save(folder/(item_id(key)+'.png'))
        (ART/'preview-1260px').mkdir(exist_ok=True);sprite.resize((1260,1260),Image.Resampling.NEAREST).save(ART/'preview-1260px'/(item_id(key)+'.png'))
        x,y=index%4*350,index//4*360;sheet.alpha_composite(sprite.resize((288,288),Image.Resampling.NEAREST),(x+31,y+8))
        draw.text((x+175,y+306),f'{index+1:02d} {zh}',font=font,fill=(238,240,246),anchor='mt')
        write(RES/f'assets/{MOD}/models/item/{item_id(key)}.json',{'parent':'minecraft:item/generated','textures':{'layer0':f'{MOD}:item/{item_id(key)}'}})
        write(RES/f'data/{MOD}/recipes/{item_id(key)}.json',{'conditions':[{'type':'forge:mod_loaded','modid':'foolish'}],
            'type':'minecraft:crafting_shaped','pattern':[' A ','BOC',' D '],
            'key':{**{ch:{'item':full_id(mat)} for ch,mat in zip('ABCD',materials)},'O':{'item':'mine_fargo:empty_soul_stone'}},
            'result':{'item':f'{MOD}:{item_id(key)}'}})
        records.append({'id':item_id(key),'name':zh,'materials':[full_id(mat) for mat in materials],'glyph':glyph,'sha256':sha(TEXTURES/(item_id(key)+'.png'))})
    sheet.save(ART/'overview.png')
    for language,texts in [('zh_cn',ZH_TEXT),('en_us',EN_TEXT)]:
        path=RES/f'assets/{MOD}/lang/{language}.json';lang=json.loads(path.read_text(encoding='utf-8'))
        for key,info in STONES.items():
            lang[f'item.{MOD}.{item_id(key)}']=info[0 if language=='zh_cn' else 1]
            lang[f'tooltip.{MOD}.material.{key}']=texts[key]
        lang[f'tooltip.{MOD}.material.rules']='中央为空白魂石；材料版不需要群系浸染。\n材料版不享受群系加成。萦光／雷石／腐蚀／琥珀\n与同主题群系魂石或异境之魂不可重复装备。' if language=='zh_cn' else 'Craft with an Empty Soul Stone; no biome attunement required.\nMaterial stones have no native biome bonus. Sacilite / Thunderstone /\nCorrosive / Amber cannot overlap their biome counterparts or Soul of Otherworld.'
        write(path,lang)
    path=RES/'data/curios/tags/items/soul_stone.json';tag=json.loads(path.read_text())
    for key in STONES:
        value={'id':f'{MOD}:{item_id(key)}','required':False}
        if value not in tag['values']:tag['values'].append(value)
    write(path,tag)
    assert all(sha(TEXTURES/name)==digest for name,digest in before.items())
    write(ART/'manifest.json',{'stones':records,'preserved_hashes':before,'native_grid':[18,18]})
    biome=json.loads((ROOT/'art/foolish-biome-stones-0.6.0/manifest.json').read_text(encoding='utf-8'))['stones']
    all_stones=records+biome
    all_sheet=Image.new('RGBA',(1500,1320),(24,26,33,255));draw=ImageDraw.Draw(all_sheet);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17)
    for i,info in enumerate(all_stones):
        x,y=i%5*300,i//5*330
        all_sheet.alpha_composite(Image.open(TEXTURES/(info['id']+'.png')).resize((252,252),Image.Resampling.NEAREST),(x+24,y+8))
        draw.text((x+150,y+272),f'{i+1:02d} {info["name"]}',font=font,fill=(235,240,245),anchor='mt')
        draw.text((x+150,y+307),'材料／功能' if i<10 else '八群系合成' if i==18 else '群系探索',font=small,fill=(164,178,190),anchor='mt')
    all_sheet.save(ROOT/'art/foolish-all-stones-0.6.0.png')
    print('PASS: 10 material/function stones; 19 new native sprites total; existing 32 sprites unchanged.')
if __name__=='__main__':main()
