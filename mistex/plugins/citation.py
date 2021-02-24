from mistune.inline_parser import LINK_LABEL


CITATION_PATTERN = r'\[\^@(' + LINK_LABEL + r')\]'


def render_citation(text):
    return '\\cite{' + text + '}'


def parse_citation(self, m, state):
    text = m.group(1)
    self._ensure_bib()
    return 'citation', self.render(text, state)


def plugin_citation(md):
    md.inline.register_rule('citation', CITATION_PATTERN, parse_citation)

    index = md.inline.rules.index('std_link')
    if index != -1:
        md.inline.rules.insert(index, 'citation')
    else:
        md.inline.rules.append('citation')

    md.renderer.register('citation', render_citation)
