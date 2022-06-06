import argparse
import os
from pathlib import Path
from .core import md2latex


def read_file(filename):
    with open(filename, "rb") as f:
        file = f.read()
    file = file.decode('utf-8')
    return file


parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="Input file.", type=str, default=None)
parser.add_argument("--out", help="Output file.", type=str, default=None)
parser.add_argument("--pdf", action="store_true", help="Also compile the resulting pure-tex file to pdf using latexmk.")
parser.add_argument("--cachedir", default=None, help="Assign a custom directory for LaTeX compilation and auxiliary files.")
args = parser.parse_args()

if args.input_file is None:
    raise ValueError('No input files.')
input_file = Path(args.input_file)

if args.out is None:
    # another suffix will be added later, either .pdf or .tex
    out = Path(args.input_file).with_suffix(".mistex").name
    out = Path(out)
else:
    out = Path(args.out).with_suffix("")
output_folder = out.parent
output_folder.mkdir(parents=True, exist_ok=True)

if args.cachedir is None:
    cachedir = Path("mistex_cache") / input_file.stem
else:
    cachedir = Path(args.cachedir)


COMPILER = "latexmk"
FLAGS = [
    "-pdf",
    f"--outdir={cachedir.resolve()}",
    "-xelatex",
    "-shell-escape",
]

# run the md parser
reader = md2latex(cachedir=cachedir.resolve())
pylatex_document = reader.parse(read_file(input_file))

# save the result to the tmp directory
if args.pdf:
    # we have to generate where the input is, in order to use the images there
    # but the pdf will be generated in cachedir and this tex file will be removed.
    temp_location = input_file.parent / "mistex_out"
    pylatex_document.generate_pdf(temp_location, compiler=COMPILER, compiler_args=FLAGS, clean_tex=True)
    # copy the output PDF from the cache dir to the desired output
    os.replace(cachedir / "mistex_out.pdf", out.with_suffix(".pdf"))
else:
    pylatex_document.generate_tex(str(out))
