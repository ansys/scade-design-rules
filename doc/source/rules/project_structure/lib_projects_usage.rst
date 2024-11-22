.. index:: single: Lib Projects Usage

Lib projects usage
==================

.. rule::
   :filename: lib_projects_usage.py
   :class: LibProjectsUsage
   :id: id_0033
   :reference: n/a
   :kind: specific
   :tags: project_structure

   Only 'Lib' prefixed projects shall be used as library Projects

Description
-----------

.. start_description

This rule checks if only library Projects (prefixed with Lib) are included in the current Project.

.. end_description

The rule parameter describes the expected prefix for library projects. Default value is ``Lib``.

Rationale
---------
This enforces compliance with a specific modeling standard by defining a naming convention for libraries used by a model.

Verification
------------
This rule checks the model's list of library projects and verifies that all project names in the list start with the expected prefix.

The rule fails if a library does not comply with the naming convention.

Resolution
----------
Rename the offending library.

Customization
-------------
N/A.
