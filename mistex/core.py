from pathlib import Path
from subprocess import call
import shutil

from mistune import Markdown

from .latex_renderer import LatexRenderer
from .plugins import plugin_citation


def tail_head_linker(markdown_instance, result, state):
    head = markdown_instance.renderer.head()
    tail = markdown_instance.renderer.tail()
    return head + result + tail


def auto_tail_head(markdown_instance, result, state):
    # automatically figure out if there is a latex header
    if '\\documentclass' in result:  # TODO this could be sped up
        return result
    return tail_head_linker(markdown_instance, result, state)


def md2latex(stylefile=None, filetype='auto', cachedir="."):
    reader = Markdown(LatexRenderer(stylefile=stylefile, cachedir=cachedir),
                      plugins=[plugin_citation])

    if filetype in ['markdown', 'md']:
        reader.after_render_hooks = [tail_head_linker]
    elif filetype == 'auto':
        reader.after_render_hooks = [auto_tail_head]
    elif filetype in ['latex', 'tex']:
        pass
    else:
        raise ValueError(f"File type '{filetype}' not understood.")

    return reader


def tex2pdf(tex_input, pdf_output, cachedir):
    # create cache directory if it doesn't exist
    cachedir = Path(cachedir)
    cachedir.mkdir(exist_ok=True, parents=True)
    # remove extension
    tex_input = Path(tex_input).with_suffix("")
    output = cachedir / tex_input

    sh = (
        f"latexmk -pdf -outdir={cachedir} -xelatex -shell-escape {tex_input}.tex;"
    )

    # execute the latex command in a shell
    call(sh, shell=True)
    # copy the output from the cache dir to here
    shutil.copy(output.with_suffix(".pdf"), pdf_output)
