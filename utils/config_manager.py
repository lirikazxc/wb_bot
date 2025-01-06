import json
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"shops": []}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        logger.error(f"Ошибка при загрузке конфигурации: {e}")
        return {"shops": []}

def save_config(data):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except IOError as e:
        logger.error(f"Ошибка при сохранении конфигурации: {e}")


def add_shop(api_key, shop_name):
    config = load_config()
    config["shops"].append({"name": shop_name, "api_key": api_key})
    save_config(config)

def delete_shop(shop_name):
    config = load_config()
    config["shops"] = [shop for shop in config["shops"] if shop["name"] != shop_name]
    save_config(config)

def list_shops():
    config = load_config()
    return config["shops"]
