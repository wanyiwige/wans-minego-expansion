"""Export 22 native SAE retextures on the exact empty-stone camera/facet map.

The original palette/glyph table is retained as historical input for older tools.
Finished composition uses epoch_reference_stone and its native 17px reference.
Only the 22 SAE soul stones are exported; vouchers and other icons are preserved.
"""
from pathlib import Path
import hashlib, json, colorsys
from PIL import Image, ImageDraw, ImageFont, ImageChops
from render_scroll_style_stones import render, colors, ROOT, TEXTURES
from generate_epoch_resources import NAMES
from epoch_reference_stone import render_reference, THEMES, REFERENCE

ART=ROOT/'art/epoch-whole-stone-redraw-20261012'

def rgb(s):return tuple(bytes.fromhex(s))
def vivid(color, gain=1, saturation=0):
    h,s,v=colorsys.rgb_to_hsv(*(c/255 for c in color))
    return tuple(round(c*255) for c in colorsys.hsv_to_rgb(h,min(1,s+saturation),min(1,v*gain)))
def design(palette,disk,rune,glyph,theme):
    assert len(glyph)==8 and all(len(row)==8 for row in glyph)
    assert set(''.join(glyph)) <= set('.OI')
    # Author a brighter color ramp on the existing native grid. Deep facets and
    # the inset are darkened so brighter midtones remain distinct from highlights.
    ramp=colors(*palette.split())
    gains=(.75,.84,.94,1.08,1.18,1.16,1.10,1.04,1.0)
    saturation=(.08,.10,.13,.18,.21,.18,.13,.06,.0)
    ramp=tuple(vivid(c,gains[i],saturation[i]) for i,c in enumerate(ramp))
    inset=tuple(vivid(rgb(c),.72,.12) for c in disk.split())
    outer,inner=map(rgb,rune.split())
    return {'palette':ramp,'disk':inset,
            'rune':(vivid(outer,1.20,.20),vivid(inner,1.10,.06)),
            'glyph':glyph,'theme':theme}

STONES={
 'fangzun':design('1d1923 38303c 574754 7b686d a69283 c6b397 e4d4b1 f8edcf fff9e8',
  '29212d 352b38','bf9d4e f5df94',
  ['OOOOOOOO','OIIII IIO'.replace(' ',''),'OI.OO.IO','OIOIIOIO','OI.OO.IO','OIOIIOIO','OIIIIIIO','OOOOOOOO'],'玄印方篆'),
 'cangyao':design('0c1826 1b3347 2d5264 407587 609dab 87bdc6 b1dce0 dcf4f2 f5ffff',
  '122b3a 1b3b49','65bacb cefcf7',
  ['OO....OO','II....II','II....II','II....II','OI....IO','OII..IIO','.OIIIIO.','..OOOO..'],'苍蓝磁环'),
 'zixu':design('21172c 3a2c48 564364 775e83 9d81ab bea4c8 decadd f2e7ee fff8f2',
  '2c2139 392b47','a2c18f e8f6bc',
  ['OOOOOO..','OIIIIOO.','OI...IO.','OI.IIIO.','OI...IO.','OI.IIIO.','OIIIIIOO','.OOOOOO.'],'玉墨绘卷'),
 'zhenyan':design('241219 48232a 743731 a94e38 d96e40 ee995e f7c18b fbe2ba fff6da',
  '381b24 47222a','eb994c ffe6a1',
  ['......OO','OOOOOOII','OIIIIIIO','OOOOOOO.','..OOO...','..II....','..II....','..OO....'],'火铳炮势'),
 'goldenhou':design('291820 4d2c2a 744639 a16b46 c79455 e2b770 f0d99e fceec8 fffae5',
  '38212c 472a34','d5a365 fbe3a2',
  ['...OO...','..OIIO..','..OIIO..','.OIIIIO.','.OIIIIO.','OIIIIIIO','OOOOOOOO','...II...'],'紫金铃火'),
 'general':design('20211d 3a3d30 565b40 798060 a0a783 c3c8a7 e0e4c7 f1f3df fcfff0',
  '292c25 373b2e','c47258 f1bd82',
  ['OO......','IIOOOOOO','IIOIIIIO','IIOIIOO.','IIOOO...','II......','II......','OO......'],'虎符军旗'),
 'magnetic_steel':design('111e27 243b48 3b5966 577b84 79a1a7 a1c2c5 c7dfe0 e5f3f0 f8fff9',
  '1e333e 2a4550','78afbc c5eced',
  ['..OOOO..','.OIIIIO.','OIIII IIO'.replace(' ',''),'OOOOOOOO','OIIIIIIO','OI....IO','OIIIIIIO','OOOOOOOO'],'磁钢铸锭'),
 'damascene':design('152016 2c3b28 49583a 657853 88a077 afc49b d2dfbe e9f2d9 f9ffee',
  '202d20 2d3a29','b5c08f eff7c5',
  ['OI....IO','.OI..IO.','..OIIO..','...II...','..OIIO..','.OI..IO.','OI....IO','O......O'],'交锋龙镔'),
 'bronze':design('271b1c 48312a 704b35 987045 bd975f dab985 edd5b0 f8ecd6 fff9ed',
  '372826 47322b','c69250 f4d89c',
  ['OOOOOOOO','OIIIIIIO','OI.OO.IO','OI.II.IO','.OIIIIO.','.OIIIIO.','..OIIO..','...OO...'],'青铜盾纹'),
 'jade':design('0d2624 1b4540 2b6559 428a70 62b08c 8ad2ad b7e8cf ddf7e9 f5fff4',
  '163c32 214c3f','82d5ad dfffe3',
  ['..OOOO..','.OIIIIO.','OIIOOIIO','OIO..OIO','OIO..OIO','OIIOOIIO','.OIIIIO.','..OOOO..'],'通透玉璧'),
 'talisman':design('2a1320 4e2633 783c42 a35c55 c7826b e2ab8b f0ceb0 f9e8d7 fff8eb',
  '402129 512b32','df7860 ffd5a0',
  ['...II...','OOOOOOOO','..OIIO..','.OIIII O.'.replace(' ',''),'....IIO.','.OOOIIO.','..IIO...','..OOOO..'],'朱砂符笔'),
 'type':design('1a1c24 333943 505761 727780 9699a1 b8bac2 d9dbe1 eeeff3 fbfbff',
  '272c36 343b46','b7c4cf eff7ff',
  ['OO.OO.OO','II.II.II','........','OO.OO.OO','II.II.II','........','OO.OO.OO','II.II.II'],'六字印版'),
 'ghost_jade':design('151c2e 2b3650 455574 647a99 89a1b7 afc3d1 d2e0e5 eaf3f4 fbffff',
  '202b45 2b3c54','91becb dcf6f2',
  ['..OOOO..','.OIIIIO.','OI.OO.IO','OI.OO.IO','OIIIIIIO','OIIOOIIO','OI.OO.IO','O.O..O.O'],'幽玉游魂'),
 'pyrotemper':design('29161c 4d2b2d 77433a a46345 c98a57 e6b176 f4d09f fbe9c8 fff9e9',
  '3d2429 4d2e30','e39b5c ffe4b1',
  ['...OO...','..OIIO..','.OIIIIO.','OIIIIIIO','OII..IIO','OI.OO.IO','.OIIIIO.','..OOOO..'],'燧火淬炼'),
 'classics':design('1a231b 334130 4f6045 738064 98a488 bec7ad dee3cf f0f3e6 fcfff7',
  '273429 344232','aec68e edf5c6',
  ['OOO..OOO','OIIOOIIO','OIIOOIIO','OIIOOIIO','OIIOOIIO','OIIOOIIO','OOOOOOOO','...II...'],'竹简典籍'),
 'cauldron':design('27221b 48402b 6d603d 978650 bca76c d7c28e ebdcb6 f7eedb fffbf1',
  '383021 463c29','bfa064 eeda9e',
  ['O......O','OOOOOOOO','OIIIIIIO','OI.OO.IO','OI.II.IO','OIIIIIIO','.OOOOOO.','.II..II.'],'双耳鼎纹'),
 'tiger':design('2a1922 4e2c34 76453f a1694e c68f63 e1b585 f0d5b2 faebd7 fff8ed',
  '3b232b 4a2e33','d89f69 ffe2ae',
  ['O.O..O.O','OOOOOOOO','.OI..IO.','OII..IIO','OO.OO.OO','.OIIIIO.','..OII O..'.replace(' ',''),'..OOOO..'],'炮虎面纹'),
 'rusted':design('251d20 44312f 684a3e 946b51 b8916f d3b496 e8d5bd f6eada fff9f0',
  '352925 45342d','b98565 eac39b',
  ['...OO...','..OIIO..','.OIIIIO.','.OI..IO.','.OI..IO.','.OIIIIO.','..OIIO..','OOOOOOOO'],'锈铜战盔'),
 'explorer':design('112523 23433d 3a6557 568c72 7bb096 a3ceb3 c9e6d0 e8f5e8 f9fff6',
  '1c3731 29483e','9ac8a8 e7fbd3',
  ['...OO...','..O..O..','.O...IO.','O...I..O','O..I...O','.OI...O.','..O..O..','...OO...'],'菱框指南针'),
 'celesterral':design('221d27 413443 62505b 8a706b b4987e d6b998 ebd9bb f9eed9 fff9ee',
  '312531 42333d','d5ba68 fbedac',
  ['...OO...','..OIIO..','.OI..IO.','OI.OO.IO','OI.OO.IO','.OI..IO.','..OIIO..','...OO...'],'玄黄菱印'),
 'four_sovereigns':design('241b28 473342 6c4e57 98746b c19d7e dfc29a f1dfbd fbeddb fffbf0',
  '34253b 463248','cea179 f8e1a4',
  ['..OIIO..','...II...','O..II..O','IIOOOOII','IIOOOOII','O..II..O','...II...','..OIIO..'],'四尊共印'),
 'epoch':design('282028 4c3a45 745952 a08365 c8ac7c e4cc9c f4e6c4 fcf3e1 fffdf5',
  '382b3e 4b394b','c795c4 ffeeac',
  ['...II...','O.OIIO.O','.IIIIII.','OIIOOIIO','OIIOOIIO','.IIIIII.','O.OIIO.O','...II...'],'棠花皇印'),
}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    ART.mkdir(parents=True,exist_ok=True)
    targets={f'epoch_{key}_soul_stone.png' for key in STONES}
    before={p:sha(p) for p in TEXTURES.glob('*.png') if p.name not in targets}
    reference_alpha=None
    sheet=Image.new('RGBA',(1320,1040),(24,26,33,255));draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',13)
    records=[]
    for i,(key,info) in enumerate(STONES.items()):
        sprite=render_reference(key,info)
        assert sprite.size==(17,17) and set(sprite.getchannel('A').tobytes())=={0,255}
        if reference_alpha is None:reference_alpha=sprite.getchannel('A')
        assert ImageChops.difference(sprite.getchannel('A'),reference_alpha).getbbox() is None
        name=f'epoch_{key}_soul_stone.png'
        for folder in [TEXTURES,ART/'native-17px']:
            folder.mkdir(parents=True,exist_ok=True);sprite.save(folder/name)
        (ART/'preview-1190px').mkdir(exist_ok=True)
        sprite.resize((1190,1190),Image.Resampling.NEAREST).save(ART/'preview-1190px'/name)
        x,y=(i%6)*220,(i//6)*260
        sheet.alpha_composite(sprite.resize((187,187),Image.Resampling.NEAREST),(x+16,y+4))
        draw.text((x+110,y+207),f'{i+1:02d} {NAMES[key][0]}',font=font,fill=(235,239,245),anchor='mt')
        draw.text((x+110,y+236),THEMES[key][0],font=small,fill=(161,178,194),anchor='mt')
        records.append({'id':name[:-4],'name':NAMES[key][0],'theme':THEMES[key][1],'mode':THEMES[key][0],'sha256':sha(TEXTURES/name),'native_grid':[17,17]})
    sheet.save(ART/'overview.png')
    # Side-by-side on the same zoom/grid: three current 0.6.0 icons and three new designs.
    comparison=Image.new('RGBA',(900,600),(24,26,33,255));d=ImageDraw.Draw(comparison)
    pairs=[('foolish_pyre_soul_stone','zhenyan'),('foolish_timewelder_soul_stone','cangyao'),('foolish_keepsteel_material_soul_stone','magnetic_steel')]
    for i,(old,new) in enumerate(pairs):
        for j,(name,label) in enumerate([(old,'旧版 0.6.0'),(f'epoch_{new}_soul_stone',NAMES[new][0])]):
            img=Image.open(TEXTURES/(name+'.png')).convert('RGBA')
            comparison.alpha_composite(img.resize((img.width*14,img.height*14),Image.Resampling.NEAREST),(i*300+24,j*300+6))
            d.text((i*300+150,j*300+265),label,font=font,fill=(235,239,245),anchor='mt')
    comparison.save(ART/'comparison.png')
    # Accepted composite art is an animation of its recipe components.
    from export_epoch_composite_animations import main as export_animations
    animations={item['id']:item for item in export_animations()}
    for item in records:
        if item['id'] in animations:
            item['sha256']=sha(TEXTURES/(item['id']+'.png'))
            item['animation']=animations[item['id']]
    for p,digest in before.items():assert sha(p)==digest,p
    (ART/'manifest.json').write_text(json.dumps({'size':[17,17],'renderer':'epoch_reference_stone.render_reference','reference':str(REFERENCE),'silhouette':'exact empty soul stone alpha and perspective','legacy_textures_unchanged':len(before),'stones':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'PASS: 22 native 17px empty-stone retextures; {len(before)} other item textures including vouchers unchanged.')

if __name__=='__main__':main()

