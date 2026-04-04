#!/bin/bash

echo " Installing AutoOps..."

# update System
sudo apt update

#install python & venv
sudo apt install -y python3 python3-venv python3-pip

# make VENV
python3 -m venv venv

#activate venv 
source venv/bin/activate

# setup leb
pip install flask psutil pyyaml

echo " Installation complete!"

echo ""
echo " To start AutoOps:"
echo "1. source venv/bin/activate"
echo "2. python -m autoops.agent.agent"
echo "3. Open new terminal and run:"
echo "   python -m autoops.web.web"

