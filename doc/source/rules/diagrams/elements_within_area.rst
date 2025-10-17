.. index:: single: Elements within area

Elements within area
####################

.. rule::
   :filename: elements_within_area.py
   :class: ElementsWithinArea
   :id: id_0015
   :reference: SDR-31
   :kind: generic
   :tags: diagrams

   Elements within area.

Description
===========
All elements shall be within the diagram format (A4, A3...).

.. end_description

The parameter defines the printer margins with the following syntax: ``margins=<width>; <height>``
(default value: ``margins=0; 0``). The sizes are expressed in hundredths of a millimeter.

Rationale
=========
This enhances the readability of the printed diagrams, making sure they are printed on a single page.

Verification
============
The rule registers to the graphical elements and raises a violation when elements do not fit in the specified area.

Message: ``Elements outside area found``

Note: The SCADE Python API does not provide information on the bounding box of texts.
For example, the bounding box of an input is fixed and corresponds to the graphical symbol, independently of the length of the input name.

Resolution
==========
There may be several options to consider:

* Split the diagram into several ones
* Move the elements to the top-left corner if the margins are large enough
* Etc.

Hint: Activate the option ``View/Page Bounds`` to anticipate the issues while editing a model.

Customization
=============
N/A.
