.. index:: single: Maximum user operators in diagram

Maximum user operators in diagram
#################################

.. rule::
   :filename: maximum_user_ops_in_diagram.py
   :class: MaximumUserOpsInDiagram
   :id: id_0074
   :reference: SDR-30-2
   :kind: generic
   :tags: structure

   Maximum user operators in diagram

Description
===========

.. start_description

Maximum graphical user-operator instances within a single diagram.
Parameter: maximum value: e.g.: '7'

.. end_description

The rule parameter is an integer value describing the maximum authorized number of user-defined operators. Default value is ``7``.

Rationale
=========
This enforces compliance with a specific modeling standard by placing an upper bound
on the number of user-defined operators that may be called in a diagram.

Verification
============
This rule checks all graphical diagrams in the model.
It retrieves the :ref:`Number of user operators in diagram <MetricNumberOfUserOpsInDiagram>` metric associated to each diagram,
and fails if the count exceeds the authorized maximum.

Resolution
==========
Modify the diagram to reduce the number of user-defined operator calls.

Customization
=============
This rule depends on the :ref:`Number of user operators in diagram <MetricNumberOfUserOpsInDiagram>`
metric, that must be included in the package. If you customize the ID of this metric, you must
provide it when instantiating the rule, using the parameter ``metric_id``.

Cf. :ref:`ug_customization` for an example.
