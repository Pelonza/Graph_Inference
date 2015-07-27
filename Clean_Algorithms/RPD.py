'''
Created by Karl Schmitt, Nicholas Juliano, Brittany Reynolds, Erin Moore, Ralucca Gera, and Erik
Commit Date 7/27/2015

You may contact the primary author at:
karl <dot> schmitt <at> valpo <dot> edu

Licensed under:

This work is licensed under a Creative Commons 
Attribution-NonCommercial-NoDerivatives 4.0 International License
Details of this license can be found at:
http://creativecommons.org/licenses/by-nc-nd/4.0/

Essentially, except by explicit permission, this code may not be adapted,
shared or sold for any reason.
'''

#Random Placement Dumb
import networkx as nx
import sys
import numpy as np
#import copy #We need a deepcopy if the self.graph gets modified.

class Alg():
    '''
    Algorithm: Random Placement Dumb (RPD)

    Randomly places nodes with replacement.
    (i.e. can pick a node with a monitor)
    This just means we might put less total monitors on.... 
    '''
    
    def __init__(self, graph, sd):
        #We need a deepcopy if the self.graph gets modified.
        #self.graph=copy.deepcopy(graph)
        self.graph = graph
        np.random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.num_monitors = 0    
        return

    #public method. Picks a random node that hasn't been a monitor yet.
    #returns the node number
    def pick_start(self):
        start_node = np.random.choice(self.graph.nodes())
        self.monitor_set.add(start_node)
        return start_node
    
    #public method. adds all edges (in NetworkX adding an edge adds the nodes if not alread there)
    #from the node to all of its neighbors
    def add_neighbors(self, node):
        #Have to add self, incase I have no neighbors.
        self.result_graph.add_node(node) 
        
        neighbors = self.graph.neighbors(node)
        for neighbor in neighbors:
            self.result_graph.add_edge(node, neighbor)
        return
   
    #public method. 
    # Simply calls the 'pick start' method, which randomly places a monitor
    # without replacement. Provided to support standard algorithm interfacing.
    def place_next_monitor(self, node, prob):              
        return self.pick_start()
        return
        
    #public method. Returns true if we have place all the monitors
    #we have available to us, else returns false
    def stop(self, allotment):
        #Probably obsolete.
        if allotment > self.graph.number_of_nodes():
            ##print "Error, cannot have more than", self.graph.number_of_nodes(), "monitors!"
            sys.exit(1)

        if len(self.monitor_set) < allotment:
            return False
        else:
            return True
