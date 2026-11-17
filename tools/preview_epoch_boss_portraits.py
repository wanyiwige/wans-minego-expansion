"""Four boss trials from verified appearance; native 17px empty-stone view."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from epoch_reference_stone import ReferenceGrid,REFERENCE
from epoch_native_hex import ramp

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'src/main/resources/assets/wans_minego_expansion'
OUT=ROOT/'art/epoch-boss-portrait-trial-20261012'
INDIGO=ramp('171726 292841 48445f 807a99 c8c3dd')
IVORY=ramp('474332 827b60 b4ad85 ddd6b6 f5efd5')
WOOD=ramp('26191c 49302d 744b3b a27155 cca383')
MAROON=ramp('2a171e 59272f 8c3a40 b26361 e39c85')
METAL=ramp('151c20 333f43 637379 a3b4b5 d9e1d9')
GOLD=ramp('49311d 7d571f b5882f dabd64 f6e29b')
COPPER=ramp('35201b 633b2e 925c41 c38b62 edc094')
ORBIT=ramp('1b201f 323933 555e52 858e7d bbc5b2')


class NativeSurface(ReferenceGrid):
    """Author directly on the reference grid, without projecting a prior design."""
    def poly(self,pts,c):
        mask=Image.new('L',(17,17));ImageDraw.Draw(mask).polygon(pts,fill=255)
        self.paint(mask,c)

    def line(self,pts,c,width=1):
        mask=Image.new('L',(17,17));ImageDraw.Draw(mask).line(pts,fill=255,width=width)
        self.paint(mask,c)

    def dot(self,x,y,c):
        mask=Image.new('L',(17,17))
        if 0<=x<17 and 0<=y<17:mask.putpixel((x,y),255)
        self.paint(mask,c)


def render_fangzun():
    # Tall engraved copper stele, crown and curled base from the actual icon.
    g=NativeSurface(COPPER)
    g.poly([(6,2),(9,2),(11,4),(10,11),(12,13),(9,15),(5,14),(3,12),(5,10),(4,5)],COPPER[1])
    g.poly([(6,3),(8,2),(10,4),(9,6),(6,6),(4,4)],COPPER[2])
    g.line([(5,4),(6,3),(8,3),(9,4)],COPPER[4])
    g.line([(5,6),(5,11)],COPPER[3]);g.line([(10,5),(10,11)],COPPER[0])
    g.rect((6,6,9,11),COPPER[2])
    # Broken channels and borders suggest its engraved body at readable scale.
    g.line([(6,6),(8,6),(8,8),(7,8),(7,10)],COPPER[0])
    g.line([(9,7),(9,10),(8,10),(8,11)],COPPER[0])
    g.dot(6,9,COPPER[4]);g.dot(8,5,COPPER[0])
    g.line([(3,11),(3,12),(5,13),(6,12)],COPPER[3])
    g.line([(10,11),(12,12),(11,13),(9,13)],COPPER[2])
    g.poly([(6,12),(9,12),(10,14),(8,15),(5,14)],COPPER[2])
    g.line([(5,13),(7,14),(9,13)],COPPER[4]);g.dot(7,15,COPPER[1])
    return g.finish()


def render_cangyao():
    # Orbital metal ring and crossed arrow-like rods, without a blue U magnet.
    g=NativeSurface(ORBIT)
    g.poly([(6,3),(10,3),(12,6),(12,10),(9,13),(5,12),(3,9),(3,6)],ORBIT[0])
    g.line([(6,3),(10,3),(12,6),(12,10),(9,13),(5,12),(3,9),(3,6),(6,3)],ORBIT[2])
    g.line([(4,5),(6,3),(9,3)],ORBIT[4])
    g.line([(3,8),(5,7),(9,8),(12,10)],ORBIT[1])
    g.line([(4,5),(6,6),(8,8),(10,11)],ORBIT[3])
    g.line([(5,11),(7,9),(9,6),(10,4)],ORBIT[2])
    g.line([(7,4),(7,7),(9,10),(9,12)],ORBIT[1],2)
    g.poly([(7,7),(9,7),(10,9),(8,10),(6,9)],ORBIT[2])
    g.dot(7,7,ORBIT[4]);g.dot(8,8,ORBIT[0]);g.dot(9,9,ORBIT[3])
    g.poly([(4,5),(4,7),(6,7)],ORBIT[3]);g.poly([(9,11),(11,11),(10,13)],ORBIT[2])
    return g.finish()


def render_zixu():
    # The whole body is ivory scroll material; a dark coil wraps its left face.
    g=NativeSurface(IVORY)
    g.poly([(7,2),(11,3),(12,6),(11,13),(7,14),(5,11),(5,5)],IVORY[3])
    g.line([(7,3),(10,4)],IVORY[4]);g.line([(11,5),(10,12)],IVORY[1])
    g.poly([(6,2),(5,4),(4,5),(3,8),(4,11),(6,13),(8,13),(8,12),(6,11),(5,8),(6,5),(7,3)],INDIGO[1])
    g.line([(6,2),(5,4),(4,6),(4,9),(5,11),(7,12)],INDIGO[3])
    for x,y in [(5,3),(4,5),(3,7),(4,9),(5,11),(6,12)]:g.dot(x,y,INDIGO[0])
    g.poly([(6,1),(8,1),(9,2),(7,3),(6,4),(5,3)],INDIGO[2])
    g.line([(6,1),(8,1),(8,2)],INDIGO[3])
    # A few ink marks suggest the model's inscribed parchment, not a central rune.
    g.line([(8,6),(9,7),(8,8)],INDIGO[0]);g.line([(8,10),(10,10)],INDIGO[1])
    g.dot(9,9,INDIGO[1]);g.dot(9,11,INDIGO[0])
    g.line([(11,4),(11,12)],WOOD[1]);g.line([(7,14),(9,14)],GOLD[2])
    g.dot(7,14,GOLD[4]);g.dot(8,15,GOLD[1])
    return g.finish()


def render_zhenyan():
    # Dark wood/red machine body replaces the previous orange molten-rock reading.
    g=NativeSurface(WOOD)
    for x,top in [(8,3),(10,2),(12,3)]:
        g.line([(x,top),(x-1,7)],WOOD[0])
        g.poly([(x,top),(x+2,top),(x+1,top+2),(x,top+2)],MAROON[2])
        g.dot(x,top,MAROON[3])
    g.poly([(4,6),(9,5),(12,7),(11,11),(6,12),(3,10)],MAROON[1])
    g.line([(4,6),(9,5),(11,7)],WOOD[3]);g.line([(6,9),(11,8)],WOOD[2])
    g.line([(5,7),(8,7)],MAROON[3]);g.line([(6,10),(10,9)],WOOD[0])
    # Squat horizontal cannon and its open muzzle.
    g.poly([(2,8),(4,7),(7,8),(7,10),(3,11),(2,10)],METAL[0])
    g.line([(3,8),(6,8)],METAL[3]);g.line([(3,9),(6,9)],METAL[1])
    g.rect((2,8,3,10),WOOD[0]);g.dot(2,8,METAL[2]);g.dot(3,9,METAL[0])
    # Angular grey supports remain visible against the brown body.
    g.line([(7,11),(7,13),(5,14)],METAL[1],2)
    g.line([(11,10),(10,13),(12,13)],METAL[1],2)
    g.dot(7,12,METAL[3]);g.dot(10,12,METAL[2]);g.dot(9,8,GOLD[2])
    return g.finish()


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    # Trials live outside official resources; verify that those resources stay intact.
    before={str(p.relative_to(ASSETS)):sha(p) for p in ASSETS.rglob('*') if p.is_file()}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'native-17px').mkdir(exist_ok=True);(OUT/'preview-1190px').mkdir(exist_ok=True)
    ref=Image.open(REFERENCE).convert('RGBA');font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20)
    small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',16)
    accepted={p.name:sha(p) for p in (OUT/'native-17px').glob('*.png') if p.name in ('epoch_zixu_soul_stone.png','epoch_zhenyan_soul_stone.png')}
    sheet=Image.new('RGBA',(960,1300),(24,26,33,255));draw=ImageDraw.Draw(sheet)
    entries=[]
    for i,(key,name,renderer,url,theme) in enumerate([
        ('fangzun','玄印方尊',render_fangzun,'https://www.mcmod.cn/item/894823.html','棕铜色雕纹柱体、上部冠饰与底部卷曲构件'),
        ('cangyao','苍尧星',render_cangyao,'https://www.mcmod.cn/item/894824.html','灰黑金属环、交错杆件和中央机械轴心'),
        ('zixu','子虚仙君',render_zixu,'https://www.mcmod.cn/item/896500.html','米白卷面、深靛蓝卷曲结构、墨迹和金色末端'),
        ('zhenyan','震焰统帅',render_zhenyan,'https://www.mcmod.cn/item/921687.html','暗红褐机体、横向炮管、灰铁支撑和背部旗列')]):
        filename=f'epoch_{key}_soul_stone.png';im=renderer()
        assert im.size==(17,17)
        assert im.getchannel('A').tobytes()==ref.getchannel('A').tobytes()
        assert set(im.getchannel('A').getdata())=={0,255}
        assert im.tobytes()==renderer().tobytes()
        im.save(OUT/'native-17px'/filename)
        preview=im.resize((1190,1190),Image.Resampling.NEAREST)
        for y in range(17):
            for x in range(17):
                assert preview.crop((x*70,y*70,(x+1)*70,(y+1)*70)).getcolors(2)==[(4900,im.getpixel((x,y)))]
        preview.save(OUT/'preview-1190px'/filename)
        old=Image.open(ASSETS/'textures/item'/filename).convert('RGBA')
        for j,(pic,label) in enumerate([(ref,'本体空白魂石'),(old,'目前的源码贴图'),(im,'参照 Boss 形象的试绘')]):
            x=j*320+41;y=i*325+22
            sheet.alpha_composite(pic.resize((238,238),Image.Resampling.NEAREST),(x,y))
            draw.text((j*320+160,y+249),label,font=small,fill='white',anchor='mt')
        draw.text((480,i*325+302),name,font=font,fill=(245,211,150),anchor='mt')
        entries.append({'id':filename[:-4],'name':name,'source_url':url,'theme':theme,'native_size':[17,17],'reference_alpha_exact':True,'same_grid':True,'sha256':sha(OUT/'native-17px'/filename)})
    assert before=={str(p.relative_to(ASSETS)):sha(p) for p in ASSETS.rglob('*') if p.is_file()}
    assert accepted=={name:sha(OUT/'native-17px'/name) for name in accepted},'Previously accepted trials changed'
    sheet.save(OUT/'before-after.png')
    (OUT/'manifest.json').write_text(json.dumps({'status':'trial only','reference':str(REFERENCE),'official_asset_files_unchanged':len(before),'previously_accepted_two_unchanged':True,'local_appearance_reference':'local-reference/; named spell icons from spirit_mediumship_spell and entity textures from splendour_ablaze_epoch','built':False,'deployed':False,'items':entries},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=['# 棠煌纪元四位 Boss 魂石试绘','', '子虚仙君与震焰统帅采用此前核对的 MC 百科模型形象；玄印方尊与苍尧星补充本地降灵法术的命名像素图标及原模组实体材质作为完整形象参考。四张均是独立试稿，未替换正式源码资源。','', '| 对象 | 主题 | 实体条目 |','| --- | --- | --- |']
    rows += [f"| {r['name']} | {r['theme']} | [MC 百科]({r['source_url']}) |" for r in entries]
    rows += ['', '四张均在本体空白魂石的 17×17 网格上直接绘制，保留其透明轮廓、原视角与明暗切面。内外像素尺度一致，预览为整数倍最近邻放大。', '没有使用高清概念图缩小，也没有将完整 Boss 图片缩成中央贴片。', '', '校验通过：原图透明轮廓逐像素一致、透明值 0/255、原生输出可复现、70 倍预览像素块一致、所有正式资源保持原样；此前认可的子虚与震焰两张试稿哈希保持一致。', '原尺寸可读性与游戏内视觉效果尚未在游戏中确认；没有构建或部署。']
    (OUT/'report.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    print(f'PASS: four native trials; accepted two unchanged; exact reference alpha; uniform pixel scale; all {len(before)} official resource files unchanged.')


if __name__=='__main__':main()
