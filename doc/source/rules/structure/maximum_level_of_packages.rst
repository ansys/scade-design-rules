.. index:: single: Maximum level of packages

Maximum level of packages
=========================

.. rule::
   :filename: maximum_level_of_packages.py
   :class: MaximumLevelOfPackages
   :id: id_0068
   :reference: n/a
   :kind: generic
   :tags: structure

   Maximum level per packages

Description
-----------

.. start_description

Maximum level per packages.

.. end_description

The rule parameter is an integer with the maximum authorized depth for nested packages. Default value is ``2``.

Rationale
---------
This enforces compliance with a specific modeling standard by placing an upper bound on the depth of nested packages.

Verification
------------
It retrieves the :ref:`Level of packages <MetricLevelOfPackages>` metric associated to each package.
It fails if a chain of nested packages exceeds the maximum authorized depth.

Resolution
----------
Modify the offending packages to reduce maximum depth, as detailed in the rule failure message.

Customization
-------------
This rule depends on the :ref:`Level of packages <MetricLevelOfPackages>`
metric, that must be included in the package. If you customize the ID of this metric, you must
provide it when instantiating the rule, using the parameter ``metric_id``.

Cf. :ref:`ug_customization` for an example.
