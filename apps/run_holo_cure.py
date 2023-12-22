# project modules
from apps.base_app import BaseApp
from gym.hCure_env import HCureEnv
from config.hcure_config import HcureConfig
import apps.hcure_utils as hcure_utils

def main():
    config_path = "E:\\Python\\Ai_Knight\\config.yaml"
    config_object = HcureConfig(config_path)

    app_proc = hcure_utils.start_hcure(config_object)
    training_app = BaseApp("Hcure", config_object, HCureEnv, app_proc=app_proc)
    training_app.run_training()

if __name__ == "__main__":
    main()