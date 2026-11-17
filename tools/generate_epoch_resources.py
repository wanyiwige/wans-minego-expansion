"""Author SAE resources and original 18x18 pixel icons; validate all SAE recipe IDs."""
from pathlib import Path
import json, zipfile, struct, zlib, shutil

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'src/main/resources'
MOD = 'wans_minego_expansion'
SAE = 'splendour_ablaze_epoch'
DATA = RES / 'data' / MOD
ASSETS = RES / 'assets' / MOD

NAMES = {
 'fangzun':('玄印方尊魂石','Fangzun Soul Stone'), 'cangyao':('苍尧星魂石','Cangyao Soul Stone'),
 'zixu':('子虚仙君魂石','Zixu Soul Stone'), 'zhenyan':('震焰统帅魂石','Zhenyan Soul Stone'),
 'goldenhou':('金毛犼魂石','Golden Hou Soul Stone'), 'general':('陶俑将军魂石','Terracotta General Soul Stone'),
 'magnetic_steel':('磁钢魂石','Magnetic Steel Soul Stone'), 'damascene':('龙镔魂石','Damascene Soul Stone'),
 'bronze':('青铜魂石','Bronze Soul Stone'), 'jade':('玉璧魂石','Jade Soul Stone'),
 'talisman':('朱砂符箓魂石','Cinnabar Talisman Soul Stone'), 'type':('活字魂石','Movable Type Soul Stone'),
 'ghost_jade':('幽灵玉魂石','Ghost Jade Soul Stone'), 'pyrotemper':('燧炼魂石','Pyrotemper Soul Stone'),
 'classics':('典籍魂石','Classics Soul Stone'), 'cauldron':('鼎兽魂石','Cauldron Beast Soul Stone'),
 'tiger':('炮虎卫魂石','Firearm Tiger Guard Soul Stone'), 'rusted':('镀锈先民魂石','Rusted Ancestor Soul Stone'),
 'explorer':('顶世界探索魂石','Upper World Explorer Soul Stone'), 'celesterral':('玄黄魂石','Celesterral Soul Stone'),
 'four_sovereigns':('四尊之魂','Soul of the Four Sovereigns'), 'epoch':('棠煌之魂','Soul of Splendour')}

ZH = {
 'fangzun':'法术抗性 +%s%%。成功受敌伤累计 %s 次后反制：%s 秒冷却，%s 字印伤害，迟缓 %s 秒。',
 'cangyao':'有效命中累计 %s 次触发磁引，冷却 %s 秒；附加 %s 伤害，牵引速度 %s。',
 'zixu':'每 %s 秒首次有效命中施加 %s 秒毒咒（中毒 I／迟缓 I）。\n你击杀仍有毒咒的目标时，返还近期实付法力的 %s%%，最多 %s 点；信用仅保留 20 秒且只消费一次。',
 'zhenyan':'每 %s 次实付火焰施法蓄满炮势；下次命中附加 %s 火炮伤害，%s 秒冷却。火伤减免 %s%%。',
 'goldenhou':'命中燃烧目标累计 %s 次后释放铃火，%s 秒冷却。\n总伤害 %s，半径 %s 格，最多 %s 个敌人，共享伤害；燃烧 %s 秒，虚弱 2 秒。',
 'general':'命中后为自己的召唤物轮换迅行／力量／防护 I，%s 秒冷却，持续 %s 秒。\n%s 格内最多 %s 个眷属，视线内集火；不生成额外实体。',
 'magnetic_steel':'护甲 +%s；磁极威能 +%s%%（对应流派存在时）。',
 'damascene':'近战命中后护甲韧性 +%s，持续 %s 秒；卸下立即结束。',
 'bronze':'盾牌成功格挡后，下一击伤害 +%s%%；反击窗口 %s 秒。',
 'jade':'两仪威能 +%s%%（对应流派存在时）；法术抗性 +%s%%。',
 'talisman':'四种符护仅生效所选一种：避火／避水／腾云／定身。\n冷却 %s 秒，持续 %s 秒；定身为迟缓 II，腾云为下落缓降。',
 'type':'每 %s 次实付施法完成六字印文；下次法术命中附加 %s 字印伤害，冷却 %s 秒。',
 'ghost_jade':'成功受敌伤后短暂隐身并获得迅捷 I，冷却 %s 秒，持续 %s 秒。\n攻击或施法解除本石隐身；不切换游戏模式，也不强制移除原有隐身。',
 'pyrotemper':'实付火焰施法返还 %s%% 法力，单次最多 %s 点，冷却 %s 秒。',
 'classics':'获得正经验后法力恢复 +%s%%，持续 %s 秒；不会额外生成经验。',
 'cauldron':'击杀掉落的合法经验额外 +%s%%（向下取整），单次最多 %s 点。',
 'tiger':'实付施法后强化下一次远程命中，附加 %s 炮击伤害，窗口 %s 秒，冷却 %s 秒。',
 'rusted':'抗击退 +%s%%；新施加或刷新的阴霾时长缩短 %s%%，每次只处理一次。',
 'explorer':'四种探索调谐仅生效所选一种。环境效果持续 %s 秒。\n玉镜：夜视，夜间法术抗性 +%s%%；桑牧：采掘速度 +10%%；鹤浪：水下呼吸与海豚恩惠；狼烟：抗击退 +10%%，缩短阴霾。',
}
EN = {
 'fangzun':'Spell resistance +%s%%. After %s successful incoming enemy hits: counter for %s damage with %s s slow; cooldown %s s.',
 'cangyao':'After %s effective hits, magnetic pull triggers every %s s for %s bonus damage; pull velocity %s.',
 'zixu':'Every %s s: poison I and slowness I for %s s.\nYour kill on a still-poisoned marked target refunds %s%% of recently observed mana payment, capped at %s. Credit expires after 20 s and is consumed once.',
 'zhenyan':'After %s paid fire casts, the next hit deals %s artillery damage; %s s cooldown. Fire damage reduction: %s%%.',
 'goldenhou':'After %s hits on burning targets: bellfire every %s s, %s total damage shared within %s blocks across at most %s enemies. Burn %s s; weakness 2 s.',
 'general':'Cycle speed, strength and resistance I on your own summons every %s s for %s s. Range %s; max %s summons; focus visible targets. No extra summons.',
 'magnetic_steel':'Armor +%s; magnetic spell power +%s%% when available.',
 'damascene':'Melee hits grant +%s armor toughness for %s s. Unequipping clears it.',
 'bronze':'A successful shield block empowers your next hit by %s%% within %s s.',
 'jade':'Symmetry spell power +%s%% when available; spell resistance +%s%%.',
 'talisman':'Select one ward: fire / water / slow falling / close attacker slow II. Cooldown %s s; duration %s s.',
 'type':'After %s paid casts, the next spell hit deals %s seal damage. Cooldown %s s.',
 'ghost_jade':'Enemy damage grants invisibility and speed I: cooldown %s s, duration %s s. Attack or cast breaks this stone\'s invisibility; never changes game mode.',
 'pyrotemper':'Paid fire casts refund %s%% of observed mana payment, capped at %s; cooldown %s s.',
 'classics':'Positive experience gain grants +%s%% mana regeneration for %s s. Does not create XP.',
 'cauldron':'Legal kill XP +%s%%, rounded down, capped at %s extra XP per kill.',
 'tiger':'A paid cast empowers the next ranged hit for %s damage within %s s; cooldown %s s.',
 'rusted':'Knockback resistance +%s%%; shorten new/refreshed haze by %s%% once per application.',
 'explorer':'Select one exploration mode. Effects last %s s.\nJade: night vision and +%s%% night spell resistance. Bamboo: +10%% mining speed. Crane: underwater breathing and dolphin grace. Battlefield: +10%% knockback resistance and shorter haze.',
}

def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')

def load(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def stone(k): return f'{MOD}:epoch_{k}_soul_stone'
def sae(k): return f'{SAE}:{k}'
def proof(k): return f'{MOD}:epoch_{k}_proof'

RECIPES = {
 'fangzun':[sae('initialseal'),sae('typefirst'),sae('typesixth'),sae('sagesfragments')],
 'cangyao':[sae('initialmagnet'),sae('magnetic_steel_ingot'),sae('magnetite'),sae('sagesfragments')],
 'zixu':[sae('initialhandscroll'),sae('inkbuliteitem'),sae('classics'),sae('sagesfragments')],
 'zhenyan':[sae('initialfirearm'),sae('firearmtube'),sae('leadbullet'),sae('blackpowder')],
 'goldenhou':[sae('purplegoldbell'),sae('cinnabar'),sae('pyrotemperdust')],
 'general':[sae('tigertally'),sae('commandflag'),sae('dagger')],
 'magnetic_steel':[sae('magnetic_steel_ingot')]*4+[sae('magnetite')]*2,
 'damascene':[sae('damascene_steel_ingot')]*4+[sae('darksaltpeter')],
 'bronze':[sae('bronze_ingot')]*4+['minecraft:shield'],
 'jade':[sae('jade')]*2+[sae('jadedebris')]*2+[sae('luminousjewel')],
 'talisman':[sae('talisman_1'),sae('talisman_2'),sae('talisman_3'),sae('talisman_4'),sae('cinnabar')],
 'type':[sae(k) for k in ['typefirst','typesecond','typethird','typefourth','typefifth','typesixth']]+['minecraft:black_dye'],
 'ghost_jade':[sae('ghostjadependant'),sae('jade'),sae('luminousjewel')],
 'pyrotemper':[sae('pyrotemperdust')]*4+[sae('blackpowder')],
 'classics':[sae('classics')]*2+['minecraft:book','minecraft:lapis_lazuli'],
 'cauldron':[proof('cauldron'),sae('bronze_ingot'),sae('bronze_ingot'),sae('magnetite')],
 'tiger':[proof('tiger'),sae('firearmtube'),sae('blackpowder'),sae('leadbullet')],
 'rusted':[proof('rusted'),sae('bronze_ingot'),sae('cinnabar'),'minecraft:iron_ingot'],
 'explorer':[proof('explorer'),sae('jade'),sae('classics'),sae('talisman')],
 'celesterral':[stone(k) for k in ['magnetic_steel','damascene','jade','talisman']]+[sae('celes_terral_ingot')],
 'four_sovereigns':[stone(k) for k in ['fangzun','cangyao','zixu','zhenyan']]+[sae('sagesfragments'),sae('celes_terral_ingot')],
 'epoch':[stone(k) for k in ['four_sovereigns','goldenhou','general','celesterral','explorer']]+[proof('complete')],
}

def png(path, pixels):
    h=len(pixels);w=len(pixels[0])
    raw=b''.join(b'\0'+bytes(c for p in row for c in p) for row in pixels)
    def chunk(t,b): return struct.pack('>I',len(b))+t+b+struct.pack('>I',zlib.crc32(t+b)&0xffffffff)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))

# Each symbol is authored separately: seal, magnet, scroll, gun, bell, banner, ingot etc.
SYMBOLS = [
 ['11111','10101','11111','10101','11111'], ['11011','11011','10001','10001','01110'],
 ['11110','10011','10101','10001','11111'], ['00001','11111','11110','01100','01000'],
 ['00100','01110','01110','11111','00100'], ['10000','11111','10110','10000','10000'],
 ['01110','11111','10001','10001','11111'], ['10101','01110','11111','01110','10101'],
 ['01110','11011','10001','11011','01110'], ['01110','11111','11011','11111','01110'],
 ['11111','10100','11110','00101','11111'], ['10101','11111','00100','11111','10101'],
 ['01110','10101','11111','10101','10101'], ['00100','01010','11011','10101','01110'],
 ['11011','10101','10101','10101','11111'], ['10001','11111','10001','11111','01010'],
 ['10101','01110','11011','11111','10101'], ['11000','11110','01111','00110','00011'],
 ['00100','01110','11111','00100','00100'], ['10101','01010','11111','01010','10101'],
 ['10001','01110','11011','01110','10001'], ['10101','11111','01110','11111','10101'],
]
COLORS=['b7aa65','679baa','9581b6','d65b36','e1a33c','a98157','678c91','729c68','a77643','61c6a2','ce594b','beb3a1',
        '698dae','ec8938','74a77e','aa9b60','b16e4b','9b6554','6fac8d','c3af50','bb905a','d8a84b']

def icon(i, proof_icon=False):
    rgb=tuple(bytes.fromhex(COLORS[i%22])); pix=[[(0,0,0,0) for _ in range(18)] for _ in range(18)]
    for y in range(2,16):
        half={2:2,3:4,4:5,5:6,6:6,7:7,8:7,9:7,10:7,11:6,12:6,13:5,14:4,15:2}[y]
        for x in range(9-half,9+half):
            edge=x in (9-half,8+half) or y in (2,15)
            shade=.3 if edge else (.95 if x+y<13 else .58 if x+y>22 else .76)
            pix[y][x]=tuple(int(c*shade) for c in rgb)+(255,)
    for y,row in enumerate(SYMBOLS[i%22]):
        for x,c in enumerate(row):
            if c=='1':pix[y+6][x+6]=(241,226,175,255)
    for x,y in [(5,4),(6,4),(4,5)]:pix[y][x]=(255,246,214,255)
    if proof_icon:
        for x in range(5,13):pix[14][x]=(228,202,129,255)
    return pix

def main():
    jar=next((ROOT.parent/'mods').glob('*splendour_ablaze_epoch*.jar'))
    with zipfile.ZipFile(jar) as z:
        lang=json.loads(z.read(f'assets/{SAE}/lang/en_us.json'))
        registry=(ROOT.parent/'.codex_work/splendour-audit/decompiled/net/mcreator/splendourablazeepoch/init/SplendourAblazeEpochModItems.java').read_text()
        for ingredients in RECIPES.values():
            for item in ingredients:
                if item.startswith(SAE+':'):
                    name=item.split(':')[1]
                    assert f'"{name}"' in registry, f'Unregistered SAE recipe ingredient: {item}'
    for key,ingredients in RECIPES.items():
        ingredients=list(ingredients)
        if key not in ('celesterral','four_sovereigns','epoch'):ingredients.insert(0,'mine_fargo:empty_soul_stone')
        assert len(ingredients)<=9
        write(DATA/'recipes'/f'epoch_{key}_soul_stone.json',{
            'conditions':[{'type':'forge:mod_loaded','modid':SAE}],
            'type':'minecraft:crafting_shapeless','ingredients':[{'item':i} for i in ingredients],
            'result':{'item':stone(key),'count':1}})
    for language,text in [('zh_cn',ZH),('en_us',EN)]:
        path=ASSETS/'lang'/f'{language}.json';lang=load(path)
        for key,names in NAMES.items():lang[f'item.{MOD}.epoch_{key}_soul_stone']=names[0 if language=='zh_cn' else 1]
        for key,value in text.items():lang[f'tooltip.{MOD}.epoch.{key}']=value
        # Keep parameter order aligned to server config keys.
        if language=='en_us':lang[f'tooltip.{MOD}.epoch.fangzun']='Spell resistance +%s%%. After %s incoming enemy hits: cooldown %s s, %s seal damage and %s s slowness.'
        iszh=language=='zh_cn'
        lang[f'tooltip.{MOD}.epoch.rules']='同能力魂石不可同时装备。派生伤害不再触发魂石。\n战斗触发共享 1 秒预算；炮击与字印不破坏方块。' if iszh else 'Overlapping abilities cannot be equipped together. Secondary damage cannot trigger stones.\nCombat procs share a 1 s budget; no block destruction.'
        lang[f'tooltip.{MOD}.epoch.switch']='手持本石，潜行右键切换模式；符护与探索使用同一所选模式。' if iszh else 'Sneak-use in hand to cycle modes; wards and exploration share the selected mode.'
        for i,(zh,en) in enumerate(zip(['玉镜／避火','桑牧／避水','鹤浪／腾云','狼烟／定身'],['Jade / Fire','Bamboo / Water','Crane / Falling','Battlefield / Binding'])):
            lang[f'tooltip.{MOD}.epoch.mode.{i}']=('当前模式：' if iszh else 'Mode: ')+(zh if iszh else en)
        for key,zh,en in [('cauldron','鼎兽凭证','Cauldron Proof'),('tiger','炮虎卫凭证','Tiger Guard Proof'),('rusted','锈战凭证','Rusted Battle Proof'),('explorer','顶世界见闻','Upper World Survey'),('complete','顶世界全境凭证','Upper World Completion Proof')]:
            lang[f'item.{MOD}.epoch_{key}_proof']=zh if iszh else en
        lang[f'message.{MOD}.epoch.visit']='顶世界到访进度：%s / %s' if iszh else 'Upper World survey: %s / %s'
        lang[f'death.attack.epoch_echo']='%1$s 被 %2$s 的棠煌魂印击败' if iszh else '%1$s was defeated by %2$s\'s epoch soul echo'
        lang[f'death.attack.epoch_echo.item']=lang[f'death.attack.epoch_echo']
        lang[f'death.attack.epoch_fire']=lang[f'death.attack.epoch_echo']
        lang[f'death.attack.epoch_fire.item']=lang[f'death.attack.epoch_echo']
        write(path,lang)
    tagpath=RES/'data/curios/tags/items/soul_stone.json';tag=load(tagpath)
    tag['values']=[v for v in tag['values'] if not (v.get('id','') if isinstance(v,dict) else v).startswith(MOD+':epoch_')]
    tag['values'] += [{'id':stone(k),'required':False} for k in NAMES];write(tagpath,tag)
    write(DATA/'damage_type/epoch_echo.json',{'message_id':'epoch_echo','scaling':'never','exhaustion':.1,'effects':'hurt'})
    write(DATA/'damage_type/epoch_fire.json',{'message_id':'epoch_fire','scaling':'never','exhaustion':.1,'effects':'burning'})
    for path in [DATA/'tags/damage_type/secondary.json',RES/'data/minecraft/tags/damage_type/bypasses_cooldown.json']:
        tag=load(path) if path.exists() else {'replace':False,'values':[]}
        if MOD+':epoch_echo' not in tag['values']:tag['values'].append(MOD+':epoch_echo')
        if MOD+':epoch_fire' not in tag['values']:tag['values'].append(MOD+':epoch_fire')
        write(path,tag)
    firepath=RES/'data/minecraft/tags/damage_type/is_fire.json'
    firetag=load(firepath) if firepath.exists() else {'replace':False,'values':[]}
    if MOD+':epoch_fire' not in firetag['values']:firetag['values'].append(MOD+':epoch_fire')
    write(firepath,firetag)
    sheet=[[(24,28,35,255) for _ in range(6*108)] for _ in range(4*108)]
    for i,key in enumerate(NAMES):
        name=f'epoch_{key}_soul_stone';pixels=icon(i)
        png(ASSETS/'textures/item'/f'{name}.png',pixels)
        write(ASSETS/'models/item'/f'{name}.json',{'parent':'minecraft:item/generated','textures':{'layer0':f'{MOD}:item/{name}'}})
        for y in range(18):
            for x in range(18):
                if pixels[y][x][3]:
                    for yy in range(6):
                        for xx in range(6):sheet[(i//6)*108+y*6+yy][(i%6)*108+x*6+xx]=pixels[y][x]
    for i,key in enumerate(['cauldron','tiger','rusted','explorer','complete']):
        name=f'epoch_{key}_proof'
        png(ASSETS/'textures/item'/f'{name}.png',icon(15+i,True))
        write(ASSETS/'models/item'/f'{name}.json',{'parent':'minecraft:item/generated','textures':{'layer0':f'{MOD}:item/{name}'}})
    png(ROOT/'audit/epoch-souls/icon-sheet.png',sheet)
    # The accepted 0.6.0 renderer owns finished stone art. Keep the resource generator from restoring draft icons.
    from render_epoch_stones import main as render_accepted
    render_accepted()
    print('Validated SAE ingredient IDs; generated 22 recipes, 27 models/textures and bilingual names/tooltips.')

if __name__=='__main__':main()
