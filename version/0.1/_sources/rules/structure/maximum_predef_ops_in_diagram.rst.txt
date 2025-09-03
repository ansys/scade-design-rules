.. index:: single: Maximum predefined operators in diagram

Maximum predefined operators in diagram
########################################

.. rule::
   :filename: maximum_predef_ops_in_diagram.py
   :class: MaximumPredefOpsInDiagram
   :id: id_0073
   :reference: SDR-30-3
   :kind: generic
   :tags: structure

   Maximum predefined operators in diagram

Description
===========

.. start_description

Maximum graphical primitive operator instances within a diagram. This metric also includes textual equations.
Parameter: maximum value: e.g.: '15'

.. end_description

The rule parameter is an integer value describing the maximum authorized number of predefined operators. Default value is ``15``.

Rationale
=========
This enforces compliance with a specific modeling standard by placing an upper bound
on the number of predefined operators that may be instantiated in a diagram.

Verification
============
This rule checks all graphical diagrams in the model.
It retrieves the :ref:`Number of predef ops in diagram <MetricNumberOfPredefOpsInDiagram>` metric associated to each diagram,
and fails if the count exceeds the authorized maximum.

Resolution
==========
Modify the diagram to reduce the number of predefined operator instances.

Customization
=============
This rule depends on the :ref:`Number of predef ops in diagram <MetricNumberOfPredefOpsInDiagram>`
metric, that must be included in the package. If you customize the ID of this metric, you must
provide it when instantiating the rule, using the parameter ``metric_id``.

Cf. :ref:`ug_customization` for an example.
