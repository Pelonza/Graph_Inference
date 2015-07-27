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

import networkx as nx
import sys
import numpy as np

#Modifications by Karl Schmitt, 7/15:
# Moved walk-length check into algorithm code by incorporating self-counter.

class Alg():
    '''
    Algorithm: Highest-Local Degree with Restart/Walk-Len/Found (HLD_rLF)

    IMPORTANT NOTE: This might not be working as thought...

    Current Algorithm Behavior:

        Pick Start: pick random, non-monitor node

        Place Next:
            Restart if half of neighbors have monitors
            OR
            Restart if walk-length > log(number of nodes in graph)
            
            Otherwise:
                Examine neighbors without monitors.
                Pick highest degree neighbor without monitor
            
                If no neighbors w/o monitors exist, teleport to a node without a monitor
                    

    '''
    
    def __init__(self, graph, sd):
        self.graph = graph
        np.random.seed(sd)
        
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        
        #Set this now, incase base graph changes
        self.maxwalklen=np.log(graph.number_of_nodes())
        self.walklen=0
        return

    def pick_start(self):
        #This try/except shouldn't matter... for speed? something else?
        try:
            temp=list(set(self.graph.nodes()) - self.monitor_set)
            start_node = np.random.choice(temp)
        except:
            start_node = np.random.choice([x for x in self.graph.nodes() if x not in self.monitor_set])        
        
        self.monitor_set.add(start_node)
        self.walklen=0
        return start_node

    def add_neighbors(self, node):
        #Have to add self, incase I have no neighbors.
        self.result_graph.add_node(node)
        
        neighbors = self.graph.neighbors(node)
        
        for neighbor in neighbors:
            self.result_graph.add_edge(node, neighbor)
        return

    def place_next_monitor(self, node, param):
        if self.walklen>self.maxwalklen:
            #Check walk length, and restart if max-len exceeded.
            next_monitor=self.pick_start()
        
        else:
            #If walklength not exceed, pick like normal (high local deg)

            neighbors = self.graph.neighbors(node)
            max_degree, neighbor_list = 0, []

            #Only look at neighbors without monitors for high local deg.
            neighbor_set = set(neighbors) - self.monitor_set

            #Check how many neighbors we have to pick from.
            if len(neighbor_set)< len(neighbors):
                #If less than half, teleport
                next_monitor=self.pick_start()
            else:
                #otherwise, continue picking the highest local degree
                for neighbor in neighbor_set:
                    degree = self.graph.degree(neighbor)

                    #This makes a list of the highest degree neighbors w/o monitors
                    if degree > max_degree:
                        neighbor_list = []
                        max_degree = degree
                        neighbor_list.append(neighbor)
                    elif degree == max_degree:
                        neighbor_list.append(neighbor)

                if len(neighbor_list)>0:
                    #If we found some max-degree nodes, pick one.
                    next_monitor = np.random.choice(neighbor_list)
                    self.walklen+=1
                else:
                    #If not, pick a random restart.
                    next_monitor= self.pick_start()

        self.monitor_set.add(next_monitor)
        return next_monitor

    def stop(self, allotment):
        '''Should be obsolete'''
        if allotment > self.graph.number_of_nodes():
            print "Error, cannot have more than", self.graph.number_of_nodes(), "monitors!"
            sys.exit(1)
        if len(self.monitor_set) < allotment:
            return False
        else:
            return True
