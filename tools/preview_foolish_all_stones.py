"""Export all 31 Foolish trials without changing official source or deployment."""
import json
from PIL import Image,ImageDraw,ImageFont
from preview_foolish_boss_stones import ROOT,ASSETS,OUT,ENTRIES,sha,REFERENCE
from foolish_exploration_stone_designs import extra_entries


def main():
    entries=ENTRIES+extra_entries();assert len(entries)==31
    before={str(p.relative_to(ASSETS)):sha(p) for p in ASSETS.rglob('*') if p.is_file()}
    active=ROOT.parent/'mods/wans_minego_expansion-0.7.1.jar';active_hash=sha(active)
    prior={stem:sha(OUT/'native-17px'/(stem+'.png')) for stem,_,_ in ENTRIES}
    lang=json.loads((ASSETS/'lang/zh_cn.json').read_text(encoding='utf-8'))
    ref=Image.open(REFERENCE).convert('RGBA');images=[];records=[];layouts=[]
    for stem,render,theme in entries:
        im=render();assert im.size==(17,17)
        assert im.getchannel('A').tobytes()==ref.getchannel('A').tobytes()
        assert set(im.getchannel('A').getdata())=={0,255};assert render().tobytes()==im.tobytes()
        p=OUT/'native-17px'/(stem+'.png');im.save(p)
        large=im.resize((1190,1190),Image.Resampling.NEAREST)
        for y in range(17):
            for x in range(17):assert large.crop((x*70,y*70,(x+1)*70,(y+1)*70)).getcolors(2)==[(4900,im.getpixel((x,y)))]
        large.save(OUT/'preview-1190px'/p.name)
        colors={};layout=[]
        for pixel in im.getdata():
            if pixel not in colors:colors[pixel]=len(colors)
            layout.append(colors[pixel])
        layouts.append(tuple(layout));images.append(im)
        records.append({'id':stem,'name':lang['item.wans_minego_expansion.'+stem],'theme':theme,'size':[17,17],'alpha_exact':True,'pixel_grid_verified':True,'sha256':sha(p)})
    assert len(set(layouts))==31
    assert prior=={stem:sha(OUT/'native-17px'/(stem+'.png')) for stem in prior}
    assert before=={str(p.relative_to(ASSETS)):sha(p) for p in ASSETS.rglob('*') if p.is_file()}
    assert sha(active)==active_hash
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',13)
    for name,start,end in [('overview-31.png',0,31),('materials-10.png',12,22),('biomes-and-otherworld-9.png',22,31)]:
        rows=(end-start+3)//4;sheet=Image.new('RGBA',(1200,rows*320),(24,26,33,255));d=ImageDraw.Draw(sheet)
        for j,k in enumerate(range(start,end)):
            x=j%4*300;y=j//4*320;sheet.alpha_composite(images[k].resize((238,238),Image.Resampling.NEAREST),(x+31,y+6))
            d.text((x+150,y+254),f"{k+1:02d} {records[k]['name']}",font=font,fill='white',anchor='mt')
            d.text((x+150,y+286),records[k]['theme'],font=small,fill=(185,203,215),anchor='mt')
        sheet.save(OUT/name)
    pairs=Image.new('RGBA',(1200,16*260),(24,26,33,255));d=ImageDraw.Draw(pairs)
    for i,r in enumerate(records):
        old=Image.open(ASSETS/'textures/item'/(r['id']+'.png')).convert('RGBA');x=i%2*600;y=i//2*260
        for pic,left,label in [(old,x+80,'原贴图'),(images[i],x+360,'新试稿')]:
            pairs.alpha_composite(pic.resize((pic.width*10,pic.height*10),Image.Resampling.NEAREST),(left,y+10));d.text((left+85,y+197),label,font=small,fill='white',anchor='mt')
        d.text((x+300,y+228),r['name'],font=font,fill=(245,214,151),anchor='mt')
    pairs.save(OUT/'before-after-31.png')
    manifest={'status':'trial only','count':31,'boss_and_composite_count':12,'material_count':10,'biome_and_otherworld_count':9,'reference':str(REFERENCE),'reference_jar':'mods/foolish-1.3.0 patched.jar','official_assets_unchanged':len(before),'previous_boss_trials_unchanged':True,'active_jar_unchanged':True,'built':False,'deployed':False,'items':records}
    (OUT/'manifest-31.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=['# Foolish 全部 31 张联动魂石试稿','', '范围：10 张 Boss 魂石、2 张 Boss 复合魂石、10 张材料魂石、8 张群系魂石与异境之魂。此前 12 张试稿保持不变。','', 'Boss 配色与结构依据当前 Foolish 1.3.0 的实体默认材质及模型骨骼；材料与群系版参考当前 JAR 中代表物品／方块模型实际引用的纹理。见 reference-inventory.json 和 material-reference-inventory.json。群系试稿是以代表地表、植物和材料作小尺寸构图，不是群系截图的逐像素复刻。','', '全部直接在本体空白魂石的 17×17 网格上绘制，沿用其透明轮廓、原视角和切面光照，不缩放高清图作为中央贴片。','', '| 魂石 | 主题 |','| --- | --- |']
    rows += [f"| {r['name']} | {r['theme']} |" for r in records]
    rows += ['', '校验通过：31 张尺寸与透明轮廓、0/255 透明、原生重生成一致、70 倍最近邻方块一致、无仅换色的相同像素布局；此前 12 张试稿哈希保持一致；全部正式资源和已安装 0.7.1 JAR 均未改变。','', '交付：overview-31.png、materials-10.png、biomes-and-otherworld-9.png、before-after-31.png、native-17px/、preview-1190px/。','', '本轮只生成试稿，没有构建或部署；游戏内视觉和原尺寸可读性尚未测试。']
    (OUT/'report-31.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    print('PASS: 31 native trials; prior 12 unchanged; exact reference alpha; equal pixel scale; all official resources and active JAR unchanged.')


if __name__=='__main__':main()
