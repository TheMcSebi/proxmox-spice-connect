import urllib3
urllib3.disable_warnings()

from proxmoxer import ProxmoxAPI

from cfg import servers, user, passw

if __name__ == "__main__":
    for s in servers.keys():
        servers[s] = ProxmoxAPI(s, user=user, password=passw, verify_ssl=False)

    for s in servers.keys():
        pve = servers[s]
        for node in pve.nodes.get():
            qemu = pve.nodes(node["node"]).qemu
            for vm in qemu.get():
                print(f'[{node["node"]}] {vm["name"]} ({vm["vmid"]}): {vm["status"]}')