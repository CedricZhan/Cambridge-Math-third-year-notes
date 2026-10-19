from PIL import Image
from pathlib import Path
out=Path('tex/figures/dynamical-systems')
crops=[(1,'unstable-nodes',(604,323,1040,982)),(1,'stable-nodes',(12,790,687,1105)),(1,'focus',(555,1250,1039,1578)),(2,'stellar-nodes',(600,309,1036,585)),(2,'improper-node',(535,615,1043,1010)),(2,'centre',(664,1051,1040,1314)),(2,'line-fixed-points',(551,1362,1033,1578)),(3,'shear',(351,280,1010,558)),(3,'classification',(46,613,1037,1074)),(4,'distorted',(40,320,1040,588))]
for page,name,box in crops:
    im=Image.open(f'tmp/lecture5/hi-{page}.png')
    im.crop(tuple(round(v*1.5) for v in box)).save(out/f'lecture5-{name}.png')
