"""Example of rule instantiations."""

from ansys.scade.design_rules.naming.camel_case_naming import CamelCaseNaming
from ansys.scade.design_rules.naming.pascal_case_naming import PascalCaseNaming
from ansys.scade.design_rules.naming.upper_case_naming import UpperCaseNaming

# Instantiate the rules with custom ids
CamelCaseNaming(id='NAMING_01')
PascalCaseNaming(id='NAMING_02')
UpperCaseNaming(id='NAMING_03')
