
from abc import ABC, abstractmethod

# Make sure you are connected to Monash vpn
import requests

from model.patient import Patient
from model.observation.observationCode import ObservationCode
from model.observation.cholesterol import Cholesterol
from model.observation.observation import Observation

class ApiFetchInterface(ABC):
    """This class requests data from monash server
    """

    @abstractmethod
    def get_patient_info(self, patient: Patient) -> bool:
        """given a patient it populates all attributes except observations such as cholesterol, returns True if successful

        Arguments:
            patient {patient} -- patient object
        """
        pass

    @abstractmethod
    def get_patients_of_hp(self, health_practitioner_identifier: str) -> [Patient]:
        """returns unique patients for a given health practitioner, returns empty list if the hp has no patients
        unless the hp has less than 10 patients, then it always returns 

        Arguments:
            health_practitioner_identifier {str} -- health practitioner identifier

        Returns:
            array -- array of patients, or empty list if the hp has no patients
        """
        pass

    @abstractmethod
    def get_more_patients_of_hp(self) -> [Patient]:
        """
        returns more unique patients, returns empty list if the hp has no patients
        It is assumed that the application is used by single person at a time(single session)
        This should be called after @get_patients_of_hp

        Returns:
            array -- array of patients, or empty list if the hp has no patients
        """

    @abstractmethod
    def get_latest_obs(self, identifier: str, observation_code: ObservationCode) -> Observation:
        """
        returns the latest observation of for a given patient id and ObservationCode, None if the patients doesn't have that observation

        Args:
            identifier {str} -- patient identifier
            observation_code {ObservationCode} -- observation code

        Returns:
            observation: an observation of the requested code, None if the patients doesn't have that observation
        """
        pass

    @abstractmethod
    def get_recent_observations(self, identifier: str, observation_code: ObservationCode, count=int) -> [Observation]:
        """
        returns the most recent(up-to 5) observations of for a given patient id and ObservationCode, None if the patients doesn't have that observation

        Args:
            identifier {str} -- patient identifier
            observation_code {ObservationCode} -- observation code
            count {str} -- number of observation to be returned (default: {5})

        Returns:
            [observation]: a list of observation, None if the patients doesn't have that observation
        """
        pass