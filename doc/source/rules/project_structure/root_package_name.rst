.. index:: single: Root package name

Root package name
=================

.. rule::
   :filename: root_package_name.py
   :class: RootPackageName
   :id: id_0079
   :reference: n/a
   :kind: specific
   :tags: project_structure

   Root Package has same name as Project

Description
-----------

.. start_description

This rule checks if the root Package has the same name as the Model in which it resides

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that the model contains exactly one root package, named the same as the model itself.

Verification
------------
This rule fails if:

* The model contains zero or more than one root package.
* The model's root package name is different from the model name.

Resolution
----------
Modify the model such that it contains exactly one root package with the same name as the model.

Customization
-------------
N/A.
