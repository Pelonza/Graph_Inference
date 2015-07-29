'''

Created by Karl Schmitt, Nicholas Juliano, Brittany Reynolds, Erin Moore, Ralucca Gera, and Erik
Original Created on Jan 25, 2015
Commit Date 7/27/2015

You may contact the primary author at:
karl <dot> schmitt <at> valpo <dot> edu

Copyright (C) 2015, Karl R. B. Schmitt & Ralucca Gera

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import networkx as nx
import sys
import numpy as np

class Alg():
    ''' 
    Algorithm: Random Walk Smart (RWS)
    
    Pick-Start : random node without a monitor
    Place-Next : randomly choose a neighbor, if choice has monitor, call pick-start
    
    '''
    def __init__(self, graph, sd):
        self.graph = graph
        np.random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.num_monitors = 0
        
        return

    #public method. Picks a random node that hasn't been a monitor yet.
    #returns the node number
    def pick_start(self):
        start_node = np.random.choice([x for x in self.graph.nodes() if x not in self.monitor_set])
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
        
        return neighbors
   
    #public method. Iterates through all neighbors, and creates a list (neighbor_list)
    #of the neighbors w/highest degree. 
    def place_next_monitor(self, node, params):
        neighbors = self.graph.neighbors(node)
        
        try:
            next_monitor = np.random.choice(neighbors)
        except:
            if len(neighbors)==0:
                print "No Neighbors, picking random"
            next_monitor=self.pick_start()
        
        #if our next monitor has already been a monitor, we need
        #to randomly select a new one
        if next_monitor in self.monitor_set:
            next_monitor = self.pick_start()
       
        self.monitor_set.add(next_monitor)

        return next_monitor
        
    #public method. Returns true if we have place all the monitors
    #we have available to us, else returns false
    def stop(self, allotment):
        ''' Should be obsolete '''
        if allotment > self.graph.number_of_nodes():
            #print "Error, cannot have more than", self.graph.number_of_nodes(), "monitors!"
            sys.exit(1)

        if len(self.monitor_set) < allotment:
            return False
        else:
            return True