import yaml

with open("app/config.yaml", "r") as f:
    config = yaml.safe_load(f)

def get_num_predict_for(dataset_name: str) -> int:
    if dataset_name in config.get("datasets", {}):
        return config["datasets"][dataset_name].get("num_predict", config["default"]["num_predict"])
    return config["default"]["num_predict"]
