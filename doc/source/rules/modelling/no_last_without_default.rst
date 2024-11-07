.. index:: single: No Last Without Default

No Last Without Default
=======================

.. rule::
   :filename: no_last_without_default.py
   :class: NoLastWithoutDefault
   :id: id_0057
   :reference: n/a
   :kind: generic
   :tags: modelling

   No last without default

Description
-----------

.. start_description

An assignment just as (last 'variable -> (L)variable) shall not be used.
Only if a default value is assigned such an statement is necessary.
Implicit behaviour of SCADE

.. end_description

Rationale
---------
This improves model readability by ensuring that redundant assignments are avoided.

In this case, using the SCADE IDE to set "Last" to "True" on a variable or signal ensures that the previous value is used.
There is no need to add an equation writing ``last 'variable`` into it.

Verification
------------
The rule registers to equations and raises a violation when the right side of the equation is a variable
or signal with "Last" set to "True" and the left side is the same variable or signal.

  Message: ``Assignment (last 'variable -> (L)variable) found (<right_side> -> <left_side>)``

Resolution
----------
Remove the redundant equation.

Customization
-------------
N/A.
