import argparse
import subprocess
import os
import sys


SERVICE_NAME = "autoops"


def require_sudo():
    if os.geteuid() != 0:
        print("🔒 Requires sudo. Restarting...")
        os.execvp("sudo", ["sudo"] + sys.argv)


def start():
    require_sudo()
    subprocess.run(["/bin/systemctl", "start", SERVICE_NAME])
    print("✅ AutoOps started")


def stop():
    require_sudo()
    subprocess.run(["/bin/systemctl", "stop", SERVICE_NAME])
    print("🛑 AutoOps stopped")


def status():
    subprocess.run(["/bin/systemctl", "status", SERVICE_NAME])


def logs():
    subprocess.run(["journalctl", "-u", SERVICE_NAME, "-f"])


def install():
    require_sudo()

    service_file = f"""
[Unit]
Description=AutoOps Service
After=network.target

[Service]
ExecStart={sys.executable} -m autoops.core.engine
Restart=always

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/autoops.service", "w") as f:
        f.write(service_file)

    subprocess.run(["/bin/systemctl", "daemon-reload"])
    subprocess.run(["/bin/systemctl", "enable", SERVICE_NAME])

    print("✅ AutoOps installed and enabled")


def main_cli():
    parser = argparse.ArgumentParser(prog="autoops", description="AutoOps CLI")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("install")
    subparsers.add_parser("start")
    subparsers.add_parser("stop")
    subparsers.add_parser("status")
    subparsers.add_parser("logs")

    args = parser.parse_args()

    if args.command == "install":
        install()
    elif args.command == "start":
        start()
    elif args.command == "stop":
        stop()
    elif args.command == "status":
        status()
    elif args.command == "logs":
        logs()
    else:
        parser.print_help()

