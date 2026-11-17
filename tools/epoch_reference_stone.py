"""Native 17px retexturing on Mine Fargo's empty soul stone and its perspective.

No resized image is used as the production input. Authoring coordinates project
to integer pixels; all pigment is lit by the original seven-level facet map.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import epoch_native_hex as authoring

REFERENCE = Path(__file__).resolve().parents[1] / 'art/epoch-whole-stone-redraw-20261012/empty-soul-stone-native.png'
SIZE = 17
THEMES = authoring.THEMES
THEMES.update({
    'fangzun':('柱体雕纹','棕铜雕纹柱体、冠饰与底部卷曲构件'),
    'cangyao':('环架结构','灰黑金属环、交错杆件与机械轴心'),
    'zixu':('卷面包覆','米白卷面、深靛蓝卷曲结构与金色末端'),
    'zhenyan':('机体结构','暗红褐机体、灰铁炮管与背部旗列'),
})


def project(p):
    x,y = p
    return round(1+(x-1)*.80), round(1+(y-1)*.90+(x-8)*.10)


def interpolate(material, value):
    stops=(36,81,140,206,243)
    if value<=stops[0]:return material[0]
    for i in range(4):
        if value<=stops[i+1]:
            t=(value-stops[i])/(stops[i+1]-stops[i])
            return tuple(round(material[i][c]*(1-t)+material[i+1][c]*t) for c in range(3))+(255,)
    return material[-1]


class ReferenceGrid:
    def __init__(self, material):
        self.reference=Image.open(REFERENCE).convert('RGBA')
        assert self.reference.size==(17,17)
        self.mask=self.reference.getchannel('A')
        self.m=material
        self.im=Image.new('RGBA',(SIZE,SIZE))
        for y in range(SIZE):
            for x in range(SIZE):
                p=self.reference.getpixel((x,y))
                if p[3]:self.im.putpixel((x,y),interpolate(material,p[0]))
        self.base=self.im.copy()

    def paint(self, coverage, color):
        for y in range(SIZE):
            for x in range(SIZE):
                ref=self.reference.getpixel((x,y))
                if coverage.getpixel((x,y)) and ref[3]:
                    # Keep the source camera/facet lighting even under overlays.
                    factor=.30+.70*(ref[0]-36)/(243-36)
                    self.im.putpixel((x,y),tuple(round(v*factor) for v in color[:3])+(255,))

    def poly(self, pts, c):
        coverage=Image.new('L',(SIZE,SIZE))
        ImageDraw.Draw(coverage).polygon([project(p) for p in pts],fill=255)
        self.paint(coverage,c)

    def rect(self, box, c):
        x1,y1,x2,y2=box
        self.poly([(x1,y1),(x2,y1),(x2,y2),(x1,y2)],c)

    def line(self, pts, c, width=1):
        coverage=Image.new('L',(SIZE,SIZE))
        ImageDraw.Draw(coverage).line([project(p) for p in pts],fill=255,width=width)
        self.paint(coverage,c)

    def dot(self, x, y, c):
        coverage=Image.new('L',(SIZE,SIZE));px,py=project((x,y))
        if 0<=px<SIZE and 0<=py<SIZE:coverage.putpixel((px,py),255)
        self.paint(coverage,c)

    def finish(self):
        # Preserve the reference's exact one-pixel side edges and top/bottom caps.
        # Theme geometry lives on its visible surfaces, never on a new silhouette.
        for y in range(SIZE):
            for x in range(SIZE):
                if not self.mask.getpixel((x,y)):
                    self.im.putpixel((x,y),(0,0,0,0));continue
                boundary=any(nx<0 or ny<0 or nx>=SIZE or ny>=SIZE or not self.mask.getpixel((nx,ny)) for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
                if boundary or x>=13:self.im.putpixel((x,y),self.base.getpixel((x,y)))
        assert self.im.getchannel('A').tobytes()==self.reference.getchannel('A').tobytes()
        return self.im


def render_reference(key, info=None):
    if key in ('fangzun','cangyao','zixu','zhenyan'):
        from preview_epoch_boss_portraits import render_fangzun,render_cangyao,render_zixu,render_zhenyan
        return {'fangzun':render_fangzun,'cangyao':render_cangyao,'zixu':render_zixu,'zhenyan':render_zhenyan}[key]()
    # Reuse editable surface strokes, without rendering the discarded hex canvas.
    return authoring.render_hex(key,info,grid_factory=ReferenceGrid)
