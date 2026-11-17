"""Independent release and data invariants for the exploration soul stones."""
from pathlib import Path
import json, re, zipfile, hashlib, sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];RES=ROOT/'src/main/resources';MOD='wans_minego_expansion'
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    manifest=load(ROOT/'art/foolish-biome-stones-0.6.0/manifest.json')
    kinds={'bloom','storm','time','scarlet','waste','mire','growth','ash'}
    forbidden={'sacilic_heart','thunder_core','radium_crystal','scarlet_talisman','mire_jewel','white_hot_pearl','star_shard'}
    all_ids=set()
    alpha=None
    for info in manifest['stones']:
        name=info['id'];all_ids.add(MOD+':'+name)
        tex=RES/f'assets/{MOD}/textures/item/{name}.png';img=Image.open(tex)
        assert img.size==(18,18) and set(img.getchannel('A').tobytes())=={0,255}
        if alpha is None:alpha=img.getchannel('A').tobytes()
        assert alpha==img.getchannel('A').tobytes()
        assert sha(tex)==info['sha256']
        if name=='soul_of_otherworld':continue
        key=name.removeprefix('foolish_').removesuffix('_biome_soul_stone')
        assert key in kinds
        recipe=load(RES/f'data/{MOD}/recipes/{name}.json')
        assert recipe['conditions']==[{'type':'forge:mod_loaded','modid':'foolish'}]
        assert recipe['pattern']==[' A ','BOC',' D ']
        assert recipe['key']['O']=={'type':'forge:partial_nbt','item':MOD+':foolish_attuned_soul_stone','nbt':{'FoolishBiomeSoul':key}}
        assert not forbidden.intersection(info['materials']),info
        assert len(info['materials'])==4
    recipe=load(RES/f'data/{MOD}/recipes/soul_of_otherworld.json')
    assert {r['item'] for r in recipe['ingredients']}==all_ids-{MOD+':soul_of_otherworld'}
    for name,digest in manifest['legacy_32_hashes'].items():
        assert sha(RES/f'assets/{MOD}/textures/item/{name}')==digest,name
    item_source=(ROOT/'src/main/java/cn/wanyiwige/minego/BiomeSoulStoneItem.java').read_text()
    cases=dict(re.findall(r'case (\w+) -> "([^"]+)"',item_source))
    for language in ['zh_cn','en_us']:
        lang=load(RES/f'assets/{MOD}/lang/{language}.json')
        for key in kinds:
            text=lang[f'tooltip.{MOD}.biome.{key}']
            assert len(re.findall(r'(?<!%)%s',text))==len(cases[key.upper()].split()),(language,key)
            assert '\n' in text
        for name in all_ids:assert 'item.'+name.replace(':','.') in lang
    tag=load(RES/f'data/{MOD}/tags/damage_type/secondary.json')
    assert MOD+':soul_ember' in tag['values']
    assert set(tag['values'])==set(load(RES/'data/minecraft/tags/damage_type/bypasses_cooldown.json')['values'])
    materials=load(ROOT/'art/foolish-material-stones-0.6.0/manifest.json')['stones']
    assert len(materials)==10
    material_source=(ROOT/'src/main/java/cn/wanyiwige/minego/MaterialSoulStoneItem.java').read_text()
    material_cases=dict(re.findall(r'case (\w+) -> "([^"]+)"',material_source))
    for info in materials:
        texture=RES/f'assets/{MOD}/textures/item/{info["id"]}.png'
        assert sha(texture)==info['sha256']
        assert Image.open(texture).getchannel('A').tobytes()==alpha
        recipe=load(RES/f'data/{MOD}/recipes/{info["id"]}.json')
        assert recipe['key']['O']=={'item':'mine_fargo:empty_soul_stone'}
        assert recipe['conditions']==[{'type':'forge:mod_loaded','modid':'foolish'}]
        key=info['id'].removeprefix('foolish_').removesuffix('_material_soul_stone')
        for language in ['zh_cn','en_us']:
            lang=load(RES/f'assets/{MOD}/lang/{language}.json')
            assert len(re.findall(r'(?<!%)%s',lang[f'tooltip.{MOD}.material.{key}']))==len(material_cases[key.upper()].split()),key
    if '--source-only' not in sys.argv:
        release=ROOT/'build/libs/wans_minego_expansion-0.6.0.jar'
        with zipfile.ZipFile(release) as jar:
            for path in RES.rglob('*'):
                if path.is_file() and path.name!='mods.toml':assert jar.read(path.relative_to(RES).as_posix())==path.read_bytes(),path
            for name in ['BiomeSoulConfig','BiomeSoulEvents','BiomeSoulStoneItem','AttunedSoulStoneItem','MaterialSoulStoneItem','MaterialSoulEvents','MaterialSoulConfig']:
                assert f'cn/wanyiwige/minego/{name}.class' in jar.namelist()
            assert 'cn/wanyiwige/minego/BiomeSoulVerification.class' not in jar.namelist(),'Dev-only verifier shipped'
            assert f'data/{MOD}/structures/empty.nbt' not in jar.namelist(),'Dev-only structure shipped'
            assert 'version="0.6.0"' in jar.read('META-INF/mods.toml').decode()
        print('Release SHA256:',sha(release))
    print('PASS: 19 new sprites, 10 material recipes, 8 distinct attunements/recipes, no Boss cores, 32 unchanged legacy icons, bilingual placeholder order, secondary damage tags and final resource parity.')
if __name__=='__main__':main()
