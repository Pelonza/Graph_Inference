# Note: If we continue to use the "seen" list in an intentional manner, with sorting required
# Work to reimplement using "SortedListWithKeys" from the "sortedcontainers" package
# This can be found at: http://grantjenks.com/docs/sortedcontainers/
# Then implement the "seen" list using 3-tuples: (degree, seen, label) with 'key=lambda item:[2]'
# This package is not already install on sage-cloud, so would need to be added or imported for us.


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
        self.no_new=0
    
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
        
        new_nodes=False
        
        #When we add the neighbors of a new node, set the seen count to 'inf'
        try:
            self.seen[node]='inf'
        except:
            print "Node (monitor) wasn't in neighbor list"
        
#        print "Neighbors of", node, ":", neighbors
        for neighbor in neighbors:
            self.result_graph.add_edge(node, neighbor) ###we will need if/else commands here
            if self.seen[neighbor]==0:
                new_nodes=True
            if self.seen[neighbor] != 'inf':
                self.seen[neighbor]+=1
                self.seen['Total']+=1
                
        #print self.seen
        if new_nodes:
            self.no_new=0
        else:
            self.no_new+=1
            #print "Didn't add any new nodes"
            
    #private method. checks whether there are
    #any nodes associated with a given degree.
    #if not, deletes that degree-key
    def _empty_check(self, key):
        if not self.next_highest[key]:
            self.next_highest.pop(key)

    def place_next_monitor(self, node, prob):
        if self.no_new>=2:
            #Investigate different number of rounds without adding newly seen neighbors
            #Investigate resetting the "no_new" count, when you jump 
            #self.now_new=0
            #print "Randomly Jumping, no new nodes added twice"
            next_monitor=self.pick_start()
        else:
            seen_list=self.seen.keys()
            seen_list.remove('Total')
            seen_list=[testnode for testnode in seen_list if self.seen[testnode] != 'inf']

            max_degree_list=maxes(seen_list, key=lambda mynode: self.graph.degree(mynode))
            best_node_list=maxes(max_degree_list, key=lambda mynode: self.seen[mynode])

            #Check if list is non-empty, otherwise restart.
            if len(best_node_list) >= 1:
                next_monitor = best_node_list.pop()
            #If no monitors in list, pick new start.
            else:
                print "Ran out of nodes to place monitors on. Pick new start."
                next_monitor=pick_start()
            
        self.monitor_set.add(next_monitor)
        #print "Next monitor", next_monitor  
        return next_monitor