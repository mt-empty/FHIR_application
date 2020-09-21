class Address:
	def __init__(self, __line, __city, __state, __postalCode, __country):
		self.__line = __line
		self.__city = __city
		self.__state = __state
		self.__postalCode = __postalCode
		self.__country = __country
		
	def get___line(self):
		return self.__line

	def get___city(self):
		return self.__city

	def get___state(self):
		return self.__state

	def get___postalCode(self):
		return self.__postalCode

	def get___country(self):
		return self.__country


	def __str__(self):
 		return "__line: " + str(self.__line) + " , " + "__city: " + str(self.__city) + " , " + "__state: " + str(self.__state) + " , " + "__postalCode: " + str(self.__postalCode) + " , " + "__country: " + str(self.__country)
