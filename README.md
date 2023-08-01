# Proxmox SPICE Connect

Python script for initiating a remote connection to a vm running on a Proxmox VE host.

## Requirements

This script depends on the `proxmoxer` library using the `requests` backend. To install both dependencies, run pip specifying the requirements.txt file as input

    pip install -r requirements

## Usage

Username and password to the PVE host can either be provided over command line by using the parameters --user and --password or by editing the cfg.py file in this directory.

To start a SPICE connection as you would using the browser, run `run_spice.py` with python and specify host and vm name over command line.

    python run_spice.py --host 192.168.2.254 --name win10

Starting virt-viewer in fullscreen mode is supported by appending the --fullscreen parameter, which defaults to False.

## Parameters
```bash
usage: run_spice.py [-h] -s SERVER -u USER -p PASSWORD -n NAME [-f | --fullscreen | --no-fullscreen]

options:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Server to connect to
  -u USER, --user USER  Username to initiate the connection with
  -p PASSWORD, --password PASSWORD
                        The users password
  -n NAME, --name NAME  Name of the VM
  -f, --fullscreen, --no-fullscreen
                        Start in fullscreen mode
```