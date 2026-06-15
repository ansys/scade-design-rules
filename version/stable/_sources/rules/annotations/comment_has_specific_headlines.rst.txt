.. index:: single: Comment has specific headlines

Comment has specific headlines
##############################

.. rule::
   :filename: comment_has_specific_headlines.py
   :class: CommentHasSpecificHeadlines
   :id: id_0009
   :reference: n/a
   :kind: specific
   :tags: annotations

   The comment of an Operator shall have specific headlines.

Description
===========

.. start_description

The comment of an object shall have specific headlines defined in parameter.
parameter: comma separated list of headlines, for example: Purpose, Algorithm

.. end_description

The list of expected headlines is given as a comma-separated string.
The operator comment is expected to start with one line per headline, starting with the headline name and a column.

For example, when ``headline=Purpose,Algorithm``, the expected comment pattern is::

  Purpose: <any text>
  Algorithm: <any text>
  <any text>

Rationale
=========
This enforces compliance with a specific modeling standard by ensuring operators include
a comment that start with a list of predetermined headlines.

Verification
============
This rule checks each operator to ensure it has a comment and that the comment matches the expected pattern.

Resolution
==========
Modify offending operator comments to comply with the expected pattern.

Customization
=============
TODO
