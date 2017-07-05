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
import numpy as np

#Modifications by Karl Schmitt, 7/15:
# Moved walk-length check into algorithm code by incorporating self-counter.

#Future Possible Modifications:
# Make the number of neighbors seen to restart a variable.

class Alg():
    '''
    Algorithm: Highest-Local Degree with Restart/Walk-Len/Found (HLD_rLF)

    Current Algorithm Behavior:

        Pick Start: pick random, non-monitor node

        Place Next:
            Restart if half of neighbors have monitors
            OR
            Restart if walk-length > log(number of nodes in graph)
            
            Otherwise:
                Examine neighbors without monitors.
                Pick highest degree neighbor without monitor
            
                If no neighbors w/o monitors exist
                Randomly decide based on parameter if we:
                    Teleport to a node without a monitor
                    Teleport to maximum degree seen node
                    

    '''
    
    def __init__(self, graph, sd):
        self.graph = graph
        np.random.seed(sd)
        
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        
        #Set this now, incase base graph changes
        self.maxwalklen=np.log(graph.number_of_nodes())
        self.walklen=0

        #Set up the dictionary for seen nodes
        self.next_highest = {}
        self.highseen_key=0
        
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
        #if 0:
            #placeholder to keep indenting the same without walk-length
        #    print "This shouldn't happen. Check logic in place next monitor"
        else:
            #If walklength not exceed, pick like normal (high local deg)

            neighbors = self.graph.neighbors(node)
            max_degree, neighbor_list = 0, []

            #Only look at neighbors without monitors for high local deg.
            neighbor_set = set(neighbors) - self.monitor_set

            #Check how many neighbors we have to pick from.
            if len(neighbor_set)< len(neighbors)*0.5:
                #If less than half, teleport
                next_monitor=self.pick_start()                              
            #if 0:
                #Default 'false' to keep code/indentation the same as when checking
                # The condition for neighbots commented out above.
            #    print "This should never occur. Check logic in place next monitor"                        
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
                    self.monitor_set.add(next_monitor) #Note this is here because 'pick_start' already adds the monitor. 
                    self.walklen+=1
                else:
                    #generate a random value between 0 and 1
                    magic_number = np.random.uniform(0,1)

                    if param >= magic_number:     
                        #If we are out of node's we've seen (i.e. sorted_degree empty)
                        if not self.next_highest.keys():
                            #Pick a random start node without a monitor
                            next_monitor = self.pick_start()
                        else:
                            #Take the next highest degree node we've seen.
                            next_monitor = self.next_highest[self.highseen_key].pop()
                            self.monitor_set.add(next_monitor)

                            #Get rid of an empty key. 
                            self._empty_check(self.highseen_key)

                    else:
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
