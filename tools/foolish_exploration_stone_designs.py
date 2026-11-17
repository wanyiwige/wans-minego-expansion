"""Ten material and nine biome/composite trials on the empty-stone grid."""
from preview_epoch_boss_portraits import NativeSurface
from preview_foolish_boss_stones import VIOLET,TEAL,BLUE,GREEN,TOXIC,PINK,SCARLET,RED,BONE,GOLD
from epoch_native_hex import ramp

METAL=ramp('282421 534842 81716a b09f96 dac9bd')
PURPLE_METAL=ramp('190c27 341545 5a286d 9252ac c58ee3')
COAT=ramp('211b18 453830 716054 a1917f d2c3ac')
SOIL=ramp('28251e 4d4738 796e56 a69778 d4c6a5')
ROSE_SOIL=ramp('351e24 69413f 986160 bc8b80 e7b9a5')
ASH=ramp('272220 4f443c 7e6e5b b3a18a e0cfb2')


def material(key):
    base={'sacilite':VIOLET,'thunderstone':TEAL,'corrosive':METAL,'blunt':METAL,
          'infernal':METAL,'keepsteel':PURPLE_METAL,'amber':BLUE,'slide':VIOLET,
          'parasitic':COAT,'soulcoat':COAT}[key]
    g=NativeSurface(base)
    if key=='sacilite':
        g.poly([(5,3),(8,2),(10,6),(8,12),(5,14),(3,9)],VIOLET[2])
        g.poly([(5,3),(8,2),(7,7),(3,9)],VIOLET[3])
        g.poly([(7,7),(10,6),(9,11),(5,14)],VIOLET[1])
        g.line([(5,4),(6,6),(5,9)],VIOLET[4]);g.line([(8,9),(7,12)],TEAL[3])
    elif key=='thunderstone':
        g.poly([(4,4),(8,3),(11,6),(10,12),(5,13),(3,9)],TEAL[2])
        g.poly([(4,4),(8,3),(6,8),(3,9)],TEAL[3])
        g.line([(8,4),(7,7),(9,8),(6,11)],TEAL[4]);g.line([(4,10),(6,12),(9,12)],TEAL[1])
        g.dot(10,6,TEAL[0]);g.dot(5,6,TEAL[4])
    elif key=='corrosive':
        g.poly([(4,4),(9,3),(11,6),(8,8),(3,7)],TOXIC[2])
        g.poly([(5,9),(9,8),(11,11),(8,14),(4,13)],TOXIC[1])
        g.line([(4,5),(7,4),(9,5)],TOXIC[4]);g.dot(4,8,METAL[0]);g.dot(9,10,METAL[0])
        g.dot(7,7,TOXIC[3]);g.line([(6,10),(6,12)],TOXIC[3])
    elif key=='blunt':
        g.poly([(3,5),(8,3),(12,6),(11,12),(6,14),(3,10)],METAL[2])
        g.line([(3,5),(8,3),(11,5)],METAL[3]);g.line([(3,9),(10,7)],METAL[1])
        g.line([(6,13),(10,11)],METAL[0]);g.dot(5,7,METAL[4]);g.dot(9,10,METAL[1])
    elif key=='infernal':
        g.poly([(3,6),(7,4),(11,6),(10,12),(6,14),(4,11)],METAL[1])
        g.line([(3,6),(7,4),(10,5)],METAL[3]);g.line([(5,8),(8,7),(10,9)],METAL[0])
        for x,y in [(4,9),(6,11),(8,6),(9,10),(7,13)]:g.dot(x,y,METAL[2])
        g.line([(6,9),(7,10),(7,12)],RED[1]);g.dot(7,10,RED[3]);g.dot(5,6,METAL[4])
    elif key=='keepsteel':
        for pts,c in [([(3,5),(9,3),(12,5),(6,8)],PURPLE_METAL[2]),([(3,9),(10,6),(11,10),(6,13)],PURPLE_METAL[1]),([(6,13),(11,10),(10,14),(7,15)],PURPLE_METAL[2])]:g.poly(pts,c)
        g.line([(3,6),(9,4),(11,5)],PURPLE_METAL[4]);g.line([(4,10),(9,8)],PURPLE_METAL[3])
        g.line([(7,12),(10,11)],PURPLE_METAL[0]);g.dot(5,9,PURPLE_METAL[4])
    elif key=='amber':
        g.poly([(5,4),(9,3),(12,7),(10,12),(6,14),(3,10)],BLUE[2])
        g.poly([(5,4),(9,3),(7,7),(3,10)],BLUE[3])
        g.line([(6,6),(9,6),(10,8),(8,10),(6,9),(7,7)],TEAL[3])
        g.line([(5,11),(8,12),(10,10)],BLUE[1]);g.dot(7,8,TEAL[4]);g.dot(5,5,BLUE[4])
    elif key=='slide':
        g.poly([(4,4),(7,3),(10,6),(11,10),(8,14),(4,12)],VIOLET[1])
        g.line([(4,6),(9,5)],VIOLET[3],2);g.line([(4,9),(10,8)],VIOLET[2],2)
        g.line([(5,12),(9,11)],VIOLET[4]);g.line([(3,13),(6,14),(10,13)],VIOLET[0])
        g.dot(5,4,PINK[3]);g.dot(10,10,PINK[2])
    elif key=='parasitic':
        g.line([(4,13),(6,10),(8,7),(10,4)],SCARLET[0],3)
        g.line([(4,13),(6,10),(8,7),(10,4)],SCARLET[2])
        g.poly([(5,10),(3,8),(7,9)],SCARLET[1]);g.poly([(8,7),(10,8),(9,5)],SCARLET[1])
        g.dot(10,4,SCARLET[4]);g.dot(7,8,SCARLET[3]);g.dot(5,12,BONE[1])
    elif key=='soulcoat':
        g.poly([(4,4),(7,5),(6,12),(4,14),(3,9)],COAT[1])
        g.poly([(10,4),(8,5),(8,12),(11,13),(12,8)],COAT[0])
        g.line([(4,4),(6,6),(5,11)],COAT[3]);g.line([(10,4),(8,6),(9,11)],COAT[2])
        g.poly([(6,7),(8,7),(8,9),(6,9)],TEAL[3]);g.dot(6,7,TEAL[4])
        g.line([(4,13),(6,14)],COAT[3]);g.dot(10,12,COAT[2])
    return g.finish()


def biome(key):
    base={'bloom':VIOLET,'storm':TEAL,'time':BLUE,'scarlet':ROSE_SOIL,
          'waste':SOIL,'mire':GREEN,'growth':GREEN,'ash':ASH,'otherworld':BLUE}[key]
    g=NativeSurface(base)
    if key=='bloom':
        g.poly([(3,7),(6,4),(11,4),(12,10),(8,14),(4,12)],VIOLET[0])
        for pts,c in [([(4,5),(5,9),(3,10)],VIOLET[3]),([(7,4),(8,8),(6,11),(5,8)],VIOLET[2]),([(10,6),(11,10),(8,12),(8,9)],VIOLET[3])]:g.poly(pts,c)
        g.line([(6,12),(9,13)],VIOLET[1]);g.dot(7,5,VIOLET[4]);g.dot(9,11,TEAL[3])
    elif key=='storm':
        g.poly([(3,5),(5,3),(9,4),(11,6),(8,7),(4,7)],GREEN[1])
        g.line([(4,5),(7,4),(9,5)],GREEN[3]);g.line([(4,8),(3,11)],TEAL[4]);g.line([(7,8),(6,12)],TEAL[3]);g.line([(10,7),(9,10)],TEAL[4])
        g.poly([(4,13),(8,12),(11,13),(8,14)],TEAL[1]);g.dot(8,9,TEAL[0])
    elif key=='time':
        g.poly([(3,7),(6,5),(10,6),(12,10),(8,14),(4,12)],BLUE[2])
        g.line([(3,8),(6,7),(10,8)],BLUE[4]);g.line([(4,10),(7,9),(11,10)],BLUE[1])
        g.line([(5,12),(8,11),(10,12)],BLUE[3])
        for x,y in [(5,9),(8,8),(7,13),(9,11)]:g.dot(x,y,BLUE[4])
        g.poly([(9,4),(11,5),(10,7),(8,6)],GOLD[2]);g.dot(9,5,GOLD[4])
    elif key=='scarlet':
        g.poly([(3,7),(7,5),(11,6),(12,11),(8,14),(3,11)],ROSE_SOIL[1])
        g.line([(3,9),(7,8),(11,9)],ROSE_SOIL[3]);g.line([(4,12),(8,11),(10,12)],ROSE_SOIL[0])
        g.poly([(5,5),(6,4),(8,5),(7,7),(5,7)],PINK[2]);g.dot(6,5,PINK[4])
        g.line([(9,9),(9,7),(10,6)],SCARLET[2]);g.dot(10,6,SCARLET[3])
    elif key=='waste':
        g.line([(3,7),(7,6),(11,7)],SOIL[1]);g.line([(4,11),(8,10),(11,12)],SOIL[0])
        g.poly([(4,8),(7,8),(8,10),(6,12),(3,11)],TOXIC[1])
        g.line([(4,9),(6,9),(7,10)],TOXIC[3]);g.dot(5,10,TOXIC[4]);g.dot(9,7,SOIL[3])
        g.line([(9,11),(10,13),(8,14)],SOIL[1]);g.dot(10,9,TOXIC[2])
    elif key=='mire':
        g.poly([(3,7),(7,5),(11,7),(12,10),(9,14),(4,13)],SOIL[0])
        g.poly([(3,9),(6,8),(10,9),(11,11),(7,13),(4,12)],TEAL[1])
        g.line([(4,10),(6,10),(7,11)],TEAL[3]);g.line([(8,12),(10,11)],TEAL[2])
        g.poly([(5,6),(7,5),(8,7),(7,9),(4,8)],GREEN[2]);g.line([(5,7),(7,7)],GREEN[4])
        g.line([(10,4),(10,7)],GREEN[1]);g.dot(10,4,GREEN[3])
    elif key=='growth':
        g.line([(5,14),(7,10),(7,6),(8,3)],GREEN[1],2)
        for pts,c in [([(7,7),(4,4),(3,6),(5,8)],GREEN[3]),([(8,5),(11,4),(12,6),(8,8)],GREEN[2]),([(6,10),(3,9),(3,12),(5,13)],GREEN[2]),([(8,10),(11,9),(12,11),(8,13)],GREEN[3])]:g.poly(pts,c)
        g.line([(4,5),(6,7)],GREEN[4]);g.line([(9,10),(10,11)],GREEN[4]);g.dot(8,4,BONE[3]);g.dot(9,3,BONE[2])
    elif key=='ash':
        g.line([(4,4),(5,8),(4,12)],ASH[0],2);g.line([(8,3),(9,6),(8,10),(10,13)],ASH[1],2)
        g.line([(5,5),(6,8),(5,11)],ASH[3]);g.line([(10,6),(11,9),(10,11)],ASH[0])
        g.line([(3,12),(7,13),(10,12)],ASH[3]);g.dot(6,11,RED[2]);g.dot(9,10,RED[3]);g.dot(7,14,ASH[0])
    elif key=='otherworld':
        g.poly([(3,5),(6,3),(7,7),(3,9)],VIOLET[2]);g.line([(4,6),(5,7)],VIOLET[4])
        g.poly([(8,3),(11,5),(11,8),(8,7)],GREEN[2]);g.line([(9,4),(10,6)],GREEN[3])
        g.poly([(3,10),(7,8),(7,13),(5,14)],TEAL[2]);g.line([(4,11),(6,11)],TEAL[4])
        g.poly([(8,8),(12,9),(10,13),(8,14)],ROSE_SOIL[2]);g.line([(9,10),(11,11)],SOIL[2])
        g.line([(6,7),(8,8),(7,11)],BLUE[4]);g.dot(7,8,GOLD[3])
    return g.finish()


MATERIAL_THEMES={
 'sacilite':'紫色萦光晶面与青光折射','thunderstone':'青绿雷石与浅青导电脉',
 'corrosive':'灰褐金属上侵蚀的黄绿镭质','blunt':'钝灰褐金属与磨损层面',
 'infernal':'灰褐合金、熔铸孔隙与少量余热','keepsteel':'深紫固钢的交叠铸层',
 'amber':'蓝色琥珀与封存的青光旋涡','slide':'紫色滑行材料与斜向胎纹',
 'parasitic':'暗褐本体上的红色刺脊','soulcoat':'棕灰衣料、翻折衣襟与青色魂芯'}
BIOME_THEMES={
 'bloom':'紫晶洞穴中的多簇生长晶体','storm':'绿冠、青雨与积水表面',
 'time':'浅蓝时沙丘层与金色时果','scarlet':'猩褐土层、粉色膜与红色菌生',
 'waste':'灰褐废土、裂隙与毒色积液','mire':'暗泥池、绿色浮叶与青色水纹',
 'growth':'绿叶包覆本体与浅色花粉','ash':'灰褐炭木纹与零星残火',
 'otherworld':'晶洞、雨林、水泽与猩野地表交织'}


def extra_entries():
    result=[]
    for key,theme in MATERIAL_THEMES.items():result.append((f'foolish_{key}_material_soul_stone',lambda k=key:material(k),theme))
    for key,theme in BIOME_THEMES.items():result.append(('soul_of_otherworld' if key=='otherworld' else f'foolish_{key}_biome_soul_stone',lambda k=key:biome(k),theme))
    return result
