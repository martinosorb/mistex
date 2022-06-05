from mistune.renderers import BaseRenderer
import re
import pylatex as pl
from .pylatex_classes import Minted, LatexList, Href, Verbatim, Strikethrough, Description

# re_quot_close = re.compile(r'("(?=[\s.,:;!?])|"$)')
# re_2quot_open = re.compile(r'\B"\b')
# re_1quot_open = re.compile(r"\B'\b")
re_surrounding_newline = re.compile(r"(^\n+|\n+$)")


class LatexRenderer(BaseRenderer):
    HEADING_LEVELS = [
        pl.section.Chapter,
        pl.section.Section,
        pl.section.Subsection,
        pl.section.Subsubsection,
        pl.section.Paragraph,
        pl.section.Subparagraph,
        pl.section.Subparagraph
    ]

    HARMFUL_PROTOCOLS = {
        'javascript:',
        'vbscript:',
        'data:',
    }

    def __init__(
        self,
        allow_harmful_protocols=None,
        cachedir=".",
    ):

        super(LatexRenderer, self).__init__()
        self._allow_harmful_protocols = allow_harmful_protocols
        self.cachedir = cachedir

    # def _ensure_bib(self):
    #     if '\\bibliographystyle' not in self.tail_string:
    #         self.tail_string = '\n\\bibliographystyle{plain}\\bibliography{thebib}\n' + self.tail_string

    def _safe_url(self, url):
        if self._allow_harmful_protocols is None:
            schemes = self.HARMFUL_PROTOCOLS
        elif self._allow_harmful_protocols is True:
            schemes = None
        else:
            allowed = set(self._allow_harmful_protocols)
            schemes = self.HARMFUL_PROTOCOLS - allowed

        if schemes:
            for s in schemes:
                if url.startswith(s):
                    url = '#harmful-link'
                    break
        return url

    def text(self, text):
        # text = re_2quot_open.sub('``', text)
        # text = re_1quot_open.sub("`", text)
        text = re_surrounding_newline.sub(" ", text)
        return pl.NoEscape(text)

    def donotparse(self, text):
        return text

    def link(self, link, text=None, title=None):
        # `title` is ignored.
        link_url = self._safe_url(link)
        link_text = text or link
        href = Href((link_url, link_text))
        return href

    def image(self, src, alt="", title=None):
        fig = pl.figure.Figure(position='h!')
        fig.add_image(src)
        if alt:
            fig.add_caption(alt)
        return fig

    # def ignored_block(self, text):  # TODO
    #     return '\n' + text + '\n'

    # --- Text properties
    def emphasis(self, text):
        return pl.utils.italic(text)

    def strong(self, text):
        return pl.utils.bold(text)

    def strikethrough(self, text):
        return Strikethrough(text)

    def codespan(self, text):
        return pl.Command('texttt', text)

    # def linebreak(self):  # TODO
    #     return '\n'

    # def inline_html(self, html):  # TODO
    #     return html

    def paragraph(self, text):
        if not isinstance(text, LatexList):
            text = LatexList(data=text)
        text.begin_paragraph = True
        return text

    def heading(self, text, level):
        return self.HEADING_LEVELS[level - 1](text, numbering=False)

    def newline(self):
        return ""

    def thematic_break(self):
        return pl.Command('par\\bigskip\\noindent\\hrulefill\\par\\bigskip\n')

    # --- Block renderers
    def block_text(self, text):
        # this is also processed by `text` above
        return text

    def block_code(self, code, info=None):
        if info:
            lang = info.strip().split(None, 1)[0]
            env = Minted(lang, self.cachedir)
        else:
            env = Verbatim()
        code = code.rstrip("\n")
        env.append(pl.NoEscape(code))
        return env

    def block_quote(self, text):
        env = pl.base_classes.Environment()
        env._latex_name = "quote"
        env.append(text)
        return env

    def block_error(self, text):
        return pl.basic.TextColor('red', text)

    # --- Lists
    def list(self, items, ordered, level, start=None):
        # if ordered and start is not None: # TODO
        #     result += '\\setcounter{enumi}{' + str(start - 1) + '}\n'
        thelist = pl.lists.Enumerate() if ordered else pl.lists.Itemize()
        for item in items:
            thelist.add_item(item)
        return thelist

    def list_item(self, text, level):
        return text

    # --- Tables
    def table(self, tabular_list, aligns):
        # turn 'left', 'right', 'center', None into l, r, c, l
        aligns = ['l' if align is None else align[0] for align in aligns]
        columns = '|'.join(aligns)
        table = pl.table.Tabular(table_spec=columns)
        table.begin_paragraph = True
        table.end_paragraph = True

        for name, element in tabular_list:
            if name == 'tablebody':
                [table.add_row(e) for e in element]
            elif name == 'tablehead':
                table.add_row(element)
                table.add_hline()

        return table

    def table_head(self, text):
        return 'tablehead', self.table_row(text)

    def table_body(self, text):
        return 'tablebody', text

    def table_row(self, text):
        return text

    def table_cell(self, text, align=None, is_head=False):
        if is_head:
            text = pl.utils.bold(text)
        return text  # TODO: this may need to escape &

    # --- Definition Lists
    def def_list(self, text):
        deflist = Description()
        deflist.data = text
        return deflist

    def def_list_header(self, text):
        return pl.Command("item", options=text)

    def def_list_item(self, text):
        return text

    # ---
    def finalize(self, data):
        ll = [i for i in data]
        if len(ll) == 1:
            return ll[0]
        else:
            container = LatexList()
            container.data = ll
            return container
