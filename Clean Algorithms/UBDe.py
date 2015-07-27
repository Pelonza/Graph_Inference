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

#Ideal Placement
import networkx as nx
import sys
import operator


class Alg():
    '''
    Algorithm: Upper Bound Discovery - Edges (UBDe)
    
    Always calls 'pick-start'
    Pick-Start always returns the highest degree node in the undiscovered graph
    
    Add-Neighbor updates original graph by removing edges to found nodes.
        This requires a deep-copy of the original graph to occur
        (so we don't mess it up for later calls or repeats to UBDe)    
    
    '''
    
    
    def __init__(self, graph, sd):
        self.graph = graph.copy()
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.num_monitors = 0
        self.total_num=self.graph.number_of_nodes()
        return
    

    def pick_start(self):
        start_node = max((self.graph.degree().iteritems()), key=operator.itemgetter(1))[0]
        self.monitor_set.add(start_node)
        return start_node

    def add_neighbors(self, node):
        #Have to add self, incase I have no neighbors.
        self.result_graph.add_node(node)
    
        neighbors = self.graph.neighbors(node)
        for neighbor in neighbors:
            self.result_graph.add_edge(node, neighbor)
        self.graph.remove_nodes_from(self.monitor_set)
        return
    

    def place_next_monitor(self,node,param):
        return self.pick_start()

    def stop(self, allotment):
        '''Obsolete'''
        if allotment > self.total_num:
            print "oh god nooo"
            sys.exit(1)
        if len(self.monitor_set) < allotment:
            return False
        else:
            return True
