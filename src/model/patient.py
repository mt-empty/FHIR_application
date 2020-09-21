from model.observable.Observer import Observer
from model.observation.observationCode import ObservationCode

# This is the maximum number of entries for a given observation 
MAX_OBSERVATION_ENTRIES = 5

class Patient(Observer):

    """

    Patient is a derived class of the Observer abstract class/interface.
    It stores important information about a patient.
    It also adopts observer behaviour, meaning it is capable of listening into another object to receive state change updates

    """

    def __init__(self, __identifier, __display_name, __given_name=None, __family_name=None, __birthdate=None, __gender=None, __address=None):

        """

        __init__ constructs a patient object with the following details, defaulting each value to None

        :param __identifier: the patient identifier (e.g. "26193")
        :param __display_name: the patient's display name
        :param __given_name: the patient's first name
        :param __family_name: the patient's last name
        :param __birthdate: the patient's DOB
        :param __gender: the patient's gender
        :param __address: the patient's address
        :param __details_has_been_fetched: bool (true if this patient's data has been fetched from the API before,
         false otherwise)
        :param __patient_observations: contains patient observations up to MAX_OBSERVATION_ENTRIES for each

        """

        self.__identifier = __identifier
        self.__display_name = __display_name
        self.__given_name = __given_name
        self.__family_name = __family_name
        self.__birthdate = __birthdate
        self.__gender = __gender
        self.__address = __address
        self.__details_has_been_fetched = False
        self.__patient_observations = {ObservationCode.CHOLESTEROL: [None]*MAX_OBSERVATION_ENTRIES, ObservationCode.BLOOD_PRESSURE: [None]*MAX_OBSERVATION_ENTRIES, ObservationCode.TOBACCO_SMOKING_STATUS_NHIS: [None]*MAX_OBSERVATION_ENTRIES}


    def get_identifier(self):

        """

        retrieves the patient's identifier

        :return: patient's identifier

        """

        return self.__identifier

    def get_display_name(self):
        """

        retrieves the patient's display name

        :return: patient's display name

        """
        return self.__display_name

    def get_given_name(self):

        """

        retrieves the patient's first name

        :return: patient's first name

        """
        return self.__given_name

    def set_given_name(self, __given_name):
        """
        sets a new first name for the patient

        :param __given_name: the new first name

        :return: None

        """
        self.__given_name = __given_name

    def get_family_name(self):
        """

        retrieves the last name of the patient

        :return: patient's last name

        """
        return self.__family_name

    def set_family_name(self, __family_name):

        """

        sets a new last name for the patient

        :param __family_name: the new last name

        :return: None

        """
        self.__family_name =__family_name

    def get_birthdate(self):

        """

        retrieves the patient's DOB

        :return: patient's DOB

        """
        return self.__birthdate

    def set_birthdate(self, __birthdate):

        """

        sets a new DOB

        :param __birthdate: the new DOB

        :return: None

        """
        self.__birthdate = __birthdate

    def get_gender(self):

        """

        retrieves the patient's gender

        :return: patient's gender

        """
        return self.__gender

    def set_gender(self, __gender):

        """

        sets a new gender

        :param __gender: the new gender

        :return: None

        """
        self.__gender = __gender

    def get_address(self):

        """

        retrieves the patient's address

        :return: the patient's address

        """
        return self.__address

    def set_address(self, __address):
        """

        sets a new address

        :param __address: the new address

        :return: None

        """
        self.__address = __address

    def get_details_has_been_fetched(self):
        """
        returns whether patient details has been fetched from the server

        Returns:
            bool: True if the details has been fetched
        """
        return self.__details_has_been_fetched

    def _set_details_has_been_fetched(self):
        """
        sets whether patient details has been fetched from the server to True

        Args:
            been_fetched (bool): True if the details has been fetched
        """
        self.__details_has_been_fetched = True

    def update_observation(self, *observation):
        """
        given one to many observation entries it, updates the given observation with the entries

        Args:
            observation (Observation): *args of observation

        Raises:
            ValueError: if observations exceed the MAX_OBSERVATION_ENTRIES
        """

        if len(observation) > MAX_OBSERVATION_ENTRIES:
            raise ValueError("can't have more than the MAX_OBSERVATION_ENTRIES")
        for i, entry in enumerate(observation):
            self.__patient_observations[entry.get_observation_type()][i] = entry

    def has_observation(self, observation_code):
        """
        returns True if it has at least on observation of the requested observation code

        Args:
            observation_code (ObservationCode): the observation code

        Returns:
            bool: True if it has at least on observation of the requested observation code, otherwise false
        """
        # if the first is none then all are none
        return self.__patient_observations[observation_code][0] != None

    def get_observation_entries(self, observation_code, num_of_entries = MAX_OBSERVATION_ENTRIES):
        """returns the latest number of entries for an observation

        Args:
            observation_code (ObservationCode): the observation for the requested entries
            num_of_entries (int, optional): the number of entries to be returned. Defaults to 5.

        Returns:
            [Observation]: the observation(s) requested

        Raises:
            ValueError: if observations exceed the MAX_OBSERVATION_ENTRIES
        """

        if num_of_entries > MAX_OBSERVATION_ENTRIES:
            raise ValueError("can't return more than the MAX_OBSERVATION_ENTRIES")

        return self.__patient_observations[observation_code][0:num_of_entries]

    def get_latest_observation_entry(self, observation_code):
        """returns the latest entry for an observation
            the first entry always hold the latest one

        Args:
            observation_code (ObservationCode): the observation for the requested entry

        Returns:
            Observation: the observation requested
        """
        return self.get_observation_entries(observation_code, num_of_entries = 1)[0]

    def __str__(self):

        """

        prints the summarised information stored for a given patient

        :return: a string containing the data linked to each patient field

        """
        return "__identifier: " + str(self.__identifier) + " , " + "__display_name: " + str(self.__display_name) + " , " + "__given_name: " + str(self.__given_name) + " , " + "__family_name: " + str(self.__family_name) + " , " + "__birthdate: " + str(self.__birthdate) + " , " + "__gender: " + str(self.__gender) + " , " + "__address: " + str(self.__address) + " , " + "__observation: " + str(self.__patient_observations)