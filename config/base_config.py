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

    def _make_attrs(self, data_to_add=None):
        # type: (dict) -> None

        """
        Potentially recursive function for add keys of dict to this class as attributes

        Args:
            data_to_add (dict): the Data we want to add as attrs, if None
            self._raw_yaml_data will be used as a starting point.

        """

        data_to_add = data_to_add or self._raw_yaml_data
        for key_name, item_value in data_to_add:
            if not self.add_top_level_attrs and type(item_value) is dict:
                self._make_attrs(item_value)
            if not hasattr(self, key_name):
                setattr(self, key_name, item_value)

    def get_value(self, attribute_name):
        if hasattr(self, attribute_name):
            return getattr(self, attribute_name)
        return None
