from api.apiFetch import ApiFetch
from model.observable.Subject import Subject
from model.observable.funcRefresh import FuncRefresh

class LatestPatientObservations(Subject):

    """

    LatestPatientObservations is a derived class of the Subject abstract class/interface.
    It is used as our class for fetching API results.
    It utilises the observer design pattern to notify observers of important state changes.

    """

    def __init__(self):
        # the set of patient objects that are observing the LatestPatientObservations at given time
        self.patient_subscribers = set()
        self.api_fetch = ApiFetch()
        self.timer = None

    def subscribe(self, patient_obj):

        """

        takes a patient object and subscribes it to the LatestPatientObservations (so it can retrieve updates about changes in state information)

        :param patient_obj: a reference to a created patient class object
        e.g. if a patient object is created by patient_test = [constructor information], then pass patient_test.

        :return: None

        """

        self.patient_subscribers.add(patient_obj)

    def unsubscribe(self, patient_obj):

        """

        takes a patient object and unsubscribes it from the LatestPatientObservations (so it can stop retrieving updates about change in state information)

        :param patient_obj: a reference to a created patient class object
        e.g. if a patient object is created by patient_test = [constructor information], then pass patient_test.

        :return: None

        """

        # unsubscribes the given patient
        self.patient_subscribers.discard(patient_obj)

    def alert_patients(self, obs):

        """

        given a set of X observations for a patient, notify the respective observer of a state change

        :param obs: a set of X most recent observations for a given patient

        :return: None

        """

        # for each patient currently subscribed to the LatestPatientObservations object
        if type(obs) != list:
            obs = [obs]
        for patient in self.patient_subscribers:
            # notify them of the state change
            patient.update_observation(*obs)

    def start_refreshing_single_patient_obs(self, N, patient_identifier, observation_code):

        """

        This function merely initiates the timer construct of the function that does the actual
        updating work for an individual patient.

        starts running timer_refresh_latest_obs every N seconds, for a given observation type.
        FOR ONE PATIENT AT A TIME (i.e. this takes a patient ID and refreshes their obs every N seconds).
        can be called multiple times for different patients.


        :param N: the number of seconds between each refresh in server retrieval
        :param patient_identifier: the identifier of a patient (e.g. "28619") // patientObj.get_identifier()
        :param observation_code: the code for the type of observation

        :return: None

        """
        # the function parameter in the FuncRefresh object construction is hardcoded to timer_refresh_latest_obs
        # can be changed to accept multiple functions if the functionality becomes required

        if self.timer is None:
            self.timer = FuncRefresh(N, self.timer_refresh_latest_single_patient_obs, patient_identifier, observation_code)

        else:
            self.timer.stop()
            self.timer = FuncRefresh(N, self.timer_refresh_latest_single_patient_obs, patient_identifier, observation_code)

        # uncomment this if you want the timer to stop

    def timer_refresh_latest_single_patient_obs(self, patient_identifier, observation_code):

        """

        This function is the one that gets run every N seconds, as initiated by start_refreshing_single_patient_obs.
        It works on a singular patient basis.

        has the same functionality as get_latest_obs, except an observation is not returned,
        it is merely sent out to its observers on an N-second basis
        FOR ONE PATIENT AT A TIME

        :param patient_identifier: the identifier of a patient (e.g. "28619") // patientObj.get_identifier()
        :param observation_code: the code for the type of observation

        :return: None

        """
        latest_obs = self.api_fetch.get_latest_obs(patient_identifier, observation_code)

        # subscribe the relevant patient to the concreteSubject object
        self.subscribe(patient_identifier)

        # notify the concreteObserver of the change (the newest observation)
        self.alert_patients(latest_obs)

        # unsubscribe the relevant patient from the concreteSubject object
        # this is to ensure that when we next call this get_latest_obs function, we will have a clear set, allowing
        # us to add the next patient into it to receive a notification.
        self.unsubscribe(patient_identifier)

    def start_refreshing_all_observed_patients_obs(self, N, hp_obj, observation_code):

        """

        This function merely constructs the timer construct of the function that does the actual
        updating work for ALL currently monitored patients. More specifically, any type of obs can be given
        can be given into this function, but this is just functionality reserved for possible expansion.

        starts running timer_refresh_latest_obs every N seconds, for a given observation type
        FOR ALL CURRENTLY-MONITORED PATIENTS AT A TIME (i.e. this takes an HP object and refreshes their monitored
        patients observations every N seconds).

        :param N: the number of seconds between each refresh in server retrieval
        :param hp_obj: a reference to a created health practitioner class object
        :param observation_code: the code for the type of observation

        :return: None

        """
        # the function parameter in the FuncRefresh object construction is hardcoded to timer_refresh_latest_obs
        # can be changed to accept multiple functions if the functionality becomes required

        if self.timer is None:
            self.timer = FuncRefresh(N, self.timer_refresh_latest_all_observed_patients_obs, hp_obj, observation_code)

        else:
            self.timer.stop()
            self.timer = FuncRefresh(N, self.timer_refresh_latest_all_observed_patients_obs, hp_obj, observation_code)

        # uncomment this if you want the timer to stop
        # timer.stop()

    def timer_refresh_latest_all_observed_patients_obs(self, hp_obj, observation_code):

        """

        This function is the one that gets run every N seconds for ALL monitored patients.
        It will iterate, using the iterator design pattern, through a list of patients of a HP
        who have an observation being monitored, and it will retrieve their latest
        observation from the server, each time the function runs. The observer design pattern is
        then used to send out this latest observation to its respective Patient class object.

        :param hp_obj: a health practitioner object (passed as a parameter from
        start_refreshing_all_observed_patients_obs)
        :param observation_code: the type of observation (passed as a parameter from
        start_refreshing_all_observed_patients_obs)

        :return: None

        """
        for p in hp_obj.get_monitored_patients_with_obs(observation_code):

            # get patient ID
            p_ID = p.get_identifier()

            # get patient's latest observation of a type
            latest_obs = self.api_fetch.get_latest_obs(p_ID, observation_code)

            # subscribe the relevant patient to the concreteSubject (LatestPatientObservations) object
            self.subscribe(p)

            # notify the concreteObserver (patient object) of the change (the newest observation value)
            self.alert_patients(latest_obs)

            # unsubscribe the relevant patient from the concreteSubject object
            # this is to ensure that when we next call this get_latest_obs function, we will have a clear set, allowing
            # us to add the next patient into it to receive a notification.
            self.unsubscribe(p)

    def start_refreshing_latest_X_observations_all_patients(self, N, hp_obj, observation_code):

        """

        This function constructs a FuncRefresh object which will actually perform the execution of
        timer_refresh_latest_X_observations_all_patients every N seconds

        :param N: the number of seconds between each refresh in server retrieval
        :param hp_obj: a health practitioner object
        :param observation_code: the enum code of a given observation type

        """

        if self.timer is None:
            self.timer = FuncRefresh(N, self.timer_refresh_latest_X_observations_all_patients, hp_obj, observation_code)

        else:
            self.timer.stop()
            self.timer = FuncRefresh(N, self.timer_refresh_latest_X_observations_all_patients, hp_obj, observation_code)

    def timer_refresh_latest_X_observations_all_patients(self, hp_obj, observation_code):

        """

        This function runs every N seconds for ALL monitored patients.
        It will iterate through a list of patients of a HP, and for each patient it will attempt to fetch their X
        most recent observations of a given type. This could be met with a valueError if X is too big, or a series of
        'None' values if there are not enough recent observations to fill up X positions.

        :param patient_identifier: ID of a patient to retrieve observations for
        :param observation_code: the enum code of a given observation type

        """

        for p in hp_obj.get_monitored_patients_with_obs(observation_code):

            # get a patient's ID, iterating through one patient at a time
            p_ID = p.get_identifier()

            # fetch the X (default is 5, since no count parameter given) most recent *observations from the api
            latest_x_obs = self.api_fetch.get_recent_observations(p_ID, observation_code)

            # subscribe the current patient to the LatestPatientObservations object
            self.subscribe(p)

            # deliver these up-to-date X (5) most recent observations for the patient to the patient class
            self.alert_patients(latest_x_obs)

            # unsubscribe the current patient, so they do not receive the next patient's observations
            self.unsubscribe(p)

    def stop(self):
        self.timer.stop()





