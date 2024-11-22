.. index:: single: Identical For Producer Consumer

Identical for producer consumer
===============================

.. rule::
   :filename: identical_for_producer_consumer.py
   :class: IdenticalForProducerConsumer
   :id: id_0027
   :reference: n/a
   :kind: specific
   :tags: annotations

   Identical annotations for producer and consumer

Description
-----------

.. start_description

The annotation notes for producer and consumer shall be identical if they both exist.
If only the consumer has a note raise a 'redefine' warning.
parameter: '-t': Name of the annotation note type

.. end_description

The rule parameter describes the type of the expected matching annotations. Default value ``-t SDD_TopLevel``.

Rationale
---------
This rule enforces harmonized notes for identical signals, as well as their connection to the root operator.

Identical signals are identified by the fact that they are used as output of one operator and input to another.

Verification
------------
The rule registers to operator inputs and outputs, examines connected outputs and inputs, and for each couple, raises a violation when:

* The consumer input defines annotation ``Unit_SI``, but its connected producer output does not

  Message: ``Unit_SI <producer_name> is redefined.``

* Both the current input/output and its connected output/input define annotation ``Unit_SI``, but with different values

  Message: ``Unit_SI: <consumer_name> != <producer_name>.``

* The consumer input defines annotation ``Min_Value``, but its connected producer output does not

  Message: ``Min_Value <producer_name> is redefined.``

* Both the current input/output and its connected output/input define annotation ``Min_Value``, but with different values

  Message: ``Min_Value: <consumer_name> != <producer_name>.``

* The consumer input defines annotation ``Max_Value``, but its connected producer output does not

  Message: ``Max_Value <producer_name> is redefined.``

* Both the current input/output and its connected output/input define annotation ``Max_Value``, but with different values

  Message: ``Max_Value: <consumer_name> != <producer_name>.``

Resolution
----------
Modify the offending annotations to match, as detailed in the rule failure message.

Customization
-------------
TODO.
