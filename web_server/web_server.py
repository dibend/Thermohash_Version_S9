from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import configparser
import subprocess
import os

app = FastAPI()

# Load configuration
config = configparser.ConfigParser()
config.read("config.ini")

LOG_FILE = Path(config.get("paths", "log_file"))
SCRIPT_PATH = Path(config.get("paths", "script_path"))

# Ensure log file exists
if not LOG_FILE.exists():
    with LOG_FILE.open("w") as f:
        f.write("Thermohash Log Initialized\n")

# Templates setup
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def read_log(request: Request):
    """Display the log file content in a web browser."""
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            log_content = f.read()
    else:
        log_content = "Log file not found."
    return templates.TemplateResponse(
        "index.html", {"request": request, "log_content": log_content}
    )


@app.post("/run-script")
async def run_script():
    """Run the script and append output to the log file."""
    try:
        with open(LOG_FILE, "a") as f:
            f.write("\n--- Running Thermohash Script ---\n")
            subprocess.run(
                ["python3", str(SCRIPT_PATH)],
                stdout=f,
                stderr=f,
                check=True,
            )
            f.write("\n--- Script Execution Complete ---\n")
    except subprocess.CalledProcessError as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"\n--- Script Execution Failed: {e} ---\n")
    return {"status": "Script executed successfully!"}
