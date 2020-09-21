from model.observation.observationCode import ObservationCode
from model.iterator.observationList import ObservationList


class HealthPractitioner:
	def __init__(self, __identifier, __given_name, __family_name):
		"""
		constructor for hp

		Args:
			__identifier (str): unique id
			__given_name (str): first name
			__family_name (str): family_name
		"""
		self.__identifier = __identifier
		self.__given_name = __given_name
		self.__family_name = __family_name
		# holds all patients
		self.__patient_list = []
		# holds only monitored patients, you should add patients to this list when the user selects them
		self.__monitored_patient = []

	def get_identifier(self):
		return self.__identifier

	def get_given_name(self):
		return self.__given_name

	def get_family_name(self):
		return self.__family_name
	
	def get_patients(self):
		return self.__patient_list

	def add_patients(self, patients):
		self.__patient_list.extend(patients)
	
	def add_monitored_patients(self, patients):
		self.__monitored_patient.extend(patients)

	def remove_monitored_patients(self, patient):
		self.__monitored_patient.remove(patient)

	def get_monitored_patients(self):
		return self.__monitored_patient

	def get_monitored_patients_with_obs(self, observation_code):
		"""
		returns a iterable of patients of the required observation

		Args:
			obs (ObservationCode): the observation code

		Returns:
			Iterable: an iterable(array) which can be used to iterate over patients with the required obs
		"""
		return ObservationList(self.__monitored_patient, observation_code)

	def __str__(self):
 		return "__identifier: " + str(self.__identifier) + " , " + "__given_name: " + str(self.__given_name) + " , " + "__family_name: " + str(self.__family_name)
