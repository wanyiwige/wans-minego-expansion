"""Static cross-checks of optional registration, recipe gates and packaged assets."""
from pathlib import Path
import hashlib,json,re,zipfile,sys
from PIL import Image
from integrate_boss_resources import SCHOOLS,STONES,MATERIALS,MOD
from create_biome_souls import STONES as BIOME_STONES, item_id
from create_material_souls import STONES as MATERIAL_STONES, item_id as material_id
ROOT=Path(__file__).resolve().parents[1];RES=ROOT/'src/main/resources'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    for path in RES.rglob('*.json'):load(path)
    matrix=load(ROOT/'art/foolish-boss-stones-v1/dependency-matrix.json')
    ids=matrix['foolish']['items'];assert len(ids)==12
    biome_ids={item_id(key) for key in BIOME_STONES}
    biome_ids.update(material_id(key) for key in MATERIAL_STONES)
    recipes=list((RES/'data'/MOD/'recipes').glob('*.json'));assert len(recipes)==72
    for p in recipes:
        r=load(p);assert 'forge:conditions' not in r
        conditions=r['conditions'];mods={c['modid'] for c in conditions if c['type']=='forge:mod_loaded'}
        result=r['result']['item'].split(':')[-1]
        required=['foolish'] if result in ids or result in biome_ids else SCHOOLS[result.removesuffix('_soul_stone')]
        assert set(required)<=mods,(p,required,mods)
        # Every combination missing a required mod must skip this recipe before parsing its items.
        for missing in required:
            installed=mods-{missing}
            assert not all(c['modid'] in installed for c in conditions if c['type']=='forge:mod_loaded')
        if any(c['type']=='bielgg_spells:unstable_enabled' for c in conditions):
            assert conditions[0]=={'type':'forge:mod_loaded','modid':'bielgg_spells'}
    assert len(load(RES/'data'/MOD/'recipes/soul_of_stellar_hollow.json')['ingredients'])==9
    assert len(load(RES/'data'/MOD/'recipes/soul_of_foolish.json')['ingredients'])==3
    for (boss,_),materials in zip(STONES.items(),MATERIALS):
        r=load(RES/'data'/MOD/'recipes'/f'foolish_{boss}_soul_stone.json')
        assert r['pattern']==[' A ','BOC',' D ']
        assert r['key']['O']['item']=='mine_fargo:empty_soul_stone'
        assert tuple(r['key'][c]['item'] for c in 'ABCD')==tuple('foolish:'+m for m in materials)
    tag=load(RES/'data/curios/tags/items/soul_stone.json')
    assert len(tag['values'])==51 and all(v['required'] is False for v in tag['values'])
    for item in ids:
        model=load(RES/'assets'/MOD/'models/item'/(item+'.json'))
        assert model['textures']['layer0']==MOD+':item/'+item
        texture=RES/'assets'/MOD/'textures/item'/(item+'.png')
        img=Image.open(texture);assert img.size==(18,18) and img.mode=='RGBA'
        assert set(img.getchannel('A').tobytes())=={0,255}
    baseline=ROOT/'backups/20261006-150143-before-foolish-integration/src/main/resources/assets'/MOD/'textures/item'
    lighting_path=ROOT/'art/axis-lighting-fix-20261009/manifest.json'
    corrected={item['file']:item['after_sha256'] for item in load(lighting_path)['items']} if lighting_path.exists() else {}
    rim_path=ROOT/'art/right-rim-fix-20261009/manifest.json'
    if rim_path.exists():corrected.update({item['file']:item['after_sha256'] for item in load(rim_path)['items']})
    grid_path=ROOT/'art/unified-grid-left-rim-20261009/manifest.json'
    if grid_path.exists():
        grid=load(grid_path)['items'];assert len(grid)==32
        corrected.update({item['file']:item['after_sha256'] for item in grid})
        for item in grid:
            img=Image.open(RES/'assets'/MOD/'textures/item'/item['file'])
            assert img.size==(18,18) and set(img.getchannel('A').tobytes())=={0,255}
    glyph_path=ROOT/'art/taiji-wind-glyph-fix-20261010/manifest.json'
    if glyph_path.exists():corrected.update({item['file']:item['after_sha256'] for item in load(glyph_path)['items']})
    review_path=ROOT/'art/infinity-annihilation-fix-20261010/manifest.json'
    if review_path.exists():corrected.update({item['file']:item['after_sha256'] for item in load(review_path)['items']})
    preserved=0
    for p in baseline.glob('*.png'):
        assert corrected.get(p.name,sha(p))==sha(RES/'assets'/MOD/'textures/item'/p.name),p
        if not p.name.startswith('foolish_'):preserved+=1
    assert preserved==20
    source=(ROOT/'src/main/java/cn/wanyiwige/minego/BossSoulStoneItem.java').read_text(encoding='utf-8')
    cases=dict(re.findall(r'case (\w+) -> "([^"]*)";',source))
    for lang in ['zh_cn','en_us']:
        text=load(RES/'assets'/MOD/'lang'/(lang+'.json'))
        for item in ids:assert text['item.'+MOD+'.'+item]
        for boss in STONES:
            key='tooltip.'+MOD+'.foolish.stats.'+boss
            assert len(re.findall(r'(?<!%)%s',text[key]))==len(cases[boss.upper()].split()),boss
    secondary=load(RES/'data'/MOD/'tags/damage_type/secondary.json')['values'];assert len(secondary)==6
    assert set(secondary)==set(load(RES/'data/minecraft/tags/damage_type/bypasses_cooldown.json')['values'])
    java='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'src/main/java').rglob('*.java'))
    assert 'import net.warphan' not in java
    assert all(name=='ATTUNED' for name in re.findall(r'SoulStoneItems\.([A-Z_]+)\.get\(',java))
    registration=(ROOT/'src/main/java/cn/wanyiwige/minego/SoulStoneItems.java').read_text(encoding='utf-8')
    assert len(re.findall(r'= stone\("',registration))==20
    assert 'SoulDependencies.loaded(school.dependencies())' in registration
    assert 'SoulDependencies.loaded("foolish")' in registration
    assert 'return null;' in registration
    school_source=(ROOT/'src/main/java/cn/wanyiwige/minego/SchoolSoulStoneItem.java').read_text(encoding='utf-8')
    powers=dict(re.findall(r'(\w+)\("([\w]+):[\w]+"\)',school_source))
    overrides={k:re.findall(r'"(\w+)"',v) for k,v in re.findall(r'case (\w+) -> new String\[\]\{([^}]+)\}',school_source)}
    for school,deps in SCHOOLS.items():
        enum=school.removesuffix('_sect').upper()
        assert deps==overrides.get(enum,[powers[enum]]),school
    if '--source-only' in sys.argv:
        print('PASS: source recipes, dependency gates, 51 optional tag entries, textures, glyphs and bilingual placeholders. JAR verification skipped (source-only).')
        return
    # Inspect the final reobfuscated release only after the final build.
    jar=ROOT/'build/libs/wans_minego_expansion-0.6.0.jar'
    with zipfile.ZipFile(jar) as z:
        names=set(z.namelist())
        for item in ids:
            for prefix,suffix in [('assets/'+MOD+'/textures/item/','.png'),('assets/'+MOD+'/models/item/','.json'),('data/'+MOD+'/recipes/','.json')]:
                assert prefix+item+suffix in names
        assert 'cn/wanyiwige/minego/BossSoulEvents.class' in names
        assert 'cn/wanyiwige/minego/BossSoulMath.class' in names
        assert not any(n.startswith('net/warphan/') for n in names)
        assert 'version="0.6.0"' in z.read('META-INF/mods.toml').decode()
        for path in RES.rglob('*'):
            if path.is_file() and path.name!='mods.toml':
                assert z.read(path.relative_to(RES).as_posix())==path.read_bytes(),path
    print(f'PASS: {len(recipes)} recipes, 51 optional tag entries, 12 Boss textures/models, 20 school texture hashes, bilingual placeholders and final JAR.')
    print('Release SHA256:',sha(jar))
if __name__=='__main__':main()
