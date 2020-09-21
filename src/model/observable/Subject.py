from abc import ABC, abstractmethod

class Subject(ABC):
    """

    Subject is an abstract class/interface used for deriving a concreteSubject class

    """

    # abstract methods have no body definition
    # this method can be overwritten by derived classes, each of which has their own body definition for said function

    @abstractmethod
    def subscribe(self, patient_obj):

        """

        takes a patient object, and subscribes
        said object to the LatestPatientObservations for updates in state change

        :param patient_obj: a reference to a created patient class object

        :return: None

        """

        pass

    @abstractmethod
    def unsubscribe(self, patient_obj):

        """

        takes a patient identifier (representing a patient object), and unsubscribes
        said object from the LatestPatientObservations, so that it stops receiving updates in state change

        :param patient_obj: a reference to a created patient class object

        :return: None

        """
        pass

    @abstractmethod
    def alert_patients(self, obs):

        """

        takes a change in LatestPatientObservations state (cholesterol values, in our use-case)
        and notifies all subscribed observers of the change

        :param obs: an observation for a patient

        :return: None

        """
        pass