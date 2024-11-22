.. index:: single: Separate Filename

Separate filename
=================

.. rule::
   :filename: separate_filename.py
   :class: SeparateFilename
   :id: id_0081
   :reference: n/a
   :kind: generic
   :tags: packages

   Separate File Name Checked

Description
-----------

.. start_description

This rule checks that all packages have the option Separate File Name selected.

.. end_description

Rationale
---------
This ensures that multi-file management settings are homogeneous across a model.
When Separate File Name is checked, each package is saved into its own individual file, facilitating teamwork across a model.

Note that root-level packages always have their own file.
Child packages may be configured to have their own file or share the parent package's file.

Verification
------------
This rule verifies each package in the model and ensures its Separate File Name setting is selected.

Resolution
----------
Fix the Separate File Name setting for offending packages.

Customization
-------------
N/A.
