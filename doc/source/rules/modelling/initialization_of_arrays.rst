.. index:: single: Initialization Of Arrays

Initialization Of Arrays
========================

.. rule::
   :filename: initialization_of_arrays.py
   :class: InitializationOfArrays
   :id: id_0029
   :reference: n/a
   :kind: generic
   :tags: modelling

   Initialization of Arrays

Description
-----------

.. start_description

If all elements of an array are identical the initialization shall be done like this: value ^size
Note: An initialization such as ' ', ' ', ' ', etc. leads to more memory usage than ' ' ^n.

.. end_description

Rationale
---------
This rule ensures that arrays are always initialized with maximum efficiency.

Initializing arrays with a ``[value, value, ...]`` notation with all-similar values generates larger model files
than using a ``value^N`` notation. On very large arrays, this may lengthen project load times in the SCADE IDE.

Enforcing a ``value^N`` notation ensures model file size and loading times are optimized.

Verification
------------

.. vale off
   avoid warning on ...

This rule registers to predefined data array initialization expressions.
It raises a violation when an array is initialized with a ``[value, value, ...]``
notation that uses the same value for each item.

.. vale on

  .. vale off
    avoid warning on ...

  Message: ``Use <value>^<array_length> instead of [<value>, ...]``

  .. vale on

Resolution
----------
Modify the offending array initialization to use a ``value^N`` notation.

Customization
-------------
N/A.
