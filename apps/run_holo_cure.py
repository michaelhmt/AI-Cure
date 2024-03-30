# project modules
from apps.base_app import BaseApp
from gym.hCure_env import HCureEnv
from config.hcure_config import HcureConfig
import apps.hcure_utils as hcure_utils
import project_constants

def main():
    config_path = project_constants.CONFIG_PATH
    config_object = HcureConfig(config_path)

    app_proc = hcure_utils.start_hcure(config_object)
    training_app = BaseApp("Hcure", config_object, HCureEnv, app_proc=app_proc)
    training_app.run_training()
    #training_app.run_testing_interface()

if __name__ == "__main__":
    main()