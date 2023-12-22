# project modules
from apps.base_app import BaseApp
from gym.hCure_env import HCureEnv
from config.hcure_config import HcureConfig

def main():
    config_path = "E:\\Python\\Ai_Knight\\config.yaml"
    config_object = HcureConfig(config_path)
    training_app = BaseApp("Hcure", config_object, HCureEnv)
    training_app.run_training()

if __name__ == "__main__":
    main()