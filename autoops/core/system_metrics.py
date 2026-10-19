import psutil


def collect_system_metrics():

    memory = psutil.virtual_memory()

    return {
        "cpu": psutil.cpu_percent(
            interval=0.5
        ),
        "ram": memory.percent,
        "ram_used": memory.used,
        "ram_total": memory.total,
        "disk": psutil.disk_usage(
            "/"
        ).percent
    }
