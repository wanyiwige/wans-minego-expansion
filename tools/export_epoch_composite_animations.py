"""Recipe-derived 4/4/11-frame Epoch soul-stone animations; no recipe edits."""
from pathlib import Path
import json,hashlib
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'src/main/resources/assets/wans_minego_expansion'
TEXTURES=ASSETS/'textures/item'
RECIPES=ROOT/'src/main/resources/data/wans_minego_expansion/recipes'
OUT=ROOT/'art/epoch-whole-stone-redraw-20261012/accepted-animations'
EXPECTED={'epoch_celesterral_soul_stone':4,'epoch_four_sovereigns_soul_stone':4,'epoch_epoch_soul_stone':11}


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    before={p.relative_to(ASSETS).as_posix():sha(p) for p in ASSETS.rglob('*') if p.is_file()}
    ref=Image.open(ROOT/'art/epoch-whole-stone-redraw-20261012/empty-soul-stone-native.png').convert('RGBA')
    OUT.mkdir(parents=True,exist_ok=True);ignored=set()
    def leaves(stem,path=()):
        assert stem not in path,('recipe cycle',stem,path)
        if stem not in EXPECTED:return [stem]
        recipe=json.loads((RECIPES/(stem+'.json')).read_text(encoding='utf-8'));result=[]
        for v in recipe['ingredients']:
            item=v.get('item','');ns,_,child=item.partition(':')
            if ns=='wans_minego_expansion' and child.startswith('epoch_') and child.endswith('_soul_stone'):result.extend(leaves(child,path+(stem,)))
            else:ignored.add(item)
        return list(dict.fromkeys(result))
    records=[]
    for stem,count in EXPECTED.items():
        children=leaves(stem);assert len(children)==count
        frames=[Image.open(TEXTURES/(key+'.png')).convert('RGBA') for key in children]
        assert all(im.size==(17,17) and im.getchannel('A').tobytes()==ref.getchannel('A').tobytes() for im in frames)
        strip=Image.new('RGBA',(17,17*count))
        for i,frame in enumerate(frames):strip.paste(frame,(0,17*i))
        p=TEXTURES/(stem+'.png');strip.save(p);strip.save(OUT/p.name)
        meta={'animation':{'frametime':20,'interpolate':True}}
        for m in [p.with_suffix('.png.mcmeta'),OUT/(stem+'.png.mcmeta')]:m.write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
        gif=[]
        for i,im in enumerate(frames):
            for tick in range(20):
                canvas=Image.new('RGBA',(17,17),(24,26,33,255));canvas.alpha_composite(Image.blend(im,frames[(i+1)%count],tick/20));gif.append(canvas.convert('RGB').resize((204,204),Image.Resampling.NEAREST))
        gif[0].save(OUT/(stem+'.gif'),save_all=True,append_images=gif[1:],duration=50,loop=0,disposal=2,optimize=False)
        actual=Image.open(p).convert('RGBA')
        for i,frame in enumerate(frames):assert actual.crop((0,17*i,17,17*(i+1))).tobytes()==frame.tobytes()
        model=json.loads((ASSETS/'models/item'/(stem+'.json')).read_text(encoding='utf-8'));assert model=={'parent':'minecraft:item/generated','textures':{'layer0':'wans_minego_expansion:item/'+stem}}
        records.append({'id':stem,'frames':children,'frame_count':count,'frame_size':[17,17],'strip_size':[17,17*count],'frametime':20,'interpolate':True,'sha256':sha(p),'frames_match_components':True})
    after={p.relative_to(ASSETS).as_posix():sha(p) for p in ASSETS.rglob('*') if p.is_file()}
    allowed={'textures/item/'+stem+s for stem in EXPECTED for s in ['.png','.png.mcmeta']}
    changed={n for n,h in after.items() if before.get(n)!=h};assert changed<=allowed;assert set(before)<=set(after)
    receipt={'animations':records,'non_stone_ingredients_excluded_from_animation':sorted(ignored),'source_only':True,'deployed':False,'game_visual_verified':False}
    (OUT/'manifest.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'report.md').write_text('# 棠煌纪元复合魂石动画\n\n玄黄魂石 4 帧、四尊之魂 4 帧、棠煌之魂递归展开 11 帧。全部来自现有配方中的下属魂石，保持 17×17 原视角，20 tick/帧，开启插值。\n\n玄黄锭、先贤残篇、全境凭证等非魂石材料继续保留在配方中，不作为动画帧。未改配方、玩法代码或安装 JAR。GIF 仅作插值预览，游戏读取纵向 PNG + 同名 mcmeta。\n',encoding='utf-8')
    print('PASS: Epoch 4/4/11 frames; exact component pixels; other assets unchanged.')
    return records


if __name__=='__main__':main()
