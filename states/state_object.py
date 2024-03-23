import copy

class StateException(Exception):
    pass


class BaseGameState:
    def __init__(self, state_name, checks, state_interface):
        self._name = state_name
        self.state_checks = copy.deepcopy(checks)
        self._interface = state_interface

        self.pre_process_checks()

    @property
    def name(self):
        return self._name

    @property
    def interface(self):
        return self._interface

    @interface.setter
    def interface(self, new_interface):
        self._interface = new_interface

    def pre_process_checks(self):
        pass

    def state_check(self):
        return None, None

    def __iter__(self):
        for check_name, check_data in self.state_checks.items():
            yield check_name, check_data
