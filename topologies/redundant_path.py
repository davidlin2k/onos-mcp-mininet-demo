"""Redundant Path Topology Module.

This module defines a Mininet topology with redundant paths between two hosts.
It creates a network with two parallel paths and cross-connections,
allowing for failover scenarios and path redundancy testing.

Usage:
------
sudo mn --custom=./topologies/redundant_path.py --topo redundant --switch ovs,protocols=OpenFlow14,stp=1 \
  --controller remote,ip=localhost
"""

from mininet.topo import Topo

class RedundantPathTopo(Topo):
    """A topology with redundant paths between two hosts.
    
    The topology consists of:
    * 2 hosts (h1, h2)
    * 4 switches (s1-s4)
    * Primary path: h1 -- s1 -- s2 -- h2
    * Backup path: h1 -- s3 -- s4 -- h2
    * Cross connections: s1 -- s3, s2 -- s4
    """
    def build(self):
        h1 = self.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/24')
        h2 = self.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.0.2/24')
    
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        
        # Primary path
        self.addLink(h1, s1)
        self.addLink(s1, s2)
        self.addLink(s2, h2, params={'mac': '00:00:00:00:00:02'})  # Explicitly set MAC for this interface
  
        
        # Backup path
        self.addLink(h1, s3)
        self.addLink(s3, s4)
        self.addLink(s4, h2, params={'mac': '00:00:00:00:00:02'})  # Same MAC for consistency
        
        # Interconnections
        self.addLink(s1, s3)
        self.addLink(s2, s4)

topos = {'redundant': (lambda: RedundantPathTopo())}
