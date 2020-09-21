# importing ABC allows us to easily create abstract classes in python.
from abc import ABC, abstractmethod


class Observer(ABC):

    """

    Observer is an abstract class/interface used for deriving a concreteObserver class.

    """

    # abstract methods have no body definition.
    # this method can be overwritten by derived classes, each of which has their own body definition for said function.
    
    @abstractmethod
    def update_observation(self, *observation):
        """
        given one to many observation entries it, updates the given observation with the entries

        Args:
            observation (Observation): *args of observation

        Raises:
            ValueError: if observations exceed the MAX_OBSERVATION_ENTRIES
        """

        # used to 'skip' the function body - this is declared in the patient class
        pass
