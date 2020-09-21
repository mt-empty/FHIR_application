
from model.observation.observation import Observation

# inherits from Observation
class BloodPressure(Observation):
    def __init__(self, observation_type, value, unit, date):
        super().__init__(observation_type, value, unit, date)
