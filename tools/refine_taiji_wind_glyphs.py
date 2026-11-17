"""Redraw only the two school glyphs, preserving every outer facet pixel."""
from pathlib import Path
import hashlib, json
from PIL import Image, ImageDraw, ImageFont
from unify_soul_stone_grid import LEGACY, TEXTURES, ROOT

ART = ROOT / 'art/taiji-wind-glyph-fix-20261010'
BACKUP = ROOT / 'backups/20261010-095756-before-taiji-wind-glyph-fix'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ART.mkdir(parents=True, exist_ok=True)
    initial = {p.name: sha(p) for p in TEXTURES.glob('*.png')}
    sheet = Image.new('RGBA', (1040,610), (24,26,33,255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 22)
    records = []
    for i, (name, label) in enumerate((('symmetry_sect','两仪学派：太极双鱼'),('wind','风学派：卷尾风纹'))):
        path = TEXTURES / (name + '_soul_stone.png')
        before = Image.open(BACKUP/path.name).convert('RGBA')
        after = before.copy()
        pattern, dark, light = LEGACY[name]
        # The corner of the existing center is clear background in both sprites.
        background = before.getpixel((5,5))
        for y, row in enumerate(pattern):
            for x, mark in enumerate(row):
                after.putpixel((x+5,y+5), background if mark=='.' else (light if mark=='I' else dark)+(255,))
        assert after.size == (18,18)
        assert after.getchannel('A').tobytes() == before.getchannel('A').tobytes()
        for y in range(18):
            for x in range(18):
                if not (5<=x<13 and 5<=y<13):
                    assert before.getpixel((x,y)) == after.getpixel((x,y))
        after.save(path)
        for folder in ('native-18px','preview-1260px'):
            (ART/folder).mkdir(exist_ok=True)
            (ROOT/'art/unified-grid-left-rim-20261009'/folder).mkdir(exist_ok=True)
            sprite = after if folder=='native-18px' else after.resize((1260,1260),Image.Resampling.NEAREST)
            sprite.save(ART/folder/path.name)
            sprite.save(ROOT/'art/unified-grid-left-rim-20261009'/folder/path.name)
        x = i*520
        sheet.alpha_composite(before.resize((234,234),Image.Resampling.NEAREST),(x+15,52))
        sheet.alpha_composite(after.resize((234,234),Image.Resampling.NEAREST),(x+270,52))
        draw.text((x+260,14),label,font=font,fill='white',anchor='mt')
        draw.text((x+132,295),'修改前',font=font,fill='white',anchor='mt')
        draw.text((x+387,295),'修改后',font=font,fill='white',anchor='mt')
        sheet.alpha_composite(after.resize((252,252),Image.Resampling.NEAREST),(x+134,346))
        records.append({'file':path.name,'before_sha256':sha(BACKUP/path.name),'after_sha256':sha(path),'after_size':[18,18],'outer_pixels_unchanged':True})
    for p in TEXTURES.glob('*.png'):
        if p.name not in {r['file'] for r in records}: assert sha(p)==initial[p.name]
    sheet.save(ART/'before-after.png')
    (ART/'manifest.json').write_text(json.dumps({'backup':str(BACKUP),'items':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS: two glyphs updated; all outer pixels, alpha, and other 30 sprites unchanged.')
    print(ART/'before-after.png')

if __name__=='__main__': main()
