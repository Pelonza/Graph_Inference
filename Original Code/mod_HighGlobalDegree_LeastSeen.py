

#This is the same code as HighGlobalDegree_LeastSeen.  The only difference between the two
#is that this can run undirected AND directed graphs.


#if you get an error about this line when you try to run,
#go to the package manager and install networkx
import networkx as nx
import random, sys, operator
#import collections


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



class alg():
    def __init__(self, graph, sd):
        self.graph = graph
        random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.next_highest = {}
        self.seen = Counter()
        #self.no_new=0
    
    #public method. Returns true if we have place all the monitors
    #we have available to us, else returns false
    def stop(self, allotment):
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
        start_node = random.choice([x for x in self.graph.nodes() if x not in self.monitor_set])
        self.monitor_set.add(start_node)
        self.result_graph.add_node(start_node)
        #print "First Monitor", start_node
        return start_node

    #public method. adds all edges (in NetworkX adding an edge adds the nodes if not already there)
    #from the node to all of its neighbors
    def add_neighbors(self, node):
        neighbors = self.graph.neighbors(node) #this was changed for new code
        
        #new_nodes=false
        
        #When we add the neighbors of a new node, set the seen count to 'inf'
        try:
            self.seen[node]='inf'
        except:
            print "Node (monitor) wasn't in neighbor list"
        
#        print "Neighbors of", node, ":", neighbors
        for neighbor in neighbors:
            self.result_graph.add_edge(node, neighbor) ###we will need if/else commands here
            #if self.seen[neighbor]==0:
            #    new_nodes=true
            if self.seen[neighbor] != 'inf':
                self.seen[neighbor]+=1
                self.seen['Total']+=1
                
        #print self.seen
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
        #if self.no_new==2:
        #    next_monitor=self.pick_start()
        #else:
        
        seen_list=self.seen.keys()
        seen_list.remove('Total')
        seen_list=[testnode for testnode in seen_list if self.seen[testnode] != 'inf']
        
        max_degree_list=maxes(seen_list, key=lambda mynode: len(self.graph.neighbors(mynode)))
        best_node_list=maxes(max_degree_list, key=lambda mynode: self.seen[mynode])
        #len .neighbor 

        
        if len(best_node_list) >= 1:
        #    next_monitor=random.choice(best_node_list)
            next_monitor = best_node_list.pop()
            #self.next_highest[max_degree].remove(next_monitor)   
            #self._empty_check(max_degree)
        else:
            print "There's an error somewhere or we have a disconnected graph"
            
        self.monitor_set.add(next_monitor)
        #print "Next monitor", next_monitor  
        return next_monitor
        
        #else:
            #continue

    #def place_next_monitor(self, node, prob, nick):
        #def place_next_monitor(self, node, prob, nick):


    #public method. Iterates through all neighbors, and creates a list (neighbor_list)
    #of the neighbors w/highest degree.


        #min_seen = float("inf")
        #new_neighbor_list = []
        #for neighbor in neighbor_list:
            #if self.seen[neighbor] < min_seen:
               # new_neighbor_list = []
                # min_seen = self.seen[neighbor]
                #  new_neighbor_list.append(neighbor)
            #elif self.seen[neighbor] == min_seen:
                #new_neighbor_list.append(neighbor)
            #else: continue


        #take the set difference between the max-degree neighbors we just found
        #and the set of all nodes that have previously been monitors
        neighbor_set = set(neighbor_list) - self.monitor_set

#        if neighbor_set != neighbor_list:
#            print "I think there's an error somewhere."
#            print "Neighbor set:", neighbor_set
#            print "Neighbor list:", neighbor_list
#        else:
#            print "We do need that code."

# Implement your own "pick next monitor" process. Based on probabilities or whatever.
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