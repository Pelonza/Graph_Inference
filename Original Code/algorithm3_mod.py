# Note: If we continue to use the "seen" list in an intentional manner, with sorting required
# Work to reimplement using "SortedListWithKeys" from the "sortedcontainers" package
# This can be found at: http://grantjenks.com/docs/sortedcontainers/
# Then implement the "seen" list using 3-tuples: (degree, seen, label) with 'key=lambda item:[2]'
# This package is not already install on sage-cloud, so would need to be added or imported for us.


#if you get an error about this line when you try to run,
#go to the package manager and install networkx
import networkx as nx
import random, sys
#import collections



class Counter(dict):
    def __missing__(self,key):
        return 0



class alg3():
    def __init__(self, graph, sd):
        self.graph = graph
        random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.next_highest = {}
        self.seen = Counter()
    
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
        start_node = random.choice([x for x in self.graph.nodes() if x not in self.monitor_set])
        self.monitor_set.add(start_node)
        self.result_graph.add_node(start_node)
        #print "First Monitor", start_node
        return start_node

    #public method. adds all edges (in NetworkX adding an edge adds the nodes if not already there)
    #from the node to all of its neighbors
    def add_neighbors(self, node):
        neighbors = self.graph.neighbors(node) #this was changed for new code
        #When we add the neighbors of a new node, set the seen count to 'inf'
        try:
            self.seen[node]='inf'
        except:
            print "Node (monitor) wasn't in neighbor list"
        
#        print "Neighbors of", node, ":", neighbors
        for neighbor in neighbors:
            self.result_graph.add_edge(node, neighbor) ###we will need if/else commands here
            if self.seen[neighbor] != 'inf':
                self.seen[neighbor]+=1
                self.seen['Total']+=1
                
        #print self.seen
    
    #private method. checks whether there are
    #any nodes associated with a given degree.
    #if not, deletes that degree-key
    def _empty_check(self, key):
        if not self.next_highest[key]:
            self.next_highest.pop(key)

    def place_next_monitor2(self):
        seen_list=self.seen.keys()
        seen_list.remove('Total')
        seen_list=[testnode for testnode in seen_list if self.seen[testnode] != 'inf']
        seen_list.sort(key=lambda mynode: self.graph.degree(mynode), reverse=True)
        max_degree=self.graph.degree(seen_list[0])
        
        #print "Sorted(?) outlist", seen_list
        #print "Degrees", self.graph.degree(seen_list)
        #print max_degree
                
        max_degree_list= [testnode for testnode in seen_list if self.graph.degree(testnode) == max_degree]
        max_degree_list.sort(key=lambda mynode: self.seen.get(mynode))
        
        #print max_degree_list
        
        best_node=self.seen.get(max_degree_list[0]) #Best in terms of least seen, and max degree
        best_node_list=[testnode for testnode in max_degree_list if self.seen.get(testnode) == best_node]
        
        #print best_node_list
        
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

    def place_next_monitor(self, node, prob):
        neighbors = self.graph.neighbors(node)
        max_degree, neighbor_list = 0, []
        for neighbor in neighbors:
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