"""Check installed ingredient/tag resources, recipe guards, native sprites and release contents."""
from pathlib import Path
import hashlib, json, sys, zipfile
from PIL import Image
from create_remaining_school_souls import ROOT, RES, MOD, rows

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    records=list(rows()); instance=ROOT.parent
    modeled=set(); tag_values={}
    for path in (instance/'mods').glob('*.jar'):
        with zipfile.ZipFile(path) as jar:
            for name in jar.namelist():
                parts=name.split('/')
                if name.endswith('.json') and name.startswith('assets/') and '/models/item/' in name:
                    modeled.add(parts[1]+':'+name.split('/models/item/')[1][:-5])
                if name.endswith('.json') and name.startswith('data/') and '/tags/items/' in name:
                    try:data=json.loads(jar.read(name))
                    except (ValueError,UnicodeDecodeError):continue
                    tag=parts[1]+':'+name.split('/tags/items/')[1][:-5]
                    if data.get('replace'):tag_values[tag]=[]
                    tag_values.setdefault(tag,[]).extend(data['values'])
    def tag_leaves(tag,visited=()):
        assert tag not in visited, ('cyclic tag',tag)
        result=[]
        for value in tag_values.get(tag,[]):
            value=value if isinstance(value,str) else value['id']
            if value.startswith('#'):result+=tag_leaves(value[1:],visited+(tag,))
            else:result.append(value)
        return result
    modeled.update(MOD+':'+r['item'] for r in records)
    def check_item(ident):
        # Vanilla ingredients here are established vanilla items, not generated mod resources.
        assert ident.startswith('minecraft:') or ident in modeled, ('missing item model',ident)
    old=ROOT/'backups/20261020-before-school-souls/src/main/resources'
    old_textures=list((old/'assets'/MOD/'textures').rglob('*.png'))
    for p in old_textures:assert sha(p)==sha(RES/p.relative_to(old)), ('changed old texture',p)
    tag=load(RES/'data/curios/tags/items/soul_stone.json')
    known={v['id'] for v in tag['values'] if isinstance(v,dict) and not v.get('required',True)}
    lang=[load(RES/f'assets/{MOD}/lang/{l}.json') for l in ['zh_cn','en_us']]
    baseline=ROOT/'art/remaining-school-souls-0.7.5/before-glyph-redraw'
    recipe_names=[];materials={}
    for r in records:
        ident=MOD+':'+r['item'];assert ident in known
        for text in lang:
            assert text['item.'+ident.replace(':','.')]
            assert text[f'tooltip.{MOD}.{r["key"]}']
        image_path=RES/f'assets/{MOD}/textures/item/{r["item"]}.png'
        im=Image.open(image_path).convert('RGBA');assert im.size==(18,18)
        assert set(im.getchannel('A').getdata())=={0,255}
        before=Image.open(baseline/image_path.name).convert('RGBA')
        assert im.tobytes()!=before.tobytes()
        assert all(im.getpixel((x,y))==before.getpixel((x,y)) for y in range(18) for x in range(18)
                   if not(5<=x<13 and 5<=y<13)),('outside redraw',r['item'])
        model=load(RES/f'assets/{MOD}/models/item/{r["item"]}.json')
        assert model['textures']['layer0']==MOD+':item/'+r['item']
        materials[r['item']]={}
        for suffix in ['', '_materials']:
            name=f'data/{MOD}/recipes/{r["item"]}{suffix}.json';recipe_names.append(name)
            recipe=load(RES/name);cs=recipe['conditions']
            assert cs[0]=={'type':'forge:mod_loaded','modid':r['provider']}
            assert cs[1]=={'type':'forge:item_exists','item':ident}
            assert recipe['result']['item']==ident
            for value in recipe['key'].values():
                if 'item' in value:
                    check_item(value['item'])
                    assert {'type':'forge:item_exists','item':value['item']} in cs
                else:
                    leaves=tag_leaves(value['tag']);assert leaves, ('empty focus tag',value['tag'])
                    for item in leaves:check_item(item)
                    assert {'type':'forge:not','value':{'type':'forge:tag_empty','tag':value['tag']}} in cs
                    materials[r['item']][value['tag']]=leaves
    assert len(recipe_names)==30
    # Compare motifs after rotations/reflections, independently of their colors.
    from render_scroll_style_stones import STONES
    def mask(g):return tuple(tuple(c!='.' for c in row) for row in g)
    def variants(g):
        for _ in range(4):
            yield g;yield tuple(tuple(reversed(row)) for row in g)
            g=tuple(zip(*g[::-1]))
    existing=[mask(v['glyph']) for v in STONES.values()]
    new=[]
    for r in records:
        g=mask(r['glyph'])
        assert not any(old in list(variants(g)) for old in existing+new),('duplicate motif',r['key'])
        new.append(g)
    artifact=ROOT/'build/libs/wans_minego_expansion-0.7.5.jar'
    result={'new_stones':15,'new_recipes':30,'old_textures_unchanged':len(old_textures),
            'ingredient_focus_resources':materials,'outside_center_unchanged':True,
            'scope':'Static/source/resource verification; no in-game acceptance.'}
    if '--jar' in sys.argv:
        with zipfile.ZipFile(artifact) as jar:
            assert jar.testzip() is None
            for r in records:
                for prefix in [f'assets/{MOD}/textures/item/',f'assets/{MOD}/models/item/']:
                    name=prefix+r['item']+('.png' if '/textures/' in prefix else '.json')
                    assert jar.read(name)==(RES/name).read_bytes()
            for name in recipe_names:assert jar.read(name)==(RES/name).read_bytes()
            assert 'version="0.7.5"' in jar.read('META-INF/mods.toml').decode()
            assert not any(n.startswith('cn/wanyiwige/minego/validation/') for n in jar.namelist())
            result['jar']={'path':str(artifact),'sha256':sha(artifact),'bytes':artifact.stat().st_size}
    target=ROOT/'audit/20261020-schools/validation.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'PASS: 15 stones, 30 gated recipes, focus/material resources, 18x18 sprites, {len(old_textures)} unchanged old textures; '+('release JAR verified.' if '--jar' in sys.argv else 'source/resources verified.'))

if __name__=='__main__':main()
