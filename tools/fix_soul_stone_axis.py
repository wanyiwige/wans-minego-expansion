"""Apply the narrow lighting correction to all existing assets, preserving glyphs."""
from pathlib import Path
import shutil,json,hashlib
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont,ImageChops
from soul_stone_lighting import soften_axis,soften_legacy_axis
ROOT=Path(__file__).resolve().parents[1]
TEXTURES=ROOT/'src/main/resources/assets/wans_minego_expansion/textures/item'
ART=ROOT/'art/axis-lighting-fix-20261009'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    backup=ROOT/'backups'/('20261009-'+datetime.now().strftime('%H%M%S')+'-before-axis-lighting-fix')
    backup.mkdir(parents=True);ART.mkdir(parents=True,exist_ok=True)
    paths=sorted(TEXTURES.glob('*.png'));assert len(paths)==32
    for path in paths:shutil.copy2(path,backup/path.name)
    labels=json.loads((ROOT/'src/main/resources/assets/wans_minego_expansion/lang/zh_cn.json').read_text(encoding='utf-8'))
    sheet=Image.new('RGBA',(1600,8*245),(24,26,33,255));draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15);records=[]
    for i,path in enumerate(paths):
        old=Image.open(path).convert('RGBA')
        if old.width in (18,1260):
            native=old if old.width==18 else old.resize((18,18),Image.Resampling.NEAREST)
            repaired=soften_axis(native)
            # Preserve every original raster pixel outside the changed native grid cells.
            new=old.copy();scale=old.width//18
            for y in range(18):
                for x in range(18):
                    if native.getpixel((x,y))!=repaired.getpixel((x,y)):
                        new.paste(repaired.getpixel((x,y)),(x*scale,y*scale,(x+1)*scale,(y+1)*scale))
        else:new=soften_legacy_axis(old)
        assert old.size==new.size and ImageChops.difference(old.getchannel('A'),new.getchannel('A')).getbbox() is None
        core=(round(old.width*5/18),round(old.height*5/18),round(old.width*13/18),round(old.height*13/18))
        assert old.crop(core).tobytes()==new.crop(core).tobytes(),path.name
        assert old.tobytes()!=new.tobytes(),path.name
        new.save(path)
        if old.width==18:
            native_path=ROOT/'art/foolish-boss-stones-v1/native-18px'/path.name
            if native_path.exists():new.save(native_path)
            new.resize((1260,1260),Image.Resampling.NEAREST).save(ROOT/'art/foolish-boss-stones-v1/preview-1260px'/path.name)
        elif old.width==1260:
            native_path=ROOT/'art/stones-18px'/path.name
            if native_path.exists():new.resize((18,18),Image.Resampling.NEAREST).save(native_path)
        x,y=(i%4)*400,(i//4)*245
        sheet.alpha_composite(old.resize((180,180),Image.Resampling.NEAREST),(x+10,y+8))
        sheet.alpha_composite(new.resize((180,180),Image.Resampling.NEAREST),(x+210,y+8))
        name=labels.get('item.wans_minego_expansion.'+path.stem,path.stem)
        draw.text((x+200,y+192),name,font=font,fill=(235,238,245),anchor='mt')
        draw.text((x+100,y+218),'修改前',font=font,fill=(175,180,190),anchor='mt')
        draw.text((x+300,y+218),'修改后',font=font,fill=(175,180,190),anchor='mt')
        records.append({'file':path.name,'size':old.size,'before_sha256':sha(backup/path.name),'after_sha256':sha(path),'alpha_preserved':True,'glyph_preserved':True})
    sheet.save(ART/'before-after-all-32.png')
    (ART/'manifest.json').write_text(json.dumps({'backup':str(backup),'items':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # Refresh the source art manifest without running the resource integration generator.
    mpath=ROOT/'art/foolish-boss-stones-v1/manifest.json';manifest=json.loads(mpath.read_text(encoding='utf-8'))
    for group in ['stones','composites']:
        for stone in manifest.get(group,[]):stone['sha256']=sha(TEXTURES/stone['file'])
    mpath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS: all 32 changed; dimensions, alpha and center glyphs preserved.')
    print('Backup:',backup);print('Preview:',ART/'before-after-all-32.png')
if __name__=='__main__':main()
