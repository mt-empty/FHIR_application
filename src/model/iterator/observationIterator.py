import collections.abc

from model.patient import Patient

class ObservationIterator(collections.abc.Iterator):
    """
    inherits from python collections.abc — Abstract Base Classes for Containers
    https://docs.python.org/3/library/collections.abc.html#module-collections.abc

    ObservationIterator - a concrete implementation of the Iterator interface.
    """

    def __init__(self, __observation_list):
        self.__observation_list = __observation_list._get_observation_list()
        self.__observation_code = __observation_list._get_observation_code()
        self.n = -1

    def __next__(self):
        self.n +=1
        if self.n >= len(self.__observation_list):  # if no_elements_to_traverse:
            raise StopIteration
        if self.__observation_list[self.n].has_observation(self.__observation_code):
            return self.__observation_list[self.n]  # return element if it meets the above condition
        else:
            return self.__next__()
