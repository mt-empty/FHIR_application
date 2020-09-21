# importing the necessary libraries
import time
from threading import Event, Thread


class FuncRefresh():

    """

    FuncRefresh is used to refresh the observations of a patient every N seconds.

    # HOW TO START THE TIMER
    # timer = FuncRefresh(Nseconds, func, arg1, arg2, arg3... etc etc)
    # e.g. the func parameter, for our use-case, would be: timer_refresh_chol_obs(patientObj, obsCode)
    # kwargs can be used too, but I only included args as they seem most relevant to us

    # HOW TO STOP THE TIMER
    # timer.stop()

    """

    def __init__(self, N, f, *args):

        """

        the timer's constructor - initialises a timer object

        :param N: the interval at which we want to retrieve an observation (seconds)
        :param f: the function that we want to execute every N seconds
        :param args: used to pass args
        :param kwargs: used to pass kwargs

        """
        self.refresh_time = N
        self.func = f
        self.args = args
        # the number of seconds that've passed since epoch
        self.time_passed = time.time()
        # allows us to create an event that controls access to the thread
        self.event = Event()
        # creates the thread
        self.thread = Thread(target=self._target_func)
        # starts the thread
        self.thread.start()

    @property
    def _ret_time(self):
        """

        NOTE: trying to print the return value here leads to an error, this only needs
        to be accessed by _target_func, it doesn't need to be touched by the user

        :return: a floating point value which represents a number of seconds based
        on the given N value and the time passed since epoch

        """
        return self.refresh_time - ((time.time() - self.time_passed) % self.refresh_time)

    def stop(self):

        """

        stops the refreshing retrievals from occurring

        :return: None

        """

        # sets the event flag to true, meaning that other threads
        # can now access the event
        self.event.set()

        # blocks the current thread until another thread who calls join() is terminated
        self.thread.join()

    def _target_func(self):

        """

        runs the given func until the thread flag state changes or a timeout is given

        :return: None

        """
        while not self.event.wait(self._ret_time):
            self.func(*self.args)


