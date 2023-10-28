# python built in
import copy

# own modules
import screen_reader.screen_reader_constants as screen_reader_constants

class GameState:
    def __init__(self, state_name, rois):
        self._name = state_name
        self.rois = rois

        self.rois_to_read = copy.deepcopy(self.rois) # type: dict
        self.rois_to_read.pop(screen_reader_constants.STATE_CHECK_ROI_KEY)

    @property
    def name(self):
        return self._name

    def state_check(self):
        # type: () -> dict[str, int]
        """
        returns a roi to test and what the expected result of that roi should be if the game is in that state

        Returns:
            dict: a dict with the coords of the roi to test on the game window

        """
        return self.rois[screen_reader_constants.STATE_CHECK_ROI_KEY]

    def __iter__(self):
        for roi_name, rois in self.rois_to_read.items():
            yield roi_name, rois
