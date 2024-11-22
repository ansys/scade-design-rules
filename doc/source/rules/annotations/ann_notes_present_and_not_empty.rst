.. index:: single: Ann Notes Present And Not Empty

Ann notes present and not empty
===============================

.. rule::
   :filename: ann_notes_present_and_not_empty.py
   :class: AnnNotesPresentAndNotEmpty
   :id: id_0108
   :reference: n/a
   :kind: specific
   :tags: annotations

   AnnotationNotes present and not empty

Description
-----------

.. start_description

Check if an element has a specific annotation note type attached to it. In addition it is checked that the given field elements are present and not empty.
parameter: '-t': Name of the annotation note type: e.g.: '-t AnnType'
'-n': Names of annotation note elements: e.g.: -n AT1_Field1 AT1_Field2 AT1_Field3

.. end_description

The rule's parameter has the following syntax: ``-t <type> -n <attribute> [<attribute> ...]``
(default value: ``-t AnnType_1 -n AT1_Field1 AT1_Field2 AT1_Field3``) with::

  -t <type>, --note_type <type>
                        note type
  -n <attribute> [<attribute> ...], --names <attribute> [<attribute> ...]
                        Names of the note elements


Rationale
---------
This enforces compliance with a specific modeling standard by ensuring uniform documentation of model elements through annotations.

Verification
------------
This rule checks that model entities of specified types contain annotations of specified types and attributes.

It applies by default to constants and operators.

Resolution
----------
Modify the offending operator interface element to add missing annotations, as detailed in the rule failure message.

Customization
-------------
You can override the ``kinds`` (default ``None``) or ``types`` (default ``[suite.Constant, suite.Operator]``) parameters
when instantiating the rule to specify the objects to consider.
