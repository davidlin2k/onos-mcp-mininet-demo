#!/usr/bin/env python3
"""
Complex Mininet scenario for Video‑Streaming Policing with random background hosts,
simulating video stream via iperf instead of HTTP.

Topology:
    Controller: ONOS at localhost:6653
    Core switch: s0 (OVS OF14)
    Leaf switches: s1, s2 (OVS OF14)
    Hosts:
        h_video_src (10.0.0.1) ↔ s1
        h_video_dst (10.0.0.4) ↔ s2
        h_bg1 (10.0.0.2) ↔ s1 (fixed background)
        h_bg2 (10.0.0.3) ↔ s2 (fixed background)
        rh1_i (10.0.1.x) ↔ s1 (random hosts)
        rh2_i (10.0.2.x) ↔ s2 (random hosts)

Each link uses TCLink with specified bandwidth and delay.

Workflow:
  1. Start Mininet with TCLink for realistic link parameters.
  2. Dynamically create random hosts on s1 and s2.
  3. Wait for ONOS to discover topology.
  6. Launch background iperf traffic: both fixed and random hosts.
  7. Start iperf UDP server on h_video_dst and simulate video stream from h_video_src at 8 Mbps.
  8. CLI for further inspection.
"""
import time
import random
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info

# ONOS configuration
onos_base = 'http://127.0.0.1:8181/onos/v1'
# Default ONOS credentials
auth = ('onos', 'rocks')

# Number of random hosts per leaf switch
NUM_RANDOM = 3
# Bandwidth range for random cross-traffic (in Mbps)
MIN_BW = 5
MAX_BW = 15

def setup_network():
    setLogLevel('info')
    net = Mininet(controller=RemoteController,
                  switch=OVSSwitch,
                  link=TCLink,
                  autoSetMacs=True)

    # Controller
    net.addController('c0', RemoteController, ip='127.0.0.1', port=6653)

    # Core and leaf switches
    s0 = net.addSwitch('s0', protocols='OpenFlow14')
    s1 = net.addSwitch('s1', protocols='OpenFlow14')
    s2 = net.addSwitch('s2', protocols='OpenFlow14')

    # Fixed hosts
    h_video_src = net.addHost('h1', ip='10.0.0.1/24')
    h_bg1 = net.addHost('h2', ip='10.0.0.2/24')
    h_bg2 = net.addHost('h3', ip='10.0.0.3/24')
    h_video_dst = net.addHost('h4', ip='10.0.0.4/24')

    # Random host lists
    rand_s1 = []
    rand_s2 = []

    # Add random hosts to s1
    for i in range(NUM_RANDOM):
        ip = f'10.0.1.{10 + i}/24'
        host = net.addHost(f'rh1{i}', ip=ip)
        net.addLink(host, s1, cls=TCLink, bw=20, delay='2ms')
        rand_s1.append(host)

    # Add random hosts to s2
    for i in range(NUM_RANDOM):
        ip = f'10.0.2.{10 + i}/24'
        host = net.addHost(f'rh2{i}', ip=ip)
        net.addLink(host, s2, cls=TCLink, bw=20, delay='2ms')
        rand_s2.append(host)

    # Fixed links
    net.addLink(s0, s1, cls=TCLink, bw=100, delay='5ms')
    net.addLink(s0, s2, cls=TCLink, bw=100, delay='5ms')
    net.addLink(h_video_src, s1, cls=TCLink, bw=50, delay='2ms')
    net.addLink(h_bg1, s1, cls=TCLink, bw=20, delay='2ms')
    net.addLink(h_video_dst, s2, cls=TCLink, bw=50, delay='2ms')
    net.addLink(h_bg2, s2, cls=TCLink, bw=20, delay='2ms')

    # Start network
    net.start()
    info('[*] Network started; waiting for ONOS discovery...\n')
    time.sleep(5)

    # Start fixed background traffic
    info('[*] Starting fixed UDP traffic h2->h3...\n')
    h_bg1.cmd('iperf -u -s &')
    h_bg2.cmd('iperf -u -c 10.0.0.2 -b 15M -t 60 &')

    # Start random background traffic
    for src in rand_s1:
        dst = random.choice(rand_s2)
        bw = random.randint(MIN_BW, MAX_BW)
        info(f'[*] Random UDP {bw}Mbps {src.name}->{dst.IP()}...\n')
        dst.cmd('iperf -u -s &')
        src.cmd(f'iperf -u -c {dst.IP()} -b {bw}M -t 60 &')

    # Simulate video stream via iperf UDP
    info('[*] Starting iperf UDP server on h4...\n')
    h_video_dst.cmd('iperf -u -s &')
    time.sleep(1)
    info('[*] Simulating video stream at 8 Mbps from h1->h4...\n')
    result = h_video_src.cmd('iperf -u -c 10.0.0.4 -b 8M -t 60')
    info(result)

    info('[*] Setup complete. Entering CLI...\n')
    from mininet.cli import CLI
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setup_network()
