# Make sure you are connected to Monash vpn
import requests
from logging import exception


from api.apiFetchInterface import ApiFetchInterface

from model.observation.cholesterol import Cholesterol
from model.observation.bloodPressure import BloodPressure
from model.observation.tobaccoSmokingStatusNHIS import TobaccoSmokingStatusNHIS
from model.observation.observation import Observation
from model.patient import Patient
from model.observation.observationCode import ObservationCode
from model.address import Address

class ApiFetch(ApiFetchInterface):
    """This class requests data from monash server
    """

    def __init__(self):
        self.__root_url = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/'
        # this unique patient ids
        self.__unique_patient_ids = []
        self.__has_called_get_patients_of_hp = False
        self.__next_page_url = None
        # max number of patients to be requested at a time
        self.__MAX_PATIENT_BATCH = 10

    def get_patient_info(self, patient):
        """given a patient it populates all attributes except observations such as cholesterol

        Arguments:
            patient {patient} -- patient object

        Returns:
            bool: True if successfull otherwise False
        """
        # toggle _set_details_has_been_fetched to True to minimize network traffic
        patient._set_details_has_been_fetched()

        url = self.__root_url + "Patient" + "/" + str(patient.get_identifier())
        data = self.__request_json(url)

        try:
            name = data.get('name')
            patient.set_given_name(name[0].get('given')[0])
            patient.set_family_name(name[0].get('family'))
            patient.set_birthdate(data.get('birthDate'))
            patient.set_gender(data.get('gender'))

            address_entry = data.get('address')[0]
            line = address_entry.get('line')[0]
            city = address_entry.get('city')
            state = address_entry.get('state')
            postalCode = address_entry.get('postalCode')
            country = address_entry.get('country')

            patient.set_address(Address(line, city, state, postalCode, country))

            return True
        except KeyError:
            return None
        except:
            return None

    def get_patients_of_hp(self, health_practitioner_identifier):
        """returns unique patients for a given health practitioner, returns empty list if the hp has no patients

        Arguments:
            health_practitioner_identifier {str} -- health practitioner identifier

        Returns:
            array -- array of patients, or empty list if the hp has no patients
        """
        self.__has_called_get_patients_of_hp = True
        patient_list = []

        url = self.__root_url+"Encounter?participant.identifier=" + \
            health_practitioner_identifier + \
            "&_include=Encounter.participant.individual&_include=Encounter.patient"
        patient_list.extend(self.__get_patients_of_hp_implementation(url))
        if len(patient_list) < self.__MAX_PATIENT_BATCH:
            patient_list.extend(self.get_more_patients_of_hp())
        return patient_list

            
    def get_more_patients_of_hp(self):
        """
        returns more unique patients, returns empty list if the hp has no patients
        It is assumed that it this application will be single session basis
        This should be called after @get_patients_of_hp()

        Returns:
            array -- array of patients, or empty list if the hp has no patients
        """
        if not self.__has_called_get_patients_of_hp:
            raise ValueError('This method must be called after "get_patients_of_hp(self, health_practitioner_identifier)"')

        patient_list = []

        while self.__next_page_url != None and len(patient_list) < self.__MAX_PATIENT_BATCH:
            patient_list.extend(self.__get_patients_of_hp_implementation(self.__next_page_url))

        return patient_list

    def __get_patients_of_hp_implementation(self, url):
        """returns a list of patients for a given encounter url

        Arguments:
            url {str} -- encounter url

        Returns:
            array -- array of patients
        """
        all_encouters_practitioner = self.__request_json(url)

        self.__next_page_url = None
        links = all_encouters_practitioner['link']
        for i in range(len(links)):
            link = links[i]
            if link['relation'] == 'next':
                self.__next_page_url = link['url']

        # print(all_encouters_practitioner)
        all_encouter_data = all_encouters_practitioner.get('entry')

        patient_list = []

        for entry in all_encouter_data:
            try:
                patient_name = entry.get('resource').get('subject').get('display')
                patient_id = entry.get('resource').get('subject').get('reference').split('/')[1]

                if patient_id not in self.__unique_patient_ids:
                    self.__unique_patient_ids.append(patient_id)

                    patient = Patient(patient_id, patient_name)
                    patient_list.append(patient)
                else:
                    continue
            except KeyError:
                # practitioner doesn't have any encounter
                continue

        return patient_list

    def get_latest_obs(self, identifier, observation_code):
        """
        returns the latest observation of for a given patient id and ObservationCode, None if the patients doesn't have that observation

        Args:
            identifier {str} -- patient identifier
            observation_code {ObservationCode} -- observation code

        Returns:
            observation: an observation of the requested code, None if the patients doesn't have that observation
        """
        obs = self.__get_patient_observations(identifier, observation_code, 1, True)
        return obs[0] if obs !=None else None

    def get_recent_observations(self, identifier, observation_code, count=5):
        """
        returns the most recent(upto 5) observations of for a given patient id and ObservationCode, None if the patients doesn't have that observation

        Args:
            identifier {str} -- patient identifier
            observation_code {ObservationCode} -- observation code
            count {str} -- number of observation to be returned (default: {5})

        Returns:
            [observation]: a list of observation, None if the patients doesn't have that observation
        """
        obs = self.__get_patient_observations(identifier, observation_code, count, True)
        return obs if obs !=None else None

    def __get_patient_observations(self, identifier, observation_code, count=None, sort_by_latest=True):
        """returns an array of observations of a given type for a given patient.

        Arguments:
            identifier {str} -- patient identifier
            observation_code {ObservationCode} -- observation code

        Keyword Arguments:
            count {str} -- number of observation to be returned (default: {None})
            sort_by_latest {boolean} -- indicates which order to return the results, defaults to returning the latest (default: {True})

        Returns:
            [observation] -- an array of observation for a given patient
        """
        observation_code_value = observation_code.value

        url = self.__root_url + "Observation?patient=" + \
            str(identifier) + "&code=" + str(observation_code_value)
        if count != None:
            url += "&_count=" + str(count)
        if sort_by_latest:
            url += "&_sort=" + "-date"
        else:
            url += "&_sort=" + "date"

        data = self.__request_json(url)

        entries = data.get('entry')
        return self.__instantiate_observations(entries,observation_code)

    def __instantiate_observations(self, entries,observation_code):
        """
        Used to instantiate observations, given a dictionary, it returns a list of observations

        Args:
            entries ({str}): a dictionary that contain observations
            observation_code {ObservationCode} -- observation code

        Raises:
            ValueError: if there is no value for the given key

        Returns:
            [observation] -- an array of observation
        """
        observations = []
        try:
            for entry in entries:

                item = entry.get('resource')
                if observation_code == ObservationCode.BLOOD_PRESSURE:
                    componenet = item.get('component')
                    Diastolic_value = componenet[0].get('valueQuantity').get('value')
                    Systolic_value = componenet[1].get('valueQuantity').get('value')
                    unit = componenet[0].get('valueQuantity').get('unit')
                    issued = item.get('issued')

                    record = BloodPressure(ObservationCode.BLOOD_PRESSURE, {"Diastolic_value": Diastolic_value, "Systolic_value": Systolic_value}, unit, issued)

                elif observation_code == ObservationCode.TOBACCO_SMOKING_STATUS_NHIS:
                    value = item.get('valueCodeableConcept').get('text')
                    unit = None
                    issued = item.get('issued')

                    record = TobaccoSmokingStatusNHIS(ObservationCode.TOBACCO_SMOKING_STATUS_NHIS, value, unit, issued)

                elif observation_code == ObservationCode.CHOLESTEROL:
                    value = item.get('valueQuantity').get('value')
                    unit = item.get('valueQuantity').get('unit')
                    issued = item.get('issued')

                    record = Cholesterol(ObservationCode.CHOLESTEROL, value, unit, issued)
                else:
                    raise ValueError('input observation code did not match any class')

                observations.append(record)

            return observations

        except KeyError:
            #patient doesn't have any observation entries
            return None
        except:
            return None

    def __request_json(self, url):
        """
        returns json format of the requested url

        Args:
            url (str): the page to request

        Raises:
            requests.exceptions.ConnectionError: if the server did not process the request

        Returns:
            json: the json format of the requested url
        """
        response = requests.get(url=url)
        if 200 >= response.status_code < 400:
            return response.json()
        else:
            message = response.text
            raise requests.exceptions.ConnectionError(message)

