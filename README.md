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

Mistex can be used to quickly compile a LaTeX file into a pdf using `xelatex` and `latexmk`.
It will take care of the auxiliary files (putting them into its own temporary directory),
and will leave you with a clean PDF. To simply compile a LaTeX file use:
```bash
python -m mistex --tex2pdf my_file.tex
```

The main purpose of mistex, however, is to pre-compile your markdown file (or mixed
LaTeX-cum-markdown) into a pure LaTeX file that can later be compiled to PDF. To
do this, use:
```bash
python -m mistex --md2tex my_file.md
```

Of course, most of the time you will want to do both things together. This is the
default, so you just need to call:
```bash
python -m mistex my_file.md
```

Note that auxiliary files are saved in a temporary directory. If your file contains
sensitive information, when you're done compiling, you may want to call:
```
python -m mistex --cleantmp
```
