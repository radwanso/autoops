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
