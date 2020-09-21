import collections.abc

from model.iterator.observationIterator import ObservationIterator
from model.observation.observationCode import ObservationCode

class ObservationList(collections.abc.Iterable):
    """
    inherits from python collections.abc — Abstract Base Classes for Containers
    https://docs.python.org/3/library/collections.abc.html#module-collections.abc

    ObservationList - a concrete implementation of Iterable abstract class
    This only supports __iter__ functionality
    """
    def __init__(self, __patient_list = [], __observation_code = ObservationCode.CHOLESTEROL):
        self.__patient_list = __patient_list
        self.__observation_code = __observation_code

    def _get_observation_list(self):
        return self.__patient_list
    
    def _get_observation_code(self):
        return self.__observation_code

    def __iter__(self):
        return ObservationIterator(self)