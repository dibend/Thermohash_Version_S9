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
temp_to_power_mapping = json.loads(config.get("temperature", "temp_to_power_mapping"))

# File to cache geolocation and last known power target
CACHE_FILE = os.path.join(script_dir, "geolocation_cache.json")
POWER_TARGET_FILE = os.path.join(script_dir, "last_power_target.json")

def get_geolocation():
    """
    Fetches geolocation data using ip-api.com. Caches the result locally to avoid redundant API calls.
    Returns:
        tuple: (latitude, longitude) if successful, otherwise (None, None)
    """
    # Check if cache exists
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cached_data = json.load(f)
                print("Using cached geolocation.")
                return cached_data["lat"], cached_data["lon"]
        except Exception as e:
            print(f"Error reading geolocation cache: {e}")
            # Proceed to fetch fresh data if cache is invalid

    # Fetch fresh geolocation data
    GEOLOCATION_API_URL = "http://ip-api.com/json/"
    try:
        response = requests.get(GEOLOCATION_API_URL)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "success":
            lat, lon = data["lat"], data["lon"]
            print(f"Geolocation fetched: Latitude {lat}, Longitude {lon}")

            # Save to cache
            with open(CACHE_FILE, "w") as f:
                json.dump({"lat": lat, "lon": lon}, f)

            return lat, lon
        else:
            print(f"Geolocation API error: {data.get('message', 'Unknown error')}")
            return None, None
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

def determine_power_target(temp, mapping):
    """
    Determine the power target based on temperature.

    Args:
        temp (int): Current temperature.
        mapping (dict): A dictionary where keys are temperature thresholds (str) 
                        and values are power targets (int).

    Returns:
        int: The power target corresponding to the temperature.
    """
    # Convert mapping keys to integers and sort in ascending order
    sorted_mapping = sorted((int(k), v) for k, v in mapping.items())

    # If temperature is below the lowest threshold, use the lowest power
    if temp < sorted_mapping[0][0]:
        return sorted_mapping[0][1]

    # If temperature is above the highest threshold, use the highest power
    if temp > sorted_mapping[-1][0]:
        return sorted_mapping[-1][1]

    # Handle in-between temperatures
    for i in range(len(sorted_mapping) - 1):
        lower_temp, lower_power = sorted_mapping[i]
        upper_temp, upper_power = sorted_mapping[i + 1]
        if lower_temp <= temp <= upper_temp:
            # Interpolate power between thresholds
            temp_range = upper_temp - lower_temp
            power_range = upper_power - lower_power
            return lower_power + (temp - lower_temp) * power_range // temp_range

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
    power_target = determine_power_target(temperature, temp_to_power_mapping)
    print(f"Determined power target: {power_target}W")

    # Load last known power target
    last_power_target = load_last_power_target()
    print(f"Last known power target: {last_power_target}W")

    # Adjust the miner's power target if necessary
    adjust_power_target(hostname, root_password, power_target, last_power_target)

if __name__ == "__main__":
    main()
