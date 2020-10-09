import mistex
import argparse
from pathlib import Path

GENERATED_TEX = Path("mistex_out.tex")
stylefile = None


parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="Input file.", type=str, default=None)
parser.add_argument(
    "--out", help="Output file.", type=str, default=None
)
parser.add_argument(
    "--pdf", action="store_true",
    help="Also compile the resulting pure-tex file to pdf using latexmk."
)
parser.add_argument(
    "--cachedir", default=None,
    help="Assign a custom directory for LaTeX compilation and auxiliary files."
)
args = parser.parse_args()

if args.input_file is None:
    raise ValueError('No input files.')
if args.out is None:
    if args.pdf:
        args.out = Path(args.input_file).with_suffix(".pdf")
    else:
        args.out = str(Path(args.input_file).with_suffix("")) + "_mis.tex"
if args.cachedir is None:
    # we put the cache in output_folder/latex_cache/input_file_name
    output_folder = Path(args.out).parent
    input_file_name = Path(args.input_file).stem
    args.cachedir = output_folder / "latex_cache" / input_file_name


# run the md parser
rendered_file = mistex.md2latex(stylefile=stylefile, cachedir=args.cachedir).read(args.input_file)
# save the result to the tmp directory
saved_pure_tex = GENERATED_TEX if args.pdf else args.out
with open(saved_pure_tex, "w") as F:
    F.write(rendered_file)

if args.pdf:
    # compile the result we just saved
    mistex.tex2pdf(GENERATED_TEX, args.out, args.cachedir)
    GENERATED_TEX.unlink()
