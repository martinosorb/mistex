# https://github.com/lepture/mistune-contrib/blob/master/mistune_contrib/math.py
import re

UNPARSED_LATEX_GROUPS = ['equation', 'eqnarray']

EQN_INLINE_PATTERN = r'\$(.+?)\$(?!\$)'
# EQN_INLINE_PATTERN = r'\\\[(.+?)\\\]'
EQN_BLOCK_PATTERN = re.compile(
    r' *(\$\$([\S\s]+?)\$\$|\\\[([\S\s]+?)\\\])'
)

# DEFINITION_LIST_PATTERN = re.compile(r"([^\n]+\n(:[ \t][^\n]+\n)+\n?)+")
group_names_r = r'|'.join(UNPARSED_LATEX_GROUPS)
LATEX_ENV_PATTERN = re.compile(
    r' *\\begin\{(' + group_names_r + r'\*?)\}(.*?)\\end\{\1\}',
    re.DOTALL
)


def parse_block_eqn(self, m, state):
    content = m.group(0).rstrip()
    return {'type': 'donotparse', 'raw': content}


def parse_block_env(self, m, state):
    content = m.group(0).rstrip()
    return {'type': 'ignored_block', 'raw': content}


# define how to parse matched item
def donotparse(self, m, state):
    text = m[0]  # the whole thing
    return 'donotparse', text


def plugin_equation(md):
    md.inline.register_rule('inline_equation', EQN_INLINE_PATTERN, donotparse)
    md.inline.rules.append('inline_equation')

    md.block.register_rule('block_equation', EQN_BLOCK_PATTERN, parse_block_eqn)
    md.block.rules.append('block_equation')

    md.block.register_rule('tex_ignored_env', LATEX_ENV_PATTERN, parse_block_env)
    md.block.rules.append('tex_ignored_env')
