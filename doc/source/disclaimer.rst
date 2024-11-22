Disclaimer
==========

This repository contains a **catalog of examples for optional rules** that
can be added to the **SCADE Metrics and Rules Checker** [1]_.
Rules are used to enforce various constraints on a model,
such as consistent naming conventions and design methods.

**Please note that all rules are optional**: users should review, select and
adapt only the provided examples that are consistent with their modelling practices [2]_.

Some sample rules in this repository are contradictory;
it would not be possible to satisfy them all on a project.
For example rule ``0088 - Upper Case Naming`` enforces ``NAMES_LIKE_THIS_ONE`` for model elements.
It is incompatible with rule ``0008 - Camel Case Naming``, which enforces ``NamesLikeThatOne``.

..
   [1] For more information about model rule checking, please refer to the
   `SCADE Suite User Manual <https://ansyshelp.ansys.com/public/Views/Secured/SCADE/v232/en/PDFS/SCADE%20Suite%20Help%20Resources/Manuals/User%20Manual/UserManual_SCS-UM-23.pdf#page=535>`_.

.. [1] For more information about model rule checking, please refer to the
   `SCADE Suite User Manual`.
.. [2] For more information about a consistent set of rules to apply to a project,
   you may refer to the SCADE Suite Application Software Design Standard document.
   It is delivered with the SCADE product, under ``<SCADE_INSTALL>\help\Common Help Resources\Design Standard\DesignStandard-SCS-SDS.pdf``.