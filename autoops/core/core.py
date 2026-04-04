import os
import yaml
from datetime import datetime
import psutil
import subprocess

def load_config():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_dir, "config", "config.yaml")

    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def log_alert(message):
    with open("/home/radwan/smart-it-agent/alerts.log","a") as f:
        f.write(f"{datetime.now()} - {message}\n")


def get_system_state():
    return {
	"cpu": psutil.cpu_percent(interval=1),
	"ram": psutil.virtual_memory().percent,
	"disk": psutil.disk_usage('/').percent
    }

def is_service_running(service):
    result = subprocess.run(
        ["systemctl", "is-active", service],
        capture_output=True,
        text=True
    )
    return result.stdout.strip() == "active"

def fix_service(service):
    subprocess.run([
        "ansible-playbook",
        "-i", "/home/radwan/smart-it-agent/inventory/hosts.ini",
        "/home/radwan/smart-it-agent/playbooks/check_service.yml",
        "--extra-vars", f"service_name={service}"
    ])

def analyze_and_act():
    config = load_config()
    state = get_system_state()

    print("=== System State ===")
    print("CPU:", state["cpu"])
    print("RAM:", state["ram"])
    print("Disk:", state["disk"])

    # (rules)
    # CPU Alert
    if state["cpu"] > config["thresholds"]["cpu"]:
        print("High CPU usage!")
        log_alert("High CPU usage")

    # RAM alert
    if state["ram"] > config["thresholds"]["ram"]:
        print("High RAM usage!")
        log_alert("High RAM usage")

    # service check
    for service in config["services"]:
        name = service["name"]
        if not is_service_running(name):
            print(f" {name} is down >>> fixing...")
            log_alert(f"{name} was down >>> fixing triggered")
            fix_service(name)
        else:
            print(f" {name} is running")
