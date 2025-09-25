# config_manager.py
import configparser
import os

CONFIG_FILE = ".credentials"

def configure_profile():
    """Interactively prompts the user to create or update a credentials profile."""
    profile_name = input("▶ Enter a profile name (default: [default]): ").strip()
    if not profile_name:
        profile_name = "default"

    api_key = input("▶ Enter your Google Custom Search API Key: ").strip()
    search_engine_id = input("▶ Enter your Search Engine ID (cx): ").strip()

    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)

    config[profile_name] = {
        "API_KEY": api_key,
        "SEARCH_ENGINE_ID": search_engine_id
    }

    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
    print(f"\n✅ Profile '{profile_name}' saved successfully to '{CONFIG_FILE}'")

def load_credentials(profile_name):
    """Loads API key and Search Engine ID for a given profile."""
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Error: Credentials file '{CONFIG_FILE}' not found.")
        print("   Please run 'python3 main.py config' to set up your credentials first.")
        return None, None

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    if profile_name in config:
        api_key = config[profile_name].get("API_KEY")
        search_engine_id = config[profile_name].get("SEARCH_ENGINE_ID")
        if not api_key or not search_engine_id:
            print(f"❌ Error: API_KEY or SEARCH_ENGINE_ID missing in profile '{profile_name}'.")
            return None, None
        return api_key, search_engine_id
    else:
        print(f"❌ Error: Profile '{profile_name}' not found in '{CONFIG_FILE}'.")
        return None, None
