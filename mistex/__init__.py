from mistune import Markdown
from .latex_renderer import LatexRenderer


def tail_head_linker(markdown_instance, result, state):
    head = markdown_instance.renderer.head()
    tail = markdown_instance.renderer.tail()
    return head + result + tail


latex = Markdown(LatexRenderer(), plugins=[])
latex.after_render_hooks = [tail_head_linker]
