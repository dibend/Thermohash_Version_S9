
# Thermohash Version S9

A powerful Python-based automation script designed to dynamically adjust the power target of Braiins OS miners (specifically for Antminer S9 models) based on real-time outdoor temperature. Thermohash Version S9 uses geolocation and weather APIs to optimize miner efficiency and performance.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Configuration](#configuration)
- [How to Run](#how-to-run)
- [Setting Up a Cron Job](#setting-up-a-cron-job)
- [Future Enhancements](#future-enhancements)

---

## Overview

Thermohash Version S9 eliminates manual tuning by leveraging:
- **Geolocation API**: Fetches your device's latitude and longitude automatically.
- **Open-Meteo API**: Retrieves accurate, real-time outdoor temperature.
- **SSH with `sshpass`**: Securely adjusts the miner's configuration dynamically without requiring a reboot.

This tool is perfect for miners operating in regions with fluctuating temperatures, ensuring power targets align with environmental conditions to improve efficiency and protect hardware.

---

## Setup

### 1. Prerequisites
Before you begin, ensure the following are installed:
- **Python 3** and necessary modules:
  ```bash
  pip install requests
  ```
- **sshpass** for automated SSH password authentication:
  ```bash
  sudo apt install sshpass
  ```

### 2. Clone the Repository
Download the script to your local machine:
```bash
git clone https://github.com/your-repo/thermohash_version_s9.git
cd thermohash_version_s9
```

---

## Configuration

1. Create a `config.ini` file in the script directory:
   ```ini
   [miner]
   hostname = your-miner-hostname-or-ip
   root_password = your-root-password

   [temperature]
   default_power_target = 750
   temp_to_power_mapping = {"30": 450, "20": 550, "10": 650, "0": 750}
   ```

   **Explanation:**
   - `hostname`: The miner's hostname or IP address.
   - `root_password`: The SSH root password for the miner.
   - `default_power_target`: A fallback power target (in watts) if temperature data is unavailable.
   - `temp_to_power_mapping`: A JSON-like dictionary mapping outdoor temperatures (in °C) to power targets.

2. Save the file and ensure it is in the same directory as the Python script.

---

## How to Run

1. Execute the script to adjust the power target dynamically:
   ```bash
   python3 thermohash_version_s9.py
   ```
2. The script will:
   - Fetch your geolocation (cached after the first run).
   - Retrieve the current outdoor temperature.
   - Map the temperature to the nearest power target.
   - Apply the configuration to your miner over SSH.

---

## Setting Up a Cron Job

Automate the script to run periodically for continuous tuning.

1. Open the crontab editor:
   ```bash
   crontab -e
   ```

2. Add an entry to execute the script every 3 hours:
   ```bash
   0 * * * * python3 /path/to/thermohash_version_s9.py >> /path/to/logfile.txt 2>&1
   ```

   **Explanation:**
   - `0 * * * *`: Runs the script every hour.
   - Replace `/path/to/thermohash_version_s9.py` with the absolute path to the script.
   - Replace `/path/to/logfile.txt` with the absolute path to the desired logfile location and name.

3. Save and exit. The cron job will now run at the specified interval.

---

## Future Enhancements

- Integration with multiple miners.
- Support for advanced APIs with historical and forecasted weather data.
- Enhanced error handling and notification systems for configuration failures.

Thermohash Version S9 ensures your mining setup operates efficiently and adaptively in all environmental conditions.
