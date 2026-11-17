"""Editable definitions for the 15 additional school stones in release 0.7.5.

Uses the established native-grid sprite renderer. Never builds or deploys a JAR.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
from render_scroll_style_stones import render

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'src/main/resources'
MOD = 'wans_minego_expansion'
OWN = 'alex_caves_spellsbook'

# name, provider, school, material, focus tag, optional armor set, specialty CN/EN,
# shadow/midtone/highlight, rune primary/highlight, 8x8 glyph.
DEFINITIONS = [
 ('smithing', '锻造', 'Smithing', 'iron_spell_smithing_template_addon', 'smithing',
  'iron_spell_smithing_template_addon:smithing_rune', 'iron_spell_smithing_template_addon:smithing_focus', None,
  '护甲 +2。', '+2 Armor.', ('291405','a45012','ffd17b'), ('ed8a27','ffe8af'),
  ('..OOOO..','..OIII..','....O...','....O...','IIIIIIII','.OOOOOO.','...OO...','..OOOO..')),
 ('curse', '诅咒', 'Curse', 'cursespells', 'curse', 'cursespells:curse_rune','cursespells:curse_focus',
  ['cursespells:transcendent_'+x for x in ['helmet','chestplate','leggings','boots']],
  '诅咒魔法命中使目标虚弱 I，持续3秒。', 'Curse magic hits inflict Weakness I for 3 seconds.',
  ('17141b','2a667d','9ad7e9'),('0875a3','8ceeff'),
  ('.OO.....','O..O....','O..O..I.','.OO..I.I','...O.I.I','...O..I.','....OO..','.....O..')),
 ('time', '时间', 'Time', 'irons_chronomancy','time','irons_chronomancy:time_rune','irons_chronomancy:time_focus',
  ['irons_chronomancy:chronomancer_'+x for x in ['helmet','chestplate','leggings','boots']],
  '法术冷却缩减 +5%。', '+5% Cooldown Reduction.', ('29211a','b38d37','fff0a3'),('d9ad44','fff5b4'),
  ('...OOO..','..O...O.','.O..I..O','O...I..O','O...III.','.O......','..OOOO..','........')),
 ('echo','回响','Echo','echo_spellbooks','echo','echo_spellbooks:echo_rune','echo_spellbooks:echo_focus',
  ['echo_spellbooks:echo_warden_'+x for x in ['helmet','chestplate','leggings','boots']],
  '回响魔法命中使目标发光，持续4秒。','Echo magic hits reveal the target with Glowing for 4 seconds.',
  ('04232a','187c83','d7ffff'),('37b6bd','c4ffff'),
  ('..I.....','..I...I.','I.I...I.','I.I.I.I.','IIIIIIII','.O.O.O..','..O.O...','........')),
 ('exo','星宇','Exo','roacw','exo','roacw:charged_auric_ingot','curios:exo_focus',None,
  '护甲韧性 +1。','+1 Armor Toughness.',('030d2e','094aa9','76dfff'),('00a7f2','b3ffff'),
  ('OO....II','OO.OO.II','...OO...','..OOOO..','..O..O..','..O..OOO','OOO..O.O','O.O..OOO')),
 ('magnetic','磁极','Magnetic',OWN,'magnetic',OWN+':magnetic_polarity_rune',OWN+':magnetic_focus',
  [OWN+':magnetic_mage_'+x for x in ['helmet','chestplate','leggings','boots']],
  '击退抗性 +0.10。','+0.10 Knockback Resistance.',('110d25','3055a5','a5b6ee'),('ef3d49','3698ff'),
  ('..OO....','OOO.....','..OOOO..','....OO..','..II....','..IIII..','.....III','....II..')),
 ('candy','糖果','Candy',OWN,'candy',OWN+':candy_rune',OWN+':candy_focus',
  [OWN+':candy_wizard_'+x for x in ['hat','robe','leggings','boots']],
  '最大生命值 +2。','+2 Maximum Health.',('351222','cf678e','ffe4ed'),('ff91b6','b8fff3'),
  ('..OOOO..','.OIIIIO.','OI....IO','OI..OOIO','OI..O.IO','.O..O.O.','...O....','..O.....')),
 ('cloud','云','Cloud',OWN,'cloud','minecraft:phantom_membrane',OWN+':cloud_focus',None,
  '移动速度 +5%。','+5% Movement Speed.',('202733','7d8696','f8f9ff'),('b8c3d1','ffe279'),
  ('..OO....','.OIIO.O.','OIIIIOIO','OOOOOOOO','..I..I..','........','.I..I...','........')),
 ('toxic','辐射','Radiation',OWN,'toxic','alexscaves:uranium',OWN+':toxic_focus',None,
  '辐射魔法命中施加中毒 I，持续3秒。','Radiation magic hits inflict Poison I for 3 seconds.',
  ('151e0c','78a00f','dcff77'),('b7f22b','ffff48'),
  ('OO....I.','O.O..III','OO....I.','..O..O..','...OO...','..O..O..','.III..OO','..I..O.O')),
 ('astral','星辉','Astral',OWN,'kubejs:astral','asterismarcanum:astral_rune','kubejs:astral_focus',None,
  '法力回复 +5%。','+5% Mana Regeneration.',('24182e','a18bac','ebffe3'),('ddd5ee','daffcf'),
  ('I....OO.','.O..O..O','..OO..OO','...I.O..','....O...','..OO....','.O..O...','I....I..')),
 ('traveller','旅者','Traveller',OWN,'kubejs:traveller','minecraft:ender_pearl','kubejs:traveller_focus',None,
  '移动速度 +5%。','+5% Movement Speed.',('052a27','29a495','d5fff3'),('62ddbd','fff09a'),
  ('OOO.....','O.IOOO..','O.IO.IO.','..IO.IO.','..IO.OIO','..IOO.IO','....I.IO','....OOO.')),
 ('hazen_cosmic','寰宇','Cosmic',OWN,'hazen_cosmic',OWN+':hazen_cosmic_rune',OWN+':hazen/cosmic_focus',
  [OWN+':hazen_cosmic_scholar_'+x for x in ['helmet','chestplate','leggings','boots']],
  '召唤物伤害 +5%。','+5% Summon Damage.',('050d1d','1e3e65','b2d9f9'),('3a81b3','ffde64'),
  ('....OOO.','...OIIIO','...OIIIO','....OOO.','..OO....','.OI.....','.O......','I.......')),
 ('hazen_radiance','光辉','Radiance',OWN,'hazen_radiance',OWN+':hazen_radiance_rune',OWN+':hazen/radiance_focus',None,
  '法术抗性 +5%。','+5% Spell Resistance.',('2a213b','a077ba','f4f7ff'),('cc99f0','fffaff'),
  ('...II...','.I.OO.I.','..O..O..','IOI..IOI','..O..O..','.IOOOOI.','........','OOOOOOOO')),
 ('hazen_shadow','黑暗','Darkness',OWN,'hazen_shadow',OWN+':hazen_shadow_rune',OWN+':hazen/shadow_focus',None,
  '施法时间缩减 +5%。','+5% Cast Time Reduction.',('0c081b','46346b','af9bd2'),('7556bd','c4a7fb'),
  ('..OOOO..','.OIIIIO.','OI.O..IO','O..O...O','...O..O.','..O..O..','.O..O...','.OOO....')),
 ('hazen_hydro','海怒','Hydro',OWN,'hazen_hydro',OWN+':hazen_hydro_rune',OWN+':hazen/hydro_focus',None,
  '游泳速度 +10%。','+10% Swim Speed.',('08172e','1b5ca6','89e6ff'),('2894e8','9af6ff'),
  ('...OO...','..OIIO..','.OIIIO..','OIIIOOOO','OOO.....','....OO..','..OOIIO.','OOOOOOOO')),
]

def rows():
    for key,zh,en,provider,school,material,focus,armor,zh_effect,en_effect,palette,runes,glyph in DEFINITIONS:
        item = key + ('_school_soul_stone' if key in {'magnetic','candy','cloud','toxic'} else '_soul_stone')
        school_id = school if ':' in school else provider + ':' + school
        yield dict(key=key,name=zh+'学派魂石',english=en+' School Soul Stone',provider=provider,
                   school=school_id,attribute=school_id.split(':')[0]+':'+school_id.split(':')[1]+'_spell_power',
                   item=item,material=material,focus=focus,armor=armor,zh_effect=zh_effect,en_effect=en_effect,
                   palette=palette,runes=runes,glyph=glyph)

def dump(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def ramp(anchors):
    anchors=[tuple(bytes.fromhex(c)) for c in anchors]
    result=[]
    for i in range(9):
        t=i/4; low=min(int(t),1); f=t-low
        result.append(tuple(round(a*(1-f)+b*f) for a,b in zip(anchors[low],anchors[low+1])))
    return tuple(result)

def main():
    records=list(rows()); art=ROOT/'art/remaining-school-souls-0.7.5';art.mkdir(parents=True,exist_ok=True)
    cn=RES/f'assets/{MOD}/lang/zh_cn.json';en=RES/f'assets/{MOD}/lang/en_us.json'
    langs=[json.loads(p.read_text(encoding='utf-8')) for p in (cn,en)]
    tagpath=RES/'data/curios/tags/items/soul_stone.json';tag=json.loads(tagpath.read_text(encoding='utf-8'))
    known={v if isinstance(v,str) else v['id'] for v in tag['values']}
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20)
    sheet=Image.new('RGBA',(5*240,3*266),(29,30,36,255));draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(records):
        ident=MOD+':'+r['item'];base=f'data/{MOD}/recipes/'+r['item']
        rune={'item':r['material']};focus={'tag':r['focus']}
        def recipe(suffix,pattern,key):
            conditions=[{'type':'forge:mod_loaded','modid':r['provider']},
                        {'type':'forge:item_exists','item':ident}]
            conditions += [{'type':'forge:item_exists','item':v['item']} for v in key.values() if 'item' in v]
            conditions += [{'type':'forge:not','value':{'type':'forge:tag_empty','tag':v['tag']}} for v in key.values() if 'tag' in v]
            dump(RES/(base+suffix+'.json'),dict(type='minecraft:crafting_shaped',pattern=pattern,key=key,
                                             result={'item':ident},conditions=conditions))
        blank={'item':'mine_fargo:empty_soul_stone'}
        if r['armor']:
            recipe('', ['EAE','BOC','EDE'],dict(E=focus,O=blank,**{c:{'item':v} for c,v in zip('ABCD',r['armor'])}))
        else:
            recipe('', ['ERE','ROR','ERE'],dict(E=focus,R=rune,O=blank))
        recipe('_materials',['RRR','ROR','RRR'],dict(R=rune,O=blank))
        dump(RES/f'assets/{MOD}/models/item/{r["item"]}.json',{'parent':'minecraft:item/generated','textures':{'layer0':MOD+':item/'+r['item']}})
        for lang,label,effect in zip(langs,[r['name'],r['english']],[r['zh_effect'],r['en_effect']]):
            lang['item.'+ident.replace(':','.')]=label
            lang[f'tooltip.{MOD}.{r["key"]}']=effect
        if ident not in known:tag['values'].append({'id':ident,'required':False})
        palette=ramp(r['palette']);rune_colors=tuple(tuple(bytes.fromhex(c)) for c in r['runes'])
        im=render(dict(palette=palette,disk=(palette[1],palette[2]),rune=rune_colors,glyph=r['glyph'],full_disk=True))
        im.save(RES/f'assets/{MOD}/textures/item/{r["item"]}.png')
        im.save(art/(r['item']+'.png'))
        im.resize((252,252),Image.Resampling.NEAREST).save(art/(r['item']+'-preview.png'))
        x=i%5*240+12;y=i//5*266+8
        sheet.alpha_composite(im.resize((216,216),Image.Resampling.NEAREST),(x,y))
        draw.text((x,y+222),r['name'],font=font,fill='white')
    dump(cn,langs[0]);dump(en,langs[1]);dump(tagpath,tag)
    sheet.save(art/'preview.png');dump(art/'definitions.json',records)
    print('Generated 15 stones, 30 recipes, models, bilingual tooltips and optional Curios entries.')

if __name__=='__main__':main()
