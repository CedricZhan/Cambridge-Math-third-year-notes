from PIL import Image, ImageDraw
from pathlib import Path
regions={'centre':[(664,1051,740,1090)],'line-fixed-points':[(760,1362,1033,1380)],'distorted':[(40,580,120,588)]}
exec(Path('tmp/lecture5/refine.py').read_text(encoding='utf-8-sig'))
for page,name,box in crops:
    if name not in regions: continue
    p=out/f'lecture5-{name}.png'
    im=Image.open(p); d=ImageDraw.Draw(im)
    for r in regions[name]:
        d.rectangle(tuple(round((v-box[i%2])*1.5) for i,v in enumerate(r)),fill='white')
    im.save(p)
