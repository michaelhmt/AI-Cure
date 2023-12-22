from typing import Any
import yaml
import os

class BaseConfig:

    def __init__(self, yaml_path, add_top_level_attrs=True):
        # type: (str, bool) -> None
        self._yaml_path = yaml_path
        self._raw_yaml_data = None
        self.add_top_level_attrs = add_top_level_attrs

        self._read_yaml()
        self._make_attrs()


    def _read_yaml(self):
        # type: () -> None
        if not os.path.exists(self._yaml_path):
            msg = f"{self._yaml_path} does not exist on disk, a config cannot be created"
            raise OSError(msg)

        with open(self._yaml_path, "r") as yaml_file:
            self._raw_yaml_data = yaml.safe_load(yaml_file)

    def _make_attrs(self, data_to_add=None, parent_name=None):
        # type: (dict, str) -> None

        """
        Potentially recursive function for adding keys of dict to this class as attributes

        Args:
            data_to_add (dict): the Data we want to add as attrs, if None
            self._raw_yaml_data will be used as a starting point.

        """

        data_to_add = data_to_add or self._raw_yaml_data
        for key_name, item_value in data_to_add.items():
            if not self.add_top_level_attrs and type(item_value) is dict:
                self._make_attrs(item_value, parent_name=key_name)
            if not hasattr(self, key_name):
                if parent_name:
                    attr_name = f"{parent_name}_{key_name}"
                else:
                    attr_name = key_name
                setattr(self, attr_name, item_value)

    def get_value(self, attribute_name, safe=False):
        # type: (str, bool) -> Any
        if hasattr(self, attribute_name):
            return getattr(self, attribute_name)
        return None

    # training getters
    def get_max_steps(self):
        return self._raw_yaml_data['training_settings']['max_steps']

    def get_output_path(self):
        return self._raw_yaml_data['training_settings'].get("output_dir")

    def get_run_steps(self):
        return self._raw_yaml_data['training_settings']['run_steps']

    def get_runs_per_update(self):
        return self._raw_yaml_data['training_settings']['runs_per_update']

    def get_updates_per_checkpoint(self):
        return self._raw_yaml_data['training_settings']['updates_per_checkpoint']

    def get_learn_steps(self):
        return self._raw_yaml_data['training_settings']['learn_steps']

    # game getters
    def get_exe_path(self):
        return self._raw_yaml_data['game_settings']["game_exe_path"]

    # vision getters
    def get_vision_model_path(self):
        return self._raw_yaml_data['vision_settings']["model_path"]

    def get_start_up_time(self):
        return self._raw_yaml_data['vision_settings']["start_up_time"]

if __name__ == "__main__":
    yaml_path = "E:\\Python\\Ai_Knight\\config.yaml"
    my_config = BaseConfig(yaml_path)
    print(dir(my_config))