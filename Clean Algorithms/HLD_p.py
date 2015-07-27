'''
Created by Karl Schmitt, Nicholas Juliano, Brittany Reynolds, Erin Moore, Ralucca Gera, and Erik
Original Created on Jan 25, 2015
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

###################
#if you get an error about this line when you try to run,
#go to the package manager and install networkx
import networkx as nx
import sys
import numpy as np
#import copy  #We need a deepcopy if the self.graph gets modified.

class Alg():
    '''
    Algorithm: Highest-Local Degree with Restart (HLD_p)
        Old Algorithm: Modified Alg 3

    IMPORTANT NOTE: This might not be working as thought...

    Current Algorithm Behavior:

        Pick Start: pick random, non-monitor node

        Place Next:
            Examine neighbors without monitors.
            Pick highest degree neighbor without monitor
            
            If no neighbors w/o monitors exist, teleport to a node without a monitor
                Note: This is supposed to then pick highest degree seen??

    '''

    def __init__(self, graph, sd):
        #We need a deepcopy if the self.graph gets modified.
        #self.graph = copy.deepcopy(graph)
        self.graph=graph
        
        np.random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.next_highest = {}

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
            self.result_graph.add_edge(node, neighbor)  ###we will need if/else commands here
  
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
    
    #public method. Iterates through all neighbors, and creates a list (neighbor_list)
    #of the neighbors w/highest degree. 
    def place_next_monitor(self, node, prob):
    
        neighbors = self.graph.neighbors(node)
       
        #Get the list of neighbors that don't have monitors yet.
        neighbor_set = set(neighbors) - self.monitor_set
        
        max_degree=0
        neighbor_list=[]
        
        for neighbor in neighbor_set:

            degree = self.graph.degree(neighbor)
            
            #maintain a dict of nodes we've seen and their degrees
            #Commented out because at last runs, did not have. Appears to be needed though!
            #See the "Else" below. Otherwise we teleport...
            
            #if degree not in self.next_highest.keys() and neighbor not in self.monitor_set:
            #    self.next_highest[degree] = set([neighbor])           
            #elif neighbor not in self.monitor_set:
            #    self.next_highest[degree].add(neighbor)                            

            if degree > max_degree:
                neighbor_list = []
                max_degree = degree
                neighbor_list.append(neighbor)
            elif degree == max_degree:
                neighbor_list.append(neighbor)
      
        #If the set is non-empty, we meet this condition and pick a next vertex
        if len(neighbor_list)>0:
            next_monitor = np.random.choice(neighbor_list)
               
        else:
            # ---------------------------
            # NEED TO CHECK CODE COVERAGE HERE.
            # I THINK THIS MOSTLY DOESN'T HAPPEN/WORK RIGHT.
            # JUST DOES pick_start() -- K
            #----------------------------            
            
            #generate a random value between 0 and 1
            magic_number = np.random.uniform(0,1)
            
            #Only algorithm 2 is prob = 1, algorithm 1 is prob = 0
            if prob >= magic_number:     
                #print "Using algorithm 2 for next monitor"
                
                #If the set is non-empty, we meet this condition and pick a next vertex
                
                #Get list of degrees seen
                sorted_degrees = self.next_highest.keys()
                
                #If we are out of node's we've seen (i.e. sorted_degree empty)
                if not self.next_highest.keys():
                    #Pick a random start node without a monitor
                    next_monitor = self.pick_start()
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
        
