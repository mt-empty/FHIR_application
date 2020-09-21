import tkinter as tk
from model.observation.observationCode import ObservationCode
from view.moreInfo import MoreInfo
import dateutil.parser


class PatientInfo(tk.Frame):

    def __init__(self, master, controller, patient, *args, **kwargs):
        """
        Display oh patient name and cholesterol info
        :param master: master window
        :param controller: controller to request data from model
        :param patient: patient to get info from
        """
        super(PatientInfo, self).__init__(master, *args, **kwargs)
        self.configure(width=950, height=30)

        # initialising variables
        self.id = patient.get_identifier()
        self.controller = controller
        self.patient = patient

        self.controller.update_patient_obs(ObservationCode.CHOLESTEROL, patient)
        self.controller.update_patient_obs(ObservationCode.BLOOD_PRESSURE, patient)
        self.controller.update_patient_obs(ObservationCode.TOBACCO_SMOKING_STATUS_NHIS, patient)

        # creating and placing display
        self.name_label = tk.Label(self, text=patient.get_display_name(), relief="groove")
        self.name_label.place(x=0, y=0, width=200, height=30)

        cholesterol = patient.get_latest_observation_entry(ObservationCode.CHOLESTEROL)
        if cholesterol is not None:
            date = dateutil.parser.parse(str(cholesterol.get_date()))
            self.chol_value = tk.Label(self, text=str(cholesterol.get_value()),
                                       relief="groove")
            self.date_value = tk.Label(self, text=str(date.date()) + " " + str(date.hour) + ":" + str(date.minute) + ":" + str(date.second), relief="groove")
        else:
            self.chol_value = tk.Label(self,
                                       text="N/A",
                                       relief="groove")
            self.date_value = tk.Label(self, text="N/A", relief="groove")

        blood_test = patient.get_latest_observation_entry(ObservationCode.BLOOD_PRESSURE)
        if blood_test is not None:
            date = dateutil.parser.parse(str(blood_test.get_date()))
            self.sys_value = tk.Label(self, text=str(blood_test.get_value()['Systolic_value']), relief="groove")
            self.dia_value = tk.Label(self, text=str(blood_test.get_value()['Diastolic_value']), relief="groove")
            self.date_value2 = tk.Label(self, text=str(date.date()) + " " + str(date.hour) + ":" + str(
                date.minute) + ":" + str(date.second), relief="groove")
        else:
            self.sys_value = tk.Label(self,
                                       text="N/A",
                                       relief="groove")
            self.dia_value = tk.Label(self,
                                      text="N/A",
                                      relief="groove")
            self.date_value2 = tk.Label(self, text="N/A", relief="groove")
        self.chol_value.place(x=200, y=0, width=175, height=30)
        self.date_value.place(x=375, y=0, width=125, height=30)
        self.dia_value.place(x=500, y=0, width=100, height=30)
        self.sys_value.place(x=600, y=0, width=100, height=30)
        self.date_value2.place(x=700, y=0, width=125, height=30)

        # Button to open more info window
        more_info = tk.Button(self, text="More Patient Info", relief="groove", bg="lime", command=self.__more_info_window)
        more_info.place(x=825, y=0, width=100, height=30)

    def update_obs(self):
        """
        updates cholesterol value to most recent
        :return: None
        """
        cholesterol = self.patient.get_latest_observation_entry(ObservationCode.CHOLESTEROL)
        if cholesterol is not None:
            date = dateutil.parser.parse(str(cholesterol.get_date()))
            self.chol_value['text'] = str(cholesterol.get_value())
            self.date_value['text'] = str(date.date()) + " " + str(date.hour) + ":" + str(date.minute) + ":" + str(date.second)

        blood = self.patient.get_latest_observation_entry(ObservationCode.BLOOD_PRESSURE)
        if blood is not None:
            date = dateutil.parser.parse(str(blood.get_date()))
            self.sys_value['text'] = str(blood.get_value()['Systolic_value'])
            self.dia_value['text'] = str(blood.get_value()['Diastolic_value'])
            self.date_value2['text'] = str(date.date()) + " " + str(date.hour) + ":" + str(date.minute) + ":" + str(date.second)

    def highlight_text(self):
        """
        Highlight cholesterol and name
        :return: None
        """
        self.chol_value['fg'] = 'red'
        self.name_label['fg'] = 'red'

    def highlight_dia(self):
        self.dia_value['fg'] = 'purple'

    def default_dia(self):
        self.dia_value['fg'] = 'black'

    def highlight_sys(self):
        self.sys_value['fg'] = 'purple'

    def default_sys(self):
        self.sys_value['fg'] = 'black'

    def default_text(self):
        """
        Remove highlight from cholesterol and name
        :return: None
        """
        self.chol_value['fg'] = 'black'
        self.name_label['fg'] = 'black'

    def __more_info_window(self):
        """
        Open more info for patient
        :return: None
        """
        self.wait_window(MoreInfo(self, self.patient, self.controller))
