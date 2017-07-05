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

# Note: If we continue to use the "seen" list in an intentional manner, with sorting required
# Work to reimplement using "SortedListWithKeys" from the "sortedcontainers" package
# This can be found at: http://grantjenks.com/docs/sortedcontainers/
# Then implement the "seen" list using 3-tuples: (degree, seen, label) with 'key=lambda item:[2]'
# This package is not already install on sage-cloud, so would need to be added or imported for us.


#if you get an error about this line when you try to run,
#go to the package manager and install networkx
import networkx as nx
import numpy as np
import sys
#import copy #We need a deepcopy if the self.graph gets modified.

#Algorithm: Highest Global Degree - Least Seen
#
# Pick start is random, without replacement
#
# Place next:
#       Choose highest degree node seen, w/o a monitor
#       If multiple highest degree, pick least seen


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
        self.graph = graph
        np.random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.next_highest = {}
        self.seen = Counter()
        #self.no_new=0
    
    #public method. Returns true if we have place all the monitors
    #we have available to us, else returns false
    def stop(self, allotment):
        #This should be obsolete now.
        if allotment > self.graph.number_of_nodes():
            print("Error, cannot have more than", self.graph.number_of_nodes(), "monitors!")
            sys.exit(1)

        if len(self.monitor_set) < allotment:
            return False
        else:
            return True

    #public method. Picks a random node that hasn't been a monitor yet.
    #returns the node number
    def pick_start(self):
        #Add for "restart" not seen
        start_node = np.random.choice([x for x in self.graph.nodes() if x not in self.monitor_set])
        self.monitor_set.add(start_node)
        return start_node

    #public method. adds all edges (in NetworkX adding an edge adds the nodes if not already there)
    #from the node to all of its neighbors
    def add_neighbors(self, node):
        #Have to add self, incase I have no neighbors.
        self.result_graph.add_node(node)
        
        neighbors = self.graph.neighbors(node) #this was changed for new code
        
        #new_nodes=false
        
        #When we add the neighbors of a new node, set the seen count to 'inf'
        try:
            self.seen[node]='inf'
        except:
            print("Node (monitor) wasn't in neighbor list")
        
        for neighbor in neighbors:
            self.result_graph.add_edge(node, neighbor)
            #if self.seen[neighbor]==0:
            #    new_nodes=true
            if self.seen[neighbor] != 'inf':
                self.seen[neighbor]+=1
                self.seen['Total']+=1
                
        #if not new_nodes:
        #    self.no_new+=1
        #else:
        #    self.no_new=0
        #
            
    #private method. checks whether there are
    #any nodes associated with a given degree.
    #if not, deletes that degree-key
    def _empty_check(self, key):
        if not self.next_highest[key]:
            self.next_highest.pop(key)
    
    
    def place_next_monitor(self, node, prob):
        next_monitor=None
        #if self.no_new==2:
        #    next_monitor=self.pick_start()
        #else:
        
        #Generate a list of seen nodes
        seen_list=list(self.seen.keys())
        seen_list.remove('Total')
        seen_list=[testnode for testnode in seen_list if (self.seen[testnode] > 0 and self.seen[testnode] !='inf')]
        
        #Pick the highest degree seen node, or the highest, least seen
        if len(seen_list)>0:
            max_degree_list=maxes(seen_list, key=lambda mynode: self.graph.degree(mynode))
            if len(max_degree_list)>0:
                best_node_list=maxes(max_degree_list, key=lambda mynode: self.seen[mynode])
                
        
                if len(best_node_list) >= 1:
                #    next_monitor=random.choice(best_node_list)
                    next_monitor = best_node_list.pop()
        
                
        if next_monitor==None:
            print("There's an error somewhere or we have a disconnected graph. Picking next randomly")
            #print "Picking next monitor randomly"
            next_monitor=self.pick_start()
            
        self.monitor_set.add(next_monitor)
        return next_monitor