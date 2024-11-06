.. index:: single: Checker No Warnings Errors

Checker No Warnings Errors
==========================

.. rule::
   :filename: checker_no_warnings_errors.py
   :class: CheckerNoWarningsErrors
   :id: id_0118
   :reference: n/a
   :kind: specific
   :tags: tool

   Semantic checker shall raise no errors and warnings

Description
-----------

.. start_description

This rule checks if the semantic checker reports no errors and no warnings.
parameter: conf=configuration name

.. end_description

Default parameter value is ``conf=KCG``.

Rationale
---------
This rule runs the SCADE semantic checker at the same time as design rules are checked.

Verification
------------
The rule launches the SCADE semantic checker on the project with the specified configuration.
It raises a violation in case of warnings or errors.

Resolution
----------
Fix semantic checker errors or warnings.

Customization
-------------
N/A.
