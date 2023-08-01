import os, platform, urllib3, subprocess
urllib3.disable_warnings()
from tempfile import TemporaryFile
from argparse import ArgumentParser, BooleanOptionalAction
from time import sleep

from proxmoxer import ProxmoxAPI
from proxmoxer.core import ResourceException

from cfg import user, passw

def open_file(filepath):
    plat = platform.system()
    if plat == 'Darwin': # macOS
        subprocess.call(('open', filepath))
    elif plat == 'Windows': # Windows
        os.startfile(filepath)
    else: # linux variants
        subprocess.call(('xdg-open', filepath))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-s", "--server", help="Server to connect to", type=str, default="192.168.178.8", required=False)
    parser.add_argument("-n", "--name", help="Name of the VM", type=str, default="win11-1", required=False)
    parser.add_argument("-f", "--fullscreen", help="Start in fullscreen mode", action=BooleanOptionalAction, default=False)
    args = parser.parse_args()


    pve = ProxmoxAPI(args.server, user=user, password=passw, verify_ssl=False)
    vms = {}
    nodes = []
    for node in pve.nodes.get():
        node_name = node["node"]
        vms[node_name] = {}
        nodes.append(node_name)
        qemu = pve.nodes(node_name).qemu
        for vm in qemu.get():
            vm_name = vm["name"]
            vms[node_name][vm_name] = vm

    vmid = None
    node_name = None
    for n in nodes:
        for vm in vms[n]:
            if vm == args.name:
                if vms[n][vm]["status"] != "running":
                    print("Error: VM not running")
                    exit(1)
                vmid = vms[n][vm]["vmid"]
                node_name = n
                break
        if vmid:
            break

    if vmid is None:
        print("Error: VM not found")
        exit(1)

    try:
        spice = pve.nodes(node_name).qemu(vmid).spiceproxy.post()
    except ResourceException as e:
        print(e)
        exit(1)

    content = "[virt-viewer]\n"
    for prop in spice:
        content += f'{prop}={spice[prop]}\n'
    if args.fullscreen:
        content += "fullscreen=1\n"

    print("Server:", args.server)
    print("Node:  ", node_name)
    print("VM:    ", args.name, f"({vmid})")

    with TemporaryFile(suffix=".vv", delete=False, mode="w", encoding="utf-8") as f:
        f.write(content)
        print("Writing spice profile to", f.name)

    sleep(3) # somehow required

    if args.fullscreen:
        print("Starting virt-viewer in fullscreen mode (Shift+F11 to exit)")
    else:
        print("Starting virt-viewer")

    open_file(f.name)