import tkinter as tk
from model.observation.observationCode import ObservationCode
from view.moreInfo import MoreInfo
import dateutil.parser
import matplotlib, numpy
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandas import DataFrame
import matplotlib.pyplot as plt


class PatientGraph(tk.Frame):

    def __init__(self, master, controller, patient, obs, obs_key=None, *args, **kwargs):
        """
        Graph to display most recent observations
        :param master: master window
        :param controller: controller to link to model
        :param obs: observation type
        :param patient: patient to get observations from
        """
        super(PatientGraph, self).__init__(master, *args, **kwargs)
        self.configure(width=950, height=300)

        # Initialize variables
        self.controller = controller
        self.patient = patient
        self.__cached_info = []
        self.obs = obs
        self.obs_key = obs_key

        self.controller.update_recent_patient_obs(obs, patient)

        # creating and placing display
        self.name_label = tk.Label(self, text=patient.get_display_name(), relief="groove")
        self.name_label.place(x=0, y=0, width=200, height=300)

        self.recent_obs_label = tk.Label(self, text='', relief='groove')
        self.recent_obs_label.place(x=200, y=0, width=300, height=300)

        self.graph_frame = None

    def update_obs(self):
        if self.__check_for_changes():
            self.__generate_graph()
            value_str = ''
            for i, value in enumerate(self.__cached_info[0]):
                if i == 0:
                    value_str += str(value) + ' (' + str(self.__cached_info[1][i]) + ')'
                else:
                    value_str += '\n' + str(value) + ' (' + str(self.__cached_info[1][i]) + ')'
            self.recent_obs_label['text'] = value_str

    def __check_for_changes(self):
        """
        Checks current patient data to see if last displayed data is up to date, if not then cached data is updated
        with current data and returns True, else return False
        :return: True if data has changed, otherwise False
        """
        values_data = []
        dates_data = []
        for observation in self.patient.get_observation_entries(self.obs):
            if observation is not None:
                if self.obs_key is not None:
                    values_data.append(observation.get_value()[self.obs_key])
                    dates_data.append(observation.get_date())
                else:
                    values_data.append(observation.get_value())
                    dates_data.append(observation.get_date())
        if (values_data, dates_data) != self.__cached_info:
            self.__cached_info = (values_data, dates_data)
            return True
        return False

    def __generate_graph(self):
        if self.graph_frame is not None:
            self.graph_frame.destroy()
        self.graph_frame = tk.Frame(self)
        self.graph_frame.place(x=500, y=0, width=450, height=300)

        data = {'Values': self.__cached_info[0],
                'Dates': self.__cached_info[1]
                }
        df = DataFrame(data, columns=['Values', 'Dates'])

        figure1 = plt.Figure(figsize=(5,4), dpi=100)
        ax1 = figure1.add_subplot(111)

        line = FigureCanvasTkAgg(figure1, self.graph_frame)
        line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

        df = df[['Values', 'Dates']].groupby('Dates').sum()
        df.plot(kind='line', legend=True, ax=ax1, color='r', marker='o', fontsize=5)
        ax1.set_title('Most Recent Observations')

