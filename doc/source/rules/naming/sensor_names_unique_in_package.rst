.. index:: single: Sensor names unique in package

Sensor names unique in package
==============================

.. rule::
   :filename: sensor_names_unique_in_package.py
   :class: SensorNamesUniqueInPackage
   :id: id_0121
   :reference: n/a
   :kind: specific
   :tags: naming

   The name of a Sensor shall not be used for variables in the same package.

Description
-----------

.. start_description

The name of a Sensor shall not be used for variables in the same package.

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that operator variables and sensor names are different in any package.

Verification
------------
This rule registers to sensors and raises a violation when an operator variable, in the same package as the sensor, uses the same name.

  Message: ``Sensor name also used for: <variable_full_path>``

Resolution
----------
Rename the offending variable or the offending sensor.

Customization
-------------
N/A.
