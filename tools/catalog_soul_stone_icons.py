"""Export numbered review sheets from current source sprites without editing them."""
from pathlib import Path
import hashlib, json
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'src/main/resources/assets/wans_minego_expansion'
OUT=ROOT/'art/soul-stone-catalog-0.6.0'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    lang=json.loads((RES/'lang/zh_cn.json').read_text(encoding='utf-8'))
    paths={p.stem:p for p in (RES/'textures/item').glob('*.png')}
    prefix='item.wans_minego_expansion.'
    ordered=[(key.removeprefix(prefix),name) for key,name in lang.items() if key.startswith(prefix) and key.removeprefix(prefix) in paths]
    assert len(ordered)==len(paths) and len(paths)>=32
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20)
    small=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',12)
    pages=[];records=[]
    for page in range((len(paths)+7)//8):
        sheet=Image.new('RGB',(1200,680),(24,26,33))
        draw=ImageDraw.Draw(sheet)
        for slot,(stem,label) in enumerate(ordered[page*8:(page+1)*8]):
            number=page*8+slot+1
            x,y=slot%4*300,slot//4*340
            native=Image.open(paths[stem]).convert('RGBA')
            assert native.size==(18,18)
            sheet.paste(native.resize((252,252),Image.Resampling.NEAREST),(x+24,y+12),native.resize((252,252),Image.Resampling.NEAREST))
            caption=f'{number:02d}  {label}'
            caption_font=font
            while draw.textlength(caption,font=caption_font)>282:
                caption_font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',caption_font.size-1)
            draw.text((x+150,y+280),caption,font=caption_font,fill=(238,242,248),anchor='mt')
            draw.text((x+150,y+313),stem,font=small,fill=(160,170,190),anchor='mt')
            records.append({'number':number,'name':label,'id':'wans_minego_expansion:'+stem,'source':str(paths[stem]),'sha256':hashlib.sha256(paths[stem].read_bytes()).hexdigest()})
        output=OUT/f'icons-{page*8+1:02d}-{(page+1)*8:02d}.png'
        sheet.save(output);pages.append(sheet)
    overview=Image.new('RGB',(1200,len(pages)*680))
    for i,page in enumerate(pages):overview.paste(page,(0,i*680))
    overview.save(OUT/f'all-{len(paths)}-icons.png')
    (OUT/'manifest.json').write_text(json.dumps({'basis':'current 0.6.0 source; includes accepted school fixes and new Foolish exploration stones','items':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=['# 魂石图标审阅目录','', '依据 0.6.0 当前源码资源；包含原有图标修正与 Foolish 新探索魂石。编号与本目录预览图一致。','', '| 编号 | 名称 | 物品 ID |','| --- | --- | --- |']
    rows += [f"| {r['number']:02d} | {r['name']} | `{r['id']}` |" for r in records]
    (OUT/'index.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    print(f'Exported {len(records)} current source icons to {OUT}')
    for r in records:print(f"{r['number']:02d} {r['name']}")

if __name__=='__main__':main()
