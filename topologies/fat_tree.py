#!/usr/bin/python

"""
Fat Tree Topology

This topology implements a Fat Tree network, commonly used in data centers.
A k-ary fat tree contains k pods, each with k/2 edge switches and k/2 aggregation switches.
Each edge switch connects to k/2 hosts and k/2 aggregation switches.
Each aggregation switch connects to k/2 edge switches and k/2 core switches.
There are (k/2)^2 core switches, each connecting to k pods.

Usage:
------
sudo mn --custom=./topologies/fat_tree.py --topo fattree,k=4 --switch ovs,protocols=OpenFlow14,stp=1 \
  --controller remote,ip=localhost
"""

from mininet.topo import Topo

class FatTreeTopo(Topo):
    def __init__(self, k=4, **opts):
        """Create a Fat Tree topology with parameter k.
        
        Args:
            k: Number of ports per switch (must be even)
        """
        self.k = k
        self.pod_count = k
        self.core_switch_count = (k//2)**2
        self.agg_switch_per_pod = k//2
        self.edge_switch_per_pod = k//2
        self.hosts_per_edge = k//2
        
        super(FatTreeTopo, self).__init__(**opts)

    def build(self):
        # Create core switches
        core_switches = []
        # Start switch numbering from 1
        switch_counter = 1
        
        # Create core switches
        for i in range(self.core_switch_count):
            sw = self.addSwitch(f's{switch_counter}')
            core_switches.append(sw)
            switch_counter += 1
        
        # For each pod
        for pod in range(self.pod_count):
            # Create aggregation switches
            agg_switches = []
            for i in range(self.agg_switch_per_pod):
                sw = self.addSwitch(f's{switch_counter}')
                agg_switches.append(sw)
                switch_counter += 1
            
            # Create edge switches
            edge_switches = []
            for i in range(self.edge_switch_per_pod):
                sw = self.addSwitch(f's{switch_counter}')
                edge_switches.append(sw)
                switch_counter += 1
            
            # Connect edge and aggregation switches
            for edge_sw in edge_switches:
                for agg_sw in agg_switches:
                    self.addLink(edge_sw, agg_sw)
            
            # Connect aggregation switches to core switches
            for i, agg_sw in enumerate(agg_switches):
                core_offset = i * (self.k//2)
                for j in range(self.k//2):
                    core_idx = core_offset + j
                    self.addLink(agg_sw, core_switches[core_idx])
            
            # Connect hosts to edge switches
            for i, edge_sw in enumerate(edge_switches):
                for j in range(self.hosts_per_edge):
                    host_id = pod * (self.k//2) * (self.k//2) + i * (self.k//2) + j + 1
                    host = self.addHost(f'h{host_id}')
                    self.addLink(edge_sw, host)

# Register the topology
topos = { 'fattree': FatTreeTopo }
