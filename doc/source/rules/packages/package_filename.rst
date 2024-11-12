.. index:: single: Package Filename

Package Filename
================

.. rule::
   :filename: package_filename.py
   :class: PackageFilename
   :id: id_0077
   :reference: n/a
   :kind: specific
   :tags: packages

   Package File Name Check

Description
-----------

.. start_description

Checks that package file names comply with format <ProjectName>_<PackageName>_Package.xscade.

.. end_description

Rationale
---------
This enforces compliance with a specific naming convention on packages.

Verification
------------
This rule verifies each package in the model and ensures that its name matches the expected pattern.

Resolution
----------
Rename the offending packages.

Customization
-------------
N/A.
