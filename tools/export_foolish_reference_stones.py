"""Install the 31 approved Foolish designs and recipe-derived PNG animations."""
from pathlib import Path
import json,hashlib
from PIL import Image
from preview_foolish_boss_stones import ROOT,ASSETS,OUT,ENTRIES,REFERENCE
from foolish_exploration_stone_designs import extra_entries

MOD='wans_minego_expansion'
TEXTURES=ASSETS/'textures/item'
RECIPES=ROOT/'src/main/resources/data'/MOD/'recipes'
ANIMATIONS=OUT/'accepted-animations'
COMPOSITES=('soul_of_stellar_hollow','soul_of_foolish','soul_of_otherworld')


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    names={stem for stem,_,_ in ENTRIES+extra_entries()}
    assert len(names)==31
    approved=json.loads((OUT/'manifest-31.json').read_text(encoding='utf-8'))
    hashes={r['id']:r['sha256'] for r in approved['items']}
    assert set(hashes)==names
    before={p.relative_to(ASSETS).as_posix():sha(p) for p in ASSETS.rglob('*') if p.is_file()}
    active=ROOT.parent/'mods/wans_minego_expansion-0.7.1.jar';active_hash=sha(active)
    ref=Image.open(REFERENCE).convert('RGBA')
    for stem in sorted(names):
        p=OUT/'native-17px'/(stem+'.png');assert sha(p)==hashes[stem]
        im=Image.open(p).convert('RGBA');assert im.size==(17,17)
        assert im.getchannel('A').tobytes()==ref.getchannel('A').tobytes()
        if stem not in COMPOSITES:(TEXTURES/p.name).write_bytes(p.read_bytes())
    # Only recurse through our registered soul stones, omitting non-stone catalysts.
    # This changes animation artwork only, never crafting requirements.
    ignored=set()
    def leaves(stem,path=()):
        assert stem not in path,('recipe cycle',path,stem)
        if stem not in COMPOSITES:return [stem]
        recipe=json.loads((RECIPES/(stem+'.json')).read_text(encoding='utf-8'))
        result=[]
        for ingredient in recipe['ingredients']:
            item=ingredient.get('item','');namespace,_,child=item.partition(':')
            if namespace==MOD and child in names:result.extend(leaves(child,path+(stem,)))
            else:ignored.add(item)
        return list(dict.fromkeys(result))
    ANIMATIONS.mkdir(parents=True,exist_ok=True)
    expected={'soul_of_stellar_hollow':9,'soul_of_foolish':10,'soul_of_otherworld':8}
    records=[]
    for stem in COMPOSITES:
        children=leaves(stem);assert len(children)==expected[stem]
        frames=[Image.open(TEXTURES/(c+'.png')).convert('RGBA') for c in children]
        assert all(im.size==(17,17) and im.getchannel('A').tobytes()==ref.getchannel('A').tobytes() for im in frames)
        strip=Image.new('RGBA',(17,17*len(frames)))
        for i,im in enumerate(frames):strip.paste(im,(0,i*17))
        p=TEXTURES/(stem+'.png');strip.save(p)
        meta={'animation':{'frametime':20,'interpolate':True}}
        p.with_suffix('.png.mcmeta').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
        strip.save(ANIMATIONS/(stem+'.png'))
        (ANIMATIONS/(stem+'.png.mcmeta')).write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
        # GIF is an inspection preview. The shipped animation is PNG + mcmeta.
        preview=[]
        for i,im in enumerate(frames):
            following=frames[(i+1)%len(frames)]
            for tick in range(20):
                blend=Image.blend(im,following,tick/20)
                canvas=Image.new('RGBA',(17,17),(24,26,33,255));canvas.alpha_composite(blend)
                canvas=canvas.convert('RGB').resize((204,204),Image.Resampling.NEAREST)
                preview.append(canvas)
        preview[0].save(ANIMATIONS/(stem+'.gif'),save_all=True,append_images=preview[1:],duration=50,loop=0,disposal=2,optimize=False)
        check=Image.open(p).convert('RGBA');assert check.size==(17,17*expected[stem])
        for i,frame in enumerate(frames):assert check.crop((0,i*17,17,(i+1)*17)).tobytes()==frame.tobytes()
        model=json.loads((ASSETS/'models/item'/(stem+'.json')).read_text(encoding='utf-8'))
        assert model=={'parent':'minecraft:item/generated','textures':{'layer0':MOD+':item/'+stem}}
        records.append({'id':stem,'frames':children,'frame_count':len(children),'frame_size':[17,17],'strip_size':list(check.size),'ticks_per_frame':20,'interpolate':True,'loop_seconds':len(children),'png_sha256':sha(p),'frame_pixels_exact':True})
    after={p.relative_to(ASSETS).as_posix():sha(p) for p in ASSETS.rglob('*') if p.is_file()}
    allowed={'textures/item/'+stem+'.png' for stem in names}|{'textures/item/'+stem+'.png.mcmeta' for stem in COMPOSITES}
    changes={n for n,h in after.items() if before.get(n)!=h}
    assert changes<=allowed,changes-allowed
    assert len([n for n in changes if n.endswith('.png')])<=31
    assert all(n in after for n in before)
    assert sha(active)==active_hash
    receipt={'status':'accepted source','static_stones':28,'animated_composites':3,'accepted_stones':31,'source_png_changes':31,'new_mcmeta':3,'active_jar_unchanged':True,'non_stone_ingredients_excluded_from_animation':sorted(ignored),'animations':records,'built':False,'deployed':False,'game_visual_verified':False}
    (ANIMATIONS/'manifest.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Foolish 魂石正式贴图与复合动画','', '已将 31 张认可试稿接入源码：28 张单帧魂石，3 张复合动画魂石。没有修改配方、属性、实体逻辑或已安装 JAR。','', '| 复合魂石 | 帧数 | 来源 | 循环周期 |','| --- | --- | --- | --- |','| 星渊之魂 | 9 | 配方中的 9 张 Boss 魂石 | 9 秒 |','| Foolish之魂 | 10 | 星渊之魂递归展开的 9 张，加阿斯塔瑞斯魂石 | 10 秒 |','| 异境之魂 | 8 | 配方中的 8 张群系魂石 | 8 秒 |','', '每帧为 17×17，保持同一空白魂石的视角和透明轮廓。每帧 20 tick，interpolate:true，顺序按现有配方展开并去重。Foolish之魂的恒星催化剂保留在原配方中，但它不是魂石，不作为动画帧。','', '游戏资源为纵向 PNG + 同名 .png.mcmeta；GIF 只是 20 帧每秒的插值演示，不打入正式 JAR。实际游戏观感仍需客户端确认。','', '静态源码 PNG 与认可试稿逐字节一致；复合 PNG 的每帧与对应单体魂石逐像素一致；模型仍为 minecraft:item/generated。正式生成入口：tools/export_foolish_reference_stones.py。']
    (ANIMATIONS/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('PASS: 31 accepted stones; 28 static + 3 animated; exact 9/10/8 recipe-derived frames; unrelated assets and installed JAR unchanged.')


if __name__=='__main__':main()
