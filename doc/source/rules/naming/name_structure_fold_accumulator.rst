.. index:: single: Accumulator Inputs/Outputs

Accumulator Inputs/Outputs
==========================

.. rule::
   :filename: name_structure_fold_accumulator.py
   :class: NameStructureFoldAccumulator
   :id: id_0049
   :reference: SDR-19
   :tags: naming

   Name structure of accumulator inputs/outputs

Description
-----------
For the operators iterated with fold constructs (fold, foldi, foldw, foldwi, mapfold, mapfoldi, mapfoldw, mapfoldwi):

* The accumulators are defined by a name prefixed by 'acc'.
* The input/output variables of an accumulator shall be discriminated by   the suffix 'In' for the inputs and 'Out' for the outputs.
* The input and output names of the accumulators match.

The parameter allows specifying a regular expression for input and output names.
For example: '-i acc(.*)In -o acc(.*)Out'. The parenthesis identifies the common part of both names that must match.

When strict is set, the rules verifies the names are not used for variables which are not accumulators.

.. end_description

The rule's parameter has the following syntax: ``in=<regular expression>, out=<regular expression>[, strict=<bool>]``
(default value: ``in=acc.*In, out=acc.*Out``) with:

* ``in``: Regular expression for the name of the accumulator inputs
* ``out``: Regular expression for the name of the accumulator outputs
* ``strict``: Optional parameter to prevent the usage of ``in``/``out`` expressions for variables which are not accumulators.

Rationale
---------
This enhances the readability of a model through homogeneous naming.

Verification
------------
The rule registers to the inputs and outputs of operators and raises a violation for each element which satisfies all these conditions:

1. The operator is instantiated with an iterator with accumulator (``fold``, ``foldi``, ``foldw``, ``foldwi``, ``mapfold``, ``mapfoldi``, ``mapfoldw``, ``mapfoldiw``).
2. The input (resp. output) corresponds to an accumulator input (resp. output).
3. The name of the input (resp. output) does not match the regular expression ``in`` (resp. ``out``) specified in the rule's parameter.

  Message: ``The name does not match the input accumulator expression <regexp>``
  (resp. ``The name does not match the output accumulator expression <regexp>``)

When the option strict is set, the rule raises a violation for inputs (resp. outputs)
which name match the regular expression ``in`` (resp. ``out``), and does not correspond to an accumulator.

Message: ``The variable is not used as an accumulator``

Resolution
----------
Rename the model element.

Customization
-------------
N/A.

.. seealso::
  * :ref:`Name structure of iterator exit condition <RuleNameStructureIteratorContinue>`
  * :ref:`Name structure of iterator index <RuleNameStructureIteratorIndex>`
