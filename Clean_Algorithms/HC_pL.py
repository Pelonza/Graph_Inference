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

###################
#if you get an error about this line when you try to run,
#go to the package manager and install networkx
import networkx as nx
import sys
import numpy as np
#import copy #We need a deepcopy if the self.graph gets modified.

#Algorithm: Hill-Climbing (HC)



def maxes(a, key=None):
    ''' Helper function to get list of things with max values.        '''
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

class Alg():
    '''
    Algorithm: Hill-Climbing with Probablistic Restart and Max Walk-Length(HC_pL)
        
    Current Algorithm Behavior:

    Pick-start finds a random, non-monitor node

    Place_Next:
        Check current walk length, if greater than log(nodes in graph), restart
        
        Otherwise:
            Examine neighbors
            If highest degree neighbor doesn't have monitor, pick it 
            Else, check probability
                Based on probability, hill-climb (find highest seen degree)
                

'''

    def __init__(self, graph, sd):
        #We need a deepcopy if the self.graph gets modified.
        #self.graph = copy.deepcopy(graph)
        self.graph=graph
        
        np.random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.next_highest = {}
        self.highseen_key = 0 #maintain the highest seen key.
        
        #Set this now, incase base graph changes
        self.maxwalklen=np.log(graph.number_of_nodes())
        self.walklen=0
        return

    #public method. 
    # Picks a random node that hasn't been a monitor yet.
    # returns the node number
    def pick_start(self):
        start_node = np.random.choice([x for x in self.graph.nodes() if x not in self.monitor_set])
        self.monitor_set.add(start_node)
        self.walklen=0
        return start_node
    
    #public method. 
    # adds all edges from the node to all of its neighbors
    # Note: in NetworkX adding an edge adds the nodes if not alread there
    def add_neighbors(self, node):
        #Have to add self, incase I have no neighbors.
        self.result_graph.add_node(node)
        
        neighbors = self.graph.neighbors(node)
        
        for neighbor in neighbors:
            self.result_graph.add_edge(node, neighbor)
            
            degree=self.graph.degree(neighbor)
            
            #maintain a dict of nodes we've seen and their degrees
            if degree not in self.next_highest.keys() and neighbor not in self.monitor_set:
                #Make a new entry into the dict if degree is unseen before.
                self.next_highest[degree] = set([neighbor])

                #Check if this is a new, highest seen degree.
                if degree>self.highseen_key:
                    self.highseen_key=degree

            elif neighbor not in self.monitor_set:
                #If degree is seen, add neighbor to list
                self.next_highest[degree].add(neighbor)       
                    
        return
  
    #private method. checks whether there are
    #any nodes associated with a given degree.
    #if not, deletes that degree-key
    def _empty_check(self, key):
        if len(self.next_highest[key])==0:
            self.next_highest.pop(key)
            
            #Check the highest seen key tracker, if needed update.
            if key==self.highseen_key and self.next_highest.keys():
                self.highseen_key=max(self.next_highest.keys())
            else:
                self.highseen_key=0
        return
                
    
    #public method. Iterates through all neighbors, and creates a list (neighbor_list)
    #of the neighbors w/highest degree. 
    def place_next_monitor(self, node, prob):
        
        if self.walklen>self.maxwalklen:
            #Check if max-walklen exceed, if so, teleport/restart
            next_monitor=self.pick_start()
        
        else:
            #Continue with Hill-Climbing
        
        
            neighbors = self.graph.neighbors(node)               

            #Set-up finding the max-degree neighbors.
            #If 'next_highest' moved to add_neighbors, consider calling maxes instead
            max_degree=0
            neighbor_list=[]

            for neighbor in neighbors:

                degree = self.graph.degree(neighbor)

                #Make a list of the maximum degree neighbors of current node
                #We could acomplish this with the maxes function from other code.
                if degree > max_degree:
                    neighbor_list = []
                    max_degree = degree
                    neighbor_list.append(neighbor)
                elif degree == max_degree:
                    neighbor_list.append(neighbor)

#            #Test code for simpler computation of finding max-neighbors
#            #Usings maxes naively causes a problem in graphs with degree 0 nodes.
#            #Needs to be encompassed in a "try" statement so as not to error out.
#            try:
#                neighbor_list2=maxes(neighbors, key=lambda mynode:self.graph.degree(mynode))
#            except:
#                print "Neigh: ",neighbors, " node: ",node
#                
#
#            if neighbor_list2==neighbor_list:
#                print "Same max neigh list"
#            else:
#                print "Not same max neigh list"

            #take the set difference between the max-degree neighbors we just found
            #and the set of all nodes that have previously been monitors
            neighbor_set = set(neighbor_list) - self.monitor_set

            #If the set is non-empty, we meet this condition and pick a next vertex
            if len(neighbor_set)>0:
                #Pop the next vertex from the set. Then update our seen structure.
                next_monitor = neighbor_set.pop()

                #Update the seen structure
                self.next_highest[max_degree].remove(next_monitor)
                self._empty_check(max_degree)

            else:                                
                #generate a random value between 0 and 1
                magic_number = np.random.uniform(0,1)

                #Only algorithm 2 is prob = 1, algorithm 1 is prob = 0
                if prob >= magic_number:     
                    #print "Using algorithm 2 for next monitor"                                                             

                    #If we are out of node's we've seen (i.e. sorted_degree empty)
                    if not self.next_highest.keys():
                        #Pick a random start node without a monitor
                        next_monitor = self.pick_start()
                    else:
                        if self.highseen_key==0:
                            #No high degree current. Pick random start again.
                            print "Picking random new start. No remaining seen"
                            next_monitor=self.pick_start()
                        else:
                            #Take the next highest degree node we've seen.
                            next_monitor = self.next_highest[self.highseen_key].pop()

                            #Get rid of an empty key. 
                            self._empty_check(self.highseen_key)

                else:
                    #print "Using algorithm 1 for next monitor"

                    #Pick a random start node that doesn't already have a monitor
                    next_monitor = self.pick_start()

                    #Check the list we're maintaining of seen nodes, if it's there
                    # remove it.
                    next_monitor_degree = self.graph.degree(next_monitor)
                    try:
                        self.next_highest[next_monitor_degree].remove(next_monitor)
                        self._empty_check(next_monitor_degree)
                    except:
                        pass

        self.monitor_set.add(next_monitor)
        #print "Next monitor", next_monitor  
        return next_monitor
        
    #public method. Returns true if we have place all the monitors
    #we have available to us, else returns false
    def stop(self, allotment):
        #This should be obsolete now and handled in the "main" code. 
        if allotment > self.graph.number_of_nodes():
            #print "Error, cannot have more than", self.graph.number_of_nodes(), "monitors!"
            sys.exit(1)

        if len(self.monitor_set) < allotment:
            return False
        else:
            return True
        
