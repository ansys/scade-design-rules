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

"""
Integration tests: run all the examples for the configuration MetricRule.

The results are assessed manually when building the examples. These tests can
not be used for regression testing. They provide level of confidence through
code coverage, mostly for the rules that do not have unit tests yet.

Design: for each example:
* create a proxy that imports for the rule to be measured
  rationale: Metrics and Rules Checker evaluates the script of a rule instead
  of importing it: no coverage can be measured
* copy the project in a temporary directory and update its settings to refer
  to the proxy
* run Metrics and Rules Checker for each test case in a separate process
  using ../utils/debug.py

Note: The function list_test_cases outputs a default set of test cases with
the examples, for the rules that do not have unit tests.
"""

from pathlib import Path
import shutil
from subprocess import run
import sys

import pytest

# shall modify sys.path to access SCACE APIs
import ansys.scade.apitools  # noqa: F401

# isort: split
import scade
from scade.model.project.stdproject import Configuration, Project

if __name__ == '__main__':
    sys.path.append(Path(__file__).parent.parent.as_posix())

from conftest import load_project


def list_test_cases():
    """
    Build the list of test cases from the existing examples: ../../examples/*/*.etp.

    Do not consider the rules that have already unit tests to save time
    when executing the tests.
    """
    # get rules with existing tests
    root = Path(__file__).parent.parent.parent
    tests = [_ for _ in root.glob('tests/*/test_*.py')]
    rules = {''.join([_.lower() for _ in path.stem[5:].split('_')]) for path in tests}
    # get the test cases from the examples
    examples = [_ for _ in root.glob('examples/*/*') if _.is_dir()]
    paths = [(_ / _.stem).with_suffix('.etp') for _ in examples]
    test_cases: list[tuple[str, Project, Configuration]] = []
    for path in paths:
        if not path.exists():
            print('    # skipping unknown project %s' % path.name)
            continue
        if path.stem.lower() in rules:
            print('    # skipping tested rule %s' % path.stem)
            continue
        category = path.parent.parent.stem
        # scade is a CPython module defined dynamically
        project = scade.load_project(str(path))  # type: ignore
        assert project
        # find the tool Metrics and Rules Checker
        for prop in project.props:
            if prop.name == '@METRICS_RULES:SELECTED_RULES' and prop.values:
                test_cases.append((path.stem, project, prop.configuration))
                print("    ('%s', '%s', '%s')," % (category, path.stem, prop.configuration.name))


# this list is the output of list_test_cases()
all_examples = [
    # skipping tested rule AnnNoteConnectedDataForPublicInterface
    # skipping tested rule AnnNotesForBasicDataTypesInStructures
    # skipping tested rule AnnNotesForBasicInterfaceTypes
    # skipping tested rule AnnNotesForNamedTypesOrVariables
    # skipping tested rule AnnNotesPresentAndNotEmpty
    ('annotations', 'CommentHasSpecificHeadlines', 'MetricRule'),
    # skipping tested rule IdenticalForProducerConsumer
    ('case', 'DefaultCase', 'MetricRule'),
    # skipping tested rule EnumHasDefaultCase
    ('case', 'StatemachineHasDefaultState', 'MetricRule'),
    ('configuration', 'CheckConfiguration', 'MetricRule'),
    ('configuration', 'CheckConfigurationCustom1', 'MetricRule'),
    # skipping tested rule ElementsWithinArea
    ('diagrams', 'PageFormat', 'MetricRule'),
    ('diagrams', 'TextualDiagrams', 'MetricRule'),
    # skipping tested rule LevelOfPackages
    # skipping tested rule NumberOfDiagramsPerElement
    # skipping tested rule NumberOfNestedActivateBlocks
    # skipping tested rule NumberOfNestedSMs
    # skipping tested rule NumberOfOperatorsPerPackage
    # skipping tested rule NumberOfOutgoingTransitionsPerState
    # skipping tested rule NumberOfPredefOpsInDiagram
    # skipping tested rule NumberOfUserOpsInDiagram
    ('modelling', 'AllConstantsTypesAreUsed', 'MetricRule'),
    ('modelling', 'AllElementsInOneEquationSet', 'MetricRule'),
    ('modelling', 'AllPrivateOperatorsAreUsed', 'MetricRule'),
    ('modelling', 'ConstantIfThenElse', 'MetricRule'),
    ('modelling', 'ConstantsHaveConstPragma', 'MetricRule'),
    ('modelling', 'DisadvisedOperators', 'MetricRule'),
    ('modelling', 'ForbiddenOperators', 'MetricRule'),
    # skipping tested rule ForbiddenRealComparisons
    ('modelling', 'IllegalOperationsOnConstants', 'MetricRule'),
    ('modelling', 'InitializationOfArrays', 'MetricRule'),
    ('modelling', 'LevelOfDepthOfStructures', 'MetricRule'),
    ('modelling', 'ModuloDenominatorNonZeroConstant', 'MetricRule'),
    # skipping tested rule NoAnonymousType
    ('modelling', 'NoBoolComparison', 'MetricRule'),
    ('modelling', 'NoExtraClock', 'MetricRule'),
    ('modelling', 'NoFloats', 'MetricRule'),
    ('modelling', 'NoLastWithoutDefault', 'MetricRule'),
    # skipping tested rule NoLiterals
    ('modelling', 'NoOperatorCallsInExpressions', 'MetricRule'),
    # skipping tested rule NoPointerBranch
    ('modelling', 'NoStructTableComparisons', 'MetricRule'),
    ('modelling', 'NoTerminations', 'MetricRule'),
    ('modelling', 'NumOfOperatorCallsInConditions', 'MetricRule'),
    # skipping tested rule PragmaManifest
    # skipping tested rule ScopeOfLocals
    ('modelling', 'TransitionActions', 'MetricRule'),
    ('modelling', 'TransitionKind', 'MetricRule'),
    # skipping tested rule CamelCaseNaming
    ('naming', 'ElementNamesUniqueInProject', 'MetricRule'),
    ('naming', 'EnumTypeNamePrefix', 'MetricRule'),
    # skipping tested rule ForbiddenKeywords
    ('naming', 'NameLengthOfElement', 'MetricRule'),
    ('naming', 'NameOfDefaultEnumValueShallEndWith', 'MetricRule'),
    ('naming', 'NameShallNotStartWith', 'MetricRule'),
    ('naming', 'NameShallStartWith', 'MetricRule'),
    ('naming', 'NameStructureConstant', 'MetricRule'),
    ('naming', 'NameStructureDiagram', 'MetricRule'),
    ('naming', 'NameStructureEnumeration', 'MetricRule'),
    ('naming', 'NameStructureEnumerationCustom1', 'MetricRule'),
    # skipping tested rule NameStructureFoldAccumulator
    # skipping tested rule NameStructureIteratorContinue
    # skipping tested rule NameStructureIteratorIndex
    ('naming', 'NameStructurePackage', 'MetricRule'),
    ('naming', 'NameStructureType', 'MetricRule'),
    # skipping tested rule PascalCaseNaming
    ('naming', 'SensorNamesUniqueInPackage', 'MetricRule'),
    # skipping tested rule UpperCaseNaming
    ('operators', 'NoImportedOperators', 'MetricRule'),
    ('packages', 'PackageFilename', 'MetricRule'),
    ('packages', 'SeparateFilename', 'MetricRule'),
    ('project_structure', 'LibProjectsOperators', 'MetricRule'),
    ('project_structure', 'LibProjectsUsage', 'MetricRule'),
    ('project_structure', 'ModelRootPackage', 'MetricRule'),
    # skipping unknown project NonLibProjects.etp
    # skipping unknown project NoScadeLibrary.etp
    ('project_structure', 'OnePublicOpPerPackage', 'MetricRule'),
    # skipping unknown project OnePublicOpPerPackageCopy.etp
    ('project_structure', 'RootPackageName', 'MetricRule'),
    # skipping unknown project RootPackageNamePositive.etp
    ('project_structure', 'TypesNotTakenFromSpecificPackage', 'MetricRule'),
    ('project_structure', 'TypesTakenFromSpecificPackage', 'MetricRule'),
    ('project_structure', 'TypesTakenFromSpecificProject', 'MetricRule'),
    # skipping unknown project UserDefinedTypesLib.etp
    # skipping tested rule LineCrossing
    # skipping tested rule LocalNameUniqueness
    ('scade_types', 'EnumDefinitionElementsOrder', 'MetricRule'),
    # skipping tested rule MaximumCallGraphDepth
    # skipping tested rule MaximumDiagramsPerElement
    # skipping tested rule MaximumLevelOfPackages
    # skipping tested rule MaximumNestedActivateBlocks
    # skipping tested rule MaximumNestedSMs
    # skipping tested rule MaximumOperatorsPerPackage
    # skipping tested rule MaximumOutgoingTransitionsPerState
    # skipping tested rule MaximumPredefOpsInDiagram
    # skipping tested rule MaximumUserOpsInDiagram
    ('tool', 'CheckerNoWarningsErrors', 'MetricRule'),
    ('tool', 'ScadeVersion', 'MetricRule'),
    # skipping tested rule AllInEqSet
    # skipping tested rule EqInEqSet
    # skipping tested rule EqInEqSetOrNet
    # skipping tested rule EqSetHasEqs
    # skipping tested rule EqSetNotEmpty
    ('traceability', 'HasLink', 'MetricRule'),
    # requires sys.version != 3.7, cf. next statement
    # ('traceability', 'HasLinkOrPartOfEquationSet', 'MetricRule'),
    # skipping tested rule LLRArchitecture
    # skipping tested rule LLRNature
    # skipping tested rule LLRNatureEqs
    # skipping tested rule LLROnly
    # skipping tested rule LLROnlyEqs
    # skipping tested rule LLROrNetNature
    # skipping tested rule LLROrNetOnly
    ('traceability', 'RequirementHasLink', 'MetricRule'),
    ('user_defined_operators', 'SeparateFileNameOperators', 'MetricRule'),
]


if sys.version_info.major == 3 and sys.version_info.minor != 7:
    # HasLinkOrPartOfEquationSet: example files not compatible with ALMGW 2023 R1
    all_examples.append(('traceability', 'HasLinkOrPartOfEquationSet', 'MetricRule'))


@pytest.mark.parametrize('category, name, configuration', all_examples)
def test_example(category, name, configuration):
    # separate function to ease debugging
    run_example(category, name, configuration)


def run_example(category, name, configuration):
    """Create a temporary project and rule in the test's directory."""
    root = Path(__file__).parent.parent.parent
    dst_dir = Path(__file__).parent / 'tmp'
    dst_dir.mkdir(exist_ok=True)
    # original project
    path_src = root / 'examples' / category / name / (name + '.etp')
    # copy
    path_dst = dst_dir / (name + '.etp')
    if path_dst.exists():
        # can't' use missing_ok=True with Python 3.7
        path_dst.unlink()
    shutil.copy(path_src, path_dst)
    # copy traceability files when present
    for ext in ['*.almgp', '*.almgr', '*.reqs']:
        for path in path_src.parent.glob(ext):
            shutil.copy(path, dst_dir)
    # files
    src = load_project(path_src)
    files = {_.name: _.pathname for _ in src.file_refs}
    dst = load_project(path_dst)
    # update the paths
    for file in dst.file_refs:
        file.set_path_name(files[file.name])
    # rule
    # one and only one rule, consider the first one anyways
    pathname = dst.get_scalar_tool_prop_def('METRICS_RULES', 'USER_DEF_FILES', '', None)
    assert pathname
    py_name = Path(pathname).name
    dst.set_scalar_tool_prop_def('METRICS_RULES', 'USER_DEF_FILES', py_name, '', None)
    # create the rule
    rule_path = dst_dir / py_name
    with rule_path.open('w') as f:
        f.write(f'from ansys.scade.design_rules.{category}.{rule_path.stem} import {name}\n')
        f.write(f'{name}()\n')

    # save the temporary project
    dst.save(dst.pathname)
    # run the check
    exe = sys.executable
    script = root / 'tests' / 'debug.py'
    cmd = [exe, str(script), str(path_dst), '-c', configuration, '-a', 'rules']
    print(cmd)
    cp = run(cmd, capture_output=True, encoding='utf-8')
    if cp.stdout:
        print(cp.stdout)
    if cp.stderr:
        print(cp.stderr)
        assert False
    print('done')


if __name__ == '__main__':
    list_test_cases()
