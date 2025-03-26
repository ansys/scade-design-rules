.. index:: single: Check configuration

Check configuration
###################

.. rule::
   :filename: check_configuration.py
   :class: CheckConfiguration
   :id: id_0103
   :reference: n/a
   :kind: generic
   :tags: configuration

   Check configuration

Description
===========

.. start_description

Check given configuration against existing project.

.. end_description

The list of parameters is given as a comma-separated string. Parameters are:

* ``conf``: name of the configuration to check in the current project.
* ``project``: path to the project containing the reference configuration. Local to the current folder.
* ``conf_source``: name of the reference configuration.

Rationale
=========
This enforces the existence of a configuration in the current project,
with the same properties and values as in a given reference project.

One use case for this is working with multiple projects that must generate the same artifacts in the same way
(for example: generate code and cross-compile for the same embedded target).

Verification
============
This rule opens the reference project and searches for the reference configuration.
Once found, it inventories the reference configuration's properties and values.

Then, it searches for the configuration to check in the current project.
Once found, it builds a set of the differences between the reference configuration and the current configuration.

The rule succeeds only if there are no differences between the reference configuration and current configuration.
Note that configuration names may be different as they are tied to two separate rule parameters.

Resolution
==========
Modify the offending configuration to comply with that of the source project, as detailed in the rule failure message.

Customization
=============
N/A.
