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

if args.out is None:
    # another suffix will be added later, either .pdf or .tex
    out = Path(args.input_file).with_suffix(".mistex")
else:
    out = Path(args.out).with_suffix("")
output_folder = out.parent
output_folder.mkdir(parents=True, exist_ok=True)

if args.cachedir is None:
    # we put the cache in output_folder/latex_cache/input_file_name
    cachedir = output_folder / "mistex_cache" / Path(args.input_file).stem
else:
    cachedir = Path(args.cachedir)

COMPILER = "latexmk"
FLAGS = [
    "-pdf",
    f"--outdir={cachedir}",
    "-xelatex",
    "-shell-escape",
]

# run the md parser
reader = md2latex(cachedir=cachedir)
pylatex_document = reader.parse(read_file(args.input_file))

# save the result to the tmp directory
if args.pdf:
    # pdf output name is the name only! the folder is the cache dir
    pylatex_document.generate_pdf(out.name, compiler=COMPILER, compiler_args=FLAGS)
    # copy the output PDF from the cache dir to here
    pdf_out_name = out.name + ".pdf"
    os.replace(cachedir / pdf_out_name, Path.cwd() / pdf_out_name)
else:
    pylatex_document.generate_tex(str(out))
