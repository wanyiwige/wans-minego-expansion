"""Validate the authorized 22-texture redraw and emit review artifacts."""
from pathlib import Path
import hashlib,json,zipfile
from PIL import Image,ImageDraw,ImageFont
from render_epoch_stones import ROOT,ART,TEXTURES,NAMES
from epoch_reference_stone import REFERENCE,render_reference

BACKUP=ROOT/'backups/20261012-125325-before-epoch-hex-redraw'
ASSETS=ROOT/'src/main/resources/assets/wans_minego_expansion'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    receipts=json.loads((BACKUP/'textures-before.json').read_text(encoding='utf-8-sig'))
    targets={f'epoch_{k}_soul_stone.png' for k in NAMES}
    changed=[]
    for r in receipts:
        p=Path(r['source'])
        if sha(p)!=r['sha256'].lower():changed.append(p.name)
    assert set(changed)==targets and len(changed)==22,changed
    jar_path=next((ROOT.parent/'mods').glob('*mine_fargo*.jar'))
    with zipfile.ZipFile(jar_path) as jar:
        reference_bytes=jar.read('assets/mine_fargo/textures/item/empty_soul_stone.png')
    assert REFERENCE.read_bytes()==reference_bytes
    reference=Image.open(REFERENCE).convert('RGBA')
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17)
    small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
    sheet=Image.new('RGBA',(1320,11*255),(24,26,33,255));d=ImageDraw.Draw(sheet)
    native=Image.new('RGBA',(17*12,17*2),(24,26,33,255))
    pairs=[];rgba=[];topologies=[]
    for i,(key,names) in enumerate(NAMES.items()):
        stem=f'epoch_{key}_soul_stone';p=TEXTURES/(stem+'.png')
        new=Image.open(p).convert('RGBA');old=Image.open(BACKUP/'textures'/p.name).convert('RGBA')
        assert new.size==(17,17)
        assert new.getchannel('A').tobytes()==reference.getchannel('A').tobytes()
        assert set(new.getchannel('A').getdata())=={0,255}
        assert render_reference(key).tobytes()==new.tobytes()
        model=json.loads((ASSETS/'models/item'/(stem+'.json')).read_text(encoding='utf-8'))
        assert model['parent']=='minecraft:item/generated'
        assert model['textures']['layer0']=='wans_minego_expansion:item/'+stem
        preview=Image.open(ART/'preview-1190px'/p.name).convert('RGBA')
        assert preview.size==(1190,1190)
        for y in range(17):
            for x in range(17):
                assert preview.crop((x*70,y*70,(x+1)*70,(y+1)*70)).getcolors(2)==[(4900,new.getpixel((x,y)))]
        rgba.append(new.tobytes())
        labels={};topology=[]
        for pixel in new.getdata():
            if pixel not in labels:labels[pixel]=len(labels)
            topology.append(labels[pixel])
        topologies.append(tuple(topology))
        x=(i%2)*660;y=(i//2)*255
        d.text((x+330,y+8),f'{i+1:02d} {names[0]}',font=font,fill='white',anchor='mt')
        # Both drawings enlarge each native pixel by exactly 10; no stretched grid.
        for img,left,title in [(old,x+95,'原贴图'),(new,x+395,'空白魂石视角重绘')]:
            enlarged=img.resize((img.width*10,img.height*10),Image.Resampling.NEAREST)
            sheet.alpha_composite(enlarged,(left,y+37))
            d.text((left+85,y+218),title,font=small,fill=(211,222,233),anchor='mt')
        native.alpha_composite(new,((i%12)*17,(i//12)*17))
        pairs.append({'id':stem,'name':names[0],'before_sha256':sha(BACKUP/'textures'/p.name),'after_sha256':sha(p),'size':[17,17],'reference_alpha_exact':True,'regeneration_exact':True,'model_reference_valid':True,'preview_grid_verified':True})
    assert len(set(rgba))==22
    assert len(set(topologies))==22
    sheet.save(ART/'before-after-all-22.png');native.save(ART/'all-22-native.png')
    # Place the exact base alongside a few finished stones for direct camera comparison.
    cam=Image.new('RGBA',(1050,300),(24,26,33,255));dc=ImageDraw.Draw(cam)
    for i,(img,label) in enumerate([(reference,'本体空白魂石'),(Image.open(TEXTURES/'epoch_magnetic_steel_soul_stone.png').convert('RGBA'),'磁钢魂石'),(Image.open(TEXTURES/'epoch_zixu_soul_stone.png').convert('RGBA'),'子虚仙君魂石'),(Image.open(TEXTURES/'epoch_epoch_soul_stone.png').convert('RGBA'),'棠煌之魂')]):
        cam.alpha_composite(img.resize((221,221),Image.Resampling.NEAREST),(i*262+20,10));dc.text((i*262+130,252),label,font=font,fill='white',anchor='mt')
    cam.save(ART/'same-view-reference.png')
    active=ROOT.parent/'mods/wans_minego_expansion-0.7.0.jar'
    manifest=json.loads((ART/'manifest.json').read_text(encoding='utf-8'))
    manifest.update({'backup':str(BACKUP),'reference_sha256':sha(REFERENCE),'textures_changed':22,'other_textures_unchanged':len(receipts)-22,'proof_textures_unchanged':5,'same_reference_alpha':True,'distinct_color_topologies':22,'native_regeneration_verified':True,'preview_pixel_size':[70,70],'active_jar_sha256':sha(active),'built':False,'deployed':False,'game_visual_verified':False,'items_verified':pairs})
    (ART/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=['# 棠煌纪元魂石重绘：空白魂石原视角','', '范围：现有 22 张棠煌纪元魂石。五张凭证与其他魂石未修改。','', '以当前安装 Mine Fargo 1.3.6 的 empty_soul_stone.png 为底图，按用户最后确认的要求沿用原图视角。底图原生为 17×17，正式贴图也使用 17×17，而不是此前扩展模组的 18×18；没有对参考图或中央图案进行缩放粘贴。','', '保留本体空白魂石的透明轮廓、宽左上受光面、右侧暗切面、上下端部与侧缘。主题颜料使用原图七级明暗分布着色，图案在同一原生网格上按表面布局。此前自行绘制的对称六边形方案已弃用。','', '| 魂石 | 设计主题 |','| --- | --- |']
    rows += [f"| {r['name']} | {r['theme']} |" for r in manifest['stones']]
    rows += ['', '## 校验', '', '- 22 张正式 PNG 与原底图透明轮廓逐像素一致，全部 17×17，透明值为 0/255。','- 中央和外侧共用同一网格；1190px 预览中每个源像素严格占 70×70 的纯色块。','- 22 张可以由正式绘制入口逐字节复现；模型引用均有效。','- 与操作前快照比较，仅 22 张魂石 PNG 改变，其他 67 张贴图，包括 5 张凭证，保持原样。','- 22 张没有完整图像或仅替换颜色的相同像素布局；同一轮廓是明确要求，不作为重复设计缺陷。','- 已人工查看实际低像素总览；原尺寸逐张的游戏内可读性仍需进游戏确认。','', '## 状态与文件', '', '已更新源码贴图和正式生成入口。尚未构建或部署；游戏安装的 0.7.0 JAR 保持原样。','', '- overview.png：最终 22 张总览，统一 11 倍最近邻放大。','- same-view-reference.png：空白魂石与三张成品的同视角对照。','- before-after-all-22.png：全部重绘前后对照，源像素均放大 10 倍。','- all-22-native.png：不放大的原尺寸总览。','- native-17px/：最终原生 PNG。','- preview-1190px/：最终 70 倍最近邻预览。','- discarded-symmetric-hex-preview/：已弃用的对称六边形试稿，不是正式资源。','', '主要编辑源为 tools/epoch_native_hex.py 中的主题笔画与 tools/epoch_reference_stone.py 中的原图表面投影、切面着色；正式导出入口为 tools/render_epoch_stones.py。未采用高清概念图作为正式贴图输入。']
    (ART/'report.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    print('PASS: 22 retextures, exact original alpha/camera template, one 17px grid, 67 untouched textures, valid models, reproducible native output.')


if __name__=='__main__':main()
