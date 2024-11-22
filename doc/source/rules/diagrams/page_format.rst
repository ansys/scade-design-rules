.. index:: single: Page format

Page format
===========

.. rule::
   :filename: page_format.py
   :class: PageFormat
   :id: id_0113
   :reference: n/a
   :kind: specific
   :tags: diagrams

   Check Page Format.

Description
-----------

.. start_description

This rule checks if the page format is set properly.
param1: format=A3 A4 B5 etc.
param2: orientation=Portrait Landscape
e.g.: format=A3,orientation=Landscape

.. end_description

The list of parameters is given as a comma-separated string. Parameters are:

* ``format``: desired page format. Possible values: ``A3``, ``A4``, ``A5``, ``LEGAL``, ``LETTER``.
* ``orientation``: desired page orientation. Possible values: ``Landscape``, ``Portrait``.

Rationale
---------
This enforces compliance with a specific project page format printing standard by ensuring properties comply with expectations.

Verification
------------
This rule checks the project-level page format properties and compares them to the given parameter values.

Resolution
----------
Modify the project's page configuration to match expectations.

Customization
-------------
TODO
