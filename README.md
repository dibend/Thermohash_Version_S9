<img src="https://njweb.solutions/img/thermohash_version_s9_logo.gif" width="90%"><b
r>
# Thermohash Version S9

A FastAPI-based production-grade web server for managing and monitoring Thermohash Version S9. This server allows users to:
- View the Thermohash log file in a web browser.
- Execute the Thermohash script via a web interface and append its output to the log file.

---

## Features
- **Log Viewer**: Displays the Thermohash log in a browser-friendly format.
- **Run Script**: Provides a button to execute the Thermohash script and appends the output to the log.
- **Configurable**: Uses `config.ini` files for path configuration.

---

## Installation (Ubuntu Environment)

### 1. Install System-Wide Packages
Install all required Python packages using `apt`:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-fastapi python3-jinja2 uvicorn -y
```

### 2. Set Up Configuration Files

#### **a. Thermohash Version S9 directory**
Create a `config.ini` file in the **Thermohash Version S9 directory** for Thermohash Version S9:
```ini
[miner]
hostname = your-miner-hostname-or-ip
root_password = your-root-password

[temperature]
default_power_target = 750
temp_to_power_mapping = {"30": 450, "20": 550, "10": 650, "0": 750}
```

- Replace `your-miner-hostname-or-ip` and `your-root-password` with the actual hostname/IP and SSH password for your miner.
- Adjust the `temp_to_power_mapping` dictionary as needed based on your environmental and operational conditions.

#### **b. Web Server Configuration**
Create a `config.ini` file in the **web server directory**:
```ini
[paths]
log_file = /path/to/your/log/file.log
script_path = /path/to/your/thermohash_script.py
```

- Replace the placeholders `/path/to/your/log/file.log` and `/path/to/your/thermohash_script.py` with your actual paths for the log file and Thermohash script.

### 3. Verify Installation
Check that all dependencies are installed correctly:
```bash
uvicorn --help           # Check Uvicorn availability
python3 -m fastapi --help  # Check FastAPI availability
```

---

## Running the Web Server
Start the web server with:
```bash
uvicorn web_server:app --host 0.0.0.0 --port 8000
```

- Open your browser and navigate to `http://localhost:8000`.
- To access the server over a network, use your machine’s IP address (e.g., `http://192.168.1.100:8000`).

---

## Setting Up Cron Jobs

Automate the execution of the Thermohash script with a cron job:

1. Open the crontab editor:
   ```bash
   crontab -e
   ```

2. Add an entry to execute the script periodically (e.g., every 3 hours):
   ```bash
   0 */3 * * * python3 /path/to/your/thermohash_script.py >> /path/to/your/log/file.log 2>&1
   ```

3. Save and exit. The script will now execute every 3 hours, appending its output to the log file.

---

## Setting Up the Web Server as a Service

Run the web server automatically on boot using `systemd`:

1. Create a new service file:
   ```bash
   sudo nano /etc/systemd/system/thermohash_web.service
   ```

2. Add the following content:
   ```ini
   [Unit]
   Description=Thermohash Version S9 Web Server
   After=network.target

   [Service]
   User=your-username
   WorkingDirectory=/path/to/your/web_server
   ExecStart=/usr/bin/uvicorn web_server:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Replace `your-username` with your Linux username and `/path/to/your/web_server` with the full path to your web server directory.

3. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable thermohash_web.service
   sudo systemctl start thermohash_web.service
   ```

4. Verify the service is running:
   ```bash
   sudo systemctl status thermohash_web.service
   ```

---

## Directory Structure
```
thermohash_web_server/
├── web_server.py       # Main FastAPI application
├── config.ini          # Configuration file for paths
├── templates/          # HTML templates for the web interface
│   └── index.html      # Log viewer and run script interface
```

---

## Troubleshooting

1. **Permission Issues**:
   Ensure the log file and script have the necessary permissions:
   ```bash
   chmod +rw /path/to/your/log/file.log
   chmod +x /path/to/your/thermohash_script.py
   ```

2. **Firewall Rules**:
   Allow traffic on port `8000` if accessing the server over a network:
   ```bash
   sudo ufw allow 8000
   ```

3. **Dependency Issues**:
   If packages are missing or not installed, re-run:
   ```bash
   sudo apt install python3 python3-fastapi python3-jinja2 uvicorn -y
   ```

---

## Future Enhancements
- Add authentication for running the script.
- Log rotation for better file management.
- Extend to support multiple Thermohash miners.

---

Thermohash Version S9 Web Server makes it easy to manage and monitor your mining operations efficiently.

## Additional Resources

- [S9 Bitcoin Space Heater Case](https://www.cryptocloaks.com/product/s9-space-heater-case-bitcoin/?srsltid=AfmBOoqL8NSlcea_XeDVuXM0SWU52W-bcEsdmaM37WsZhYx4Lo3qTSk6)
- [The Future of Space Heaters: A Bitcoin ASIC Build](https://www.cryptocloaks.com/the-future-of-space-heaters-s9-bitcoin-asic/?srsltid=AfmBOop71RDiPaTOjFqDfBs4psvR06L-8d0M4caqBR3oORT8iZ8Qsvjh)

![S9 Bitcoin Space Heater Case](https://i0.wp.com/www.cryptocloaks.com/wp-content/uploads/2024/01/IMG_20230130_201457_904.jpg?w=576&ssl=1)
