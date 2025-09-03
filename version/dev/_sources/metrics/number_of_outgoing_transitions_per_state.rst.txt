.. index:: single: Number of outgoing transitions per state

Number of outgoing transitions per state
########################################

.. metric::
   :filename: number_of_outgoing_transitions_per_state.py
   :class: NumberOfOutgoingTransitionsPerState
   :id: id_0125
   :reference: n/a
   :kind: specific
   :tags: metrics

   Number of outgoing transitions per state

Description
===========

.. start_description

Number of outgoing transitions per state.

.. end_description

Computation
===========
This metric counts the outgoing transitions of a state, flattening the forked transitions.
The outgoing transitions of sub-states are not considered.

Customization
=============
N/A.
