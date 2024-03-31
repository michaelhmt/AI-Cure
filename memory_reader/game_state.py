# python built in
import copy

# own modules
import memory_reader.mem_addresses as mem_constants
from states.state_object import BaseGameState, StateException

class MemoryGameState(BaseGameState):

    def pre_process_checks(self):
        if not self.state_checks.get(mem_constants.STATE_CHECK_KEY):
            raise StateException(f"{self.name} is not a valid state no state {mem_constants.STATE_CHECK_KEY} key found in provided addresses of \n{self.state_checks}")

        self.all_adresses = copy.deepcopy(self.state_checks)  # type: dict
        self.state_checks.pop(mem_constants.STATE_CHECK_KEY)


    def state_check(self):
        # type: () -> tuple[dict[str, int], str]
        """
        returns a roi to test and what the expected result of that roi should be if the game is in that state

        Returns:
            dict: a dict with the coords of the roi to test on the game window

        """
        test_key = mem_constants.STATE_CHECK_KEY
        results_key = mem_constants.STATE_CHECK_RESULTS_STR
        check_op_key = mem_constants.STATE_CHECK_KEY

        test_address = self.all_adresses[test_key]
        expected_result = test_address[results_key]
        check_op = test_address.get(check_op_key)

        return test_address, expected_result