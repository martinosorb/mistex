import mistex
import os
import sys

if len(sys.argv) <= 1:
    raise ValueError('No input files.')

file = sys.argv[1]
fname = os.path.splitext(os.path.basename(file))[0]
SOURCE_DIR = os.path.dirname(os.path.abspath(file))
HERE = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.join(HERE, '..', 'tmp')
TEX_TARGET_FILE = os.path.join(TMP_DIR, 'mistexfile')
PDF_TARGET_FILE = os.path.join(SOURCE_DIR, fname + '.pdf')
STYLEFILE = os.path.join(HERE, '..', 'styles', 'structure2')

rendered_file = mistex.md2latex(STYLEFILE).read(file)

with open(TEX_TARGET_FILE + '.tex', 'w') as F:
    F.write(rendered_file)

sh = (
    f'latexmk -cd -xelatex -shell-escape {TEX_TARGET_FILE}.tex '
    f'&& cp {TEX_TARGET_FILE}.pdf {PDF_TARGET_FILE}'
)

os.system(sh)
