'''
Created by Karl Schmitt, Nicholas Juliano, Brittany Reynolds, Erin Moore, Ralucca Gera, and Erik
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
#import numpy as np #should be no random in here.

#Helper function to get list of things with max values.        
def maxes(a, key=None):
    if key is None:
        key = lambda x: x
    m, max_list = key(a[0]), []
    for s in a:
        k = key(s)
        if k > m:
            m, max_list = k, [s]
        elif k == m:
            max_list.append(s)
    return max_list


class Counter(dict):
    def __missing__(self,key):
        return 0
# If you try to index into a dictionary, and index doesn't exist, then you get an error...

class Alg():
    def __init__(self, graph, sd):
        #We need a deepcopy if the self.graph gets modified.
        self.graph = graph.copy()
        
        #np.random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.seen = Counter()
        self.monitor_free=nx.nodes(self.graph) #Save this list to speed computations.
        
        #Initialize all fake degrees to degree
        self.fake_degree=dict()
        for node in self.monitor_free:
            self.fake_degree[node]=self.graph.degree(node)
        return

    
    #public method. Returns true if we have placed all the monitors
    #we have available to us, else returns false
    def stop(self, allotment):
        #This may be obsolete.
        
        if allotment > self.graph.number_of_nodes():
            print "Error, cannot have more than", self.graph.number_of_nodes(), "monitors!"
            sys.exit(1)

        if len(self.monitor_set) < allotment:
            return False
        else:
            return True

    #public method. Picks a random node that hasn't been a monitor yet.
    #returns the node number
    def pick_start(self):
        #Add for "restart" not seen
        not_seen=[x for x in nx.nodes(self.graph) if self.seen[x]==0]
        start_node = max(not_seen, key=lambda mynode: self.graph.degree(mynode) )

        self.monitor_set.add(start_node)
        self.monitor_free.remove(start_node)
        
        return start_node

    #public method. adds all edges (in NetworkX adding an edge adds the nodes if not already there)
    #from the node to all of its neighbors
    def add_neighbors(self, node):
        #Have to add self, incase I have no neighbors.
        self.result_graph.add_node(node)
    
        
        neighbors = self.graph.neighbors(node) #this was changed for new code

        #Set of unique nodes that need to have their fake degrees updated, seeded with neighbors
        fake_update_set=set(neighbors) 
        
        #Add self to list to update
        fake_update_set.add(node) 

        #When we add the neighbors of a new node, set the seen count to 'inf'
        try:
            self.seen[node]='inf'
        except:
            print "Node (monitor) wasn't in neighbor list"

        for neighbor in neighbors:
            #Add edge between monitor (node) and it's neighbor to found graph
            self.result_graph.add_edge(node, neighbor)
            
            #Remove edge from monitor to neighbor
            self.graph.remove_edge(node,neighbor)
            
            #Add unique neighbors of neighbor to update list
            fake_update_set |=set(self.graph.neighbors(neighbor))
            
            #Update the seen count for each neighbor. We can use this to make new fake-degree also.
            if self.seen[neighbor] != 'inf':
                self.seen[neighbor]+=1
                self.seen['Total']+=1

        #Update the fake-degrees
        for node_to_update in fake_update_set:
            self.fake_degree[node_to_update]=self.graph.degree(node_to_update)-len([x for x in self.graph.neighbors(node_to_update) if self.seen[x]>0])

    #For cross-algorithm compatability, this accepts both a node, and a set of
    # of parameters that can be parsed.
    #
    #For this algorithm (UBN), the input node and parameters are unused.
    
    def place_next_monitor(self, node, params):
        
        fake_max_degree_list=maxes(self.monitor_free, key=lambda mynode: self.fake_degree[mynode])                                                #added
        best_node_list=maxes(fake_max_degree_list, key=lambda mynode: self.graph.degree(mynode))                                                        #added


        if len(best_node_list) >= 1:
            next_monitor = best_node_list.pop()
        else:
            print "There's an error somewhere or we have a disconnected graph"

        self.monitor_set.add(next_monitor)
        self.monitor_free.remove(next_monitor)
        return next_monitor