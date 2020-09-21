from api.apiFetch import ApiFetch
from model.observation.observation import Observation
from model.observation.observationCode import ObservationCode
from model.healthPractitioner import HealthPractitioner


class Controller:

    def __init__(self):
        """
        Initialize links to the model
        """
        self.api = ApiFetch()
        self.HP_ID = "http://hl7.org/fhir/sid/us-npi|500"  # hard coded Health Practitioner (since log in function isn't needed)
        self.HP_OBJ = HealthPractitioner(self.HP_ID, "Vada440", "Nienow652")

    def get_patients(self):
        """
        Retrieve patients of the Health Practitioner
        :return: List of patients
        """
        patients = self.api.get_patients_of_hp(self.HP_ID)
        self.HP_OBJ.add_patients(patients)
        return patients

    def get_more_patients(self):
        """
        Retrieve more patients of the Health Practitioner
        :return: List of patients
        """
        patients = self.api.get_more_patients_of_hp()
        self.HP_OBJ.add_patients(patients)
        return patients

    def get_detailed_patient_info(self, patient):
        """
        Retrieve detailed information of patient
        :param patient: patient to get info for
        :return: True if successful, False otherwise
        """
        return self.api.get_patient_info(patient)

    def add_monitored_patient(self, patient):
        """
        Add patient to monitor list of Health Practitioner
        :param patient: patient to add to the monitor list
        :return: None
        """
        self.HP_OBJ.add_monitored_patients([patient])

    def remove_monitored_patient(self, patient):
        """
            Remove patient from monitor list of Health Practitioner
            :param patient: patient to remove from the monitor list
            :return: None
        """
        self.HP_OBJ.remove_monitored_patients(patient)

    def update_patient_obs(self, obs_code, patient):
        """
        Update patient observation
        :param obs_code: code of observation to update
        :param patient: patient to update
        :return: None
        """
        obs = self.api.get_latest_obs(patient.get_identifier(), obs_code)
        if obs is not None:
            patient.update_observation(obs)

    def update_recent_patient_obs(self, obs_code, patient):
        """
        Update recent patient observations
        :param obs_code: code of observation to update
        :param patient: patient to update
        :return: None
        """
        obs = self.api.get_recent_observations(patient.get_identifier(), obs_code)
        if obs is not None:
            patient.update_observation(*obs)
