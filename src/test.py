
import requests
import pandas as pd
from datetime import datetime

from model.observation.cholesterol import Cholesterol
from model.patient import Patient
from model.healthPractitioner import HealthPractitioner
from model.observation.observationCode import ObservationCode
from model.address import Address
from api.apiFetch import ApiFetch
from model.iterator.observationList import ObservationList

HEALTH_PRACTITIONER_IDENTIFIER_1 = "http://hl7.org/fhir/sid/us-npi|500"
# this one has more patients
HEALTH_PRACTITIONER_IDENTIFIER_2 = "http://hl7.org/fhir/sid/us-npi|850"

# instanciating patients for patient tests
PATIENT_OBJ_1 = Patient("1", "test 1")
PATIENT_OBJ_2 = Patient("29163", "test 2")

# instanciating hp for hp tests
HP_OBJ = HealthPractitioner(
    HEALTH_PRACTITIONER_IDENTIFIER_1, "Vada440", "Nienow652")
api_fetch = ApiFetch()


def test_get_patient_info():
    print("\n##########")
    # get a patient object
    api_fetch.get_patient_info(PATIENT_OBJ_2)
    print("patient", PATIENT_OBJ_2)


def test_get_latest_observation():
    print("\n##########")
    # update the latest observation of this patient
    print("getting the latest observation\n")
    latest_chol = api_fetch.get_latest_obs(
        PATIENT_OBJ_2.get_identifier(), ObservationCode.CHOLESTEROL)
    print("chol observation", latest_chol)

    latest_BP = api_fetch.get_latest_obs(
        PATIENT_OBJ_2.get_identifier(), ObservationCode.BLOOD_PRESSURE)
    print("BP observation", latest_BP)

    latest_SM = api_fetch.get_latest_obs(
        PATIENT_OBJ_2.get_identifier(), ObservationCode.TOBACCO_SMOKING_STATUS_NHIS)
    print("SM observation", latest_SM)

    PATIENT_OBJ_2.update_observation(latest_chol)
    PATIENT_OBJ_2.update_observation(latest_BP)
    print("patient", PATIENT_OBJ_2)

def test_get_resent_observation():
    print("\n##########")
    # update the recent observation of this patient
    print("getting the recent observation\n")
    recent_obs_chol = api_fetch.get_recent_observations(
        PATIENT_OBJ_2.get_identifier(), ObservationCode.CHOLESTEROL)
    print("chol observations", recent_obs_chol)

    recent_obs_BP = api_fetch.get_recent_observations(
        PATIENT_OBJ_2.get_identifier(), ObservationCode.BLOOD_PRESSURE)
    print("BP observations", recent_obs_BP)

    # How to use args, https://stackoverflow.com/questions/3394835/use-of-args-and-kwargs
    PATIENT_OBJ_2.update_observation(*recent_obs_chol)
    PATIENT_OBJ_2.update_observation(*recent_obs_BP)
    print("patient", PATIENT_OBJ_2)

def test_health_practitioner():
    print("\n##########")
    print("health practitioner:", HP_OBJ)


def test_get_patients_of_hp():
    # get list of all encounters with cholesterol
    HP_OBJ.add_patients(api_fetch.get_patients_of_hp(HP_OBJ.get_identifier()))

    print("hp patient list after adding more patients")
    for patient in HP_OBJ.get_patients():
        print(patient)


def test_get_more_patients():
    print("\n##########")
    print("requesting more patients")
    
    temp_array = api_fetch.get_more_patients_of_hp()
    HP_OBJ.add_patients(temp_array)
    i = 0
    while len(temp_array) != 0 and i != 10:
        temp_array = api_fetch.get_more_patients_of_hp()
        HP_OBJ.add_patients(temp_array)
        i+=1
   
    print("\n patient list after getting more patients")
    for patient in HP_OBJ.get_patients():
        print(patient)


def test_get_observation_for_all_hp_patients(observation_code):
    print("\n##########")
    print("test getting patients with", observation_code)

    print("getting", observation_code.name, "for all patients")
    for patient in HP_OBJ.get_patients():
        obs = api_fetch.get_latest_obs(
            patient.get_identifier(), observation_code)
        # check if obs is None
        if obs != None:
            patient.update_observation(obs)

    print("\n patient list after getting updating", observation_code.name)
    for patient in HP_OBJ.get_patients():
        print(patient)


def test_iterator(observation_code):
    print("\n##########")
    print("test iterating through patient with", observation_code)
    print("adding all existing patients to monitored list")
    HP_OBJ.add_monitored_patients(HP_OBJ.get_patients())

    # add patient 2 to test iterator
    HP_OBJ.add_monitored_patients([PATIENT_OBJ_2])

    print("iterating through patients with", observation_code.name)
    for p in HP_OBJ.get_monitored_patients_with_obs(observation_code):
        print("iterating", p)


if __name__ == "__main__":

    # test_get_patient_info()
    # test_get_latest_observation()
    test_get_resent_observation()
    test_get_latest_observation()
    # test_health_practitioner()
    # test_get_patients_of_hp()
    # test_get_more_patients()
    # test_get_observation_for_all_hp_patients(ObservationCode.CHOLESTEROL)
    # test_get_observation_for_all_hp_patients(ObservationCode.BLOOD_PRESSURE)
    # test_get_observation_for_all_hp_patients(ObservationCode.TOBACCO_SMOKING_STATUS_NHIS)
    # test_iterator(ObservationCode.CHOLESTEROL)
    # test_iterator(ObservationCode.BLOOD_PRESSURE)
    # test_iterator(ObservationCode.TOBACCO_SMOKING_STATUS_NHIS)
    # test_next_page()

    # this should throw an error
    # api_fetch.__get_patient_observations(3689, ObservationCode.CHOLESTEROL)

