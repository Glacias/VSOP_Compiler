# Install necessary packages
install-tools:
	sudo apt-get install --yes python3-pip
	sudo apt-get install --yes python-setuptools
	yes | sudo pip3 install ply
	yes | sudo pip3 install pyinstaller
	yes | sudo pip3 install argparse
	yes | sudo pip3 install llvmlite

# Create executable of compiler
vsopc:
	mv main.py vsopc
	chmod +x vsopc
