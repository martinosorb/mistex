import mistex
import os
import sys

if len(sys.argv) <= 1:
    raise ValueError('No input files.')

file = sys.argv[1]
r = mistex.latex.read(file)
fname = file.strip('.md')

with open(f'{fname}.tex', 'w') as F:
    F.write(r)

sh = (
      f'latexmk -xelatex -shell-escape {fname}.tex '
      # f'&& open {fname}.pdf; '
      # f'rm {fname}' + '.{log,aux,out};'
      # f'rm -r _minted-{fname}'
)

os.system(sh)
