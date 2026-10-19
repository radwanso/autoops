import subprocess
import psutil

def get_system_state():
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "nginx": is_service_running("nginx"),
        "cron": is_service_running("cron")
    }



def is_service_running(service):
    try:
        result = subprocess.run(
            ["/bin/systemctl", "is-active", service],
            capture_output=True,
            text=True
        )

        service_active = result.stdout.strip() == "active"
        if service_active:
            print(f"DEBUG {service}: active")
            return True

        # Socket-activated services (such as OpenSSH on Ubuntu) can be
        # available while their service unit is inactive. Treat the matching
        # listening socket as available instead of reporting a false outage.
        service_unit = service[:-8] if service.endswith(".service") else service
        socket_unit = f"{service_unit}.socket"
        socket_result = subprocess.run(
            ["/bin/systemctl", "is-active", socket_unit],
            capture_output=True,
            text=True
        )
        socket_active = socket_result.stdout.strip() == "active"
        print(f"DEBUG {service}: {'active via socket' if socket_active else result.stdout.strip()}")
        return socket_active
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def get_system_metrics():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }
