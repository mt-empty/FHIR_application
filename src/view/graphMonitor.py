import tkinter as tk
from view.scrolledFrame import ScrolledFrame
from view.patientGraph import PatientGraph
from model.observation.observationCode import ObservationCode


class GraphMonitor(ScrolledFrame):

    def __init__(self, master, controller, *args, **kwargs):
        super(GraphMonitor, self).__init__(master, *args, **kwargs)
        self._count = 0
        self.controller = controller
        self.monitored = []
        self.displayed = []
        self.p_info_dict = {}
        self.__update_clock()

    def update_list(self):
        for patient in self.displayed:
            if patient not in self.monitored:
                self.displayed.remove(patient)
                self.p_info_dict[patient.get_identifier()].destroy()
                self.p_info_dict[patient.get_identifier()] = None

        for patient in self.monitored:
            if patient not in self.displayed:
                temp_widget = PatientGraph(self.interior, self.controller, patient, ObservationCode.BLOOD_PRESSURE, obs_key='Systolic_value')
                temp_widget.grid(row=self._count, column=0, sticky=tk.NSEW)
                self.p_info_dict[patient.get_identifier()] = temp_widget
                self.displayed.append(patient)
            self._count += 1

    def update_obs(self):
        # self.graph_window.update_graph()
        for info_box in self.interior.winfo_children():
            if hasattr(info_box, 'patient'):
                info_box.update_obs()

    def __update_clock(self):
        self.update_obs()
        self.after(100, self.__update_clock)
