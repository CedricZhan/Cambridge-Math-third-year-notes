from pathlib import Path
p=Path('tex/dynamical-systems.tex')
s=p.read_text(encoding='utf-8')
a=Path('tmp/lecture5/addition.tex').read_text(encoding='utf-8-sig')
assert 'End of Lecture 5' not in s
p.write_text(s.replace('\\end{document}', a+'\n\\end{document}'),encoding='utf-8')
