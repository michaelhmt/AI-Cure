
class StateException(Exception):
    pass


class BaseGameState:
    def __init__(self, state_name, checks):
        self._name = state_name
        self.state_checks = checks

        self.pre_process_checks()

    @property
    def name(self):
        return self._name

    def pre_process_checks(self):
        pass

    def state_check(self):
        return None, None

    def __iter__(self):
        for check_name, check_data in self.rois_to_read.items():
            yield check_name, check_data
