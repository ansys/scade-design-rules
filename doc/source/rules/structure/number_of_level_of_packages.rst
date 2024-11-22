.. index:: single: Number Of Level Of Packages

Number of level of packages
===========================

.. rule::
   :filename: number_of_level_of_packages.py
   :class: NumberOfLevelOfPackages
   :id: id_0068
   :reference: n/a
   :kind: generic
   :tags: structure

   Number of level per packages

Description
-----------

.. start_description

Number of level per packages.

.. end_description

The rule parameter is an integer with the maximum authorized depth for nested packages. Default value is ``2``.

Rationale
---------
This enforces compliance with a specific modeling standard by placing an upper bound on the depth of nested packages.

Verification
------------
This rule recursively checks, for each package in the model, the depth of nested sub-packages.
It fails if a chain of nested packages exceeds the maximum authorized depth.

Note: a package with no sub-package has depth ``1``.

Resolution
----------
Modify the offending packages to reduce maximum depth, as detailed in the rule failure message.

Customization
-------------
N/A.
