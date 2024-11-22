.. index:: single: No SCADE library

No SCADE library
================

.. rule::
   :filename: no_scade_library.py
   :class: NoScadeLibrary
   :id: id_0061
   :reference: SDR-32
   :kind: generic
   :tags: project_structure

   SCADE libraries shall not be used in production

Description
-----------
Only SCADE libraries that are under full control of the project(configuration management, verification) shall be used.
In particular the designer shall NOT use the SCADE product installation libraries, as they are delivered as examples.

.. end_description

The parameter has an attribute to specify where is the CM root with respect to the project,
with the following syntax: ``upper_levels=<number>`` (default value: ``upper_levels=1``).
All libraries within the hierarchy from the root are considered under full control of the project.

Rationale
---------
This ensures a proper configuration management of all the models involved in the verification and code generation process.

Verification
------------
The rule registers to the model and raises a single violation, if any, listing all the libraries.

The rule can't verify the used libraries *are under full control of the project*.
However, it raises a violation for the libraries which match one of the following conditions:
1. The library is referenced though $(SCADE).
2. The library is not part of the root hierarchy with respect to the rule's parameter.

Message: ``The model <model> shall not use SCADE product libraries
or libraries outside of the CM workspace: <list of libraries>``

For example, if the value of ``upper_levels`` is ``2``, a library referenced as
``../../library/library.etp`` is accepted but a reference to
``../../../libraries/library/library.etp`` shall raise a violation.

Resolution
----------
1. Use of a SCADE product library:
    * Create a new library in the CM project, for example `libscade.etp`.
    * Copy the used operators from the SCADE library(ies) to the new one, with the same package structure.
    * Delete the SCADE library(ies) from the project, in the FileView, which leads to temporary undefined references in the model.
    * Add the new library to the project: The pending references shall be restored automatically.
2. External libraries: Reorganize the project structure.

Customization
-------------
N/A.
