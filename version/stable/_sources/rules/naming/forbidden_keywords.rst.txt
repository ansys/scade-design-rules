.. index:: single: Forbidden keywords

Forbidden keywords
##################

.. rule::
   :filename: forbidden_keywords.py
   :class: ForbiddenKeywords
   :id: id_0022
   :reference: n/a
   :kind: generic
   :tags: naming

   Forbidden Keyword

Description
===========

.. start_description

Specific keywords shall not be used as name.

The parameter is a file containing the keywords, one word per line.

.. end_description

Rationale
=========
This enforces compliance with a specific modeling standard by restricting authorized names throughout a model.

One use case could be to avoid confusion born from naming model elements with names that have an already-established meaning.

Verification
============
The rule subscribes to all model elements. It raises a violation when the element name is a forbidden keyword.

  Message: ``Forbidden keyword used as name``

Resolution
==========
Rename the offending element to avoid using a reserved keyword.

Customization
=============
TODO
