# -*- coding: utf-8 -*-

# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Provides utilities for developing naming rules."""

import re
from typing import Dict, List

# list from Scade LRM, section 2.4, KCG 6.6
_keywords = set(
    """
abstract, activate, and, assume, automaton,
bool,
case, char, clock, const,
default, do,
else, elsif, emit, end, enum, every,
false, fby, final, flatten, float, float32, float64, fold, foldi, foldw, foldwi, function,
guarantee, group,
if, imported, initial, int8, int16, int32, int64, integer, is,
land, last, let, lnot, lor, lsl, lsr, lxor,
make, map, mapfold, mapfoldi, mapfoldw, mapfoldwi, mapi, mapw, mapwi, match, merge, mod,
node, not, numeric,
of, onreset, open, or,
package, parameter, pre, private, probe, public,
restart, resume, returns, reverse,
sensor, sig, signed, specialize, state, synchro,
tel, then, times, transpose, true, type,
uint8, uint16, uint32, uint64, unless, unsigned, until,
var,
when, where, with,
xor
""".replace('\n', ' ')
    .replace(',', '')
    .split()
)


def is_scade_keyword(name: str) -> bool:
    """
    Return whether the name is a Scade keyword.

    Parameters
    ----------
    name : str
        Input identifier.

    Returns
    -------
    bool
    """
    return name in _keywords


# the patterns accept acronyms of 2 letters at most
# cf. https://docs.microsoft.com/en-us/previous-versions/dotnet/netframework-1.1/141e06ef(v=vs.71)/
_pascal_case_pattern = re.compile('(?:[A-Z]{1,3}[a-z0-9]+)*(?:[A-Z]{1,2})?')
_camel_case_pattern = re.compile('[a-z0-9]+(?:[A-Z]{1,3}[a-z0-9]+)*(?:[A-Z]{1,2})?')


def is_camel_case(name: str) -> bool:
    """
    Return whether the name matches the camel case pattern.

    Parameters
    ----------
    name : str
        Input identifier.

    Returns
    -------
    bool
    """
    return _camel_case_pattern.fullmatch(name) is not None


def is_pascal_case(name: str) -> bool:
    """
    Return whether the name matches the pascal case pattern.

    Parameters
    ----------
    name : str
        Input identifier.

    Returns
    -------
    bool
    """
    return _pascal_case_pattern.fullmatch(name) is not None


def substitute_names(text: str, aliases: Dict[str, str]) -> str:
    """
    Return a text with substitutions of words.

    Parameters
    ----------
    text : str
        Input text.
    aliases : Dict[str, str]
        Dictionary of replacements.

    Returns
    -------
    str
        Updated text.
    """
    for alias, value in aliases.items():
        text = re.sub(rf'\b{alias}\b', value, text)
    return text


def tokenize_name(word: str) -> List[str]:
    """
    Return the list of tokens constituting a word.

    Parameters
    ----------
    word : str
        Input word.

    Returns
    -------
    List[str]
        List of tokens.
    """
    tokens = []
    for name in word.split('_'):
        if name == '':
            # word is prefixed or suffixed by '_'
            tokens.append('')
            continue
        # there must be a more clever algorithm, one pass
        # for now, adapt an existing one
        prev = name[0]
        lower = prev
        for c in name[1:]:
            if c.isupper() and prev != '_':
                lower += '_'
            prev = c
            lower += c
        lst = lower.split('_')
        # merge successive uppercase singletons
        prev = lst[0]
        for token in lst[1:]:
            if prev.isupper() and len(token) == 1 and token.isupper():
                prev += token
            else:
                tokens.append(prev)
                prev = token
        tokens.append(prev)
    return tokens
