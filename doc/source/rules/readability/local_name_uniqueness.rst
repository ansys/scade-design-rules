.. index:: single: Local Name Uniqueness

Local Name Uniqueness
=====================

.. rule::
   :filename: local_name_uniqueness.py
   :class: LocalNameUniqueness
   :id: id_0038
   :reference: SDR-24
   :kind: generic
   :tags: readability

   Local name uniqueness

Description
-----------
The names of local variables and signals shall be unique within an operator.

Rationale
-----------
This ensures an unambiguous interpretation of Scade diagrams without referring to the declarations.

For example, the following use cases can be misleading:

* Homonymous variables in sibling states.

  .. image:: img/local_name_uniqueness_11.png
  .. image:: img/local_name_uniqueness_12.png
* Overriding of a local variable in a decision tree.

  .. image:: img/local_name_uniqueness_21.png
  .. image:: img/local_name_uniqueness_22.png

Verification
-------------
The rule registers to the flows of a Scade model, for example local variables, and raises a violation for each flow which name is not unique in the operator.

Message: ``<variable name>: Not unique name``

Resolution
----------
Rename the homonymous local variables.

Customization
-------------
N/A.
