import tkinter as tk
from view.scrolledFrame import ScrolledFrame


class PatientList(ScrolledFrame):

    def __init__(self, master, display, display2, controller, *args, **kwargs):
        super(PatientList, self).__init__(master, *args, **kwargs)
        self.display = display  # for displaying monitored patients
        self.display2 = display2  # for displaying recent blood obs of patients
        self.controller = controller

        self.configure(width=250, height=650)
        self['bg'] = 'grey'

        # initial values
        self._count = 0
        self.data = []
        self.monitored = []

        # holds the load more button (needs to be moved around when more patients are loaded)
        self.load_more = tk.Button(self.interior, text="Load More Patients", bg="lime",
                                   command=lambda: self.load_more_patients())
        self.create_patients(self.controller.get_patients())

    def create_patients(self, patients):
        for p in patients:
            p_label = tk.Label(self.interior, text=p.get_display_name(), relief='groove', bg="lightgrey")
            p_label.grid(row=self._count, column=0, sticky=tk.NSEW)
            var = tk.StringVar()
            self.data.append(p)
            check = tk.Checkbutton(self.interior, variable=var, onvalue=p, offvalue=None, bg="lightgrey",
                                   relief="groove", command=lambda x=self._count: self.__monitor(self.data[x]))
            check.grid(row=self._count, column=1, sticky=tk.NSEW)
            check.deselect()

            self._count += 1

        self.load_more.grid(row=self._count + 1, column=0, columnspan=2, sticky=tk.NSEW)

    def __monitor(self, patient):
        if patient in self.display.monitored:
            self.display.monitored.remove(patient)
            self.display2.monitored.remove(patient)
            self.controller.remove_monitored_patient(patient)
        else:
            self.display.monitored.append(patient)
            self.display2.monitored.append(patient)
            self.controller.add_monitored_patient(patient)
        self.display.update_list()
        self.display2.update_list()

    def load_more_patients(self):
        patients = self.controller.get_more_patients()
        if patients:
            self.create_patients(patients)
        else:
            self.load_more['state'] = 'disabled'
            self.load_more['bg'] = 'grey'

