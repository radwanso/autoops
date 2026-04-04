# Smart IT Agent

A simple autonomous IT system built with Python and Ansible.

## Features 
- Monitors system (CPU usage)
- Checks service status (nginx)
- Automatically fixes issues 
- Logs all actions
- Runs automatically using cron

## Technologies
- Python 
- Ansible
- Linux (WSL Ubuntu)

## How it works
1. The agent checks CPU usage
2. Verifies if nginx is running
3. If nginx is down >> runs Ansible playbook

## Run Manually
````bash
python scripts/agent.py
