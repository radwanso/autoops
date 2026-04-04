from autoops.core.core import load_config, get_system_state, is_service_running
from flask import Flask, render_template_string, request, redirect
import psutil
import subprocess


app = Flask(__name__)
project_dir ="/home/radwan/smart-it-agent"


def is_nginx_running():
    result = subprocess.run(["systemctl", "nginx","status" ], capture_output=True, text=True)
    return result.stdout.strip()

def get_alerts():
    try:
        with open("/home/radwan/smart-it-agent/alerts.log", "r") as f:
            return f.readlines()[-10:] # 10 last Alerts
    except:
        return []


def get_logs():
    try:
        with open(f"{project_dir}/logs/agent.log") as f:
            return f.readlines()[-10:]
    except:
        return []

def run_playbook():
    subprocess.Popen([
        "ansible-playbook",
	"-i", f"{project_dir}/inventory/hosts.ini",
	f"{project_dir}/playbooks/check_service.yml"
    ])






@app.route("/fix", methods=["POST"])
def fix():
    service = request.form.get("service")

    subprocess.Popen([
        "ansible-playbook",
        "-i", "/home/radwan/smart-it-agent/inventory/hosts.ini",
        "/home/radwan/smart-it-agent/playbooks/check_service.yml",
        "--extra-vars", f"service_name={service}"
    ])

    return redirect(f"/?status=fixing_{service}")

@app.route("/")
def home():
    config = load_config()
    services = config["services"]
    service_status = []

    state = get_system_state()
    cpu = state["cpu"]
    ram = state["ram"]
    disk = state["disk"]
    service_status = []
    for s in services:
        name = s["name"]
        running = is_service_running(name)

        if running:
            status_text = "Running"
        else:
            status_text = "Stopped"

        service_status.append({
            "name" : name,
            "status": status_text,
            "running": running
        })
    logs = get_logs()
    alerts = get_alerts()

    status = request.args.get("status")


    return render_template_string("""

<!DOCTYPE html>
<html>
<head>
    <title>smart IT Dashboard</title>
    <style>
        body {
            font-family: Arial;
            background-color: #f4f6f9;
            padding: 20px;
        }

        h1 {
            text-align: center;
        }

        .container {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }
        {% if status =="success" %}
            <P style="color: green;"><b> Nginx fixed sucessfully</b></p>
        {% endif %}

        .card {
            flex: 1;
            padding: 20px;
            border-radius: 10px;
            color: white;
            font-size: 20px;
        }
        .cpu {
            bakground: #3498db;
            padding: 15px:
            border-radius: 10px;
        }
        .ram { background: #2ecc71; }
        .disk { background: #9b59b6;  }
        .nginx { background: #f39c12;  }

        .alerts {
            background: #fff;
            padding: 15px;
            border-radius: 10px;
        }

        button {

            padding: 10px 20 px;
            font-size: 16px;
            margin-top: 10px;
        }
    </style>
</head>
<bod>

<h1> Smart IT Dashboard</h1>
<h2>Services</h2>
<div class="container">
{% for s in services %}
    <div class="card">CPU: {{cpu}}%</div>
    <div class="card">RAM: {{ram}}%</div>
    <div class="card">Disk: {{disk}}%</div>
    <div class="card nginx" style="background: {% if s.running %}#2ecc71{% else %}red{% endif %};">
        <p>{{s.name}}: {{s.status}}</p>
        <from method="post" action="/fix">
           <input type="hidden" name="service" value="{{s.name}}">
           <button type="submit">Fix</button>
        </from>
    </div>
    {% endfor %}
</div>

<from method="post" action="/fix">
    <button type="submit">Fix Nginx</button>
</from>
<h2> Alerts</h2>
<div class="alert">
<pre>
{% for alert in alerts %}
{{alert}}
{% endfor %}
</pre>
</div>
{% if status == "fixing" %}
    <p style="color: orange;"><b> Fix in progress...</b></p>
{% endif %}

{% if status == "success" %}
    <p style="color: green;"><b> Nginx fixed successfully</b></p>
{% endif %}

<script>
    setInterval(function(){
        window.location.reload();
    }, 5000); // every 5 second
</script>


</body>
</html>
""", cpu=cpu, ram=ram, disk=disk, services=service_status, logs=logs, status=status, alerts=alerts)


#best make methods with only "POST" but just for test i can add "GET" but i should make only "POST"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
