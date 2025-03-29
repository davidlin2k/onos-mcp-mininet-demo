#!/usr/bin/python

"""
Example Usage:
--------------

Basic command structure:
sudo mn --custom=./examples/spine_and_leaf.py --topo spineleaf[,PARAMS] [MININET_OPTIONS]

Parameters (with defaults):
- spine_count=2    : Number of spine switches in the topology
- leaf_count=4     : Number of leaf switches in the topology  
- hosts_per_leaf=1 : Number of hosts connected to each leaf switch

Common Mininet options:
- --mac            : Set MAC addresses automatically based on node position
- --switch SWITCH  : Use specified switch type (ovs is Open vSwitch)
- --controller CONTROLLER : Use specified controller type
- --ipbase IP/PREFIX : Base IP network for hosts

Examples:
---------

1. Basic spine-leaf topology with default settings (2 spines, 4 leaves, 1 host per leaf):
   sudo mn --custom=./examples/spine_and_leaf.py --topo spineleaf --controller remote,ip=localhost

2. Custom spine-leaf topology with 3 spines, 6 leaves, and 4 hosts per leaf:
   sudo mn --custom=./examples/spine_and_leaf.py --topo spineleaf,spine_count=3,leaf_count=6,hosts_per_leaf=4 \
     --mac --switch ovs,protocols=OpenFlow14,stp=1 --controller remote,ip=localhost

3. Small testing topology with OpenFlow 1.5:
   sudo mn --custom=./examples/spine_and_leaf.py --topo spineleaf,spine_count=2,leaf_count=2,hosts_per_leaf=2 \
     --mac --switch ovs,protocols=OpenFlow15 --controller remote,ip=localhost

After the topology starts, you can use Mininet CLI commands like:
- pingall        : Test connectivity between all hosts
- iperf          : Run iperf between hosts
- h1 ping h2     : Ping from host 1 to host 2
- links          : Display network links
- net            : Display network connections
- dump           : Show node info
"""

from mininet.topo import Topo

class SpineLeafTopo(Topo):
    def __init__(self, spine_count=2, leaf_count=4, hosts_per_leaf=1, **opts):
        """Create a spine-leaf topology with configurable number of switches.
        
        Args:
            spine_count: Number of spine switches
            leaf_count: Number of leaf switches
            hosts_per_leaf: Number of hosts connected to each leaf switch
        """
        # Store parameters as instance variables
        self.spine_count = spine_count
        self.leaf_count = leaf_count
        self.hosts_per_leaf = hosts_per_leaf
        
        # Initialize topo
        super(SpineLeafTopo, self).__init__(**opts)

    def build(self):
        # Create spine switches
        spines = []
        for i in range(1, self.spine_count + 1):
            spine = self.addSwitch(f's{i}')
            spines.append(spine)
        
        # Create leaf switches
        leaves = []
        for i in range(self.spine_count + 1, self.spine_count + self.leaf_count + 1):
            leaf = self.addSwitch(f's{i}')
            leaves.append(leaf)
        
        # Connect leaf switches to spine switches
        for leaf in leaves:
            for spine in spines:
                self.addLink(leaf, spine)
        
        # Create and connect hosts to leaf switches
        host_num = 1
        for i, leaf in enumerate(leaves, 1):
            for j in range(self.hosts_per_leaf):
                host = self.addHost(f'h{host_num}')
                self.addLink(host, leaf)
                host_num += 1

# Register the topology
topos = { 'spineleaf': SpineLeafTopo }
