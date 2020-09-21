import tkinter as tk
import tkinter.ttk as ttk
import matplotlib, numpy
from model.observation.observationCode import ObservationCode
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandas import DataFrame


class CholesterolGraph(tk.Frame):

    def __init__(self, master, controller, *args, **kwargs):
        """
        Graph to display Cholesterol values of monitored patients
        :param master: master window
        :param controller: for getting data from model
        """
        super(CholesterolGraph, self).__init__(master, *args, **kwargs)
        self.controller = controller
        self.frame = None
        self.update_graph()

    def update_graph(self):
        """
        Used to keep graph up to date to reflect the monitored patients
        :return: None
        """
        if self.frame is not None:
            self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.place(x=0, y=0, width=950, height=620)
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(211)
        df = self.generate_data()
        canvas = FigureCanvasTkAgg(f, self.frame)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        if len(self.controller.HP_OBJ.get_monitored_patients()) == 0:
            df = df[['Cholesterol(mg/dL)', 'Patient_Name']].groupby('Patient_Name')
        else:
            df = df[['Cholesterol(mg/dL)', 'Patient_Name']].groupby('Patient_Name').sum()
        df.plot.bar(ax=a, title="Total Cholesterol mg/dL", grid=True)

    def generate_data(self):
        """
        Create data to be displayed by the graph
        :return: None
        """
        datax = []
        datay = []
        for patient in self.controller.HP_OBJ.get_monitored_patients():
            obs = patient.get_latest_observation_entry(ObservationCode.CHOLESTEROL)
            if obs is not None:
                datay.append(float(obs.get_value()))
                datax.append(patient.get_display_name())
        data1 = {'Cholesterol(mg/dL)': datay,
                 'Patient_Name': datax
                 }
        df1 = DataFrame(data1, columns=['Cholesterol(mg/dL)', 'Patient_Name'])
        return df1
