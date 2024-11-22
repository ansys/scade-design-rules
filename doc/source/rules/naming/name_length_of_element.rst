.. index:: single: Name Length Of Element

Element name length
===================

.. rule::
   :filename: name_length_of_element.py
   :class: NameLengthOfElement
   :id: id_0041
   :reference: n/a
   :kind: generic
   :tags: naming

   Name length too long

Description
-----------

.. start_description

Detect elements with a name length of more than 'parameter-value'

.. end_description

The rule parameter describes the desired maximum name length. Default value is ``32``.

Rationale
---------
This enforces compliance with a specific modeling standard by placing an upper bound on name length throughout a model.

Verification
------------
The rule registers to all model elements. It raises a violation when the element name is strictly longer than the parameter value.

  Message: ``<element> name longer than <parameter> characters``

Resolution
----------
Rename the offending element.

Customization
-------------
TODO
