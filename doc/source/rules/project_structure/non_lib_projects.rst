.. index:: single: Non Lib Projects

Non Lib Projects
================

.. rule::
   :filename: non_lib_projects.py
   :class: NonLibProjects
   :id: id_0059
   :reference: n/a
   :kind: specific
   :tags: project_structure

   Projects shall contain only one top-level Operator and its used Types and Constants

Description
-----------

.. start_description

This rule checks if all non-top-level operators, types and constants of Non-'Lib' projects are located in other packages nested within the root package

.. end_description

The rule parameter describes the expected prefix for library projects. Default value is ``Lib``.

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that a project only contains
one root package containing one top-level operator with its required types and constants.

Verification
------------
This rule skips all checks if the current project's name starts with the expected prefix for a library.

For non-library projects, the rule checks all packages, types and constants in the model. It fails if:

* The root package contains more than one operator.
* The root package contains a type or constant that is unused by the root operator.

Resolution
----------
Modify the project such that it only contains one top-level operator along with its required types and constants.

Customization
-------------
N/A.
