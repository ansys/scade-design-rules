.. index:: single: Maximum operators per package

Maximum operators per package
#############################

.. rule::
   :filename: maximum_operators_per_package.py
   :class: MaximumOperatorsPerPackage
   :id: id_0071
   :reference: n/a
   :kind: generic
   :tags: structure

   Maximum operators per package

Description
===========

.. start_description

Maximum operators per package.

.. end_description

The rule parameter is an integer value describing the maximum authorized number of operators per package. Default value is ``10``.

Rationale
=========
This enforces compliance with a specific modeling standard by placing an upper bound on the number of operators in each package.

Verification
============
This rule checks each package in the model.
It retrieves the :ref:`Number of operators per package <MetricNumberOfOperatorsPerPackage>` metric associated to each package,
and fails if the count exceeds the authorized maximum.

Resolution
==========
Modify the offending package to reduce its number of operators.

Customization
=============
This rule depends on the :ref:`Number of operators per package <MetricNumberOfOperatorsPerPackage>`
metric, that must be included in the package. If you customize the ID of this metric, you must
provide it when instantiating the rule, using the parameter ``metric_id``.

Cf. :ref:`ug_customization` for an example.
