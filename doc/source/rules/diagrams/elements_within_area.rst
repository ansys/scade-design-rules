.. index:: single: Elements Within Area

Elements Within Area
====================

.. rule::
   :filename: elements_within_area.py
   :class: ElementsWithinArea
   :id: id_0015
   :reference: SDR-31
   :kind: generic
   :tags: diagrams

   Elements within area

Description
-----------
All elements shall be within the page format (A4, A3).

.. end_description

The parameter defines the printable size with the following syntax: ``<width>, <height>``
(default value: ``28435, 19174`` which corresponds to DINA4). The sizes are expressed in hundredth of millimeters.

Rationale
---------
This enhances the readability of the printed diagrams, making sure they are printed on a single page.

Verification
------------
The rule registers to the graphical diagrams and raises a violation when elements do not fit in the specified area.

Message: ``Elements outside area found (<count>) in <diagram name>: <list of elements>``

Note: The SCADE Python API does not provide information on the bounding box of texts.
For example, the bounding box of an input is fixed and corresponds to the graphical symbol, independently of the length of the input name.

Resolution
----------
There may be several options to consider:

* Split the diagram into several ones
* Move the elements to the top-left corner if the margins are large enough
* Etc.

Hint: Make sure the diagrams' page format corresponds to the checked one
and activate the option ``View/Page Bounds`` to anticipate the issues while editing a model.

Customization
-------------
N/A.
