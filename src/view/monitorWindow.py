import tkinter as tk
from view.scrolledFrame import ScrolledFrame
from view.patientInfo import PatientInfo
from model.observation.observationCode import ObservationCode


class MonitorWindow(ScrolledFrame):

    def __init__(self, master, controller, graph_window, *args, **kwargs):
        super(MonitorWindow, self).__init__(master, *args, **kwargs)
        self.highlight_value = 0
        self.sys_high_value = 0
        self.dia_high_value = 0
        self._count = 0
        self.patient_chol_lookup = {}
        self.controller = controller
        self.graph_window = graph_window
        self.totals = tk.Frame(self.interior)
        self.monitored = []
        self.displayed = []
        self.p_info_dict = {}
        self.__generate_totals_display()
        self.__update_clock()

    def update_list(self):
        for patient in self.displayed:
            if patient not in self.monitored:
                self.displayed.remove(patient)
                self.p_info_dict[patient.get_identifier()].destroy()
                self.p_info_dict[patient.get_identifier()] = None

        for patient in self.monitored:
            if patient not in self.displayed:
                self.totals.grid(row=self._count + 1, column=0, sticky=tk.NSEW)
                tempWidget = PatientInfo(self.interior, self.controller, patient)
                tempWidget.grid(row=self._count, column=0, sticky=tk.NSEW)
                self.p_info_dict[patient.get_identifier()] = tempWidget
                self.displayed.append(patient)
            self._count += 1
        self.__update_highlighting()
        self.__update_dia_highlights()
        self.__update_sys_highlights()
        self.__update_smokers()
        self.graph_window.update_graph()

    def update_obs(self):
        if self.__check_for_changes():
            # self.graph_window.update_graph()
            for info_box in self.interior.winfo_children():
                if hasattr(info_box, 'patient'):
                    info_box.update_obs()
            self.__update_highlighting()
            self.__update_dia_highlights()
            self.__update_sys_highlights()
            self.__update_smokers()

    def __check_for_changes(self):
        for patient in self.controller.HP_OBJ.get_monitored_patients():
            if self.patient_chol_lookup.get(patient.get_identifier()) is None:
                self.update_patient_vals()
                return True
            if self.patient_chol_lookup.get(patient.get_identifier()).get_value() != patient.get_latest_observation_entry(ObservationCode.CHOLESTEROL).get_value() \
                    and self.patient_chol_lookup.get(patient.get_identifier()).get_date() != patient.get_latest_observation_entry(ObservationCode.CHOLESTEROL).get_date():
                self.update_patient_vals()
                return True
        if len(self.patient_chol_lookup) != len(self.controller.HP_OBJ.get_patients()):
            self.update_patient_vals()
            return True
        return False

    def update_patient_vals(self):
        for patient in self.controller.HP_OBJ.get_patients():
            self.patient_chol_lookup[patient.get_identifier()] = patient.get_latest_observation_entry(ObservationCode.CHOLESTEROL)

    def set_highlight_value(self, value):
        self.highlight_value = value
        self.__update_highlighting()

    def set_sys_value(self, value):
        self.sys_high_value = value
        self.__update_sys_highlights()

    def set_dia_value(self, value):
        self.dia_high_value = value
        self.__update_dia_highlights()

    def __update_dia_highlights(self):
        count = 0
        for info_box in self.interior.winfo_children():
            if hasattr(info_box, 'patient'):
                new_blood = info_box.patient.get_latest_observation_entry(ObservationCode.BLOOD_PRESSURE)
                if new_blood is not None:
                    if new_blood.get_value()['Diastolic_value'] > self.dia_high_value:
                        info_box.highlight_dia()
                        count += 1
                    else:
                        info_box.default_dia()
        self.gtx_dia['text'] = count

    def __update_smokers(self):
        count = 0
        for info_box in self.interior.winfo_children():
            if hasattr(info_box, 'patient'):
                smoker = info_box.patient.get_latest_observation_entry(ObservationCode.TOBACCO_SMOKING_STATUS_NHIS)
                if smoker is not None:
                    if str(smoker.get_value()) == 'Never smoker':
                        count += 1
        self.smoker_count['text'] = count

    def __update_sys_highlights(self):
        count = 0
        for info_box in self.interior.winfo_children():
            if hasattr(info_box, 'patient'):
                new_blood = info_box.patient.get_latest_observation_entry(ObservationCode.BLOOD_PRESSURE)
                if new_blood is not None:
                    if new_blood.get_value()['Systolic_value'] > self.sys_high_value:
                        info_box.highlight_sys()
                        count += 1
                    else:
                        info_box.default_sys()
        self.gtx_sys['text'] = count

    def __update_highlighting(self):
        count = 0
        chol_total = 0
        gta_chol = 0
        for patient in self.displayed:
            chol = patient.get_latest_observation_entry(ObservationCode.CHOLESTEROL)
            if chol is not None:
                chol_total += chol.get_value()
                count += 1

        if count > 0:
            average_chol = chol_total/count

            for info_box in self.interior.winfo_children():
                if hasattr(info_box, 'patient'):
                    new_chol = info_box.patient.get_latest_observation_entry(ObservationCode.CHOLESTEROL)
                    if new_chol is not None:
                        if new_chol.get_value() > (average_chol if self.highlight_value == 0 else self.highlight_value):
                            info_box.highlight_text()
                            if new_chol.get_value() > average_chol:
                                gta_chol += 1
                        else:
                            info_box.default_text()
        self.gta_chol['text'] = gta_chol

    def __generate_totals_display(self):
        self.totals.configure(width=950, height=60)
        self.totals['bg'] = "grey"
        chol_lbl = tk.Label(self.totals, text="Total > Average Cholesterol", relief="groove", bg='grey', fg='white')
        chol_lbl.place(x=0, y=0, width=200, height=30)
        self.gta_chol = tk.Label(self.totals, text='0', relief="groove", bg='grey', fg='white')
        self.gta_chol.place(x=200, y=0, width=100, height=30)

        dia_lbl = tk.Label(self.totals, text="# High diastolic blood pressure", relief="groove", bg='grey', fg='white')
        dia_lbl.place(x=300, y=0, width=200, height=30)
        self.gtx_dia = tk.Label(self.totals, text='0', relief="groove", bg='grey', fg='white')
        self.gtx_dia.place(x=500, y=0, width=100, height=30)

        sys_lbl = tk.Label(self.totals, text="# High systolic blood pressure", relief="groove", bg='grey', fg='white')
        sys_lbl.place(x=600, y=0, width=200, height=30)
        self.gtx_sys = tk.Label(self.totals, text='0', relief="groove", bg='grey', fg='white')
        self.gtx_sys.place(x=800, y=0, width=100, height=30)

        smoker_lbl = tk.Label(self.totals, text="# Never Smokers", relief="groove", bg='grey', fg='white')
        smoker_lbl.place(x=0, y=30, width=200, height=30)
        self.smoker_count = tk.Label(self.totals, text='0', relief="groove", bg='grey', fg='white')
        self.smoker_count.place(x=200, y=30, width=100, height=30)

    def __update_clock(self):
        self.update_obs()
        self.after(100, self.__update_clock)

