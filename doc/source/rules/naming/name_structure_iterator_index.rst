.. index:: single: Iterator Index

Iterator Index
==============

.. rule::
   :filename: name_structure_iterator_index.py
   :class: NameStructureIteratorIndex
   :id: id_0051
   :reference: n/a
   :kind: generic
   :tags: naming

   Name structure of iterator index

Description
-----------
For iterators which use an index (mapi, mapwi, foldi, foldwi, mapfoldi, mapfoldwi), the input corresponding to the index shall be named or prefixed by 'index'.

.. end_description

The parameter allows defining an alternate name, with the following syntax: ``-i <regular expression>`` (default value: ``-i index``).

Rationale
---------
This enhances the readability of a model through homogeneous naming.

Verification
------------
The rule registers to the inputs of operators and raises a violation for each input which satisfies all these conditions:

1. The operator is instantiated with an iterator with index (``mapi``, ``mapwi``, ``foldi``, ``foldwi``, ``mapfoldi``, ``mapfoldwi``)
2. The input corresponds to the index
3. The name of the input does not match the regular expression specified in the rule's parameter

   Message: ``The name does not match the index expression <regexp>``

Resolution
----------
Rename the input.

Customization
-------------
N/A.

.. seealso::
   * :ref:`Name structure of iterator exit condition <RuleNameStructureIteratorContinue>`
   * :ref:`Name structure of accumulator inputs/outputs <RuleNameStructureFoldAccumulator>`
