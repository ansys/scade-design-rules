.. index:: single: Number of user ops in diagram

Number of user ops in diagram
=============================

.. rule::
   :filename: number_of_user_ops_in_diagram.py
   :class: NumberOfUserOpsInDiagram
   :id: id_0074
   :reference: n/a
   :kind: generic
   :tags: structure

   Number of user operators in diagram

Description
-----------

.. start_description

Number of graphical user-operator instances within a single diagram.
Parameter: maximum value: e.g.: '7'

.. end_description

The rule parameter is an integer value describing the maximum authorized number of user-defined operators. Default value is ``7``.

Rationale
---------
This enforces compliance with a specific modeling standard by placing an upper bound
on the number of user-defined operators that may be called in a diagram.

Verification
------------
This rule checks all graphical diagrams in the model. For each one, it counts the number of user-defined operator calls.

The rule fails if the number of user-defined operator calls exceeds the authorized maximum.

Resolution
----------
Modify the diagram to reduce the number of user-defined operator calls.

Customization
-------------
N/A.
