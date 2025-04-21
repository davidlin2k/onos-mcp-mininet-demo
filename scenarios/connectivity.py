#!/usr/bin/env python3
"""
Mininet script to automate the example scenario:
1. Start Mininet with an OVS switch (OpenFlow14) and a remote controller.
2. Install a misconfigured backup path flow rule via ONOS REST API.
3. Disable the primary path link programmatically.
4. Test connectivity and drop into the CLI for invoking MCP diagnostics.
"""
import requests
import json
import time
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI

def install_bad_flow():
    """
    Push a misconfigured flow rule to ONOS to simulate a bad backup path.
    """
    ONOS_API = "http://127.0.0.1:8181/onos/v1/flows/of%3A0000000000000001"
    AUTH = ('onos', 'rocks')
    flow_rule = {
        "priority": 50000,
        "timeout": 0,
        "isPermanent": True,
        "deviceId": "of:0000000000000001",
        "treatment": {"instructions": [{"type": "OUTPUT", "port": "1"}]},
        "selector": {"criteria": [{"type": "ETH_TYPE", "ethType": "0x0800"}]}
    }

    print(f"[STEP 2] Installing misconfigured flow to ONOS at {ONOS_API}...")
    headers = {"Content-Type": "application/json"}
    resp = requests.post(ONOS_API,
                         auth=AUTH,
                         headers=headers,
                         data=json.dumps(flow_rule))
    print(f"Response: HTTP {resp.status_code}\n{resp.text}")
    if resp.status_code not in (200, 201):
        raise RuntimeError("Failed to install bad flow rule on ONOS")


def setup_network():
    # Create the Mininet instance with OVS switch and remote controller
    net = Mininet(controller=RemoteController, switch=OVSSwitch)

    # Add the remote controller pointing to localhost:6653
    net.addController('c0', RemoteController, ip='127.0.0.1', port=6653)

    # Add hosts and switch
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    s1 = net.addSwitch('s1', protocols='OpenFlow14')

    # Create links
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    # Start network
    net.start()

    # Give ONOS a moment to discover devices
    time.sleep(2)

    # Step 2: Install misconfigured backup path via ONOS API
    install_bad_flow()

    # Step 3: Disable the primary path link (h1 <-> s1)
    print("[STEP 3] Disabling the primary path link between h1 and s1...")
    net.configLinkStatus('h1', 's1', 'down')

    # Step 4: Test connectivity (expect ping failures)
    print("[STEP 4] Testing connectivity from h1 to h2:")
    result = h1.cmd('ping -c3 10.0.0.2')
    print(result)

    # Enter CLI for MCP diagnostics
    print("Entering CLI. You can now interact with the network or invoke MCP diagnostics.")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setup_network()
