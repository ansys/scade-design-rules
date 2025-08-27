.. index:: single: Name shall not start with

Name shall not start with
#########################

.. rule::
   :filename: name_shall_not_start_with.py
   :class: NameShallNotStartWith
   :id: id_0043
   :reference: n/a
   :kind: generic
   :tags: naming

   Name shall not start with

Description
===========

.. start_description

Name shall not start with 'parameter-value'

.. end_description

The rule parameter describes the forbidden prefix. Default value is ``_``.

Rationale
=========
This enforces compliance with a specific modeling standard by ensuring that no name starts with a given prefix.

Verification
============
The rule registers to all diagram elements. It raises a violation when the element name starts with the forbidden prefix.

  Message: ``Name starts with <parameter>``

Resolution
==========
Rename the offending element

Customization
=============
TODO
