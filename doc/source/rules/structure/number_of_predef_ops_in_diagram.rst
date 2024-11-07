.. index:: single: Number Of Predefined Operators In Diagram

Number Of Predefined Operators In Diagram
=========================================

.. rule::
   :filename: number_of_predef_ops_in_diagram.py
   :class: NumberOfPredefOpsInDiagram
   :id: id_0073
   :reference: n/a
   :kind: generic
   :tags: structure

   Number of predefined operators in diagram

Description
-----------

.. start_description

Number of graphical primitive operator instances within a diagram. This metric also includes textual equations.
Parameter: maximum value: e.g.: '15'

.. end_description

The rule parameter is an integer value describing the maximum authorized number of predefined operators. Default value is ``15``.

Rationale
---------
This enforces compliance with a specific modeling standard by placing an upper bound
on the number of predefined operators that may be instantiated in a diagram.

Verification
------------
This rule checks all graphical diagrams in the model. For each one, it counts the number of predefined operator instances.

The rule fails if the number of predefined operator calls exceeds the authorized maximum.

Resolution
----------
Modify the diagram to reduce the number of predefined operator instances.

Customization
-------------
N/A.
