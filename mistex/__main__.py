import mistex
import argparse
from pathlib import Path


HERE = Path(__file__).resolve().parent
GENERATED_TEX = Path("mistex_out.tex")
stylefile = None


parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="Input file.", type=str, default=None)
parser.add_argument("output_file", help="Output file.", type=str, default=None)
parser.add_argument(
    "--tex2pdf", action="store_true",
    help="Only compile the given tex file to pdf using latexmk."
)
parser.add_argument(
    "--md2tex", action="store_true",
    help="Only process the given markdown or markdown+latex file into pure latex."
)
parser.add_argument(
    "--rmcache", action="store_true",
    help="Remove all files from mistex's cache directory. Use with caution if a custom directory is specified."
)
parser.add_argument(
    "--cachedir", default=HERE.parent / "tmp",
    help="Assign a custom directory for LaTeX compilation and auxiliary files."
)
args = parser.parse_args()


if args.input_file is None and not args.rmcache:
    raise ValueError('No input files.')
if args.output_file is None and not args.rmcache:
    raise ValueError('Output file not specified.')


if args.md2tex and not args.tex2pdf:
    # run the md parser
    rendered_file = mistex.md2latex(stylefile=stylefile, cachedir=args.cachedir).read(args.input_file)
    # save the result in working directory
    with open(args.output_file, "w") as F:
        F.write(rendered_file)

elif args.tex2pdf:
    mistex.tex2pdf(args.input_file, args.output_file, args.cachedir)

else:  # no action specified, we do both
    # run the md parser
    rendered_file = mistex.md2latex(stylefile=stylefile, cachedir=args.cachedir).read(args.input_file)
    # save the result to the tmp directory
    with open(GENERATED_TEX, "w") as F:
        F.write(rendered_file)
    # compile the result we just saved
    mistex.tex2pdf(GENERATED_TEX, args.output_file, args.cachedir)
    GENERATED_TEX.unlink()


if args.rmcache:
    raise NotImplementedError()  # TODO
