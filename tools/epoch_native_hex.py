"""Editable whole-stone designs on one 18px grid; no raster downsampling."""
from PIL import Image, ImageDraw

SIZE = 18
HEX = [(5, 1), (12, 1), (16, 8), (12, 16), (5, 16), (1, 8)]


def ramp(s):
    return tuple(tuple(bytes.fromhex(c)) + (255,) for c in s.split())


BRONZE = ramp('30221e 745039 b48850 e2bd7b ffedb5')
JADE = ramp('103d36 226b58 4bab7b a0dec0 e1fff0')
STEEL = ramp('172433 3d5268 738fa8 b8d7eb f1fbff')
GOLD = ramp('51351e 966126 c69441 eed17e fff0b1')
PURPLE = ramp('281c3f 50395e 88618b c4a3c7 f8dfed')
INK = ramp('1d2228 354043 566763 9fada0 e1e7cb')
PAPER = ramp('5b4237 967955 c6ac7b e6d6a8 fff2cb')
FIRE = ramp('471c22 9d3625 df682d f3b44e fff2ac')
RUST = ramp('382b2d 754936 ae7148 d7a875 f7d7a3')
PINK = ramp('422044 874066 c579a0 eaaac9 ffe2ec')
PALE_JADE = ramp('233d3d 547b70 99b9a1 c8dfba f0f8dc')

THEMES = {
    'fangzun': ('刻印型', '青铜印玺：整面凹刻与玉青铜锈'),
    'cangyao': ('结构型', '苍蓝磁石：相向磁极与环形回路'),
    'zixu': ('镶嵌型', '玉墨手卷：纸带贯穿紫玉本体'),
    'zhenyan': ('分区型', '火铳炮势：冷铁炮管与橙色热腔'),
    'goldenhou': ('结构型', '紫金铃火：金壳、紫玉内腔与朱绳'),
    'general': ('包覆型', '陶俑军令：赤旗斜覆青铜陶石'),
    'magnetic_steel': ('材质型', '磁钢晶片：整块冷蓝分层金属'),
    'damascene': ('材质型', '龙镔钢：暗钢中的银色流动锻纹'),
    'bronze': ('材质型', '青铜铸甲：铸造接缝与青绿铜锈'),
    'jade': ('材质型', '玉璧：通透绿玉与真实环状暗孔'),
    'talisman': ('包覆型', '朱砂符纸：暖纸斜包本体与朱砂笔势'),
    'type': ('结构型', '六字印版：六块阴刻活字拼装'),
    'ghost_jade': ('镶嵌型', '幽玉佩：月弧玉环与红色悬绳'),
    'pyrotemper': ('材质型', '燧炼熔石：红黑结壳与贯穿熔缝'),
    'classics': ('包覆型', '典籍：紫色封皮、纸页与金色书扣'),
    'cauldron': ('结构型', '双耳鼎：青铜耳柄与鼎足参与本体'),
    'tiger': ('镶嵌型', '炮虎卫：陶虎斜纹中嵌入冷铁炮口'),
    'rusted': ('材质型', '镀锈先民：斑驳锈铜与氧化裂隙'),
    'explorer': ('图景型', '四域探索：玉镜、桑牧、鹤浪与狼烟'),
    'celesterral': ('分区型', '玄黄：上部银蓝与下部金土合铸'),
    'four_sovereigns': ('镶嵌型', '四尊：青铜、苍蓝、玉墨和火铳四区'),
    'epoch': ('晶体型', '棠煌：棠花瓣状粉晶与金绿玉座'),
}


class Grid:
    def __init__(self, material):
        self.im = Image.new('RGBA', (SIZE, SIZE))
        self.d = ImageDraw.Draw(self.im)
        self.m = material
        self.mask = Image.new('L', (SIZE, SIZE))
        ImageDraw.Draw(self.mask).polygon(HEX, fill=255)
        self.poly(HEX, material[2])
        # Large, deliberate facets rather than a small dark center disk.
        self.poly([(5,1),(12,1),(8,6),(1,8)], material[3])
        self.poly([(1,8),(8,6),(6,13),(5,16)], material[2])
        self.poly([(12,1),(16,8),(12,16),(11,8),(8,6)], material[1])
        self.poly([(5,16),(6,13),(11,8),(12,16)], material[1])
        self.line([(5,2),(10,2)], material[4])
        self.line([(3,5),(2,7)], material[4])

    def poly(self, pts, c):
        self.d.polygon(pts, fill=c)

    def rect(self, box, c):
        self.d.rectangle(box, fill=c)

    def line(self, pts, c, width=1):
        self.d.line(pts, fill=c, width=width)

    def dot(self, x, y, c):
        if 0 <= x < SIZE and 0 <= y < SIZE:
            self.im.putpixel((x, y), c)

    def finish(self):
        # Every design shares the requested unmistakable hexagonal silhouette.
        # All material strokes are clipped on this same native grid.
        for y in range(SIZE):
            for x in range(SIZE):
                if not self.mask.getpixel((x,y)):
                    self.im.putpixel((x,y),(0,0,0,0))
        for y in range(SIZE):
            for x in range(SIZE):
                if not self.mask.getpixel((x,y)):
                    continue
                outside_left = x == 0 or not self.mask.getpixel((x-1,y))
                outside_top = y == 0 or not self.mask.getpixel((x,y-1))
                outside_right = x == 17 or not self.mask.getpixel((x+1,y))
                outside_bottom = y == 17 or not self.mask.getpixel((x,y+1))
                if outside_left or outside_top:
                    self.im.putpixel((x,y), self.m[3] if y < 10 else self.m[1])
                elif outside_right or outside_bottom:
                    self.im.putpixel((x,y), self.m[0])
        assert self.im.size == (18,18)
        assert set(self.im.getchannel('A').getdata()) == {0,255}
        return self.im


def render_hex(key, info=None, grid_factory=None):
    material = {
        'fangzun':BRONZE, 'cangyao':STEEL, 'zixu':PURPLE, 'zhenyan':INK,
        'goldenhou':GOLD, 'general':BRONZE, 'magnetic_steel':STEEL,
        'damascene':INK, 'bronze':BRONZE, 'jade':JADE, 'talisman':PAPER,
        'type':STEEL, 'ghost_jade':PALE_JADE, 'pyrotemper':FIRE,
        'classics':PURPLE, 'cauldron':BRONZE, 'tiger':RUST,
        'rusted':RUST, 'explorer':JADE, 'celesterral':GOLD,
        'four_sovereigns':GOLD, 'epoch':PINK,
    }[key]
    g = (grid_factory or Grid)(material)
    if key == 'fangzun':
        # Recessed channels span the whole cast seal face.
        g.rect((4,4,13,13),BRONZE[0]); g.rect((5,5,12,12),BRONZE[2])
        for path in [[(6,5),(6,9),(10,9),(10,7)],[(12,6),(8,6),(8,8)],[(5,11),(8,11),(8,12)],[(10,11),(12,11),(12,12)]]:
            g.line(path,BRONZE[0])
        g.line([(4,4),(12,4)],BRONZE[4]);g.line([(4,5),(4,11)],BRONZE[3])
        g.dot(3,10,JADE[1]);g.dot(12,14,JADE[2]);g.dot(5,14,JADE[1])
    elif key == 'cangyao':
        # Magnetic poles are part of the metal body, not an inset U icon.
        g.poly([(4,3),(7,3),(7,11),(10,11),(10,3),(13,3),(13,12),(11,14),(6,14),(4,12)],STEEL[0])
        g.rect((4,3,6,10),JADE[2]);g.rect((10,3,12,10),STEEL[2])
        g.rect((4,3,6,5),JADE[4]);g.rect((10,3,12,5),STEEL[4])
        g.line([(4,11),(6,13),(11,13),(12,11)],STEEL[3],2)
        g.line([(7,7),(9,7)],JADE[3]);g.dot(8,5,JADE[4]);g.dot(8,9,STEEL[4])
    elif key == 'zixu':
        g.poly([(8,2),(12,3),(10,15),(5,14)],PAPER[1])
        g.poly([(8,3),(11,4),(9,13),(6,13)],PAPER[3])
        g.line([(8,6),(9,6),(8,8),(9,9),(7,11)],INK[1])
        g.line([(6,3),(13,4)],PURPLE[1],2);g.line([(4,13),(10,15)],PURPLE[1],2)
        g.dot(6,3,GOLD[3]);g.dot(13,4,GOLD[2]);g.dot(4,13,GOLD[3]);g.dot(10,15,GOLD[2])
        g.line([(3,7),(6,8),(5,11)],JADE[2],2)
    elif key == 'zhenyan':
        g.line([(3,13),(6,10),(7,7),(12,4)],FIRE[1],3)
        g.line([(3,13),(6,10),(8,7),(12,4)],FIRE[3]);g.dot(7,9,FIRE[4])
        g.poly([(8,5),(13,4),(15,6),(15,9),(10,10),(8,8)],STEEL[0])
        g.line([(9,5),(13,5)],STEEL[3]);g.rect((10,6,13,8),STEEL[2])
        g.rect((14,6,15,8),INK[0]);g.dot(13,6,STEEL[4]);g.line([(5,4),(7,5)],INK[3])
    elif key == 'goldenhou':
        g.poly([(6,5),(11,5),(12,11),(14,13),(4,13),(5,11)],GOLD[0])
        g.poly([(7,6),(10,6),(11,11),(6,11)],PURPLE[2])
        g.line([(6,5),(5,11),(4,13),(13,13)],GOLD[3],2)
        g.line([(11,5),(12,11)],GOLD[2]);g.line([(7,3),(7,2),(10,2),(11,3),(10,4)],FIRE[1])
        g.line([(7,6),(7,9)],PURPLE[4]);g.dot(8,14,GOLD[4]);g.dot(9,14,GOLD[2])
    elif key == 'general':
        g.poly([(3,4),(11,3),(14,6),(12,13),(5,12)],FIRE[1])
        g.poly([(4,4),(10,4),(12,6),(6,8)],FIRE[2])
        g.poly([(6,8),(12,6),(11,12),(5,11)],FIRE[1])
        g.line([(5,3),(5,14)],BRONZE[0],2);g.line([(4,3),(4,13)],GOLD[3])
        g.line([(6,8),(12,6)],GOLD[2]);g.rect((9,8,10,10),BRONZE[3]);g.dot(10,9,BRONZE[0])
    elif key == 'magnetic_steel':
        g.poly([(3,5),(10,2),(14,5),(6,9)],STEEL[2])
        g.line([(3,6),(10,3),(13,5)],STEEL[4])
        g.poly([(3,9),(12,5),(15,8),(6,13)],STEEL[0])
        g.line([(3,10),(12,6),(14,8)],STEEL[3])
        g.poly([(5,13),(14,9),(13,13),(9,16)],STEEL[2])
        g.line([(6,13),(13,10)],STEEL[4]);g.line([(4,8),(6,8)],PURPLE[2])
    elif key == 'damascene':
        for pts in [[(5,3),(7,5),(6,8),(8,11),(7,15)],[(9,2),(11,5),(9,8),(11,12),(10,15)],[(13,4),(14,7),(12,10),(13,12)]]:
            g.line(pts,INK[0],3);g.line(pts,INK[3])
        g.line([(3,7),(4,9),(3,11)],INK[2]);g.dot(6,4,INK[4])
    elif key == 'bronze':
        g.poly([(4,4),(12,3),(14,8),(10,15),(5,13)],BRONZE[2])
        g.line([(4,4),(12,3),(14,8)],BRONZE[3]);g.line([(4,5),(5,12),(10,15)],BRONZE[0])
        g.line([(8,4),(9,13)],BRONZE[1]);g.line([(5,8),(13,7)],BRONZE[1])
        for x,y in [(5,5),(11,5),(6,11),(11,10)]:g.dot(x,y,BRONZE[4])
        g.poly([(11,12),(13,9),(14,12),(11,15),(8,15)],JADE[1]);g.dot(12,12,JADE[2]);g.dot(4,9,JADE[2])
    elif key == 'jade':
        g.poly([(6,4),(11,4),(14,7),(13,12),(10,14),(5,12),(3,8)],JADE[2])
        g.poly([(6,4),(11,4),(8,6),(4,8)],JADE[3])
        g.poly([(7,6),(10,6),(12,8),(11,11),(8,12),(6,10),(5,8)],JADE[0])
        g.poly([(7,7),(10,7),(11,9),(9,11),(7,10),(6,8)],JADE[1])
        g.line([(5,5),(8,4),(10,4)],JADE[4]);g.line([(12,7),(13,9),(12,11)],JADE[3]);g.dot(5,11,JADE[4])
    elif key == 'talisman':
        g.poly([(5,2),(12,4),(12,12),(9,16),(4,13)],PAPER[1])
        g.poly([(5,3),(11,4),(10,13),(8,15),(4,12)],PAPER[3])
        g.line([(5,4),(9,4)],PAPER[4]);g.line([(11,5),(10,12)],PAPER[2])
        g.line([(7,5),(9,6),(6,8),(9,9),(7,11),(8,13)],FIRE[1],2)
        g.dot(7,5,FIRE[2]);g.line([(4,12),(6,13)],PAPER[2])
    elif key == 'type':
        for i,(x,y) in enumerate([(4,3),(9,3),(3,7),(9,7),(4,11),(9,11)]):
            g.rect((x,y,x+3,y+3),STEEL[0]);g.line([(x,y),(x+3,y)],STEEL[3]);g.line([(x,y+1),(x,y+2)],STEEL[2])
            g.dot(x+1,y+1,STEEL[4]);g.dot(x+2,y+1 if i%2 else y+2,STEEL[4])
            if i in (1,4):g.dot(x+1,y+2,STEEL[2])
    elif key == 'ghost_jade':
        g.poly([(8,4),(12,5),(14,8),(13,12),(10,14),(6,13),(4,10),(4,7)],PALE_JADE[3])
        g.poly([(8,5),(12,6),(10,8),(9,11),(6,11),(5,9)],PALE_JADE[0])
        g.poly([(10,5),(12,6),(13,8),(12,11),(9,13)],PALE_JADE[2])
        g.line([(5,7),(5,9),(7,12)],PALE_JADE[4]);g.line([(9,3),(12,2),(14,3),(14,5)],FIRE[1])
        g.line([(7,13),(6,15),(4,15)],FIRE[1]);g.dot(5,14,FIRE[2])
    elif key == 'pyrotemper':
        g.poly([(3,5),(8,2),(12,4),(10,8),(5,10)],FIRE[1])
        g.poly([(10,8),(14,5),(15,11),(11,15),(8,13)],INK[0])
        g.line([(3,10),(6,8),(8,9),(10,6),(13,7),(15,5)],FIRE[2],3)
        g.line([(3,10),(6,8),(8,9),(10,6),(13,7),(15,5)],FIRE[4])
        g.line([(8,9),(9,12),(7,15)],FIRE[3]);g.line([(4,5),(7,3)],FIRE[3]);g.dot(12,12,FIRE[1])
    elif key == 'classics':
        g.poly([(5,3),(13,5),(12,14),(4,12)],PAPER[1])
        g.poly([(6,4),(12,6),(11,13),(5,11)],PAPER[3])
        for y in (7,9,11):g.line([(6,y),(10,y+1)],PAPER[1])
        g.poly([(4,3),(7,4),(6,13),(3,11)],PURPLE[1])
        g.line([(4,3),(12,5)],PURPLE[4]);g.line([(4,12),(12,14)],PURPLE[0],2)
        g.line([(9,4),(8,13)],GOLD[2]);g.dot(9,6,GOLD[4]);g.dot(8,12,GOLD[4])
    elif key == 'cauldron':
        g.rect((3,4,5,8),BRONZE[0]);g.rect((12,4,14,8),BRONZE[0])
        g.line([(3,7),(3,4),(5,4),(5,6)],JADE[2]);g.line([(12,6),(12,4),(14,4),(14,7)],BRONZE[3])
        g.poly([(5,6),(12,6),(13,11),(11,13),(6,13),(4,11)],JADE[1])
        g.line([(4,7),(13,7)],GOLD[3]);g.line([(5,8),(5,11),(7,12),(11,12)],BRONZE[2])
        g.rect((7,9,10,10),BRONZE[3]);g.rect((8,9,9,9),BRONZE[0])
        g.rect((5,13,6,15),BRONZE[2]);g.rect((11,13,12,15),BRONZE[1]);g.dot(5,13,BRONZE[4])
    elif key == 'tiger':
        g.line([(4,3),(8,6),(6,8)],INK[0],2);g.line([(10,3),(11,6),(13,7)],INK[0],2)
        g.line([(3,10),(6,11),(5,14)],INK[0],2);g.line([(12,11),(10,14)],INK[0],2)
        g.line([(5,6),(6,7)],GOLD[4]);g.line([(11,6),(10,7)],GOLD[3])
        g.poly([(7,8),(13,8),(14,10),(12,12),(7,11)],STEEL[0])
        g.line([(7,8),(12,8)],STEEL[3]);g.rect((8,9,11,10),STEEL[2]);g.rect((12,9,13,10),INK[0])
        g.dot(6,12,PAPER[3]);g.dot(7,13,PAPER[2])
    elif key == 'rusted':
        for pts in [[(3,7),(5,5),(7,5),(6,8),(4,10)],[(10,3),(13,5),(12,8),(9,6)],[(7,11),(11,10),(13,12),(10,15),(7,14)]]:
            g.poly(pts,JADE[1])
        g.line([(8,3),(7,7),(9,9),(8,13),(6,15)],RUST[0]);g.line([(4,11),(7,10),(10,11),(14,9)],RUST[0])
        for x,y in [(5,6),(11,5),(9,12),(11,13)]:g.dot(x,y,JADE[2])
        g.dot(5,10,RUST[4]);g.dot(12,8,RUST[2])
    elif key == 'explorer':
        g.poly([(2,8),(5,2),(9,2),(8,8)],PALE_JADE[2]);g.line([(4,6),(6,3),(8,3)],PALE_JADE[4])
        g.poly([(9,2),(12,2),(15,8),(9,8)],JADE[1]);g.line([(11,3),(10,7)],JADE[3]);g.dot(12,5,JADE[2])
        g.poly([(2,9),(8,9),(8,15),(5,15)],STEEL[2]);g.line([(3,10),(6,10),(7,11)],STEEL[4]);g.line([(5,13),(7,13)],STEEL[3])
        g.poly([(9,9),(15,9),(12,15),(9,15)],RUST[1]);g.line([(10,11),(12,10),(14,11)],RUST[3]);g.dot(11,14,INK[0])
        g.line([(8,2),(8,15)],GOLD[2]);g.line([(2,8),(15,8)],GOLD[3]);g.dot(8,8,GOLD[4])
    elif key == 'celesterral':
        g.poly([(5,2),(12,2),(15,8),(2,8)],STEEL[2]);g.poly([(5,2),(11,2),(8,6),(3,7)],STEEL[3])
        g.line([(5,3),(9,3)],STEEL[4]);g.poly([(3,9),(15,9),(12,15),(5,15)],GOLD[2])
        g.poly([(9,9),(14,10),(12,15),(7,15)],GOLD[1]);g.line([(3,8),(6,9),(9,8),(12,9),(15,8)],GOLD[4])
        g.line([(5,11),(6,13),(8,12)],GOLD[3]);g.dot(11,11,GOLD[4])
    elif key == 'four_sovereigns':
        g.poly([(5,2),(8,2),(8,8),(2,8)],BRONZE[2]);g.line([(4,5),(7,5),(7,7)],BRONZE[0])
        g.poly([(9,2),(12,2),(15,8),(9,8)],STEEL[2]);g.line([(11,3),(10,5),(12,7)],STEEL[4])
        g.poly([(2,9),(8,9),(8,15),(5,15)],PURPLE[2]);g.line([(4,11),(6,11),(5,13),(7,14)],PAPER[3])
        g.poly([(9,9),(15,9),(12,15),(9,15)],FIRE[1]);g.line([(10,11),(13,11)],STEEL[3],2);g.dot(13,11,INK[0])
        g.line([(8,2),(8,15)],GOLD[2]);g.line([(2,8),(15,8)],GOLD[3]);g.rect((7,7,9,9),GOLD[1]);g.dot(8,8,GOLD[4])
    elif key == 'epoch':
        g.poly([(3,10),(5,7),(7,11),(9,10),(12,7),(15,10),(12,15),(5,15)],JADE[1])
        g.line([(3,10),(5,12),(6,10),(9,13),(12,10),(14,11)],GOLD[2])
        for pts,c in [([(8,2),(10,3),(9,7),(7,6)],PINK[3]),([(5,4),(7,5),(8,8),(5,8),(3,6)],PINK[2]),([(11,4),(14,6),(12,9),(9,8)],PINK[1]),([(5,9),(8,8),(8,12),(6,13),(4,11)],PINK[3]),([(9,9),(12,9),(13,11),(10,13),(8,11)],PINK[2])]:
            g.poly(pts,c)
        g.line([(8,3),(8,5)],PINK[4]);g.dot(5,6,PINK[4]);g.rect((7,7,9,9),GOLD[2]);g.dot(8,8,GOLD[4]);g.dot(5,14,GOLD[3]);g.dot(12,13,GOLD[3])
    else:
        raise KeyError(key)
    return g.finish()
