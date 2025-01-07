.. index:: single: Maximum diagrams per element

Maximum diagrams per element
============================

.. rule::
   :filename: maximum_diagrams_per_element.py
   :class: MaximumDiagramsPerElement
   :id: id_0065
   :reference: SDR-30-1
   :kind: generic
   :tags: structure

   Maximum diagrams per element

Description
-----------

.. start_description

Maximum diagrams defining an operator, a state, or an action.
Parameter: maximum value: e.g.: '7'

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by placing an upper bound on the number of graphical diagrams for each model element.

Verification
------------
This rule checks all operators, state machines, state machine actions/states, and variables in the model.
It retrieves the :ref:`Number of diagrams per element <MetricNumberOfDiagramsPerElement>` metric associated to each element.

The rule fails if the limit exceeds the authorized maximum.

Resolution
----------
Modify the offending element to reduce its number of diagrams, as detailed in the rule failure message.

Customization
-------------
This rule depends on the :ref:`Number of diagrams per element <MetricNumberOfDiagramsPerElement>`
metric, that must be included in the package. If you customize the ID of this metric, you must
provide it when instantiating the rule, using the parameter ``metric_id``.

Cf. :ref:`ug_customization` for an example.
