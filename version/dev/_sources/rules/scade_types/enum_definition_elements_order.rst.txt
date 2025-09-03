.. index:: single: Enumeration definition element order

Enumeration definition element order
####################################

.. rule::
   :filename: enum_definition_elements_order.py
   :class: EnumDefinitionElementsOrder
   :id: id_0016
   :reference: n/a
   :kind: generic
   :tags: scade_types

   Enumeration definition elements order

Description
===========

.. start_description

Checks if the order of definition elements of enumerations is ascending (``order=asc``) or descending (``order=desc``).
The elements are ordered by name (``by=name``) or by value (``by=value``).

.. end_description

Rationale
=========
Improves legibility and consistency of SCADE enumeration definitions across a model.

Verification
============
The rule iterates over enumeration definitions and checks that their elements are correctly ordered.

Resolution
==========
Modify the offending enumeration to reorder their elements.

Customization
=============
N/A.
