import sys
import subprocess

def start():
    print("Starting AutoOps...")
#    stop werking all time because this is service not working always
#    subprocess.Popen(["python", "-m", "autoops.agent.agent"])
    subprocess.Popen(["python", "-m", "autoops.web.web"])

def stop():
    print("Stopping AutoOps...")
    subprocess.run(["pkill", "-f", "autoops"])

def status():
    subprocess.run(["systemctl", "status", "autoops"])

if __name__ == "__main__":
    if len(sys.argv) <2:
        print("Usage: autoops [start|stop|status]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start":
        start()
    elif command == "stop":
        stop()
    elif command == "status":
        status()
    else:
        print("Unknow command")
