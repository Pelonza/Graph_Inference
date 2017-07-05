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
import numpy as np
import sys

#Algorithm: Fake-Degree Discovery (FDD)
#
# Pick Start: Random node, not in monitor set
#
# Place Next:
#   Max Fake Degree, followed by max real degree
#
# Updates by removing edges of monitor nodes
# Fake degree is the number of unseen neighbors

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

class Alg():
    def __init__(self, graph, sd):
        #We need a deepcopy if the self.graph gets modified.
        self.graph = graph.copy() 
        np.random.seed()
        self.result_graph = nx.Graph()
        
        #Sets with/without monitors.
        self.monitor_set = set()
        self.monitor_free=nx.nodes(self.graph) #Save this list to speed computations.
        
        #Internal dictionaries
        self.next_highest = {}
        self.seen = Counter()
                        
        #Initialize all fake degrees to degree
        self.fake_degree=dict()
        #for node in self.monitor_free:
        for node in nx.nodes(self.graph):
            self.fake_degree[node]=self.graph.degree(node)

    #public method. Returns true if we have placed all the monitors
    #we have available to us, else returns false
    def stop(self, allotment):
        #May be obsolete.
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
        start_node = np.random.choice([x for x in self.graph.nodes() if x not in self.monitor_set])
        self.monitor_set.add(start_node)
        self.monitor_free.remove(start_node)
        print("start_node: " +  start_node)
        return start_node

    #public method. adds all edges (in NetworkX adding an edge adds the nodes if not already there)
    #from the node to all of its neighbors
    def add_neighbors(self, node):
        '''
        if('B' in node[0]):
            print("Blue Node: " + node)
        else:
            print("Red Node: " + node)
        '''
        #Have to add self, incase I have no neighbors.
        self.result_graph.add_node(node)
        
        neighbors = self.graph.neighbors(node)

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
            #Fake degree is the number of neighbors unseen.
            tmp_len=len([x for x in self.graph.neighbors(node_to_update) if self.seen[x]>0])
            self.fake_degree[node_to_update]=self.graph.degree(node_to_update)-tmp_len

    #private method. checks whether there are
    #any nodes associated with a given degree.
    #if not, deletes that degree-key
    def _empty_check(self, key):
        if not self.next_highest[key]:
            self.next_highest.pop(key)


    def place_next_monitor(self, node, prob):
        br_node = 0.0
        best_node_list = []
        #print("Next Monitor: " + node)

        #for iy in G.neighbors(ix)

        
        #Get the list of seen nodes, without monitors
        seen_list=self.seen.keys()
        seen_list.remove('Total')
        seen_list=[testnode for testnode in seen_list if (self.seen[testnode] > 0 and self.seen[testnode] !='inf') ]
        
        comp_node_list = []
        node_list = self.graph.neighbors(node)
    
        for n in self.graph.neighbors(node):
            if n in seen_list:
                if('R' in n[0]):
                    br_node = (float(int(n.split('_')[1]) + int(n.split('_')[2]) + int(n.split('_')[3])) * float(n.split('_')[11]))
                    comp_node_list.append(br_node)
                else:
                    #br_node = 0.0
                    br_node = (float(int(n.split('_')[1]) + int(n.split('_')[2]) + int(n.split('_')[3]) + int(n.split('_')[4]) + int(n.split('_')[5]) + int(n.split('_')[6]) + int(n.split('_')[7]) + int(n.split('_')[8]) + int(n.split('_')[9]) + int(n.split('_')[10])) * float(n.split('_')[11]))
                    comp_node_list.append(br_node)
            else:
                br_node = -1
                comp_node_list.append(br_node)

        #Get the node(s) with the highest fake-degree, and then the highest degree.
        if not comp_node_list:
            fake_max_degree_list=maxes(seen_list, key=lambda mynode: self.fake_degree[mynode])                                       #added
            best_node_list=maxes(fake_max_degree_list, key=lambda mynode: self.graph.degree(mynode))                                                        #added
        else:
            #change this. 
            if(max(comp_node_list) == -1):
                fake_max_degree_list=maxes(seen_list, key=lambda mynode: self.fake_degree[mynode])                                       #added
                best_node_list=maxes(fake_max_degree_list, key=lambda mynode: self.graph.degree(mynode))   
            else:
                red_node = node_list[comp_node_list.index(max(comp_node_list))]
                best_node_list.append(red_node)
        #test_fake_max_degree_list=maxes(self.monitor_free, key=lambda mynode: self.fake_degree[mynode])
        
        #Test FDD vs. UBDn
        #if fake_max_degree_list==test_fake_max_degree_list:
        #    print "Lists are same"
        #else:
        #    print "Lists are different"

        #Pop the first 'best' node for the next monitor
        
        if len(best_node_list) >= 1:
            next_monitor = best_node_list.pop()
        else:
            print "There's an error somewhere or we have a disconnected graph"

        self.monitor_set.add(next_monitor)
        
        
        try:
            self.monitor_free.remove(next_monitor)
        except:
            print("Cannot place new monitor: " + next_monitor)
            
        if('B' in next_monitor[0]):
            print("Blue Node: " + next_monitor)
        else:
            print("Red Node: " + next_monitor)
        

        return next_monitor
