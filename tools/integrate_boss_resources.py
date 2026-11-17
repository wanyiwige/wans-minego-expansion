"""Generate boss assets/recipes and align optional school recipe dependencies."""
from pathlib import Path
import json,hashlib
from PIL import Image, ImageDraw, ImageFont
from render_foolish_boss_stones import STONES, stone, render
from soul_tooltip_layout import format_lang

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'src/main/resources'
MOD='wans_minego_expansion'
def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def loaded(mod): return {'type':'forge:mod_loaded','modid':mod}
SCHOOLS={
 'symmetry_sect':['iss_magicfromtheeast'], 'spirit_sect':['iss_magicfromtheeast'],
 'insect':['entomology_spell'],'dream':['dreammagic'],'wind':['wind_spellbooks'],
 'annihilation':['legendary_spellbooks'],'shadow':['bielgg_spells','roaring'],
 'unstable':['bielgg_spells'],'relicron':['bielgg_spells','eeeabsmobs'],
 'infinity':['bielgg_spells','avaritia'],'tainted':['bielgg_spells','witherstormmod'],
 'trailblazer_arcana':['astralrail_cube'],'fusion':['iss_csw'],'ars_nouveau':['ars_nouveau_spellbooks'],
 'abyssal':['cataclysm_spellbooks'],'technomancy':['cataclysm_spellbooks'],
 'esoteric':['esoteric_spell'],'gluttony':['farmers_spell'],'glintstone':['iss_elden_ring'],'glutton':['bigeater_magic']}
MATERIALS=[
 ('white_hot_pearl','incinerator_2','blazing_pitchfork','white_hot_pearl'),
 ('chronos_solitaire','timewelder_spear','warp_amber','chronos_solitaire'),
 ('mire_jewel','thrashing_apparatus','horrendon_fin','mire_jewel'),
 ('sacilic_heart','sacilite_hammer','shining_sacilite_lens','sacilic_heart'),
 ('radium_crystal','corrosion_cannon','mutilator_sword','radium_crystal'),
 ('thunder_core','thunder_caduceus','charged_thunderstone_rod','thunder_core'),
 ('scarlet_talisman','scarlet_scepter_staff','scarlet_crown_helmet','scarlet_talisman'),
 ('flora_gem','gaia_staff','gaia_ingrain','flora_gem'),
 ('immortal_artillery','charm_of_carnage','soul_coat_chestplate','wendigo_skull'),
 ('star_shard','stellar_sword','stellar_upgrade_template','star_shard')]
TOOLTIPS={
 'pyre':'白炽余火：概率点燃；攻击燃烧目标增伤，火系法术获得强化。耐热：减少火焰伤害。',
 'timewelder':'时流偏转：提高移速，概率令敌人减速并使自身加速。时能回流：概率返还实际消耗的法力。',
 'thrasher':'泥潭猎手：提高游泳速度、水中攻击伤害。鞭打冲击：对周围其他敌人附加范围伤害。',
 'sacilic_abomination':'紫晶甲壳：提高护甲韧性。晶刺反击：受击反伤。晶震：概率束缚普通敌人，Boss 改为轻微减速。',
 'varmint_king':'腐蚀性毒素：攻击施加中毒；再次攻击中毒目标概率降低其护甲。自然／污秽法术对中毒目标增伤。',
 'thunderbird':'风暴跃迁：概率向两个其他敌人释放电弧，直接雷系法术必定触发。余电：成功跃迁后短暂加速。',
 'scarlant_queen':'女王统御：提高所属召唤物伤害。猩红援军：概率召唤临时猩红随从，拥有独立主人和数量上限。',
 'terrorflora':'蔓生缠绕：概率束缚普通敌人，Boss 改为轻微减速。孢子摄生：按实际原始伤害回血，每秒设有上限。',
 'wendigrudge':'怀恨不灭：低血量时增伤，战斗中缓慢回血。怨灵炮击：概率释放短程追踪怨灵弹。',
 'astralis':'星刃追击：概率附加追踪星刃。星辰招架：概率减免敌方伤害，并短暂提高原始攻击伤害。'}
STATS_ZH={
 'pyre':'点燃 %s%% / %s秒；燃烧增伤 %s%%（火法 %s%%）；火伤减免 %s%%',
 'timewelder':'移速 +%s%%；时流 %s%%（法术 %s%%）/ ±%s%% / %s秒 / 冷却%s秒；回流 %s%% / 返还%s%% / 上限%s / 冷却%s秒',
 'thrasher':'游泳 +%s%%；水中增伤 %s%%；冲击 %s%%（法术 %s%%）/ %s格 / %s目标 / 冷却%s秒',
 'sacilic_abomination':'韧性 +%s；反伤 %s + %s%% / 上限%s / 冷却%s秒；晶震 %s%% / %s秒 / 冷却%s秒',
 'varmint_king':'中毒 %s秒；腐蚀 %s%% / 护甲 -%s%% / %s秒；自然与污秽法术增伤 %s%%',
 'thunderbird':'电弧 %s%% / 伤害%s%%、%s%% / 上限%s / 冷却%s秒；移速 +%s%% / %s秒',
 'scarlant_queen':'召唤增伤 %s%%；援军 %s%%（法术 %s%%）/ 最多%s只 / %s秒 / 生命%s / 攻击%s / 冷却%s秒',
 'terrorflora':'缠绕 %s%%（自然 %s%%）/ %s秒 / 冷却%s秒；吸血 %s%% / 每秒最多%s HP',
 'wendigrudge':'生命低于%s%%开始增伤，%s%%时达到%s%%；每次恢复%s HP / 间隔%s秒；炮击 %s%% / 伤害%s%% / 上限%s / 冷却%s秒',
 'astralis':'星刃 %s%%（法术 %s%%）/ 伤害%s%% / 上限%s / 冷却%s秒；招架 %s%% / 减伤%s%% / 冷却%s秒；反击增伤 %s%% / %s秒'}
STATS_EN={
 'pyre':'Ignite %s%% / %ss; burning bonus %s%% (fire %s%%); fire reduction %s%%',
 'timewelder':'Speed +%s%%; temporal %s%% (spell %s%%) / shift %s%% / %ss / CD %ss; rebate %s%% / refund %s%% / cap %s / CD %ss',
 'thrasher':'Swim +%s%%; water bonus %s%%; splash %s%% (spell %s%%) / %s blocks / %s targets / CD %ss',
 'sacilic_abomination':'Toughness +%s; reflect %s + %s%% / cap %s / CD %ss; stagger %s%% / %ss / CD %ss',
 'varmint_king':'Poison %ss; corrosion %s%% / armor -%s%% / %ss; spell bonus %s%%',
 'thunderbird':'Arc %s%% / damage %s%%, %s%% / cap %s / CD %ss; speed +%s%% / %ss',
 'scarlant_queen':'Summon bonus %s%%; attendant %s%% (spell %s%%) / max %s / %ss / HP %s / attack %s / CD %ss',
 'terrorflora':'Root %s%% (nature %s%%) / %ss / CD %ss; leech %s%% / max %s HP per second',
 'wendigrudge':'Bonus starts below %s%% HP, peaks at %s%% HP with %s%%; heal %s HP every %ss; bolt %s%% / damage %s%% / cap %s / CD %ss',
 'astralis':'Blade %s%% (spell %s%%) / damage %s%% / cap %s / CD %ss; parry %s%% / reduction %s%% / CD %ss; riposte %s%% / %ss'}

def main():
    recipes=RES/'data'/MOD/'recipes'
    for path in recipes.glob('*.json'):
        data=json.loads(path.read_text(encoding='utf-8'))
        result=data.get('result',{}).get('item','').split(':')[-1]
        school=result.removesuffix('_soul_stone')
        if school not in SCHOOLS:continue
        old=data.pop('forge:conditions',data.get('conditions',[]))
        if isinstance(old,dict):old=[old]
        extras=[c for c in old if c.get('type')!='forge:mod_loaded']
        deps=list(SCHOOLS[school])
        def collect(obj):
            if isinstance(obj,dict):
                for k,v in obj.items():
                    if k in ('item','tag') and isinstance(v,str):
                        namespace=v.split(':')[0]
                        if namespace not in ('minecraft',MOD,'mine_fargo') and namespace not in deps:deps.append(namespace)
                    else:collect(v)
            elif isinstance(obj,list):
                for v in obj:collect(v)
        collect(data.get('key',{}));collect(data.get('ingredients',[]))
        data['conditions']=[loaded(d) for d in deps]+extras
        write(path,data)
    ids=[]
    for (boss,info),materials in zip(STONES.items(),MATERIALS):
        item=f'foolish_{boss}_soul_stone';ids.append(item)
        key={letter:{'item':'foolish:'+material} for letter,material in zip('ABCD',materials)}
        key['O']={'item':'mine_fargo:empty_soul_stone'}
        write(recipes/(item+'.json'),{'conditions':[loaded('foolish')],'type':'minecraft:crafting_shaped','pattern':[' A ','BOC',' D '],'key':key,'result':{'item':MOD+':'+item}})
    for item,ingredients in [('soul_of_stellar_hollow',ids[:9]),('soul_of_foolish',['soul_of_stellar_hollow',ids[9],'foolish:stellar_catalyst'])]:
        write(recipes/(item+'.json'),{'conditions':[loaded('foolish')],'type':'minecraft:crafting_shapeless','ingredients':[{'item':i if ':' in i else MOD+':'+i} for i in ingredients],'result':{'item':MOD+':'+item}})
        ids.append(item)
    for item in ids:
        write(RES/'assets'/MOD/'models/item'/(item+'.json'),{'parent':'minecraft:item/generated','textures':{'layer0':MOD+':item/'+item}})
    composites={
      'soul_of_stellar_hollow':stone('星渊之魂','九魂聚合','13152a 29254a 484073 695b99 8a78b8 afa0d3 cec4eb e7dff8 f9f4ff','1e1b36 292343','bba3ed f9ecc3',['..OOOO..','.OI..IO.','OI.OO.IO','O.OIIO.O','O.OIIO.O','OI.OO.IO','.OI..IO.','..OOOO..']),
      'soul_of_foolish':stone('Foolish之魂','十魂星冠','251628 492c40 76514e a5795e cea579 e7c797 f3dfbe fbeddb fffff4','30223d 3b2b49','e9a9da fff3b5',['...II...','O.OIIO.O','OOOIIOOO','.OIIIIO.','OOIIIIOO','.OI..IO.','..OIIO..','...OO...'])}
    for item,info in composites.items():
        sprite=render(info);path=RES/'assets'/MOD/'textures/item'/(item+'.png');sprite.save(path)
        out=ROOT/'art/foolish-boss-stones-v1/native-18px'/(item+'.png');sprite.save(out)
        sprite.resize((1260,1260),Image.Resampling.NEAREST).save(ROOT/'art/foolish-boss-stones-v1/preview-1260px'/(item+'.png'))
    art=ROOT/'art/foolish-boss-stones-v1'
    manifest=json.loads((art/'manifest.json').read_text(encoding='utf-8'))
    manifest['composites']=[{'file':item+'.png','name':info['name'],'native_size':[18,18],
        'sha256':hashlib.sha256((RES/'assets'/MOD/'textures/item'/(item+'.png')).read_bytes()).hexdigest(),
        'glyph':info['glyph'],'palette':info['palette']} for item,info in composites.items()]
    write(art/'manifest.json',manifest)
    preview=Image.new('RGBA',(1200,960),(24,26,33,255));draw=ImageDraw.Draw(preview)
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
    for index,info in enumerate(list(STONES.values())+list(composites.values())):
        x,y=(index%4)*300,(index//4)*320
        preview.alpha_composite(render(info).resize((252,252),Image.Resampling.NEAREST),(x+24,y+12))
        draw.text((x+150,y+280),info['name'],font=font,fill=(235,238,245),anchor='mt')
    preview.save(art/'foolish-souls-preview-0.5.0.png')
    tag=RES/'data/curios/tags/items/soul_stone.json'
    write(tag,{'replace':False,'values':[{'id':MOD+':'+s+'_soul_stone','required':False} for s in SCHOOLS]+[{'id':MOD+':'+s,'required':False} for s in ids]})
    for lang in ['zh_cn','en_us']:
        path=RES/'assets'/MOD/'lang'/(lang+'.json');data=json.loads(path.read_text(encoding='utf-8'))
        for boss,info in STONES.items():
            item=f'foolish_{boss}_soul_stone'
            data['item.'+MOD+'.'+item]=(info['name']+'魂石') if lang=='zh_cn' else boss.replace('_',' ').title()+' Soul Stone'
            data['tooltip.'+MOD+'.foolish.'+boss]=TOOLTIPS[boss] if lang=='zh_cn' else {'pyre':'Burning attacks, fire spell synergy and fire resistance.','timewelder':'Movement speed, temporal slow/haste and mana rebate.','thrasher':'Swimming speed, underwater damage and splash attacks.','sacilic_abomination':'Armor toughness, crystal retaliation and stagger.','varmint_king':'Poison, corrosion and nature/tainted spell synergy.','thunderbird':'Chain lightning and temporary haste.','scarlant_queen':'Owned summon damage and temporary scarlet attendants.','terrorflora':'Root enemies and heal from original damage with a shared budget.','wendigrudge':'Low-health damage, combat regeneration and homing wraith bolts.','astralis':'Homing star blades and probabilistic parry/riposte.'}[boss]
            data['tooltip.'+MOD+'.foolish.stats.'+boss]=(STATS_ZH if lang=='zh_cn' else STATS_EN)[boss]
        data['item.'+MOD+'.soul_of_stellar_hollow']='星渊之魂' if lang=='zh_cn' else 'Soul of the Stellar Hollow'
        data['item.'+MOD+'.soul_of_foolish']='Foolish之魂' if lang=='zh_cn' else 'Soul of Foolish'
        data['tooltip.'+MOD+'.foolish_rules']='同系列组成能力互斥；派生攻击不触发派生链。数值以服务器魂石配置为准。' if lang=='zh_cn' else 'Overlapping abilities cannot be equipped together. Secondary hits cannot proc chains. Values follow server soul configuration.'
        for effect,cn in [('time_slow','时流迟滞'),('time_speed','时流加速'),('storm_speed','余电'),('soul_rooted','蔓生束缚'),('crystal_slow','晶震'),('flora_slow','蔓生迟滞'),('soul_corrosion','腐蚀')]:
            data['effect.'+MOD+'.'+effect]=cn if lang=='zh_cn' else effect.replace('_',' ').title()
        data['entity.'+MOD+'.soul_ant']='猩红随从' if lang=='zh_cn' else 'Scarlet Attendant'
        data['entity.'+MOD+'.soul_bolt']='魂石追击' if lang=='zh_cn' else 'Soul Pursuit'
        for dtype in ['soul_crystal','soul_splash','soul_lightning','soul_wraith','soul_star']:
            data['death.attack.'+dtype]='%1$s 被魂石力量击败' if lang=='zh_cn' else '%1$s was slain by soul power'
            data['death.attack.'+dtype+'.player']='%1$s 被 %2$s 的魂石力量击败' if lang=='zh_cn' else '%1$s was slain by %2$s with soul power'
        write(path,format_lang(data,lang))
    damage=[]
    for dtype in ['soul_crystal','soul_splash','soul_lightning','soul_wraith','soul_star']:
        write(RES/'data'/MOD/'damage_type'/(dtype+'.json'),{'message_id':dtype,'scaling':'never','exhaustion':0.1,'effects':'hurt'})
        damage.append(MOD+':'+dtype)
    write(RES/'data'/MOD/'tags/damage_type/secondary.json',{'replace':False,'values':damage})
    write(RES/'data/minecraft/tags/damage_type/is_projectile.json',{'replace':False,'values':[MOD+':soul_wraith',MOD+':soul_star']})
    write(RES/'data/minecraft/tags/damage_type/bypasses_cooldown.json',{'replace':False,'values':damage})
    write(RES/'data/irons_spellbooks/tags/damage_type/lightning_magic.json',{'replace':False,'values':[MOD+':soul_lightning']})
    write(RES/'data/forge/tags/entity_types/bosses.json',{'replace':False,'values':[{'id':'foolish:'+b,'required':False} for b in STONES]+['minecraft:ender_dragon','minecraft:wither']})
    # A simple scarlet arthropod skin on the vanilla segmented model's 64x32 UV grid.
    entity=RES/'assets'/MOD/'textures/entity/soul_ant.png';entity.parent.mkdir(parents=True,exist_ok=True)
    skin=Image.new('RGBA',(64,32),(126,25,46,255));d=ImageDraw.Draw(skin)
    for y in range(32):
        for x in range(64):
            d.point((x,y),fill=[(67,16,30,255),(126,25,46,255),(184,43,70,255),(226,83,104,255)][((x//3)+(y//3))%4])
    skin.save(entity)
    for boss,name in [('astralis','soul_star'),('wendigrudge','soul_wraith')]:
        sprite=Image.new('RGBA',(16,16),(0,0,0,0));draw=ImageDraw.Draw(sprite)
        info=STONES[boss]
        for y,row in enumerate(info['glyph']):
            for x,pixel in enumerate(row):
                if pixel!='.':draw.point((x+4,y+4),fill=info['rune'][pixel=='I']+(255,))
        sprite.save(RES/'assets'/MOD/'textures/entity'/(name+'.png'))
    icons={'time_slow':'timewelder','time_speed':'timewelder','storm_speed':'thunderbird','soul_rooted':'terrorflora','crystal_slow':'sacilic_abomination','flora_slow':'terrorflora','soul_corrosion':'varmint_king'}
    for effect,boss in icons.items():
        path=RES/'assets'/MOD/'textures/mob_effect'/(effect+'.png');path.parent.mkdir(parents=True,exist_ok=True)
        render(STONES[boss]).crop((1,1,17,17)).save(path)
    write(ROOT/'art/foolish-boss-stones-v1/dependency-matrix.json',{'schools':SCHOOLS,'foolish':{'requires':['foolish'],'items':ids}})
    # Optional ordering never makes an addon mandatory.
    toml=RES/'META-INF/mods.toml';text=toml.read_text(encoding='utf-8')
    for addon in sorted(set(sum(SCHOOLS.values(),[]))|{'foolish'}):
        if 'modId="'+addon+'"' not in text:text+='\n[[dependencies.${mod_id}]]\nmodId="'+addon+'"\nmandatory=false\nversionRange="[0,)"\nordering="AFTER"\nside="BOTH"\n'
    toml.write_text(text,encoding='utf-8')
    script=ROOT/'tools/generate_school_stones.py'
    if script.exists():script.write_text(script.read_text(encoding='utf-8').replace('forge:conditions','conditions'),encoding='utf-8')
    print('12 recipes/models, 2 composite sprites, 7 effect icons, 5 damage types; school recipe conditions normalized.')
if __name__=='__main__': main()
