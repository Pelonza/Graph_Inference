#Ideal Placement
import networkx as nx
import random, sys
import operator

class IP():
    def __init__(self, graph, sd):
        self.graph = graph.copy()
        random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.num_monitors = 0
        self.total_num=self.graph.number_of_nodes()

    def pick_start(self):
        start_node = max((self.graph.degree().iteritems()), key=operator.itemgetter(1))[0]
        self.monitor_set.add(start_node)
        self.result_graph.add_node(start_node)
        return start_node

    def add_neighbors(self, node):
        neighbors = self.graph.neighbors(node)
        for neighbor in neighbors:
            self.result_graph.add_edge(node, neighbor)
        self.graph.remove_nodes_from(self.monitor_set)

    def stop(self, allotment):
        if allotment > self.total_num:
            print "oh god nooo"
            sys.exit(1)
        if len(self.monitor_set) < allotment:
            return False
        else:
            return True
