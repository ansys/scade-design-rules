"""Example of custom metric and rule."""

from ansys.scade.design_rules.metrics.number_of_outgoing_transitions_per_state import (
    NumberOfOutgoingTransitionsPerState,
)
from ansys.scade.design_rules.structure.maximum_outgoing_transitions_per_state import (
    MaximumOutgoingTransitionsPerState,
)

# Instantiation of a metric with a custom id
NumberOfOutgoingTransitionsPerState(id='COUNT_OUT_TRANS')
# Instantiation of a rulen based on this metric, with a custom id
MaximumOutgoingTransitionsPerState(id='MAX_OUT_TRANS', metric_id='COUNT_OUT_TRANS')
