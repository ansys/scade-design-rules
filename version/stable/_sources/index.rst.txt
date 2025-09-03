Ansys SCADE Design Rules
########################

Ansys SCADE Design Rules is a database of metrics and rules that enforce various design practices on a SCADE model.

.. grid:: 1 2 3 3
   :gutter: 1 2 3 3
   :padding: 1 2 3 3

   .. grid-item-card:: :material-regular:`power_settings_new;1.25em` Getting started
      :link: getting-started/index
      :link-type: doc

      Learn how to install and use Ansys SCADE Design Rules.

   .. grid-item-card:: :material-regular:`description;1.25em` User guide
      :link: user-guide/index
      :link-type: doc

      Learn how to use Ansys SCADE Design Rules in your SCADE projects.

   .. grid-item-card:: :material-regular:`numbers;1.25em` Metrics
      :link: metrics/index
      :link-type: doc

      Learn more about the metrics included in Ansys SCADE Design Rules.

   .. grid-item-card:: :material-regular:`rule;1.25em` Rules
      :link: rules/index
      :link-type: doc

      Learn more about available rules in Ansys SCADE Design Rules.

   .. grid-item-card:: :material-regular:`group;1.25em` Contributing
      :link: contributing/index
      :link-type: doc

      Learn how to contribute to Ansys SCADE Design Rules.

   .. grid-item-card:: :material-regular:`download;1.25em` Examples
      :link: examples
      :link-type: doc

      Download the example assets (latest version)

   .. grid-item-card:: :material-regular:`update;1.25em` Changelog
      :link: changelog
      :link-type: doc

      View the changelog for Ansys SCADE Design Rules.

.. admonition:: Disclaimer

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

   .. [1] For more information about model rule checking, please refer to the `SCADE Suite User Manual`_.
   .. [2] For more information about a consistent set of rules to apply to a project,
      you may refer to the SCADE Suite Application Software Design Standard document.
      It is delivered with the SCADE product, under ``<SCADE_INSTALL>\help\Common Help Resources\Design Standard\DesignStandard-SCS-SDS.pdf``.

.. toctree::
   :maxdepth: 1
   :hidden:

   getting-started/index
   user-guide/index
   metrics/index
   rules/index
   contributing/index
   examples
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
