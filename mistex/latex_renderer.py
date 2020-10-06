from mistune.renderers import BaseRenderer
import re

re_quot_close = re.compile(r'("(?=[\s.,:;!?])|"$)')
re_quot_open = re.compile(r'((?<=\s)"|^")')


def escape_latex(s, quote=True):
    # s = s.replace("&", "\\&")
    # s = s.replace("%", "\\%")
    s = re_quot_close.sub("''", s)
    s = re_quot_open.sub('``', s)
    # s = s.replace('#', '\\#')
    return s


HEADING_LEVELS = [
    'chapter*',
    'section*',
    'subsection*',
    'subsubsection*',
    'paragraph*',
    'subparagraph*',
    'subparagraph*'
]


class LatexRenderer(BaseRenderer):
    # NAME = 'latex'
    # IS_TREE = False
    HARMFUL_PROTOCOLS = {
        'javascript:',
        'vbscript:',
        'data:',
    }

    def __init__(self, escape=True,
                 allow_harmful_protocols=None,
                 stylefile=None,
                 add_header=True,
                 cachedir=".",
                 ):
        super(LatexRenderer, self).__init__()
        self._escape = escape
        self._allow_harmful_protocols = allow_harmful_protocols

        self.stylefile = stylefile
        self.add_header = add_header
        self.cachedir = cachedir

        self.packages = []
        self.pkg_opt = {}
        self.tail_string = "\n\\end{document}"

    def tail(self):
        return self.tail_string if self.add_header else ''

    def head(self):
        if not self.add_header:
            return ''

        head = "\\documentclass{report}\n"
        if self.stylefile is not None:
            head += "\\input{" + self.stylefile.split('.tex') + "}\n"
        for pkg in self.packages:
            head += "\\usepackage"
            if pkg in self.pkg_opt:
                head += "[" + self.pkg_opt[pkg] + "]"
            head += "{" + pkg + "}\n"
        head += '\\date{}\n'
        head += '\\begin{document}\n'
        return head

    def _ensure_pkg(self, package, options=None):
        if package not in self.packages:
            self.packages.append(package)
            if options is not None:
                self.pkg_opt[package] = options

    def _ensure_bib(self):
        if '\\bibliographystyle' not in self.tail_string:
            self.tail_string = '\n\\bibliographystyle{plain}\\bibliography{thebib}\n' + self.tail_string

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
        print("::", text)
        return escape_latex(text)

    def link(self, link, text=None, title=None):
        self._ensure_pkg('hyperref')
        if text is None:
            text = link
        if title is not None:
            pass  # TODO

        s = '\\href{' + self._safe_url(link) + '}{' + escape_latex(text) + '}'  # TODO escape
        return s

    def image(self, src, alt="", title=None):
        self._ensure_pkg('graphicx')
        s = '\\begin{figure}[h!]\n    \\begin{center}'
        s += '\n        \\includegraphics[width=\\textwidth]{' + src + '}\n'
        if alt:
            s += '        \\caption{' + alt + '}\n'
        s += '    \\end{center}\n\\end{figure}'
        return s

    def emphasis(self, text):
        return '\\textit{' + text + '}'

    def strong(self, text):
        return '\\textbf{' + text + '}'

    def codespan(self, text):
        return '\\texttt{' + escape_latex(text) + '}'

    def linebreak(self):
        return '\n'

    def inline_html(self, html):
        raise NotImplementedError('inline html')  # TODO
        # if self._escape:
        #     return escape_latex(html)
        # return html

    def paragraph(self, text):
        return '\n' + text + '\n'

    def heading(self, text, level):
        return '\n\\' + HEADING_LEVELS[level - 1] + '{' + text + '}'

    def newline(self):
        return ''

    def thematic_break(self):
        return '\\par\\bigskip\\noindent\\hrulefill\\par\\bigskip\n'

    def block_text(self, text):
        return text

    def block_code(self, code, info=None):
        if info:
            self._ensure_pkg('minted', options=f"outputdir={self.cachedir}")
            lang = info.strip().split(None, 1)[0]
            tex = '\n\\begin{minted}{' + lang + '}\n'
            return tex + code + '\\end{minted}'
        return '\n\\begin{verbatim}\n' + code + '\\end{verbatim}'

    def block_quote(self, text):
        return '\\begin{quote}' + text + '\\end{quote}\n'

    def block_html(self, html):
        return html  # TODO
        # raise NotImplementedError('block html')
        # if not self._escape:
        #     return html + '\n'
        # return '<p>' + escape_html(html) + '</p>\n'

    def block_error(self, html):
        raise NotImplementedError('block error')  # TODO
        # return '<div class="error">' + html + '</div>\n'

    def list(self, text, ordered, level, start=None):
        if ordered:
            result = '\n\\begin{enumerate}\n'
            if start is not None:
                result += '\\setcounter{enumi}{' + str(start - 1) + '}\n'
            return result + text + '\\end{enumerate}'
        return '\n\\begin{itemize}\n' + text + '\\end{itemize}'

    def list_item(self, text, level):
        return '    \\item ' + text + '\n'
