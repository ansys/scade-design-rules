.. index:: single: Diagram name

Diagram name
############

.. rule::
   :filename: name_structure_diagram.py
   :class: NameStructureDiagram
   :id: id_0047
   :reference: SDR-18
   :tags: naming

   Diagram name

Description
===========
When there are several diagrams in a scope, the name of each diagram shall be characteristic of its function.
Otherwise the default name created by the editor shall be updated to the name of its scope.

Rationale
=========
This enhances the readability of a model.

Verification
============
The rule registers to the diagrams of a model.

* When there is a single diagram and the scope is either an operator or a state, the rule raises a violation if the names are different

  Message: ``<name>: The name shall be the name of its scope <scope name>``

* When a diagram has siblings, it is not possible to verify the names of the diagrams are characteristic of their functions.
  However, the rule raises violations corresponding to some SCADE Editor's defaults:

  * The name of the diagram is the name of its scope suffixed by a number

    Message: ``<name>: The name derives from its scope's name instead of a description``

  * The name of the diagram differs from the name of a sibling diagram only by a numeric suffix

    Message: ``<name>: The name shall be a description``

Resolution
==========
Rename the diagram.

Customization
=============
N/A.
