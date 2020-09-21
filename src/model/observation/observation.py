from abc import ABC, abstractmethod

class Observation(ABC):
    """
    the observation abstract class, this so concrete class can inherit from

    Args:
        ABC (class): python abstract module
    """
    def __init__(self, observation_type, value, unit, date):
        """
        the int method

        Args:
            observation_type (ObservationCode): observation code
            value (int): the value of the observation
            unit (str): the unit of the observation
            date (str): the issue date of the observation
        """
        self.__observation_type = observation_type
        self.__name =  self.__observation_type.name
        self.__value = value
        self.__unit = unit
        self.__date = date
    
    def get_observation_type(self):
        return self.__observation_type

    def get_observation_name(self):
        return self.__name

    def get_value(self):
        """the value of the observation

        Returns:
            any: this could be any type
        """
        return self.__value
    
    def set_value(self, value):
        self.__value = value

    def get_unit(self):
        return self.__unit

    def set_unit(self, unit):
        self.__unit = unit

    def get_date(self):
        return self.__date

    def set_date(self, date):
        self.__date = date

    def __str__(self):
        return "__name: " + str(self.get_observation_name()) + " , " + "__value: " + str(self.get_value()) + " , " + "__unit: " + str(self.get_unit()) + " , " + "__date: " + str(self.get_date())