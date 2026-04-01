.. index:: single: Structure depth level

Structure depth level
#####################

.. rule::
   :filename: level_of_depth_of_structures.py
   :class: LevelOfDepthOfStructures
   :id: id_0031
   :reference: n/a
   :kind: generic
   :tags: modelling

   Level of Depth of Structures

Description
===========

.. start_description

A SCADE structure type shall contain at most 'parameter-value' level of sub structures.
var.level1.level2.level3

.. end_description

The rule parameter is an integer defining the maximum allowed structure depth. Default value is ``4``.

Rationale
=========
This enforces compliance with a specific modeling standard by ensuring that structures remain below a given complexity level.

Verification
============
This rule recursively checks all structures throughout the model to determine their maximum depth.
A simple structure with primitive fields has depth ``1``.
The rule fails if a structure exceeds the maximum allowed depth.

Resolution
==========
Modify the offending structure to reduce its depth, as detailed in the rule failure message.

Customization
=============
N/A.
