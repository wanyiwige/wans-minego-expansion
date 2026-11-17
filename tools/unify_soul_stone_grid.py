"""Normalize all item sprites onto one native grid and clarify the left light ridge."""
from pathlib import Path
from datetime import datetime
import hashlib,json,shutil
from PIL import Image,ImageDraw,ImageFont
from soul_stone_lighting import clarify_upper_left
from render_scroll_style_stones import SOURCE
ROOT=Path(__file__).resolve().parents[1]
TEXTURES=ROOT/'src/main/resources/assets/wans_minego_expansion/textures/item'
ART=ROOT/'art/unified-grid-left-rim-20261009'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
LEGACY={
 'annihilation':(['...OO...','...II...','..OIIO..','OOIIIIOO','OOIIIIOO','..OIIO..','...II...','...OO...'],(121,234,90),(255,254,185)),
 'dream':(['..OOOO..','.OII.O..','OII.....','OII...I.','OII.....','OII.....','.OII.O..','..OOOO..'],(186,167,255),(238,235,255)),
 'infinity':(['.........','.........','.OO...OO.','O..O.O..O','O...I...O','O..O.O..O','.OO...OO.','.........'],(90,185,252),(247,241,144)),
 'insect':(['..O..O..','...OO...','..OOOO..','O.OIIO.O','.OOIIOO.','O.OIIO.O','..OOOO..','...OO...'],(232,174,18),(255,218,75)),
 'relicron':(['..O..O..','.OOOOOO.','OO....OO','O..II..O','O..II..O','OO....OO','.OOOOOO.','..O..O..'],(48,148,240),(132,223,255)),
 'shadow':(['...OOOO.','..OII.O.','.OII....','OII.....','OII.....','.OII....','..OII.O.','...OOOO.'],(201,204,218),(246,247,255)),
 'spirit_sect':(['....OO..','...OIO..','..OI.O..','.OII.O..','OIIO.O..','OIIIOO..','.OIIIO..','..OOO...'],(107,110,247),(210,210,255)),
 'symmetry_sect':(['..IIIO..','.IIIIIO.','IIIIOIOO','IIIIIOOO','IIIOOOOO','IIOIOOOO','.IOOOOO.','..IOOO..'],(17,49,46),(234,255,246)),
 'tainted':(['..OOO...','.O...O..','O..O..O.','O.OO..O.','O.O...O.','.O.OOO..','..O.....','...OO...'],(108,25,154),(176,48,207)),
 'unstable':(['...OO...','..OI....','.OI.....','OOIIOOO.','....IIO.','...IIO..','..IIO...','..OO....'],(232,22,195),(75,165,253)),
 'wind':(['....OO..','......O.','IIIIIIO.','........','OOOOOOOO','.......O','..IIIIO.','........'],(123,226,252),(240,252,255))}
def rebuild_legacy(native,name):
    result=native.copy();original=native.copy()
    for y in range(18):
        for x in range(18):
            a=SOURCE.getpixel((round((x+.5)*SOURCE.width/18),round((y+.5)*SOURCE.height/18)))[3]
            if a<128:result.putpixel((x,y),(0,0,0,0))
            elif result.getpixel((x,y))[3]==0:
                candidates=[(abs(px-x)+abs(py-y),original.getpixel((px,py))) for py in range(18) for px in range(18) if original.getpixel((px,py))[3]]
                result.putpixel((x,y),min(candidates,key=lambda p:p[0])[1][:3]+(255,))
    glyph,outer,inner=LEGACY[name]
    core=sorted([original.getpixel((x,y))[:3] for y in range(5,13) for x in range(5,13)],key=lambda p:sum(p))
    background=core[8]
    for y in range(5,13):
        for x in range(5,14 if name=='infinity' else 13):result.putpixel((x,y),background+(255,))
    rainbow=[(48,166,247),(87,89,229),(181,48,229),(232,44,175),(242,80,81),(244,161,43),(225,218,53),(58,218,112)]
    for y,row in enumerate(glyph):
        for x,mark in enumerate(row):
            if mark!='.':result.putpixel((x+5,y+5),(rainbow[round(x*7/8)] if name=='infinity' else inner if mark=='I' else outer)+(255,))
    return result
def main():
    backup=ROOT/'backups'/('20261009-'+datetime.now().strftime('%H%M%S')+'-before-grid-left-rim-fix')
    backup.mkdir(parents=True);(ART/'native-18px').mkdir(parents=True,exist_ok=True)
    (ART/'preview-1260px').mkdir(exist_ok=True)
    labels=json.loads((ROOT/'src/main/resources/assets/wans_minego_expansion/lang/zh_cn.json').read_text(encoding='utf-8'))
    sheet=Image.new('RGBA',(1600,1960),(24,26,33,255));draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15);records=[]
    for i,path in enumerate(sorted(TEXTURES.glob('*.png'))):
        shutil.copy2(path,backup/path.name);old=Image.open(path).convert('RGBA')
        native=old.resize((18,18),Image.Resampling.NEAREST)
        native.putdata([p[:3]+(255,) if p[3]>=128 else (0,0,0,0) for p in native.getdata()])
        name=path.stem.removesuffix('_soul_stone')
        if name in LEGACY:native=rebuild_legacy(native,name)
        new=clarify_upper_left(native)
        assert new.crop((5,5,13,13)).tobytes()==native.crop((5,5,13,13)).tobytes()
        assert new.getchannel('A').tobytes()==native.getchannel('A').tobytes()
        assert set(new.getchannel('A').tobytes())=={0,255}
        new.save(path);new.save(ART/'native-18px'/path.name)
        large=new.resize((1260,1260),Image.Resampling.NEAREST);large.save(ART/'preview-1260px'/path.name)
        # Every preview cell is exactly 70x70 of one source pixel, including the glyph.
        for y in range(18):
            for x in range(18):assert large.crop((x*70,y*70,(x+1)*70,(y+1)*70)).getcolors(2)==[(4900,new.getpixel((x,y)))]
        school_native=ROOT/'art/stones-18px'/path.name
        if school_native.exists():new.save(school_native)
        boss_native=ROOT/'art/foolish-boss-stones-v1/native-18px'/path.name
        if boss_native.exists():
            new.save(boss_native);large.save(ROOT/'art/foolish-boss-stones-v1/preview-1260px'/path.name)
        x,y=(i%4)*400,(i//4)*245
        sheet.alpha_composite(old.resize((180,180),Image.Resampling.NEAREST),(x+10,y+8))
        sheet.alpha_composite(new.resize((180,180),Image.Resampling.NEAREST),(x+210,y+8))
        draw.text((x+200,y+192),labels.get('item.wans_minego_expansion.'+path.stem,path.stem),font=font,fill=(235,238,245),anchor='mt')
        draw.text((x+100,y+218),'修改前',font=font,fill=(175,180,190),anchor='mt')
        draw.text((x+300,y+218),'修改后',font=font,fill=(175,180,190),anchor='mt')
        records.append({'file':path.name,'before_size':old.size,'after_size':[18,18],
            'before_sha256':sha(backup/path.name),'after_sha256':sha(path),'glyph_redrawn':name in LEGACY,'native_glyph_preserved':True,'alpha':'binary 0/255'})
    assert len(records)==32
    sheet.save(ART/'before-after.png')
    (ART/'manifest.json').write_text(json.dumps({'backup':str(backup),'items':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    mp=ROOT/'art/foolish-boss-stones-v1/manifest.json';manifest=json.loads(mp.read_text(encoding='utf-8'))
    for group in ('stones','composites'):
        for item in manifest.get(group,[]):item['sha256']=sha(TEXTURES/item['file'])
    mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS: 32 native 18x18 sprites; all rim/glyph pixels share one grid; binary alpha and 70x nearest-neighbor preview cells verified.')
    print('Backup:',backup);print('Preview:',ART/'before-after.png')
if __name__=='__main__':main()
