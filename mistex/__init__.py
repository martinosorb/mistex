from mistune import Markdown
from .latex_renderer import LatexRenderer
from .footnotes import plugin_citation


def tail_head_linker(markdown_instance, result, state):
    head = markdown_instance.renderer.head()
    tail = markdown_instance.renderer.tail()
    return head + result + tail


def auto_tail_head(markdown_instance, result, state):
    # automatically figure out if there is a latex header
    if '\\documentclass{' in result:  # TODO this could be sped up
        return result
    return tail_head_linker(markdown_instance, result, state)


def md2latex(stylefile=None, filetype='auto'):
    reader = Markdown(LatexRenderer(stylefile=stylefile), plugins=[plugin_citation])

    if filetype in ['markdown', 'md']:
        reader.after_render_hooks = [tail_head_linker]
    elif filetype == 'auto':
        reader.after_render_hooks = [auto_tail_head]
    elif filetype in ['latex', 'tex']:
        pass
    else:
        raise ValueError(f"File type '{filetype}' not understood.")

    return reader
