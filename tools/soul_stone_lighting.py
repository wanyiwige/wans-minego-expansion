"""Remove the inherited axial light ridge without repainting the center glyph."""
from PIL import Image

# Upper-right rim only; the 8x8 glyph and the primary upper-left light are outside this mask.
RIGHT_FACETS={(10,2),(11,2),(12,2),(12,3),(13,3),(14,3),(14,4),(13,5),(14,5),(15,5),(15,6),(16,6),(15,7),(16,7)}
RIGHT_RIDGE={(12,2),(14,3),(15,5),(16,6),(16,7)}
def luminance(rgb):return .2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2]

def clarify_upper_left(original: Image.Image) -> Image.Image:
    """Keep the key light, but separate its illuminated face from the upper-left ridge."""
    original=original.convert('RGBA');assert original.size==(18,18);result=original.copy()
    brightest=max(luminance(p) for p in original.getdata() if p[3])
    facets={(17-x,y) for x,y in RIGHT_FACETS}
    ridge={(17-x,y) for x,y in RIGHT_RIDGE}
    for x,y in facets:
        old=original.getpixel((x,y))
        if old[3] and luminance(old)>=brightest*.62:
            factor=.64 if (x,y) in ridge else .82
            result.putpixel((x,y),tuple(round(c*factor) for c in old[:3])+(old[3],))
    return result

def clarify_upper_right(original: Image.Image) -> Image.Image:
    original=original.convert('RGBA');result=original.copy();w,h=original.size
    # Reference brightness is sampled across the existing pixel grid, not across newly added detail.
    brightest=max(luminance(original.getpixel((min(w-1,round((x+.5)*w/18)),min(h-1,round((y+.5)*h/18)))))
                  for y in range(18) for x in range(18))
    candidates=[original.getpixel((min(w-1,round((x+.5)*w/18)),min(h-1,round((y+.5)*h/18)))) for x,y in RIGHT_FACETS]
    if max(luminance(p) for p in candidates if p[3])<brightest*.72:return result
    for x,y in RIGHT_FACETS:
        x0,x1=round(x*w/18),round((x+1)*w/18);y0,y1=round(y*h/18),round((y+1)*h/18)
        factor=.58 if (x,y) in RIGHT_RIDGE else .76
        for py in range(y0,y1):
            for px in range(x0,x1):
                old=original.getpixel((px,py))
                if old[3] and luminance(old)>=brightest*.60:
                    result.putpixel((px,py),tuple(round(c*factor) for c in old[:3])+(old[3],))
    return result

def soften_axis(sprite: Image.Image) -> Image.Image:
    assert sprite.size == (18,18)
    original=sprite.convert('RGBA');result=original.copy()
    for y in list(range(5))+list(range(13,18)):
        sample_y=min(16,max(1,y))
        while sample_y>1 and (original.getpixel((7,sample_y))[3]<128 or original.getpixel((10,sample_y))[3]<128):
            sample_y-=1
        left,right=original.getpixel((7,sample_y)),original.getpixel((10,sample_y))
        for x,t in [(8,1/3),(9,2/3)]:
            old=original.getpixel((x,y))
            if old[3]==0:continue
            rgb=tuple(round(left[c]*(1-t)+right[c]*t) for c in range(3))
            result.putpixel((x,y),rgb+(old[3],))
    return result

def soften_legacy_axis(original: Image.Image) -> Image.Image:
    """Preserve irregular historical pixels and canvas; modify only their thin axial band."""
    original=original.convert('RGBA');result=original.copy();w,h=original.size
    lo,hi=round(w*.47),round(w*.533)
    left_x,right_x=round(w*.435),round(w*.565)
    for y in list(range(round(h*5/18)))+list(range(round(h*.735),h)):
        sample_y=min(round(h*.88),max(round(h*.08),y))
        left,right=original.getpixel((left_x,sample_y)),original.getpixel((right_x,sample_y))
        if left[3]<128 or right[3]<128:
            sample_y=round(h*(.10 if y<h/2 else .85))
            left,right=original.getpixel((left_x,sample_y)),original.getpixel((right_x,sample_y))
        # Use one solid facet color per existing row rather than adding a horizontal gradient.
        rgb=tuple(round(left[c]*.35+right[c]*.65) for c in range(3))
        for x in range(lo,hi):
            old=original.getpixel((x,y))
            if old[3]:result.putpixel((x,y),rgb+(old[3],))
    return result
