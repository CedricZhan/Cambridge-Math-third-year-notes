from pathlib import Path
from PIL import Image, ImageDraw
exec(Path('tmp/lecture5/crop.py').read_text(encoding='utf-8-sig'))
fixes={'stable-nodes':[(592,790,687,982)],'classification':[(46,1048,789,1074)],'shear':[(351,280,627,445)],'distorted':[(40,320,435,340)]}
for page,name,box in crops:
    if name not in fixes: continue
    im=Image.open(f'tmp/lecture5/hi-{page}.png')
    d=ImageDraw.Draw(im)
    for r in fixes[name]: d.rectangle(tuple(round(v*1.5) for v in r),fill='white')
    im.crop(tuple(round(v*1.5) for v in box)).save(out/f'lecture5-{name}.png')
p=Path('tex/dynamical-systems.tex')
s=p.read_text(encoding='utf-8').replace('in \\underline{autonomous Hamiltonian} systems.', 'in \\underline{autonomous} \\underline{Hamiltonian} systems.')
p.write_text(s,encoding='utf-8')
