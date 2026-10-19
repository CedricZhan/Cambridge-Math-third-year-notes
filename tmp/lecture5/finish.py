from pathlib import Path
from PIL import Image, ImageDraw
p=Path('tex/dynamical-systems.tex'); s=p.read_text(encoding='utf-8')
s=s.replace('of $H(x,y)$ in \\underline{autonomous} \\underline{Hamiltonian} systems.', 'of $H(x,y)$\\\\\nin \\underline{autonomous Hamiltonian} systems.')
s=s.replace('Get different \\underline{patterns} depending on','\\raggedright\nGet different \\underline{patterns} depending on')
p.write_text(s,encoding='utf-8')
for name,rect in [('shear',(0,0,465,47)),('line-fixed-points',(0,0,723,18)),('stable-nodes',(0,459,140,473))]:
 p=Path('tex/figures/dynamical-systems')/f'lecture5-{name}.png'
 im=Image.open(p); ImageDraw.Draw(im).rectangle(rect,fill='white'); im.save(p)
