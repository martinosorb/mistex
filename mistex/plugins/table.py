# Significant parts of the code in this file are derived from mistune, which is
# licensed under the BSD 3-Clause "New" or "Revised" License, with only slight modifications.
# The following notice applies:
#
# Copyright (c) 2014, Hsiaoming Yang. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# * Neither the name of the creator nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re
from mistune.plugins.table import (
    TABLE_PATTERN, NP_TABLE_PATTERN, HEADER_SUB, _process_row, _process_table
)


def parse_table(self, m, state):
    header = HEADER_SUB.sub('', m.group(1)).strip()
    align = HEADER_SUB.sub('', m.group(2))
    thead, aligns = _process_table(header, align)

    text = re.sub(r'(?: *\| *)?\n$', '', m.group(3))
    rows = []
    for i, v in enumerate(text.split('\n')):
        v = re.sub(r'^ *\| *| *\| *$', '', v)
        rows.append(_process_row(v, aligns))

    children = [thead, {'type': 'table_body', 'children': rows}]
    return {'type': 'table', 'children': children, 'params': (aligns, )}


def parse_nptable(self, m, state):
    thead, aligns = _process_table(m.group(1), m.group(2))

    text = re.sub(r'\n$', '', m.group(3))
    rows = []
    for i, v in enumerate(text.split('\n')):
        rows.append(_process_row(v, aligns))

    children = [thead, {'type': 'table_body', 'children': rows}]
    return {'type': 'table', 'children': children, 'params': (aligns, )}


def plugin_table(md):
    md.block.register_rule('table', TABLE_PATTERN, parse_table)
    md.block.register_rule('nptable', NP_TABLE_PATTERN, parse_nptable)
    md.block.rules.append('table')
    md.block.rules.append('nptable')
