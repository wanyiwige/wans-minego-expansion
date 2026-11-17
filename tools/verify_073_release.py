import hashlib, io, json, zipfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
old = ROOT / 'backups/20261012-213344-before-epoch-composite-animation/wans_minego_expansion-0.7.2.jar'
new = ROOT / 'build/libs/wans_minego_expansion-0.7.3.jar'
active = ROOT.parent / 'mods/wans_minego_expansion-0.7.1.jar'
with zipfile.ZipFile(old) as a, zipfile.ZipFile(new) as b:
    aa, bb = set(a.namelist()), set(b.namelist())
    changed = sorted(n for n in aa & bb if a.read(n) != b.read(n))
    added = sorted(bb-aa)
    assert not aa-bb
    texture = 'assets/wans_minego_expansion/textures/item/'
    ids = ['epoch_celesterral_soul_stone', 'epoch_four_sovereigns_soul_stone', 'epoch_epoch_soul_stone']
    assert set(changed) == {'META-INF/mods.toml', *(texture+x+'.png' for x in ids)}
    assert set(added) == {texture+x+'.png.mcmeta' for x in ids}
    classes = [n for n in aa if n.endswith('.class')]
    assert all(a.read(n) == b.read(n) for n in classes)
    resources = list((ROOT/'src/main/resources').rglob('*'))
    resources = [p for p in resources if p.is_file() and p.name != 'mods.toml']
    assert all(b.read(p.relative_to(ROOT/'src/main/resources').as_posix()) == p.read_bytes() for p in resources)
    art = ROOT/'art/epoch-whole-stone-redraw-20261012/accepted-animations'
    manifest = json.loads((art/'manifest.json').read_text(encoding='utf-8'))
    for entry in manifest['animations']:
        sprite = Image.open(io.BytesIO(b.read(texture+entry['id']+'.png'))).convert('RGBA')
        assert sprite.size == (17,17*len(entry['frames']))
        for i, frame in enumerate(entry['frames']):
            component = Image.open(io.BytesIO(b.read(texture+frame+'.png'))).convert('RGBA')
            assert sprite.crop((0,i*17,17,(i+1)*17)).tobytes() == component.tobytes()
        assert json.loads(b.read(texture+entry['id']+'.png.mcmeta')) == {'animation':{'frametime':20,'interpolate':True}}
        gif = Image.open(art/(entry['id']+'.gif'))
        duration = 0
        for i in range(gif.n_frames):
            gif.seek(i); duration += gif.info['duration']
        assert duration == len(entry['frames'])*1000
    manifest.update(source_only=False, built=True, version='0.7.3', jar_sha256=sha(new), deployed=False)
    (art/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert sha(active) == '2b036aded938cae783acd2040280a024a6b64a483cd94832b0e6f16367aa9ed9'
receipt = {'version':'0.7.3','jar_sha256':sha(new),'changed_entries':changed,'added_entries':added,'unchanged_classes':len(classes),'source_resource_parity':len(resources),'active_jar_unchanged':True,'deployed':False,'game_visual_verified':False}
out = ROOT/'audit/20261012-epoch-animation-release'
out.mkdir(parents=True,exist_ok=True)
(out/'verification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
