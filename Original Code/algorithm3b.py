'''
Created on Jan 25, 2015

@author: erik
'''
###################
#if you get an error about this line when you try to run,
#go to the package manager and install networkx
import networkx as nx
import random, sys

class alg3():
    def __init__(self, graph, sd):
        self.graph = graph
        random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.next_highest = {}

    #public method. Picks a random node that hasn't been a monitor yet.
    #returns the node number
    def pick_start(self):
        start_node = random.choice([x for x in self.graph.nodes() if x not in self.monitor_set])
        self.monitor_set.add(start_node)
        self.result_graph.add_node(start_node)
        return start_node
    
    #public method. adds all edges (in NetworkX adding an edge adds the nodes if not alread there)
    #from the node to all of its neighbors
    def add_neighbors(self, node):
        neighbors = self.graph.neighbors(node)
#        print "Neighbors of", node, ":", neighbors
        for neighbor in neighbors:
            self.result_graph.add_edge(node, neighbor)  ###we will need if/else commands here
  
    #private method. checks whether there are
    #any nodes associated with a given degree.
    #if not, deletes that degree-key
    def _empty_check(self, key):
        if not self.next_highest[key]:
            self.next_highest.pop(key)
    
    #public method. Iterates through all neighbors, and creates a list (neighbor_list)
    #of the neighbors w/highest degree. 
    def place_next_monitor(self, node, prob):
        neighbors = self.graph.neighbors(node)
        max_degree, neighbor_list = 0, []

        #take the set difference between the max-degree neighbors we just found
        #and the set of all nodes that have previously been monitors
        neighbor_set = set(neighbors) - self.monitor_set
        
        for neighbor in neighbor_set:
            degree = self.graph.degree(neighbor)
            #maintain a dict of nodes we've seen and 
            #their degrees
            if degree not in self.next_highest.keys() and neighbor not in self.monitor_set:
                self.next_highest[degree] = set([neighbor])
            
            elif neighbor not in self.monitor_set:
                self.next_highest[degree].add(neighbor)

            if degree > max_degree and neighbor not in self.monitor_set:
                neighbor_list = []
                max_degree = degree
                neighbor_list.append(neighbor)
            elif degree == max_degree and len(neighbor_list) >= 1 and neighbor not in self.monitor_set:
                neighbor_list.append(neighbor)
            elif degree > max_degree:
                neighbor_list = []
                max_degree = degree
            else:
                continue

        
        if neighbor_set:
            next_monitor = neighbor_set.pop()
            self.next_highest[max_degree].remove(next_monitor)   
            self._empty_check(max_degree)
       
        else:
            #generate a random value between 0 and 1
            magic_number = random.uniform(0,1)
            #Algorithm 2 is prob = 1, Algorithm 1 is prob = 0
            if prob >= magic_number:     
                #print "Using algorithm 2 for next monitor"
                #If the set is non-empty, we meet this condition and pick a next vertex
                sorted_degrees = self.next_highest.keys()
                if not sorted_degrees:
                    next_monitor = self.pick_start()
                else:
                    sorted_degrees.sort(reverse=True)
                    high_degree = sorted_degrees[0]
                    next_monitor = self.next_highest[high_degree].pop()
                    self._empty_check(high_degree)
            
            else:
                #print "Using algorithm 1 for next monitor"
                next_monitor = self.pick_start()
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
        if allotment > self.graph.number_of_nodes():
            #print "Error, cannot have more than", self.graph.number_of_nodes(), "monitors!"
            sys.exit(1)

        if len(self.monitor_set) < allotment:
            return False
        else:
            return True
        
