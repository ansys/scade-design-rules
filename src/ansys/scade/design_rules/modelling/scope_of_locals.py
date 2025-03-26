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

"""Implements the ScopeOfLocals rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


from typing import List

import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class ScopeOfLocals(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0092',
        label='Declaration scope of a local variable',
        description=(
            'The scope of a local variable shall be the least common '
            'scope containing all its references.'
        ),
        category='Modelling',
        severity=Rule.ADVISORY,
        **kwargs,
    ):
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            types=[suite.LocalVariable],
            has_parameter=False,
            **kwargs,
        )

    def on_check(self, var: suite.LocalVariable, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""

        def _get_scope_path(top: suite.DataDef, object_: suite.Object) -> List[suite.Object]:
            scope = object_
            owner = object_
            path = []
            while scope != top:
                while not isinstance(owner, suite.DataDef):
                    owner = owner.owner
                    if isinstance(owner, suite.Action) and isinstance(
                        owner.owner, suite.Transition
                    ):
                        # skip transition's action
                        owner = owner.owner
                    if isinstance(owner, suite.Transition):
                        main = owner.main_transition
                        if main.transition_kind == 'Strong':
                            # the scope of a strong transition is its state's scope
                            assert isinstance(owner.owner, suite.State)
                            owner = owner.owner.owner

                scope = owner
                owner = scope.owner
                path.insert(0, scope)
            return path

        if not (var.is_local() and not var.is_internal() or var.is_signal()):
            # the rule does not apply
            return Rule.NA

        # declaration scope
        top = var.owner
        # build the set of scopes for the r/w references
        paths = [_get_scope_path(top, _) for _ in var.expr_ids]
        paths += [_get_scope_path(top, _) for _ in var.definitions]
        if not paths:
            # the variable is unused
            return Rule.OK

        # each path shall start with top
        assert {_[0] for _ in paths} == {top}
        # get the least common scope containing all the scopes
        # get an arbitrary element as the reference
        ref = paths.pop()
        done = False
        lcs = None
        while ref and not done:
            scope = ref.pop(0)
            for path in paths:
                if not path or path.pop(0) != scope:
                    # found a difference
                    # lsc can't None since all paths start with top
                    assert lcs
                    done = True
                    break
            else:
                lcs = scope

        if lcs == top:
            # nothing to declare
            status = Rule.OK
        else:
            status = Rule.FAILED
            message = 'the local variable %s shall be declared in its least common scope %s' % (
                var.name,
                lcs.get_full_path(),
            )
            self.set_message(message)
        return status


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    ScopeOfLocals()
