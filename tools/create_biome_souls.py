"""Extend the accepted native soul-stone renderer; preserve all 32 existing icons.

This is the project-native pixel art pipeline, not image resizing or replacement.
The accepted renderer applies the axis and both upper-rim lighting corrections.
"""
from pathlib import Path
import hashlib, json, re, zipfile
from PIL import Image, ImageDraw, ImageFont
from render_scroll_style_stones import render, colors, ROOT, TEXTURES

MOD = 'wans_minego_expansion'
ART = ROOT / 'art/foolish-biome-stones-0.6.0'
RES = ROOT / 'src/main/resources'
STONES = {
 'bloom': ('绽晶魂石', 'Bloom Soul Stone', ['sacilite_bloom','sacilite_cavern'],
    ['sacilite_shard','dull_sacilite_shard','azure_sacilite_lens','rose_sacilite_lens'],
    '190e32 342049 51316b 734994 9864b9 b489d0 d5ace7 ebd5f6 fbf2ff',
    '26173b 301c49', 'c395eb f5e6ff',
    ['...II...','..OIIO..','.O.OO.O.','OOO..OOO','.OIIIIO.','..OIIO..','...OO...','...OO...']),
 'storm': ('风暴魂石', 'Storm Soul Stone', ['storm_jungle'],
    ['thunderstone','electrical_charge','storm_apple','thunderstone'],
    '101c24 203e42 31595b 427677 579391 73b2a8 9ed1c1 c8e8d9 eefaf0',
    '182e36 213c40', '9dcbd0 ffe9a5',
    ['..OOOO..','.OIIOIO.','OIIIIIIO','OOOOOOOO','...II...','..II....','...II...','..II....']),
 'time': ('时沙魂石', 'Timesand Soul Stone', ['sands_of_time'],
    ['chronosand','warp_amber','timefruit','timewood_log'],
    '211727 403040 65504e 8b705d ae9075 c9af94 e0cbb3 f0e4d2 fff7e8',
    '302337 3d2d41', 'b98ccf fce7a8',
    ['..OOOO..','.O.II.O.','O..II..O','O..I...O','O..III.O','O......O','.O....O.','..OOOO..']),
 'scarlet': ('猩野魂石', 'Scarlet Fields Soul Stone', ['scarlet_fields'],
    ['scarlet_silt','egg_membrane','scarlet_glow_fungus','scarlant_capsule'],
    '260d1a 49152b 6c2439 94394f b65168 cf758a e6a0b2 f5cbd4 fff0ec',
    '381827 431c30', 'ebacbd fff0c8',
    ['...OO...','..OOOO..','.OI..IO.','OIIOOIIO','OII..IIO','.OI..IO.','..OOOO..','...OO...']),
 'waste': ('废土魂石', 'Wasteland Soul Stone', ['wasteland','irradiated_undergrowth'],
    ['radium','toxic_waste','corroded_metal','waste_soil'],
    '202016 373820 52542a 707137 8c924b aeb66c cdd49c e7edc4 f7fadd',
    '29291b 343320', 'b7ce6f eff6bb',
    ['O......O','OO....OO','OIO..OIO','.OOOOOO.','..OIIO..','.OOOOOO.','OIO..OIO','OO....OO']),
 'mire': ('泥沼魂石', 'Mire Soul Stone', ['miserable_mire'],
    ['bunyip_fur','large_lily_pad','darkenstone','murken_berry'],
    '111e22 223938 34524b 4b7060 669078 89af93 b1ceae d5e7d0 f1f7e8',
    '1b3031 243e3b', '90bea7 dcf7e6',
    ['........','..OOOO..','.OIIOOO.','OIIIOOOO','OIIIO..O','.OOOOOO.','...II...','...OO...']),
 'growth': ('繁生魂石', 'Overgrowth Soul Stone', ['overgrowth'],
    ['soft_leaf','sharp_leaf','pollen_burst','stem_planks'],
    '142018 293c28 40583a 5b794d 7d9c63 a3bd83 c8dba9 e7efd0 f9fce8',
    '1d3021 263c28', 'a9d476 fce8b2',
    ['.....OOO','....OIIO','...OIIO.','..OIIO..','.OOIO...','OIOOO...','OO.OOO..','...OO...']),
 'ash': ('灰烬魂石', 'Ashen Soul Stone', ['ashen_woods','volcanic_valley','emberlight_valley'],
    ['ashen_log','scorchslate','ashflower','volcanic_hollowstone_rod'],
    '211b1d 3c3032 5c4542 80594b a57759 c49d75 dfc29f f1e4cd fff7e6',
    '302427 3c2c2c', 'cb9260 ffe5ae',
    ['...OO...','..OIIO..','.OIIO...','.OIO..O.','..OO.OIO','.....OO.','OOOOOOOO','.IIIIII.']),
 'otherworld': ('异境之魂', 'Soul of Otherworld', [], [],
    '16152b 30304c 4c496b 696789 908bab b1aac9 d1cce3 eae6f5 fcf8ff',
    '24223a 302b49', 'b7c6dc f9e7b7',
    ['...II...','..O..O..','.O....O.','I..OO..I','I..OO..I','.O....O.','..O..O..','...II...']),
}
def item_id(key): return 'soul_of_otherworld' if key == 'otherworld' else f'foolish_{key}_biome_soul_stone'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
def rgb_list(value): return tuple(tuple(bytes.fromhex(c)) for c in value.split())

ZH = {
 'bloom': '绽晶：挖掘速度 +%s%%。\n攻击每 %s 秒释放一枚追踪晶体，\n伤害为实际命中伤害的 %s%%，上限 %s HP。',
 'storm': '风暴：疾跑 %s 秒蓄满电荷，水中或雨中蓄电速度 ×1.5。\n下一次攻击释放电击，伤害为实际命中伤害的 %s%%，\n上限 %s HP；电击冷却 %s 秒。',
 'time': '时沙：移动速度 +%s%%，挖掘速度 +%s%%。\n受击后获得速度 I，持续 %s 秒，冷却 %s 秒。',
 'scarlet': '猩野：攻击有 %s%% 概率召唤一只魂蚁，冷却 %s 秒。\n与女王魂蚁共用附近数量上限 %s；存续 %s 秒。\n魂蚁生命 %s HP、攻击力 %s；不掉落物品或经验。',
 'waste': '废土：新施加的 Foolish 腐蚀持续时间缩短 %s%%。\n攻击有 %s%% 概率施加 %s 秒 Foolish 腐蚀，冷却 %s 秒。',
 'mire': '泥沼：游泳速度 +%s%%。\n水中或雨中每 %s 秒恢复 %s HP。',
 'growth': '繁生：战斗中每 %s 秒向周围 %s 格释放花粉。\n最多减速 %s 个敌人 %s 秒，并恢复 %s HP。',
 'ash': '灰烬：新施加的燃烧持续时间缩短 %s%%。\n自身燃烧时攻击伤害 +%s%%；每 %s 秒对 %s 格内\n最多 %s 个敌人造成 %s HP 余烬伤害。',
}
EN = {
 'bloom': 'Bloom: +%s%% mining speed.\nEvery %s s, a hit launches a seeking crystal for %s%%\nof effective hit damage, capped at %s HP.',
 'storm': 'Storm: sprint for %s s to charge; water/rain charges ×1.5 faster.\nThe next hit discharges for %s%% effective hit damage,\ncapped at %s HP; discharge cooldown %s s.',
 'time': 'Timesand: +%s%% movement and +%s%% mining speed.\nTaking damage grants Speed I for %s s; cooldown %s s.',
 'scarlet': 'Scarlet: %s%% chance to summon a soul ant on hit; cooldown %s s.\nNearby ants share a cap of %s with queen ants; lifetime %s s.\nAnt health %s HP, attack %s; no loot or XP.',
 'waste': 'Waste: new Foolish Corrosion durations are reduced by %s%%.\nHits have a %s%% chance to apply %s s of Foolish Corrosion; cooldown %s s.',
 'mire': 'Mire: +%s%% swimming speed.\nRestore %s HP every %s s in water/rain.',
 'growth': 'Growth: in combat, release pollen every %s s within %s blocks.\nSlow up to %s enemies for %s s and restore %s HP.',
 'ash': 'Ash: new burn durations reduced by %s%%.\nWhile burning, +%s%% attack damage; every %s s, embers hit\nup to %s enemies within %s blocks for %s HP each.',
}
# Placeholder order must match the Java stats list in both languages.
EN['mire'] = 'Mire: +%s%% swimming speed.\nEvery %s s, restore %s HP in water/rain.'
EN['ash'] = 'Ash: new burn durations reduced by %s%%.\nWhile burning, +%s%% attack damage; every %s s, embers hit\nenemies within %s blocks, up to %s targets, for %s HP each.'
REGIONS_ZH = {'bloom':'绽晶之地／紫晶峡谷','storm':'风暴丛林','time':'时间之沙','scarlet':'猩红田野',
 'waste':'荒原／辐照下层植被','mire':'悲惨沼泽','growth':'过度生长','ash':'灰烬森林／火山谷／余烬光谷'}
BONUS_ZH = {'bloom':'挖掘增益、晶体伤害','storm':'蓄电速度、电击伤害','time':'挖掘增益、受击加速持续时间',
 'scarlet':'召唤概率','waste':'腐蚀缩时比例、附加腐蚀概率','mire':'单次回复量','growth':'减速持续时间、回复量','ash':'燃烧缩时比例、燃烧增伤、余烬伤害'}
BONUS_EN = {'bloom':'mining bonus and crystal damage','storm':'charge rate and discharge damage',
 'time':'mining bonus and escape duration','scarlet':'summon chance','waste':'corrosion reduction and proc chance',
 'mire':'healing amount','growth':'slow duration and healing','ash':'burn reduction, burning bonus and ember damage'}

def main():
    ART.mkdir(parents=True,exist_ok=True)
    before = {p.name:sha(p) for p in TEXTURES.glob('*.png') if p.stem not in {item_id(k) for k in STONES} and not p.stem.endswith('_material_soul_stone')}
    assert len(before) == 32, f'Expected the accepted 32 legacy icons, got {len(before)}'
    foolish = ROOT.parent / 'mods/foolish-1.3.0 patched.jar'
    with zipfile.ZipFile(foolish) as jar:
        # Exact registered IDs, not translations or guesses.
        registry = jar.read('net/mcreator/foolish/init/FoolishModItems.class')
        block_registry = jar.read('net/mcreator/foolish/init/FoolishModBlocks.class')
        for key, info in STONES.items():
            for material in info[3]:
                assert material.encode() in registry or material.encode() in block_registry, material
            for biome in info[2]: assert f'data/foolish/worldgen/biome/{biome}.json' in jar.namelist()
    sheet = Image.new('RGBA',(1050,1080),(24,26,33,255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
    small = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
    alpha = None; records=[]
    for index,(key,info) in enumerate(STONES.items()):
        name,en,biomes,materials,palette,disk,rune,glyph=info
        sprite=render({'palette':colors(*palette.split()),'disk':rgb_list(disk),'rune':rgb_list(rune),'glyph':glyph})
        assert sprite.size==(18,18) and set(sprite.getchannel('A').tobytes())=={0,255}
        if alpha is None: alpha=sprite.getchannel('A').tobytes()
        assert sprite.getchannel('A').tobytes()==alpha
        # Silhouette agrees with the existing accepted Boss icon.
        old=Image.open(TEXTURES/'foolish_pyre_soul_stone.png').convert('RGBA')
        assert old.getchannel('A').tobytes()==alpha
        filename=item_id(key)
        for folder in (TEXTURES,ART/'native-18px'):
            folder.mkdir(parents=True,exist_ok=True); sprite.save(folder/(filename+'.png'))
        (ART/'preview-1260px').mkdir(exist_ok=True)
        sprite.resize((1260,1260),Image.Resampling.NEAREST).save(ART/'preview-1260px'/(filename+'.png'))
        x,y=(index%3)*350,(index//3)*360
        sheet.alpha_composite(sprite.resize((288,288),Image.Resampling.NEAREST),(x+31,y+8))
        draw.text((x+175,y+300),f'{index+1:02d} {name}',font=font,fill=(238,240,246),anchor='mt')
        draw.text((x+175,y+335),'八种能力合成' if key=='otherworld' else REGIONS_ZH[key],font=small,fill=(172,185,197),anchor='mt')
        write(RES/f'assets/{MOD}/models/item/{filename}.json',{'parent':'minecraft:item/generated','textures':{'layer0':f'{MOD}:item/{filename}'}})
        if key != 'otherworld':
            write(RES/f'data/{MOD}/recipes/{filename}.json',{
                'conditions':[{'type':'forge:mod_loaded','modid':'foolish'}],
                'type':'minecraft:crafting_shaped','pattern':[' A ','BOC',' D '],
                'key':{**{ch:{'item':'foolish:'+mat} for ch,mat in zip('ABCD',materials)},
                       'O':{'type':'forge:partial_nbt','item':f'{MOD}:foolish_attuned_soul_stone','nbt':{'FoolishBiomeSoul':key}}},
                'result':{'item':f'{MOD}:{filename}'}})
        records.append({'id':filename,'name':name,'biomes':biomes,'materials':materials,'glyph':glyph,'palette':palette,'sha256':sha(TEXTURES/(filename+'.png'))})
    sheet.save(ART/'overview.png')
    # The intermediate has the existing empty soul-stone appearance, no new icon or ability.
    write(RES/f'assets/{MOD}/models/item/foolish_attuned_soul_stone.json',{'parent':'mine_fargo:item/empty_soul_stone'})
    write(RES/f'data/{MOD}/recipes/soul_of_otherworld.json',{'conditions':[{'type':'forge:mod_loaded','modid':'foolish'}],
        'type':'minecraft:crafting_shapeless','ingredients':[{'item':f'{MOD}:{item_id(key)}'} for key in STONES if key!='otherworld'],
        'result':{'item':f'{MOD}:soul_of_otherworld'}})
    for language,strings in [('zh_cn',ZH),('en_us',EN)]:
        lang_path=RES/f'assets/{MOD}/lang/{language}.json'; lang=json.loads(lang_path.read_text(encoding='utf-8'))
        chinese=language=='zh_cn'
        for key,info in STONES.items():
            lang[f'item.{MOD}.{item_id(key)}']=info[0 if chinese else 1]
            if key!='otherworld':
                lang[f'tooltip.{MOD}.biome.{key}']=strings[key]
                region=REGIONS_ZH[key] if chinese else ' / '.join(info[2])
                lang[f'tooltip.{MOD}.biome.region.{key}']=(f'对应群系：{region}。\n当地强化：{BONUS_ZH[key]}。' if chinese else f'Native biomes: {region}.\nNative bonus: {BONUS_EN[key]}.')
        lang[f'item.{MOD}.foolish_attuned_soul_stone']='浸染魂石' if chinese else 'Attuned Soul Stone'
        lang[f'item.{MOD}.attuned_named']='浸染魂石 · %s' if chinese else 'Attuned Soul Stone · %s'
        lang[f'tooltip.{MOD}.attuned']='已记录群系气息；置于配方中央，与四种材料合成。\n潜行持空白魂石，在对应群系右键方块即可浸染。\n此物品是合成材料，不能装备。' if chinese else 'Place at the recipe center with four materials.\nSneak-right-click a block with an Empty Soul Stone in a native biome to attune.\nCrafting ingredient only; cannot be equipped.'
        lang[f'message.{MOD}.attuned']='已浸染：%s' if chinese else 'Attuned: %s'
        lang[f'tooltip.{MOD}.biome.rules']='对应群系内，列出的当地强化项 ×%s。\n伤害上限、冷却、数量上限不变；缩时比例最高 90%%。\n离开群系保留基础能力；同系列能力不重复叠加。' if chinese else 'In native biomes, listed bonus terms are multiplied by %s.\nCaps, cooldowns and count limits stay fixed; duration reduction caps at 90%%.\nBase abilities work elsewhere; overlapping abilities cannot stack.'
        lang[f'death.attack.soul_ember']='%1$s 被 %2$s 的余烬吞没' if chinese else '%1$s was consumed by %2$s\'s embers'
        lang[f'death.attack.soul_ember.item']='%1$s 被 %2$s 使用 %3$s 释放的余烬吞没' if chinese else '%1$s was consumed by %2$s\'s embers using %3$s'
        write(lang_path,lang)
    tag_path=RES/'data/curios/tags/items/soul_stone.json';tag=json.loads(tag_path.read_text())
    for key in STONES:
        value={'id':f'{MOD}:{item_id(key)}','required':False}
        if value not in tag['values']:tag['values'].append(value)
    write(tag_path,tag)
    write(RES/f'data/{MOD}/damage_type/soul_ember.json',{'message_id':'soul_ember','scaling':'never','exhaustion':.1,'effects':'burning'})
    for path in [RES/f'data/{MOD}/tags/damage_type/secondary.json',RES/'data/minecraft/tags/damage_type/is_fire.json',
                 RES/'data/minecraft/tags/damage_type/bypasses_cooldown.json']:
        tag=json.loads(path.read_text()) if path.exists() else {'replace':False,'values':[]}
        if f'{MOD}:soul_ember' not in tag['values']:tag['values'].append(f'{MOD}:soul_ember')
        write(path,tag)
    # Small crystal billboard, on a true 16x16 pixel grid with binary alpha.
    bolt=Image.new('RGBA',(16,16));draw=ImageDraw.Draw(bolt)
    draw.polygon([(8,1),(12,6),(11,12),(8,15),(4,11),(3,6)],fill=(112,65,177,255))
    draw.polygon([(8,1),(8,13),(4,10),(4,6)],fill=(192,148,236,255))
    draw.line([(8,2),(8,12)],fill=(244,223,255,255),width=1)
    bolt.save(RES/f'assets/{MOD}/textures/entity/soul_bloom.png')
    assert before=={name:sha(TEXTURES/name) for name in before}, 'Legacy artwork modified'
    write(ART/'manifest.json',{'version':'0.6.0','native_grid':[18,18],'lighting':'accepted axis and upper-left/right corrections',
        'legacy_32_hashes':before,'stones':records,'foolish_sha256':sha(foolish)})
    print('PASS: nine native 18x18 icons, eight NBT-gated recipes, one composite, bilingual tooltip resources; all 32 legacy icons unchanged.')
    print(ART/'overview.png')
if __name__=='__main__':main()
