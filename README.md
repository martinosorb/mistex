# Mistex

[![Build Status](https://travis-ci.com/martinosorb/mistex.svg?branch=master)](https://travis-ci.com/martinosorb/mistex)

A common criticism of LaTeX is that its syntax is outdated and cumbersome, in a way that gets in the way of your thoughts while writing. Additionally, it leaves many auxiliary files around, which is annoying when you want to write a quick-and-dirty note.

Conversely, markdown has a very lightweight syntax that is designed to be easy to read even without compilation into a graphical document, but is far less powerful.

Mistex is a simple tool for cross-compiling markdown code into LaTeX, with the peculiarity that markdown and LaTeX syntax can be freely mixed in your source file. Using it, you will be able to write markdown and turn it into a LaTeX-style PDF document. If you need the full power or LaTeX, you can simply use a little bit of markdown as syntactic sugar in your LaTeX source instead. You will never have to type `\textbf`, `\begin{enumerate} \item ... \end{enumerate}` and the like again.

Mistex is based on the markdown compiler [`mistune`](https://github.com/lepture/mistune/).

## Table of contents

- [Mistex](#mistex)
  * [Understanding mistex](#understanding-mistex)
    + [Examples](#examples)
  * [Installation](#installation)
    + [Requirements](#requirements)
    + [Installing with pip](#installing-with-pip)
  * [Usage](#usage)

## Understanding mistex

To understand what mistex does, consider the following edge cases:
- If mistex is called on any LaTeX source file, it should do nothing and output the same file (bugs notwithstanding).
- If mistex is called on any Markdown file, it will cross-compile it into LaTeXcode and, optionally, compile the latter into a PDF. All the syntax listed by [the markdown guide](https://www.markdownguide.org/basic-syntax) is supported, and more, if the best practices therein are respected. The only unexpected things can happen if your markdown document contains symbols that have a special role in LaTeX,such as `&`, `\`, `%` (and possibly others). These will have to be escaped as`\&`, `\backslash` and `\%` respectively.

### Examples

## Installation

### Requirements
- A working **Python 3** installation. In the commands below, change `python` to `python3` and `pip` to `pip3` if the default for your system is python 2.
- A sufficiently complete **LaTeX** installation, which includes `latexmk` and `xelatex`. You won't need this if you're only interested in cross-compiling markdown to latex.

### Installing with pip
```bash
git clone https://github.com/martinosorb/mistex.git
cd mistex
pip install --user .
```

**NOTE**: mistex requires `mistune>=2.*`. This unfortunately conflicts with other packages, such as `nbconvert` (used by `jupyter`), which use `mistune` version 0.8.*. If you experience problems, you should consider using virtual environments.

## Usage

The purpose of mistex is to pre-compile your markdown file (or mixed LaTeX-plus-markdown) into a pure LaTeX file that can later be compiled to PDF. To do this, use:
```bash
python -m mistex my_file.md [--out my_out_file.tex]
```
(where the part in square brackets is optional, in case you want a custom output name or location).

Mistex can be used to quickly compile a LaTeX file into a pdf using `xelatex` and `latexmk`.
It will take care of the auxiliary files (putting them into a separate directory), and will leave you with a clean PDF.
To run mistex followed by the latex compilers, use:
```bash
python -m mistex --pdf my_file.md [--out my_out_file.pdf]
```
(again the part in square brackets is optional).

Note that auxiliary files are saved in a separate directory. By default, this
is a folder called `latex_cache/your_input_filename`, placed in the output directory.
If your file contains sensitive information, when you're done compiling, you may want to remove it. You can choose a custom cache directory with `--cachedir mydir`.

## Usage within TeX IDEs

### TeXShop on Mac OS X

This was not thoroughly tested, but works for me:
- First, check that your TeXShop directory is `~/Library/TeXShop/`. If not, change the path in the command below.
- You can then issue the following command to generate a new "engine" file:
```bash
echo "#\!/bin/bash\n$(which python) -m mistex --pdf \"\$1\"" > ~/Library/TeXShop/Engines/mistex.engine
```
This should create a file in the Engines directory of TeXShop, containing the mistex command.
If you use a virtual environment, make sure it is active while you do this (`which python` needs to give the correct result). If you use pyenv-virtualenv, use `pyenv which` instead of `which`.
- Now, open TeXShop again. You should see `mistex` among the list of LaTeX commands (in the drop-down menu together with LaTeX, BibTeX, etc.). Select it, and compile your file.

Feedback on this is welcome.
