# Mistex

## Installation

### Requirements
- A working **Python 3** installation. In the commands below, change `python` to `python3`
and `pip` to `pip3` if relevant for your system.
- A sufficiently complete **LaTeX** installation, which includes `latexmk` and `xelatex`.
You won't need this if you're only interested in compiling md to latex.

### Installing with pip
```bash
git clone https://github.com/martinosorb/mistex.git
cd mistex
pip install --user .
```

*NOTE*: mistex requires `mistune` 2.*. This unfortunately conflics with other packages,
such as `jupyter`, which use `mistune` version 0.8. If you experience problems, please
use a virtual environment.

## Usage

The purpose of mistex is to pre-compile your markdown file (or mixed
LaTeX-plus-markdown) into a pure LaTeX file that can later be compiled to PDF. To
do this, use:
```bash
python -m mistex my_file.md my_out_file.tex
```

Mistex can be used to quickly compile a LaTeX file into a pdf using `xelatex` and `latexmk`.
It will take care of the auxiliary files (putting them into its own temporary directory), and will leave you with a clean PDF.
To run mistex followed by the latex compilers, use
```bash
python -m mistex --pdf my_file.md my_out_file.pdf
```

Note that auxiliary files are saved in a temporary directory. By default, this
is a folder called `latex_cache/your_input_filename`, placed in the output directory.
If your file contains sensitive information, when you're done compiling, you may want to remove it.
