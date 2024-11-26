import os
import json
import requests
import configparser
import subprocess

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load configuration
config_path = os.path.join(script_dir, "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

# Miner settings
hostname = config.get("miner", "hostname")
root_password = config.get("miner", "root_password")

# Temperature and power settings
default_power_target = int(config.get("temperature", "default_power_target"))
temp_to_power_mapping = json.loads(config.get("temperature", "temp_to_power_mapping"))

# File to cache geolocation and last known power target
CACHE_FILE = os.path.join(script_dir, "geolocation_cache.json")
POWER_TARGET_FILE = os.path.join(script_dir, "last_power_target.json")

# Get geolocation (cached)
def get_geolocation():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)
            print("Using cached geolocation.")
            return data["lat"], data["lon"]

    try:
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()
        data = response.json()
        lat, lon = map(float, data["loc"].split(","))
        with open(CACHE_FILE, "w") as f:
            json.dump({"lat": lat, "lon": lon}, f)
        print("Geolocation fetched and cached.")
        return lat, lon
    except Exception as e:
        print(f"Error fetching geolocation: {e}")
        return None, None

# Get outdoor temperature
def get_outdoor_temperature(lat, lon):
    try:
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data["current_weather"]["temperature"]
    except Exception as e:
        print(f"Error fetching outdoor temperature: {e}")
        return None

# Determine the power target based on temperature
def determine_power_target(temp, mapping, default):
    for t, power in sorted(mapping.items(), key=lambda x: int(x[0]), reverse=True):
        if temp >= int(t):
            return power
    return default

# Load the last known power target
def load_last_power_target():
    if os.path.exists(POWER_TARGET_FILE):
        with open(POWER_TARGET_FILE, "r") as f:
            return json.load(f).get("last_power_target")
    return None

# Save the current power target
def save_last_power_target(power_target):
    with open(POWER_TARGET_FILE, "w") as f:
        json.dump({"last_power_target": power_target}, f)

# Adjust the miner power target
def adjust_power_target(hostname, root_password, power_target, last_power_target):
    if power_target == last_power_target:
        print(f"Power target remains the same ({power_target}W). No action needed.")
        return

    command = (
        f"sshpass -p '{root_password}' ssh -o StrictHostKeyChecking=no root@{hostname} "
        f"\"busybox sed -i '/\\[autotuning\\]/,/\\[/{{s/power_target = .*/power_target = {power_target}/}}' /etc/bosminer.toml && "
        f"busybox killall -HUP bosminer\""
    )
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Power target set to {power_target}W successfully.")
        save_last_power_target(power_target)
    except subprocess.CalledProcessError as e:
        print(f"Error adjusting power target: {e}")

def main():
    # Get geolocation
    lat, lon = get_geolocation()
    if not lat or not lon:
        print("Unable to fetch geolocation. Exiting.")
        return

    # Get outdoor temperature
    temperature = get_outdoor_temperature(lat, lon)
    if temperature is None:
        print("Unable to fetch outdoor temperature. Exiting.")
        return

    print(f"Current outdoor temperature: {temperature}°C")

    # Determine the power target
    power_target = determine_power_target(temperature, temp_to_power_mapping, default_power_target)
    print(f"Determined power target: {power_target}W")

    # Load last known power target
    last_power_target = load_last_power_target()
    print(f"Last known power target: {last_power_target}W")

    # Adjust the miner's power target if necessary
    adjust_power_target(hostname, root_password, power_target, last_power_target)

if __name__ == "__main__":
    main()
