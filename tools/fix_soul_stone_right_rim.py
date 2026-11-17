"""Reduce excessive upper-right reflection, leaving all other artwork intact."""
from pathlib import Path
from datetime import datetime
import hashlib,json,shutil
from PIL import Image,ImageDraw,ImageFont,ImageChops
from soul_stone_lighting import clarify_upper_right
ROOT=Path(__file__).resolve().parents[1]
TEXTURES=ROOT/'src/main/resources/assets/wans_minego_expansion/textures/item'
ART=ROOT/'art/right-rim-fix-20261009'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    backup=ROOT/'backups'/('20261009-'+datetime.now().strftime('%H%M%S')+'-before-right-rim-fix')
    backup.mkdir(parents=True);ART.mkdir(parents=True,exist_ok=True)
    records=[];pairs=[]
    labels=json.loads((ROOT/'src/main/resources/assets/wans_minego_expansion/lang/zh_cn.json').read_text(encoding='utf-8'))
    for path in sorted(TEXTURES.glob('*.png')):
        shutil.copy2(path,backup/path.name);old=Image.open(path).convert('RGBA')
        new=clarify_upper_right(old)
        assert old.size==new.size and old.getchannel('A').tobytes()==new.getchannel('A').tobytes()
        core=(round(old.width*5/18),round(old.height*5/18),round(old.width*13/18),round(old.height*13/18))
        assert old.crop(core).tobytes()==new.crop(core).tobytes(),path.name
        assert old.crop((0,0,round(old.width*10/18),old.height)).tobytes()==new.crop((0,0,round(old.width*10/18),old.height)).tobytes()
        changed=old.tobytes()!=new.tobytes()
        if changed:
            new.save(path);pairs.append((path.stem,old,new))
            if old.width==18:
                new.save(ROOT/'art/foolish-boss-stones-v1/native-18px'/path.name)
                new.resize((1260,1260),Image.Resampling.NEAREST).save(ROOT/'art/foolish-boss-stones-v1/preview-1260px'/path.name)
            elif old.width==1260:
                native=ROOT/'art/stones-18px'/path.name
                if native.exists():new.resize((18,18),Image.Resampling.NEAREST).save(native)
        records.append({'file':path.name,'changed':changed,'before_sha256':sha(backup/path.name),'after_sha256':sha(path),'glyph_preserved':True,'alpha_preserved':True})
    rows=(len(pairs)+3)//4;sheet=Image.new('RGBA',(1600,rows*245),(24,26,33,255));draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15)
    for i,(name,old,new) in enumerate(pairs):
        x,y=(i%4)*400,(i//4)*245
        sheet.alpha_composite(old.resize((180,180),Image.Resampling.NEAREST),(x+10,y+8))
        sheet.alpha_composite(new.resize((180,180),Image.Resampling.NEAREST),(x+210,y+8))
        draw.text((x+200,y+192),labels.get('item.wans_minego_expansion.'+name,name),font=font,fill=(235,238,245),anchor='mt')
        draw.text((x+100,y+218),'修改前',font=font,fill=(175,180,190),anchor='mt')
        draw.text((x+300,y+218),'修改后',font=font,fill=(175,180,190),anchor='mt')
    sheet.save(ART/'before-after.png')
    (ART/'manifest.json').write_text(json.dumps({'backup':str(backup),'items':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest_path=ROOT/'art/foolish-boss-stones-v1/manifest.json';manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    for group in ('stones','composites'):
        for item in manifest.get(group,[]):item['sha256']=sha(TEXTURES/item['file'])
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'PASS: {len(pairs)} overbright rims corrected; {len(records)-len(pairs)} unchanged. Alpha, dimensions, glyphs and upper-left light preserved.')
    print('Backup:',backup);print('Preview:',ART/'before-after.png')
if __name__=='__main__':main()
