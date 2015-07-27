'''
Created on Jan 25, 2015

@author: erik
'''
###################
#if you get an error about this line when you try to run,
#go to the package manager and install networkx
import networkx as nx
import random, sys

class RW():
    def __init__(self, graph, sd):
        self.graph = graph
        random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.num_monitors = 0

    #public method. Picks a random node that hasn't been a monitor yet.
    #returns the node number
    def pick_start(self):
        start_node = random.choice([x for x in self.graph.nodes() if x not in self.monitor_set])
        self.monitor_set.add(start_node)
        self.result_graph.add_node(start_node)
        return start_node
    
    #public method. adds all edges (in NetworkX adding an edge adds the nodes if not alread there)
    #from the node to all of its neighbors
    def add_neighbors(self, node):
        neighbors = self.graph.neighbors(node)
        for neighbor in neighbors:
            self.result_graph.add_edge(node, neighbor)
   
    #public method. Iterates through all neighbors, and creates a list (neighbor_list)
    #of the neighbors w/highest degree. 
    def place_next_monitor(self, node):
        neighbors = self.graph.neighbors(node)
        next_monitor = random.choice(neighbors)
        
        #if our next monitor has already been a monitor, we need
        #to randomly select a new one
        if next_monitor in self.monitor_set:
            print "Ran out of potential monitors, need to pick new random one"
            next_monitor = self.pick_start()
       
        else:
            self.monitor_set.add(next_monitor)

        print "Next monitor", next_monitor  
        return next_monitor
        
    #public method. Returns true if we have place all the monitors
    #we have available to us, else returns false
    def stop(self, allotment):
        if allotment > self.graph.number_of_nodes():
            print "Error, cannot have more than", self.graph.number_of_nodes(), "monitors!"
            sys.exit(1)

        if len(self.monitor_set) < allotment:
            return False
        else:
            return True
        
