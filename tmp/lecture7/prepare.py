from pathlib import Path
from PIL import Image, ImageDraw
import json

root = Path(__file__).resolve().parents[2]
out = root / 'tex/figures/dynamical-systems'
crops = [
    (1, 'stable-focus', (780, 985, 1130, 1185)),
    (1, 'unstable-focus', (845, 1210, 1130, 1365)),
    (1, 'nonlinear-centre', (830, 1365, 1130, 1665)),
    (2, 'line-fixed-points', (820, 110, 1130, 295)),
    (2, 'saddle-node', (650, 295, 1120, 655)),
    (2, 'nonlinear-saddle', (470, 780, 1110, 1035)),
    (2, 'polar-sectors', (55, 1235, 1120, 1665)),
    (3, 'nullclines', (35, 685, 515, 1005)),
    (3, 'phase-portrait', (540, 675, 1110, 1080)),
]
manifest = []
for page, name, box in crops:
    im = Image.open(root / f'tmp/lecture7/high-{page}.png')
    preview = Image.open(root / f'tmp/lecture7/page-{page}.png')
    sx, sy = im.width / preview.width, im.height / preview.height
    rect = tuple(round(v * (sx if i % 2 == 0 else sy)) for i, v in enumerate(box))
    filename = f'lecture7-{name}.png'
    cropped = im.crop(rect)
    masks = []
    if name == 'nonlinear-saddle':
        masks = [(470, 780, 740, 970)]
    elif name == 'saddle-node':
        masks = [(845, 295, 1120, 345)]
    draw = ImageDraw.Draw(cropped)
    for x0, y0, x1, y1 in masks:
        draw.rectangle((round((x0-box[0])*sx), round((y0-box[1])*sy),
                        round((x1-box[0])*sx), round((y1-box[1])*sy)), fill='white')
    cropped.save(out / filename)
    manifest.append(dict(file=filename, source='Lecture7.pdf', pdf_page=page,
                         handwritten_page=25+page, crop_pixels=rect, dpi=250,
                         excluded_adjacent_text_rectangles=masks))
(out / 'lecture7-sources.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
source = root / 'tex/dynamical-systems.tex'
text = source.read_text(encoding='utf-8')
addition = (root / 'tmp/lecture7/addition.tex').read_text(encoding='utf-8').replace('centrelines', 'contours')
if 'End of Lecture 7' in text:
    raise SystemExit('Screenshots refreshed; lecture already inserted.')
assert text.count('\\end{document}') == 1
source.write_text(text.replace('\\end{document}', addition+'\\end{document}'), encoding='utf-8')
