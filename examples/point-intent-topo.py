from mininet.topo import Topo

class TriangularTopo(Topo):
    def build(self):
        # Hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')

        # Switches
        s1 = self.addSwitch('s1')  # connects to h1
        s2 = self.addSwitch('s2')  # connects to h2
        s3 = self.addSwitch('s3')  # connects to h3

        # Host links
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)

        # Core links
        self.addLink(s1, s2)  # direct path (LLM should avoid this)
        self.addLink(s1, s3)
        self.addLink(s2, s3)

topos = { 'triangle': ( lambda: TriangularTopo() )}
