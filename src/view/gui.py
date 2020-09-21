import tkinter as tk
import tkinter.ttk as ttk
from controller.controller import Controller
from view.patientList import PatientList
from view.monitorWindow import MonitorWindow
from view.cholesterolGraph import CholesterolGraph
from view.graphMonitor import GraphMonitor
from model.observable.latestPatientObservations import LatestPatientObservations
from model.observation.observationCode import ObservationCode
from view.errorWindow import ErrorWindow

import matplotlib, numpy
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class Gui(tk.Tk):

    def __init__(self):
        """
        Initialisation of GUI
        """
        super(Gui, self).__init__()
        self.configure(width=1200, height=650)
        self.resizable(False, False)
        self.controller = Controller()
        self.__load_display()
        self.protocol("WM_DELETE_WINDOW", self.__on_close)
        self.title("Cholesterol Monitor")

    def __load_display(self):
        tab_control = ttk.Notebook(self)
        tab1 = tk.Frame(tab_control)
        tab2 = tk.Frame(tab_control)
        tab3 = tk.Frame(tab_control)

        tab_control.add(tab1, text='Basic Monitor')
        tab_control.add(tab2, text='Cholesterol Graph Monitor')
        tab_control.add(tab3, text='Systolic Monitor')
        tab_control.place(x=250, y=0, width=950, height=650)

        self.graph_window = CholesterolGraph(tab2, self.controller)
        self.graph_window.place(x=0, y=0, width=950, height=620)

        self.blood_monitor = GraphMonitor(tab3, self.controller)
        self.blood_monitor.place(x=0, y=0, width=950, height=620)

        self.__tab1(tab1)
        self.__tab3(tab3)

        self.cholObs = LatestPatientObservations()
        self.cholObs.start_refreshing_all_observed_patients_obs(10, self.controller.HP_OBJ, ObservationCode.CHOLESTEROL)

        self.bloodRecentObs = LatestPatientObservations()
        self.bloodRecentObs.start_refreshing_latest_X_observations_all_patients(10, self.controller.HP_OBJ, ObservationCode.BLOOD_PRESSURE)

        self.smokerStatusObs = LatestPatientObservations()
        self.smokerStatusObs.start_refreshing_all_observed_patients_obs(10, self.controller.HP_OBJ, ObservationCode.TOBACCO_SMOKING_STATUS_NHIS)

        self.patient_list = PatientList(self, self.monitor_window, self.blood_monitor, self.controller)
        self.patient_list.place(x=0, y=0, width=250, height=650)

    def __tab1(self, tab1):
        update_n_title = tk.Label(tab1, text="Update Speed (seconds): ", relief="groove")
        update_n_title.place(x=0, y=0, width=200, height=30)

        self.var_n = tk.StringVar()
        self.entry_n = tk.Entry(tab1, textvariable=self.var_n, relief="groove")
        self.entry_n.place(x=200, y=0, width=50, height=30)
        self.var_n.set(10)

        button = tk.Button(tab1, text="Set Speed", relief="groove", bg="lime",
                           command=self.__set_n)
        button.place(x=250, y=0, width=150, height=30)

        sys_n_title = tk.Label(tab1, text="Highlight Systolic : ", relief="groove")
        sys_n_title.place(x=0, y=30, width=200, height=30)

        self.sys_n = tk.StringVar()
        self.sys_entry_n = tk.Entry(tab1, textvariable=self.sys_n, relief="groove")
        self.sys_entry_n.place(x=200, y=30, width=50, height=30)
        self.sys_n.set(0)

        button = tk.Button(tab1, text="Set Sys Value", relief="groove", bg="lime",
                           command=self.__set_sys)
        button.place(x=250, y=30, width=150, height=30)

        dia_n_title = tk.Label(tab1, text="Highlight Diastolic : ", relief="groove")
        dia_n_title.place(x=400, y=30, width=200, height=30)

        self.dia_n = tk.StringVar()
        self.dia_entry_n = tk.Entry(tab1, textvariable=self.dia_n, relief="groove")
        self.dia_entry_n.place(x=600, y=30, width=50, height=30)
        self.dia_n.set(0)

        button = tk.Button(tab1, text="Set Dia Value", relief="groove", bg="lime",
                           command=self.__set_dia)
        button.place(x=650, y=30, width=150, height=30)

        highlight_title = tk.Label(tab1, text="Highlight Cholesterol (mg/dL): ", relief="groove")
        highlight_title.place(x=400, y=0, width=200, height=30)

        self.var_high = tk.StringVar()
        self.entry_high = tk.Entry(tab1, textvariable=self.var_high, relief="groove")
        self.entry_high.place(x=600, y=0, width=50, height=30)
        self.var_high.set(0)

        button = tk.Button(tab1, text="Set Highlight Value", relief="groove", bg="lime",
                           command=self.__set_highlight)
        button.place(x=650, y=0, width=150, height=30)

        self.monitor_window = MonitorWindow(tab1, self.controller, graph_window=self.graph_window, bg="light grey")
        self.monitor_window.place(x=-1, y=90, width=945, height=530)

        name_title = tk.Label(tab1, text="Name", relief="groove", bg="grey", fg="white")
        chol_title = tk.Label(tab1, text="Cholesterol (mg/dL)", relief="groove", bg="grey", fg="white")
        date_title = tk.Label(tab1, text="Date", relief="groove", bg="grey", fg="white")
        dis_blood_title = tk.Label(tab1, text="Diastolic Blood", relief="groove", bg="grey", fg="white")
        sys_blood_title = tk.Label(tab1, text="Systolic Blood", relief="groove", bg="grey", fg="white")
        date_title2 = tk.Label(tab1, text="Date", relief="groove", bg="grey", fg="white")
        name_title.place(x=0, y=60, width=200, height=30)
        chol_title.place(x=200, y=60, width=175, height=30)
        date_title.place(x=375, y=60, width=125, height=30)
        dis_blood_title.place(x=500, y=60, width=100, height=30)
        sys_blood_title.place(x=600, y=60, width=100, height=30)
        date_title2.place(x=700, y=60, width=125, height=30)

    def __tab3(self, tab3):
        pass

    def __set_highlight(self):
        try:
            highlight_v = float(self.var_high.get())
            assert highlight_v >= 0, ""
            self.monitor_window.set_highlight_value(highlight_v)
        except Exception as e:
            print(e)
            self.wait_window(ErrorWindow(self))

    def __set_dia(self):
        try:
            highlight_v = float(self.dia_entry_n.get())
            assert highlight_v >= 0, ""
            self.monitor_window.set_dia_value(highlight_v)
        except Exception as e:
            print(e)
            self.wait_window(ErrorWindow(self))

    def __set_sys(self):
        try:
            print(self.sys_entry_n.get())
            highlight_v = float(self.sys_entry_n.get())
            assert highlight_v >= 0, ""
            self.monitor_window.set_sys_value(highlight_v)
        except Exception as e:
            print(e)
            self.wait_window(ErrorWindow(self))

    def __set_n(self):
        try:
            n = float(self.var_n.get())
            assert n > 0, ""
            self.cholObs.start_refreshing_all_observed_patients_obs(n, self.controller.HP_OBJ,
                                                                    ObservationCode.CHOLESTEROL)
            self.bloodRecentObs.start_refreshing_latest_X_observations_all_patients(n, self.controller.HP_OBJ,
                                                                                    ObservationCode.BLOOD_PRESSURE)
            self.smokerStatusObs.start_refreshing_all_observed_patients_obs(n, self.controller.HP_OBJ,
                                                                            ObservationCode.TOBACCO_SMOKING_STATUS_NHIS)
        except Exception as e:
            print(e)
            self.wait_window(ErrorWindow(self))

    def __on_close(self):
        self.cholObs.stop()
        self.bloodRecentObs.stop()
        self.smokerStatusObs.stop()
        self.destroy()
