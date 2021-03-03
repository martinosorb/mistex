import re

CODESPAN_1APX = r"(?<!\\|`)(?:\\\\)*(`)(?!`)((?:(?!')[\s\S])+?)(?<!`)`(?!`)"
CODESPAN_2APX = r"(?<!\\|`)(?:\\\\)*(``)(?!`)((?:(?!(''|\"))[\s\S])+?)(?<!`)``(?!`)"
CODESPAN_3APX = r"(?<!\\|`)(?:\\\\)*(`{3,})(?!`)([\s\S]+?)(?<!`)\1(?!`)"


def parse_codespan(self, m, state):
    code = re.sub(r'[ \n]+', ' ', m.group(2).strip())
    return 'codespan', code


def plugin_codespan(md):
    md.inline.rules.remove('codespan')

    md.inline.register_rule('codespan_1apx', CODESPAN_1APX, parse_codespan)
    md.inline.register_rule('codespan_2apx', CODESPAN_2APX, parse_codespan)
    md.inline.register_rule('codespan_3apx', CODESPAN_3APX, parse_codespan)

    md.inline.rules.append('codespan_1apx')
    md.inline.rules.append('codespan_2apx')
    md.inline.rules.append('codespan_3apx')
