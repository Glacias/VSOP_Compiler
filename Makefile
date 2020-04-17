# Install necessary packages
install-tools:
	sudo apt-get install --yes python3-pip
	sudo apt-get install --yes python-setuptools
	yes | sudo pip3 install ply
	yes | sudo pip3 install pyinstaller
	yes | sudo pip3 install argparse

# Create executable of compiler
vsopc:
	pyinstaller \
		--onefile main.py \
		--distpath ./ \
		--clean \
		--name vsopc \
		--specpath ./build \
		--workpath ./build \
		--add-data ../parsetab.py:/ \
