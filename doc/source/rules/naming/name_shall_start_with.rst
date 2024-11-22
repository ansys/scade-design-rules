.. index:: single: Name shall start with

Name shall start with
=====================

.. rule::
   :filename: name_shall_start_with.py
   :class: NameShallStartWith
   :id: id_0044
   :reference: n/a
   :kind: generic
   :tags: naming

   Name shall start with

Description
-----------

.. start_description

Name shall start with 'parameter'
parameter: starting string, for example: 'eq\_'

.. end_description

The rule parameter describes the desired prefix. Default value is ``eq_``.

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that all names start with the same prefix.

Verification
------------
The rule registers to diagrams. It raises a violation when the element name does not start with the expected prefix.

  Message: ``Name does not start with <parameter>``

Resolution
----------
Rename the offending element.

Customization
-------------
TODO
