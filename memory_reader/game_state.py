# python built in
import copy
from typing import Tuple, Any

# own modules
import screen_reader.screen_reader_constants as screen_reader_constants
from states.state_object import BaseGameState, StateException

class MemoryGameState(BaseGameState):

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