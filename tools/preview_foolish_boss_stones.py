"""Native-grid Foolish boss trials based on the installed textures and models."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
from preview_epoch_boss_portraits import NativeSurface
from epoch_reference_stone import REFERENCE
from epoch_native_hex import ramp

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'src/main/resources/assets/wans_minego_expansion'
OUT=ROOT/'art/foolish-reference-redraw-20261012'
RED=ramp('3c1016 791723 b73027 ec652f ffd783')
BLUE=ramp('24233f 4a4881 8a8dd0 bbc6f0 e8efff')
GREEN=ramp('162914 28441e 486c28 84a345 c9d690')
TEAL=ramp('0a292b 125357 268b86 70c8ba d0fff1')
VIOLET=ramp('1e0d37 3e1768 7131a8 b477e2 e4c1ff')
GRAY=ramp('202923 384439 667363 a5b09a dde1bd')
TOXIC=ramp('20320a 4e6b12 8fa826 c5e351 f3ffad')
SCARLET=ramp('3b0b17 80101e c62435 f06168 ffb5b1')
PINK=ramp('391132 75235d bb4389 e983ba ffcbea')
FLESH=ramp('241417 4b2428 77383b a96b60 e1ada0')
BONE=ramp('41372c 776752 b0a48a dacdb0 fff2d3')
GOLD=ramp('503019 94601d c99735 f0d16e fff7c2')


def pyre():
    g=NativeSurface(RED)
    # Red-hot lion-like head and pale jaw are integrated into the fiery body.
    g.poly([(4,4),(7,3),(11,5),(12,9),(9,12),(5,11),(3,8)],RED[1])
    g.line([(4,5),(5,3),(7,4),(9,3),(11,5)],RED[3],2)
    g.dot(5,6,GOLD[4]);g.dot(9,6,GOLD[3])
    g.line([(5,8),(8,9),(10,8)],RED[0],2)
    g.line([(5,9),(7,11),(9,10)],BONE[3]);g.dot(5,9,BONE[4])
    g.line([(3,11),(5,13),(7,12),(9,14),(11,11)],RED[2],2)
    g.dot(4,12,GOLD[3]);g.dot(8,13,GOLD[4])
    return g.finish()


def timewelder():
    g=NativeSurface(BLUE)
    g.poly([(4,4),(7,3),(9,4),(11,7),(10,12),(6,13),(3,10)],BLUE[2])
    g.poly([(4,4),(6,3),(6,6),(4,8),(3,6)],VIOLET[2])
    g.poly([(10,4),(12,6),(11,10),(9,8)],VIOLET[1])
    g.line([(4,5),(8,4),(11,6)],GOLD[3])
    # The source model includes Clock and sand bones: an embedded time mechanism.
    g.poly([(6,7),(9,6),(11,8),(10,11),(7,12),(5,10)],GOLD[1])
    g.poly([(7,7),(9,7),(10,9),(9,11),(7,11),(6,9)],BLUE[0])
    g.line([(8,8),(8,9),(9,10)],GOLD[4]);g.dot(6,9,GOLD[3])
    g.line([(4,12),(6,13),(9,13)],BLUE[3]);g.dot(8,14,GOLD[3])
    return g.finish()


def thrasher():
    g=NativeSurface(GREEN)
    g.poly([(3,4),(6,3),(6,6),(4,8)],TEAL[2])
    g.line([(3,5),(5,5),(4,7)],TEAL[3])
    g.poly([(6,4),(10,4),(12,7),(11,11),(8,13),(4,10)],GREEN[1])
    g.dot(7,6,TEAL[4]);g.dot(10,6,TEAL[2])
    g.line([(4,8),(7,9),(10,8)],GREEN[0],2)
    for x,y in [(5,8),(7,9),(9,8)]:g.dot(x,y,BONE[3])
    g.line([(5,10),(8,12),(10,11)],GREEN[3])
    g.line([(3,11),(4,13),(6,13)],GRAY[2]);g.dot(5,13,GRAY[4])
    return g.finish()


def sacilic():
    g=NativeSurface(VIOLET)
    for pts,c in [([(5,3),(6,6),(3,8),(3,5)],VIOLET[3]),([(8,2),(10,5),(8,8),(6,6)],VIOLET[4]),([(11,4),(12,8),(9,10),(9,6)],VIOLET[2])]:g.poly(pts,c)
    g.poly([(5,8),(9,7),(11,10),(9,13),(5,12),(3,10)],VIOLET[1])
    g.line([(4,9),(6,10),(9,10)],VIOLET[0],2)
    g.dot(5,9,VIOLET[4]);g.dot(7,10,VIOLET[3]);g.dot(9,10,TEAL[3])
    g.line([(3,6),(4,7)],TEAL[2]);g.dot(10,6,TEAL[4]);g.line([(6,12),(8,14)],VIOLET[3])
    return g.finish()


def varmint():
    g=NativeSurface(GRAY)
    g.poly([(3,4),(5,3),(7,5),(10,4),(12,6),(10,11),(6,12),(3,9)],GRAY[1])
    g.poly([(3,4),(5,4),(5,6),(3,6)],BONE[1]);g.poly([(9,4),(11,4),(11,6)],GRAY[3])
    g.dot(5,7,TOXIC[4]);g.dot(9,7,TOXIC[3])
    g.poly([(5,9),(7,8),(9,10),(7,12),(4,11)],GRAY[3]);g.dot(6,9,GRAY[0])
    g.line([(5,11),(7,12),(9,11)],BONE[2]);g.dot(6,11,BONE[4])
    g.line([(3,12),(5,13),(9,14),(11,12)],TOXIC[2]);g.dot(10,13,TOXIC[3])
    return g.finish()


def thunderbird():
    g=NativeSurface(TEAL)
    # Cyan feathered face and eye lightning, not a yellow lightning-logo disk.
    g.poly([(4,3),(6,5),(5,8),(3,7)],TEAL[2])
    g.poly([(9,3),(11,4),(12,7),(9,8)],TEAL[1])
    g.line([(3,4),(5,6),(4,7)],TEAL[4]);g.line([(10,4),(11,6)],TEAL[3])
    g.poly([(6,5),(9,5),(10,8),(8,10),(5,9)],TEAL[0])
    g.dot(6,6,TEAL[4]);g.dot(9,6,GOLD[4])
    g.poly([(7,8),(10,9),(8,11),(6,10)],GOLD[2])
    g.line([(4,10),(6,12),(5,14)],TEAL[3]);g.line([(9,11),(11,12),(10,14)],TEAL[2])
    g.dot(5,12,GOLD[3]);g.dot(10,12,GOLD[3])
    return g.finish()


def queen():
    g=NativeSurface(SCARLET)
    # Red chitin plates, dark mandibles and lateral limbs from the source material.
    g.poly([(6,3),(9,3),(11,5),(10,8),(7,9),(4,7),(4,5)],SCARLET[2])
    g.line([(5,4),(8,4),(10,5)],SCARLET[4])
    g.line([(5,3),(4,2)],SCARLET[1]);g.line([(10,3),(11,2)],SCARLET[1])
    g.dot(5,6,SCARLET[0]);g.dot(9,6,SCARLET[0])
    g.poly([(5,8),(7,9),(6,11),(4,10)],SCARLET[0])
    g.poly([(9,8),(10,10),(8,11),(7,9)],SCARLET[1])
    g.line([(3,8),(2,10),(4,12)],SCARLET[2]);g.line([(11,8),(12,10),(11,12)],SCARLET[2])
    g.poly([(6,11),(9,11),(10,14),(7,15),(5,13)],SCARLET[2]);g.line([(6,12),(8,12)],SCARLET[3])
    return g.finish()


def terrorflora():
    g=NativeSurface(GREEN)
    for pts,c in [([(5,3),(8,4),(7,7),(4,6)],PINK[3]),([(9,4),(12,6),(10,8),(8,7)],PINK[2]),([(4,7),(6,8),(5,11),(2,9)],PINK[2]),([(8,9),(11,9),(10,12),(7,11)],PINK[1])]:g.poly(pts,c)
    g.poly([(5,6),(8,5),(10,7),(9,10),(6,10),(4,8)],GREEN[0])
    g.line([(5,7),(8,7),(9,8)],BONE[2]);g.line([(6,9),(7,11)],RED[3])
    g.line([(6,11),(7,14)],GREEN[3],2);g.poly([(3,12),(5,11),(6,13),(4,14)],GREEN[3])
    g.dot(7,5,PINK[4]);g.dot(3,7,PINK[4])
    return g.finish()


def wendigrudge():
    g=NativeSurface(FLESH)
    g.poly([(4,3),(7,4),(6,8),(3,9)],FLESH[0]);g.poly([(10,4),(12,6),(11,10),(8,8)],FLESH[1])
    g.poly([(5,5),(9,5),(11,7),(10,10),(7,12),(4,9)],BONE[1])
    g.line([(5,5),(8,5)],BONE[3]);g.dot(5,7,FLESH[0]);g.dot(9,7,FLESH[0])
    g.line([(5,9),(7,10),(9,9)],FLESH[0],2)
    for x in [5,7,9]:g.dot(x,9,BONE[3])
    g.line([(6,11),(5,13),(7,14),(10,12)],BONE[2]);g.dot(6,12,BONE[4])
    g.line([(3,10),(3,12)],FLESH[2]);g.line([(11,10),(12,12)],FLESH[2])
    return g.finish()


def astralis():
    g=NativeSurface(PINK)
    g.poly([(4,4),(7,3),(9,6),(7,9),(3,8)],VIOLET[2])
    g.poly([(9,5),(12,6),(11,11),(8,12),(7,9)],GOLD[1])
    g.line([(5,3),(7,5),(8,8),(10,11)],GOLD[3],2)
    g.line([(3,10),(5,8),(8,8),(10,5),(11,3)],GOLD[4])
    g.poly([(6,7),(8,6),(10,8),(8,10),(6,9)],GOLD[2]);g.dot(7,7,GOLD[4])
    g.line([(4,12),(6,13),(7,11)],PINK[4]);g.line([(10,11),(11,13)],VIOLET[3])
    return g.finish()


def composite(final=False):
    g=NativeSurface(GOLD if final else BLUE)
    # Multiple boss materials interlock around the Astralis star core.
    g.poly([(3,4),(7,3),(7,7),(3,8)],RED[2] if final else BLUE[2])
    g.poly([(8,3),(11,5),(11,8),(8,7)],TEAL[2])
    g.poly([(3,9),(7,8),(7,13),(5,14)],VIOLET[2])
    g.poly([(8,8),(12,9),(10,13),(8,14)],SCARLET[2] if final else GREEN[2])
    g.line([(4,5),(6,6)],BONE[2]);g.line([(9,5),(10,7)],TEAL[4])
    g.line([(5,10),(6,12)],VIOLET[4]);g.line([(9,10),(10,12)],GOLD[2])
    g.poly([(7,5),(8,7),(10,8),(8,9),(7,12),(6,9),(4,8),(6,7)],GOLD[3])
    g.dot(7,8,GOLD[4]);g.dot(7,6,PINK[3])
    return g.finish()


ENTRIES=[
 ('foolish_pyre_soul_stone',pyre,'赤红熔躯、狮口与浅骨腭'),
 ('foolish_timewelder_soul_stone',timewelder,'浅蓝紫躯体与内嵌金色时钟'),
 ('foolish_thrasher_soul_stone',thrasher,'绿皮鱼兽、青色鳍与钩状下颌'),
 ('foolish_sacilic_abomination_soul_stone',sacilic,'深紫晶体、裂口与青色萦光'),
 ('foolish_varmint_king_soul_stone',varmint,'灰绿鼠兽、浅骨口部与毒绿侵染'),
 ('foolish_thunderbird_soul_stone',thunderbird,'青黑羽面、金喙与眼部电光'),
 ('foolish_scarlant_queen_soul_stone',queen,'猩红甲壳、暗色颚与侧肢'),
 ('foolish_terrorflora_soul_stone',terrorflora,'绿叶本体、粉红花瓣与橙色口部'),
 ('foolish_wendigrudge_soul_stone',wendigrudge,'暗红褐肉躯、骨色颅腭与翼侧'),
 ('foolish_astralis_soul_stone',astralis,'紫粉躯体、金色星芒与白金刃'),
 ('soul_of_stellar_hollow',lambda:composite(False),'多种 Boss 材质环绕星刃核心'),
 ('soul_of_foolish',lambda:composite(True),'熔红、青羽、紫晶与猩甲合铸'),
]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    before={str(p.relative_to(ASSETS)):sha(p) for p in ASSETS.rglob('*') if p.is_file()}
    active=ROOT.parent/'mods/wans_minego_expansion-0.7.1.jar';active_hash=sha(active)
    lang=json.loads((ASSETS/'lang/zh_cn.json').read_text(encoding='utf-8'))
    ref=Image.open(REFERENCE).convert('RGBA');f=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',13)
    overview=Image.new('RGBA',(1200,960),(24,26,33,255));d=ImageDraw.Draw(overview)
    pairs=Image.new('RGBA',(1200,6*260),(24,26,33,255));pd=ImageDraw.Draw(pairs)
    (OUT/'native-17px').mkdir(exist_ok=True);(OUT/'preview-1190px').mkdir(exist_ok=True)
    records=[];topologies=[]
    for i,(stem,renderer,theme) in enumerate(ENTRIES):
        name=lang['item.wans_minego_expansion.'+stem];im=renderer();assert im.size==(17,17)
        assert im.getchannel('A').tobytes()==ref.getchannel('A').tobytes()
        assert set(im.getchannel('A').getdata())=={0,255};assert renderer().tobytes()==im.tobytes()
        p=OUT/'native-17px'/(stem+'.png');im.save(p)
        large=im.resize((1190,1190),Image.Resampling.NEAREST)
        for y in range(17):
            for x in range(17):assert large.crop((x*70,y*70,(x+1)*70,(y+1)*70)).getcolors(2)==[(4900,im.getpixel((x,y)))]
        large.save(OUT/'preview-1190px'/p.name)
        x=i%4*300;y=i//4*320;overview.alpha_composite(im.resize((238,238),Image.Resampling.NEAREST),(x+31,y+6));d.text((x+150,y+254),f'{i+1:02d} {name}',font=f,fill='white',anchor='mt')
        caption=theme
        while d.textlength(caption,font=small)>290:caption=caption[:-1]
        d.text((x+150,y+286),caption,font=small,fill=(185,203,215),anchor='mt')
        old=Image.open(ASSETS/'textures/item'/p.name).convert('RGBA');x=i%2*600;y=i//2*260
        for pic,left,label in [(old,x+80,'原贴图'),(im,x+360,'新试稿')]:
            pairs.alpha_composite(pic.resize((pic.width*10,pic.height*10),Image.Resampling.NEAREST),(left,y+10));pd.text((left+85,y+197),label,font=small,fill='white',anchor='mt')
        pd.text((x+300,y+228),name,font=f,fill=(245,214,151),anchor='mt')
        labels={};top=[]
        for pix in im.getdata():
            if pix not in labels:labels[pix]=len(labels)
            top.append(labels[pix])
        topologies.append(tuple(top));records.append({'id':stem,'name':name,'theme':theme,'sha256':sha(p),'size':[17,17],'alpha_exact':True,'pixel_grid_verified':True})
    assert len(set(topologies))==12,'Duplicate pigment topology'
    assert before=={str(p.relative_to(ASSETS)):sha(p) for p in ASSETS.rglob('*') if p.is_file()}
    assert sha(active)==active_hash
    overview.save(OUT/'overview-12.png');pairs.save(OUT/'before-after-12.png')
    (OUT/'manifest.json').write_text(json.dumps({'status':'trial only','reference':str(REFERENCE),'reference_jar':'mods/foolish-1.3.0 patched.jar','official_assets_unchanged':len(before),'active_jar_unchanged':True,'built':False,'deployed':False,'items':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=['# Foolish Boss 魂石重绘试稿','', '范围：10 张 Boss 魂石与 2 张复合魂石。材料、群系魂石本轮尚未重绘。','', '核对当前 Foolish 1.3.0 patched.jar 中实体的默认材质和实际模型结构；材质索引见 reference-inventory.json。配色和结构来自实体材质及模型骨骼，不把名称作为形象证据。','', '全部沿用本体空白魂石的 17×17 网格、透明轮廓、原视角和明暗切面。构图在原生网格直接绘制，没有把大图缩成中央贴片。','', '| 魂石 | 本轮设计 |','| --- | --- |']
    rows += [f"| {r['name']} | {r['theme']} |" for r in records]
    rows += ['', '校验通过：12 张原生图、轮廓逐像素一致、0/255 透明、重生成一致、70 倍最近邻像素块一致、无仅换色的相同像素布局；全部正式资源及已安装 0.7.1 JAR 不变。','', '本轮只生成试稿与对照，没有构建或部署。图中造型是适合小尺寸的特征提取，不是对完整 Boss 模型的逐像素复刻；游戏内视觉与原尺寸可读性尚未测试。']
    (OUT/'report.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    print(f'PASS: 12 native trials; exact empty-stone alpha; uniform grid; {len(before)} official assets and active JAR unchanged.')


if __name__=='__main__':main()
