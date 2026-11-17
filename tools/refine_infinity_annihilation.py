"""Apply review items 06 and 10 from the current numbered soul-stone catalog."""
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
from unify_soul_stone_grid import ROOT,TEXTURES,LEGACY
from render_scroll_style_stones import render,STONES

ART=ROOT/'art/infinity-annihilation-fix-20261010'
BACKUP=ROOT/'backups/20261010-100430-before-infinity-annihilation-fix'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ART.mkdir(exist_ok=True)
    initial={p.name:sha(p) for p in TEXTURES.glob('*.png')}
    sheet=Image.new('RGBA',(1040,650),(24,26,33,255));draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',21)
    records=[]
    for i,(name,label) in enumerate((('annihilation','06 湮灭学派：卷轴绿色'),('infinity','10 无限学派：交叉无限符号'))):
        path=TEXTURES/(name+'_soul_stone.png')
        before=Image.open(BACKUP/path.name).convert('RGBA')
        if name=='annihilation':after=render(STONES[name])
        else:
            after=before.copy();background=before.getpixel((5,5))
            rainbow=[(48,166,247),(87,89,229),(181,48,229),(232,44,175),(242,80,81),(244,161,43),(225,218,53),(58,218,112)]
            for y,row in enumerate(LEGACY[name][0]):
                for x,mark in enumerate(row):
                    after.putpixel((x+5,y+5),background if mark=='.' else rainbow[round(x*7/8)]+(255,))
            for y in range(18):
                for x in range(18):
                    if not (5<=x<14 and 5<=y<13):assert before.getpixel((x,y))==after.getpixel((x,y))
        assert after.size==(18,18) and after.mode=='RGBA'
        assert before.getchannel('A').tobytes()==after.getchannel('A').tobytes()
        assert set(after.getchannel('A').tobytes())=={0,255}
        after.save(path)
        for folder in ('native-18px','preview-1260px'):
            (ART/folder).mkdir(exist_ok=True)
            sprite=after if folder=='native-18px' else after.resize((1260,1260),Image.Resampling.NEAREST)
            sprite.save(ART/folder/path.name)
            sprite.save(ROOT/'art/unified-grid-left-rim-20261009'/folder/path.name)
        x=i*520
        draw.text((x+260,14),label,font=font,fill='white',anchor='mt')
        for image,offset,title in ((before,15,'修改前'),(after,270,'修改后')):
            sheet.alpha_composite(image.resize((234,234),Image.Resampling.NEAREST),(x+offset,52))
            draw.text((x+offset+117,295),title,font=font,fill='white',anchor='mt')
        sheet.alpha_composite(after.resize((288,288),Image.Resampling.NEAREST),(x+116,350))
        records.append({'file':path.name,'before_sha256':sha(BACKUP/path.name),'after_sha256':sha(path),'after_size':[18,18],'alpha_unchanged':True})
    for p in TEXTURES.glob('*.png'):
        if p.name not in {r['file'] for r in records}:assert sha(p)==initial[p.name]
    sheet.save(ART/'before-after.png')
    (ART/'manifest.json').write_text(json.dumps({'backup':str(BACKUP),'scroll_source':"legendary_spellbooks-1.20.1+forge-0.4.1.jar:assets/legendary_spellbooks/textures/item/scroll_annihilation.png",'items':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS: reviewed sprites are native 18x18; alpha unchanged; other 30 textures unchanged.')

if __name__=='__main__':main()
