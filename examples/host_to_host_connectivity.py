#!/usr/bin/env python

from mininet.topolib import TreeTopo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def run():
    # Tree topo with depth=2, fanout=2 → 4 hosts: h1, h2, h3, h4
    topo = TreeTopo(depth=2, fanout=2)

    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6653),
        switch=OVSSwitch,
        autoSetMacs=True,
        build=True,
        autoStaticArp=True
    )

    # Set OpenFlow version 1.4 for all switches
    for sw in net.switches:
        sw.cmd("ovs-vsctl set Bridge {} protocols=OpenFlow14".format(sw.name))

    net.start()

    print("\n*** Topology is up (tree,2,2). Hosts: h1–h4")
    print("*** Waiting for LLM agent to install flow rules (e.g., h1 <-> h4) ...")
    input(">>> Press Enter once flow rules are installed.\n")

    h1 = net.get('h1')
    h4 = net.get('h4')

    print("*** Testing connectivity with ping (h1 <-> h4)")
    net.ping([h1, h4])

    print("\n*** You can run further tests in the CLI (e.g., pingall, dpctl dump-flows)")
    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
