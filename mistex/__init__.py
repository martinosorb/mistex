from mistune import Markdown
from .latex_renderer import LatexRenderer
from .footnotes import plugin_citation


def tail_head_linker(markdown_instance, result, state):
    head = markdown_instance.renderer.head()
    tail = markdown_instance.renderer.tail()
    return head + result + tail


latex = Markdown(LatexRenderer(), plugins=[plugin_citation])
latex.after_render_hooks = [tail_head_linker]
