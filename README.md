
# Thermohash Version S9 Web Server

A FastAPI-based production-grade web server for managing and monitoring Thermohash Version S9. This server allows users to:
- View the Thermohash log file in a web browser.
- Execute the Thermohash script via a web interface and append its output to the log file.

---

## Features
- **Log Viewer**: Displays the Thermohash log (`/home/david/Desktop/s9.out`) in a browser-friendly format.
- **Run Script**: Provides a button to execute the Thermohash script (`/home/david/ThermohashVs9/thermohash_version_s9.py`) and appends the output to the log.
- **Configurable**: Uses a `config.ini` file to define paths for the log file and script.

---

## Installation (Ubuntu Environment)

### 1. Install System-Wide Packages
Install all required Python packages using `apt`:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-fastapi python3-jinja2 uvicorn -y
```

### 2. Verify Installation
Check that all dependencies are installed correctly:
```bash
uvicorn --help           # Check Uvicorn availability
python3 -m fastapi --help  # Check FastAPI availability
```

### 3. Configure Paths
Edit the `config.ini` file to point to your specific paths:
```ini
[paths]
log_file = /home/david/Desktop/s9.out
script_path = /home/david/ThermohashVs9/thermohash_version_s9.py
```

Replace `/home/david/Desktop/s9.out` and `/home/david/ThermohashVs9/thermohash_version_s9.py` with your actual file paths if they are different.

---

## Running the Web Server
Start the web server with:
```bash
uvicorn web_server:app --host 0.0.0.0 --port 8000
```

- Open your browser and navigate to `http://localhost:8000`.
- To access the server over a network, use your machine’s IP address (e.g., `http://192.168.1.100:8000`).

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
   chmod +rw /home/david/Desktop/s9.out
   chmod +x /home/david/ThermohashVs9/thermohash_version_s9.py
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
