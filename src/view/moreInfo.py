import tkinter as tk
from view.general_methods import center_to_win


class MoreInfo(tk.Toplevel):

    def __init__(self, master, patient, controller, *args, **kwargs):
        """
        Create more info patient window to display extra patient info
        :param master: master window
        :param patient: patient to display
        :param controller: controller to connect with model
        :param args: extra args
        :param kwargs: extra keyword args
        """
        super(MoreInfo, self).__init__(master, *args, **kwargs)

        # initialise class variables
        self.patient = patient
        self.controller = controller

        # configuring the windows settings
        self.configure(width=375, height=200)
        self.grab_set()
        center_to_win(self, self.master.master.master.master.master.master.master)
        self.resizable(False, False)
        self.title(self.patient.get_display_name())

        # load display of window
        self.__load_display()

    def __load_display(self):
        """
        create display of window
        :return: None
        """
        if not self.patient.get_details_has_been_fetched():
            self.controller.get_detailed_patient_info(patient=self.patient)

        id_title = tk.Label(self, text="ID", relief="groove", bg="grey", fg="white")
        id_title.place(x=0, y=0, width=125, height=25)
        fname_title = tk.Label(self, text="Given Name", relief="groove", bg="grey", fg="white")
        fname_title.place(x=125, y=0, width=125, height=25)
        lname_title = tk.Label(self, text="Family Name", relief="groove", bg="grey", fg="white")
        lname_title.place(x=250, y=0, width=125, height=25)
        bday_title = tk.Label(self, text="Birthday", relief="groove", bg="grey", fg="white")
        bday_title.place(x=0, y=50, width=125, height=25)
        gen_title = tk.Label(self, text="Gender", relief="groove", bg="grey", fg="white")
        gen_title.place(x=0, y=100, width=125, height=25)
        add_lin_title = tk.Label(self, text="Address Line", relief="groove", bg="grey", fg="white")
        add_lin_title.place(x=125, y=50, width=250, height=25)
        city_title = tk.Label(self, text="City", relief="groove", bg="grey", fg="white")
        city_title.place(x=125, y=100, width=125, height=25)
        state_title = tk.Label(self, text="State", relief="groove", bg="grey", fg="white")
        state_title.place(x=250, y=100, width=125, height=25)
        post_code_title = tk.Label(self, text="Post Code", relief="groove", bg="grey", fg="white")
        post_code_title.place(x=125, y=150, width=125, height=25)
        country_title = tk.Label(self, text="Country", relief="groove", bg="grey", fg="white")
        country_title.place(x=250, y=150, width=125, height=25)

        ok_button = tk.Button(self, text="OK", relief="groove", bg='lime', command=self.__on_close)
        ok_button.place(x=0, y=150, width=125, height=50)

        p_id = self.patient.get_identifier()
        p_id = tk.Label(self, text=p_id if p_id is not None else "N/A", relief="groove")
        fname = self.patient.get_given_name()
        fname = tk.Label(self, text= fname if fname is not None else "N/A", relief="groove")
        lname = self.patient.get_family_name()
        lname = tk.Label(self, text=lname if lname is not None else "N/A", relief="groove")
        bday = self.patient.get_birthdate()
        bday = tk.Label(self, text=bday if bday is not None else "N/A", relief="groove")
        gender = self.patient.get_gender()
        gender = tk.Label(self, text=gender if gender is not None else "N/A", relief="groove")

        address = self.patient.get_address()
        add_line = address.get___line()
        city = address.get___city()
        state = address.get___state()
        post_code = address.get___postalCode()
        country = address.get___country()

        add_line = tk.Label(self, text=add_line if add_line is not None else "N/A", relief="groove")
        city = tk.Label(self, text=city if city is not None else "N/A", relief="groove")
        state = tk.Label(self, text=state if state is not None else "N/A", relief="groove")
        post_code = tk.Label(self, text=post_code if post_code is not None else "N/A", relief="groove")
        country = tk.Label(self, text=country if country is not None else "N/A", relief="groove")

        p_id.place(x=0, y=25, width=125, height=25)
        fname.place(x=125, y=25, width=125, height=25)
        lname.place(x=250, y=25, width=125, height=25)
        bday.place(x=0, y=75, width=125, height=25)
        gender.place(x=0, y=125, width=125, height=25)
        add_line.place(x=125, y=75, width=250, height=25)
        city.place(x=125, y=125, width=125, height=25)
        state.place(x=250, y=125, width=125, height=25)
        post_code.place(x=125, y=175, width=125, height=25)
        country.place(x=250, y=175, width=125, height=25)

    def __on_close(self):
        self.destroy()
