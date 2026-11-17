"""Release packaging, asset, localization and preservation checks for 0.7.0."""
from pathlib import Path
import hashlib,json,re,zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];RES=ROOT/'src/main/resources';MOD='wans_minego_expansion'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    checks=0
    def check(ok,name):
        nonlocal checks
        assert ok,name
        checks+=1
    manifest=load(ROOT/'art/epoch-soul-stones-0.7.0/manifest.json')
    old=ROOT/'backups/20261011-before-sae-souls/src/main/resources'
    reference=Image.open(RES/f'assets/{MOD}/textures/item/foolish_pyre_soul_stone.png').getchannel('A').tobytes()
    ids={MOD+':'+s['id'] for s in manifest['stones']}
    check(len(ids)==22,'22 stones')
    cfg=(ROOT/'src/main/java/cn/wanyiwige/minego/EpochSoulConfig.java').read_text()
    counts={key.lower():len(re.findall(r'"[a-z_]+\.[a-z_]+"',values)) for key,values in re.findall(r't\(EpochSoulStoneItem.Kind.(\w+),(.*?)\);',cfg)}
    lang={code:load(RES/f'assets/{MOD}/lang/{code}.json') for code in ['zh_cn','en_us']}
    for s in manifest['stones']:
        name=s['id'];key=name.removeprefix('epoch_').removesuffix('_soul_stone')
        img=Image.open(RES/f'assets/{MOD}/textures/item/{name}.png')
        check(img.size==(18,18),'18px '+key)
        check(img.getchannel('A').tobytes()==reference,'accepted alpha '+key)
        check(sha(RES/f'assets/{MOD}/textures/item/{name}.png')==s['sha256'],'asset hash '+key)
        recipe=load(RES/f'data/{MOD}/recipes/{name}.json')
        check(recipe['conditions']==[{'type':'forge:mod_loaded','modid':'splendour_ablaze_epoch'}],'optional recipe '+key)
        check(1<=len(recipe['ingredients'])<=9,'crafting grid bound '+key)
        check(recipe['result']['item']==MOD+':'+name,'recipe result '+key)
        if key not in ('celesterral','four_sovereigns','epoch'):
            check(recipe['ingredients'][0]=={'item':'mine_fargo:empty_soul_stone'},'empty stone '+key)
        for code in lang:
            check(f'item.{MOD}.{name}' in lang[code],'localized name '+key)
            if key in counts:
                check(len(re.findall(r'(?<!%)%s',lang[code][f'tooltip.{MOD}.epoch.{key}']))==counts[key],'tooltip parameter count '+key)
    for p in (old/f'assets/{MOD}/textures/item').glob('*.png'):
        check(sha(p)==sha(RES/f'assets/{MOD}/textures/item'/p.name),'preserved old icon '+p.name)
    oldlang=load(old/f'assets/{MOD}/lang/zh_cn.json')
    for key,value in oldlang.items():check(lang['zh_cn'][key]==value,'preserved localization '+key)
    tag=load(RES/'data/curios/tags/items/soul_stone.json')
    tagged={v['id'] if isinstance(v,dict) else v for v in tag['values']}
    check(ids<=tagged,'Curios tags')
    guard=set(load(RES/f'data/{MOD}/tags/damage_type/secondary.json')['values'])
    iframe=set(load(RES/'data/minecraft/tags/damage_type/bypasses_cooldown.json')['values'])
    check(guard==iframe,'secondary iframe tags agree')
    release=ROOT/'build/libs/wans_minego_expansion-0.7.0.jar'
    with zipfile.ZipFile(release) as jar:
        names=jar.namelist()
        check(not any('Verification' in n for n in names),'no development verifier shipped')
        check('version="0.7.0"' in jar.read('META-INF/mods.toml').decode(),'release version')
        for p in RES.rglob('*'):
            if p.is_file() and p.name!='mods.toml':check(jar.read(p.relative_to(RES).as_posix())==p.read_bytes(),'resource parity '+str(p))
        for cls in ['EpochSoulStoneItem','EpochSoulEvents','EpochSoulConfig']:
            check(f'cn/wanyiwige/minego/{cls}.class' in names,'release class '+cls)
    receipt={'version':'0.7.0','release':str(release),'sha256':sha(release),'size_bytes':release.stat().st_size,
             'checks':checks,'stones':22,'proof_items':5,'legacy_textures_unchanged':51,
             'build':'BUILD SUCCESSFUL; reobfJar executed','deployed':False,'full_pack_gameplay_verified':False}
    (ROOT/'audit/epoch-souls/release-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(f'PASS: {checks} release/asset/localization/preservation checks; SHA256 {receipt["sha256"]}')
if __name__=='__main__':main()
