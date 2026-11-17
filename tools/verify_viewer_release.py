"""Verify the viewer release preserves gameplay recipes and accepted art."""
import hashlib, json, re, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
new = ROOT/'build/libs/wans_minego_expansion-0.7.4.jar'
old = ROOT/'backups/20261012-before-viewer-integration/wans_minego_expansion-0.7.3.jar'
with zipfile.ZipFile(old) as a, zipfile.ZipFile(new) as b:
    aa = {n for n in a.namelist() if not n.endswith('/')}
    bb = {n for n in b.namelist() if not n.endswith('/')}
    changed = sorted(n for n in aa & bb if a.read(n) != b.read(n))
    added = sorted(bb-aa)
    assert not aa-bb
    assert all(a.read(n) == b.read(n) for n in aa if n.startswith('data/') or '/textures/' in n or '/models/' in n)
    assert not any(n.startswith(('dev/emi/', 'mezz/jei/')) or 'Verification' in n for n in bb)
    expected = {'cn/wanyiwige/minego/compat/'+c+'.class' for c in
                ['SoulJeiPlugin','SoulEmiPlugin','SoulAcquisitionInfo','SoulAcquisitionInfo$Page']}
    assert set(added) == expected
    assert b'mezz/jei/api/JeiPlugin' in b.read('cn/wanyiwige/minego/compat/SoulJeiPlugin.class')
    assert b'dev/emi/emi/api/EmiEntrypoint' in b.read('cn/wanyiwige/minego/compat/SoulEmiPlugin.class')
    resources = [p for p in (ROOT/'src/main/resources').rglob('*') if p.is_file() and p.name != 'mods.toml']
    assert all(b.read(p.relative_to(ROOT/'src/main/resources').as_posix()) == p.read_bytes() for p in resources)
    source = (ROOT/'src/main/java/cn/wanyiwige/minego/compat/SoulAcquisitionInfo.java').read_text()
    keys = set(re.findall(r'"(info\.wans_minego_expansion\.[a-z_]+)"', source))
    keys.discard('info.wans_minego_expansion.proof_')
    keys.update(['info.wans_minego_expansion.proof_explorer','info.wans_minego_expansion.proof_complete'])
    for lang in ['en_us','zh_cn']:
        name = 'assets/wans_minego_expansion/lang/'+lang+'.json'
        before, after = json.loads(a.read(name)), json.loads(b.read(name))
        assert all(after[k] == v for k,v in before.items())
        assert len(set(after)-set(before)) == 9
        assert keys <= set(after)
active = ROOT.parent/'mods/wans_minego_expansion-0.7.1.jar'
assert sha(active) == '2b036aded938cae783acd2040280a024a6b64a483cd94832b0e6f16367aa9ed9'
receipt = {'version':'0.7.4','sha256':sha(new),'size_bytes':new.stat().st_size,
           'changed_entries':changed,'added_entries':added,'source_resource_parity':len(resources),
           'textures_models_recipes_unchanged':True,'optional_viewer_apis_not_bundled':True,
           'build':'BUILD SUCCESSFUL; reobfJar executed','deployed':False,
           'game_ui_verified':False,'active_jar_unchanged':True}
out = ROOT/'audit/20261012-viewer-integration'
out.mkdir(exist_ok=True)
(out/'verification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
