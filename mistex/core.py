from mistune import Markdown
from pylatex import Document

from .latex_renderer import LatexRenderer
from .plugins.table import plugin_table
from mistune.plugins import plugin_strikethrough, plugin_def_list

PLUGINS = [plugin_table, plugin_strikethrough, plugin_def_list]


def _parse_escape(m, state):
    text = m.group(0)
    return 'text', text


def make_document(markdown_instance, result, state):
    document = Document(documentclass="report")
    document.data = result
    return document


def md2latex(cachedir="."):
    renderer = LatexRenderer(cachedir=cachedir)
    reader = Markdown(renderer, plugins=PLUGINS)

    # make the rule that un-escapes \$ \& \% etc do nothing
    # reader.inline.rules.remove("escape")  # causes problems with \ at the end of lines.
    reader.inline.parse_escape = _parse_escape
    # remove the rule that considers indented blocks as verbatim code.
    # reader.block.rules.remove("indent_code")
    reader.block.rules.remove("block_html")
    reader.after_render_hooks = [make_document]

    return reader
