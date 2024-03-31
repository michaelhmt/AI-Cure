# python built in
import copy

# own modules
import screen_reader.screen_reader_constants as screen_reader_constants
from states.state_object import BaseGameState, StateException


class GameVisualState(BaseGameState):

    def pre_process_checks(self):
        if not self.state_checks .get(screen_reader_constants.STATE_CHECK_ROI_KEY):
            raise StateException(f"{self.name} is not a valid state no state check roi key found in provided rois")

        self.rois_to_read = copy.deepcopy(self.state_checks)  # type: dict
        self.rois_to_read.pop(screen_reader_constants.STATE_CHECK_ROI_KEY)

    @property
    def name(self):
        return self._name

    def state_check(self):
        # type: () -> tuple[dict[str, int], str]
        """
        returns a roi to test and what the expected result of that roi should be if the game is in that state

        Returns:
            dict: a dict with the coords of the roi to test on the game window

        """
        test_key = screen_reader_constants.STATE_CHECK_ROI_KEY
        results_key = screen_reader_constants.STATE_CHECK_RESULTS_STR
        test_roi = self.state_checks[test_key]
        expected_result = test_roi[results_key]

        return test_roi, expected_result

    def __iter__(self):
        for roi_name, rois in self.rois_to_read.items():
            yield roi_name, rois
