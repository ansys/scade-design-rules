.. index:: single: Element Names Unique In Project

Element Names Unique In Project
===============================

.. rule::
   :filename: element_names_unique_in_project.py
   :class: ElementNamesUniqueInProject
   :id: id_0124
   :reference: n/a
   :kind: specific
   :tags: naming

   The name of an element shall not be used for any other element.

Description
-----------

.. start_description

The name of an element shall not be used for any other element (of the same kind) in the entire project (+ libraries)

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that names are unique throughout the model.

Verification
------------
The rule registers to constants and raises a violation when a name is used by another constant in the model.

  Message: ``Element name also used here: <list_of_conflicting_constant_paths>``

Resolution
----------
Rename the offending constants to ensure unicity.

Customization
-------------
N/A.
