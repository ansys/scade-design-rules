.. index:: single: Check configuration custom1

Check configuration custom1
###########################

.. rule::
   :filename: check_configuration_custom1.py
   :class: CheckConfigurationCustom1
   :id: id_0104
   :reference: n/a
   :kind: specific
   :tags: configuration

   Check configuration

Description
===========

.. start_description

Check given configuration for these settings:
parameter: 'conf=' Name of configuration: e.g.: conf=KCG
'rootPackage=' Name of root package: e.g.: rootPackage=package1

.. end_description

The list of parameters is given as a comma-separated string. Parameters are:

* ``conf``: name of the configuration to check.
* ``rootPackage``: name of the root package in the configuration.

Rationale
=========
This illustrates how to perform a series of arbitrary, custom checks on a configuration.

Verification
============
This rule finds the target configuration in the current project and makes a series of custom verifications on it:

#. "Skip unused model objects" parameter is unchecked
#. Root node name starts with ``SoftwareComponents::ACD_Appl::``
#. Target adaptor is set to "None" under Code Integration
#. Under Optimizations, "Local variables as static" and "Input threshold" are unchecked
#. User configuration is set to ``..\..\include\<model_name>_user_macros.h``
#. CPU type is set to ``win64``
#. Annotation type file ``..\..\..\..\architecture\scade_plugins\fcmsAnnotationType\MyAnnotationType_suite.aty`` is used
#. If "Global Prefix" is set, its value also prefixes the name of the root operator

Resolution
==========
Modify the offending configuration as detailed in the rule failure message.

Customization
=============
N/A.
