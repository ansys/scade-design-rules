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

"""Implements the PragmaManifest rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade
import scade.model.suite as suite

import ansys.scade.apitools.prop as prop
import ansys.scade.apitools.query as query
from ansys.scade.design_rules.utils.rule import SCK, Rule


class PragmaManifest(Rule):
    """Implements the rule interface."""

    # abbreviations for computing the signatures of the types
    _predef_signatures = {
        'bool': 'b',
        'char': 'c',
        'int8': 'i8',
        'int16': 'i16',
        'int32': 'i32',
        'int64': 'i64',
        'uint8': 'u8',
        'uint16': 'u16',
        'uint32': 'u32',
        'uint64': 'u64',
        'float32': 'f32',
        'float64': 'f64',
    }

    def __init__(
        self,
        id='id_0123',
        label='Pragma manifest for complex types',
        description=(
            "A pragma 'manifest' shall be used for each type declaration.\n"
            'Optionally, the rule applies only for each type declaration '
            'used in the interface of a root operator / imported operator: '
            'Either all the root operators, or the ones of '
            'the specified configuration.'
        ),
        category='Modelling',
        severity=Rule.ADVISORY,
        parameter='configuration=,interface=false',
        **kwargs,
    ):
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            kinds=[SCK.TYPE],
            has_parameter=True,
            default_param=parameter,
            **kwargs,
        )
        self.roots = None

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        # restore the default values
        self.roots = None
        # the parameters are optional
        d = self.parse_values(parameter) if parameter else {}
        if d is None:
            message = f"'{parameter}': parameter syntax error"
            self.set_message(message)
            scade.output(message + '\n')
            return Rule.ERROR
        name = d.get('configuration')
        self.interface = d.get('interface', 'false') == 'true'
        if name:
            # get the project associated to the model
            project = model.project
            configuration = project.find_configuration(name)
            if configuration:
                self.roots = project.get_tool_prop_def('GENERATOR', 'ROOTNODE', [], configuration)

        # cache dictionary type -> signature
        self.signatures = {}
        # cache dictionary signature -> has pragma manifest
        self.manifests = {}
        # store the presence of a pragma manifest for all type equivalence classes
        # from the model and its libraries.
        for type_ in model.all_named_types:
            # consider only structures and arrays
            if not (query.is_structure(type_) or query.is_array(type_)):
                continue
            self._update_manifest(type_)

        # no error
        return Rule.OK

    def on_check_ex(self, type_: suite.NamedType, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        if not (query.is_structure(type_) or query.is_array(type_)):
            # the pragma manifest is not required for imported or scalar types
            return Rule.NA
        if self.interface:
            # search the root operators where the type is used, as main type, in the interface
            operators = set()
            for typed in type_.typed_objects:
                if (
                    isinstance(typed, suite.LocalVariable)
                    and (typed.is_input() or typed.is_hidden() or typed.is_output())
                    and self._is_root(typed.operator)
                ):
                    operators.add(typed.operator.get_full_path().strip('/'))
            if not operators:
                # the type is not directly involved in the signature of a root operator
                return Rule.NA
            # consider the type and its dependencies
            # get the equivalence class using the signature
            for used in type_.used_types:
                if not (query.is_structure(used) or query.is_array(used)):
                    continue
                signature = self.get_signature(used)
                if not self.manifests[signature]:
                    message = (
                        'The type {} has no KCG pragma "manifest" and is'
                        ' used in the interface of root operators: {}'
                    )
                    self.set_message(message.format(query.get_type_name(used), operators))
                    return Rule.FAILED
        else:
            signature = self.get_signature(type_)
            if not self.manifests[signature]:
                self.set_message(
                    f'The type {query.get_type_name(type_)} has no KCG pragma "manifest"'
                )
                return Rule.FAILED
        return Rule.OK

    def _is_root(self, operator: suite.Operator) -> bool:
        # no configuration specified, consider any root operator
        # which is not polymorphic nor parameterized by size
        if operator.parameters or operator.typevars:
            return False
        return (
            operator.is_imported()
            or not operator.expr_calls
            # configuration specified: consider its root operators
            and (not self.roots or operator.get_full_path().strip('/') in self.roots)
        )

    def get_signature(self, type_) -> str:
        """Return the signature of the type."""
        signature = self.signatures.get(type_)
        if not signature:
            if isinstance(type_, suite.NamedType):
                if type_.is_imported():
                    signature = '({})'.format(type_.name)
                elif type_.is_predefined():
                    signature = self._predef_signatures[type_.name]
                else:
                    signature = self.get_signature(type_.type)
            elif isinstance(type_, suite.Enumeration):
                signature = '({})'.format(type_.owner.name)
            elif isinstance(type_, suite.Table):
                signature = '{}^{:.0f}'.format(self.get_signature(type_.type), type_.size)
            elif isinstance(type_, suite.Structure):
                elements = [f'{_.name}:{self.get_signature(_.type)}' for _ in type_.elements]
                signature = '({})'.format(','.join(elements))
            elif isinstance(type_, suite.SizedType):
                prefix = 'u' if type_.constraint.is_unsigned() else 'i'
                size = type_.size_expression.evaluate_expression()
                if not size:
                    size = '({})'.format(type_.size_expression.to_string())
                signature = prefix + size
            else:
                assert type_ is None
                signature = '()'
            self.signatures[type_] = signature

        return signature

    def _update_manifest(self, type_):
        manifest = prop.find_pragma_tool(type_, 'kcg', 'manifest') is not None
        # update the status for the type's equivalence class
        signature = self.get_signature(type_)
        self.manifests[signature] = manifest or self.manifests.setdefault(signature, False)


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    PragmaManifest()
