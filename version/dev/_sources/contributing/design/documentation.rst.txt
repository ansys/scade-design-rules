Documentation
#############

Design
======

Rule
----

Each rule must have an associated documentation file with the following sections:

* Description: Description of the checks performed by the rule.
* Rationale: Purpose of the rule.
* Verification: How the verification is performed, which is particularly useful
  when it is not possible to automate completely the verification of a rule.
* Resolution: How to fix the violation.
* Customization: How to customize the rule, when applicable.
  The most common means are as follows:

  * Checked elements: For example, model elements that should comply to a given naming rule.
  * Sub-classing: Modify the default behavior of a rule by deriving a new one and redefining one or more functions.

The documentation file also contains metadata for queries or building tables.

The files are located in the ``./doc/source/rules`` directory.
The structure of this directory must match the structure of ``./src/ansys/scade/design_rules``.

Each directory containing rules' documentation must have a ``index.rst`` file that
provides a general overview and a table listing all the contained rules.

Metric
------

Each metric must have an associated documentation file with the following sections:

* Description: Description of the metric.
* Computation: How the computation is performed.
* Customization: How to customize the metric, when applicable.

The documentation file also contains metadata for queries or building tables.

The files are located in the directory ``./doc/source/metrics``.
The structure of this directory must match the structure of ``./src/ansys/scade/design_rules/metrics``.

The directory containing metrics' documentation must have a ``index.rst`` file that
provides a general overview and a table listing all the contained metrics.

Tools
=====

The ``pre-commit`` hook ``update_doc`` ensures each metric or rule is documented and consistent.
It is based on naming rules.

When a rule has no associated documentation, the hook creates a new file
with all sections and metadata.
Then, it replicates information from the rule's Python file:
* id
* label
* description
* filename
* class

The part of the updated description is delimited by:

* The beginning of the section ``Description`` or the tag ``.. start_description`` if present
* The end of the section ``Description`` or the tag ``.. end_description`` if present.

Any additional description text outside those limits is preserved when updating the documentation.

This tool also creates a default ``index.rst`` file when it does not exist.
