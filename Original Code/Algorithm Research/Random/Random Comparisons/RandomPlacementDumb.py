#Trying to make the random placement.

#Random Placement Smart
import networkx as nx
import random, sys

class RP():
    def __init__(self, graph, sd):
        self.graph = graph
        random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.num_monitors = 0

    def pick_start(self):
        start_node = random.choice(self.graph.nodes())
        self.monitor_set.add(start_node)
        self.result_graph.add_node(start_node)
        return start_node
    
    def add_neighbors(self, node):
        neighbors = self.graph.neighbors(node)
        for neighbor in neighbors:
            self.result_graph.add_edge(node, neighbor)
   

    def stop(self, allotment):
        if allotment > self.graph.number_of_nodes():
            sys.exit(1)

        if len(self.monitor_set) < allotment:
            return False
        else:
            return True