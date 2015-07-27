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
#
# If you try to index into a dictionary, and index doesn't exist, then you get an error...

class alg():
    def __init__(self, graph, sd):
        self.graph = graph
        random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()
        self.next_highest = {}
        self.seen = Counter()
        
        #Initialize all fake degrees to degree
        self.fake_degree=dict()
        for node in nx.nodes(self.graph):
            self.fake_degree[node]=self.graph.degree(node)
            
        
    #public method. Returns true if we have placed all the monitors
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
        not_seen=[x for x in nx.nodes(self.graph) if self.seen[x]==0]
        start_node = max(not_seen, key=lambda mynode: self.graph.degree(mynode) )                                                            #added                                                             #added
        #best_node_list=maxes(max_degree_list, key=lambda mynode: self.seen[mynode])                                                             #added
        self.monitor_set.add(start_node)
        self.result_graph.add_node(start_node)
        #print "First Monitor", start_node
        return start_node

    #public method. adds all edges (in NetworkX adding an edge adds the nodes if not already there)
    #from the node to all of its neighbors
    def add_neighbors(self, node):
        neighbors = self.graph.neighbors(node) #this was changed for new code

        fake_update_set=set(neighbors) #Set of unique nodes that need to have their fake degrees updated, seeded with neighbors
        fake_update_set.add(node) #Add self to list to update
        #new_nodes=false

        #When we add the neighbors of a new node, set the seen count to 'inf'
        try:
            self.seen[node]='inf'
        except:
            print "Node (monitor) wasn't in neighbor list"

        for neighbor in neighbors:
            #Add edge between monitor (node) and it's neighbor to found graph
            self.result_graph.add_edge(node, neighbor)
            
            #Add unique neighbors of neighbor to update list
            fake_update_set |=set(self.graph.neighbors(neighbor))
            
            #Update the seen count for each neighbor. We can use this to make new fake-degree also.
            if self.seen[neighbor] != 'inf':
                self.seen[neighbor]+=1
                self.seen['Total']+=1

        #Update the fake-degrees
        for node_to_update in fake_update_set:
            self.fake_degree[node_to_update]=self.graph.degree(node_to_update)-len([x for x in self.graph.neighbors(node_to_update) if self.seen[x]>0])

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

        #nx.set_node_attributes(self.graph,'seen',bb)                                                                                           #added
        #nodes_unseen_neigh=[myneigh for myneigh in node.neighbors if myneigh[seen]==1]                                                         #added
        #fake_degree=len(nodes_unseen_neigh)                                                                                                    #added

        fake_max_degree_list=maxes(seen_list, key=lambda mynode: self.fake_degree[mynode])                                                #added
        best_node_list=maxes(fake_max_degree_list, key=lambda mynode: self.seen[mynode])                                                        #added


        if len(best_node_list) >= 1:
            next_monitor = best_node_list.pop()
        else:
            print "There's an error somewhere or we have a disconnected graph"

        self.monitor_set.add(next_monitor)
        return next_monitor
        #else:
            #continue

    #public method. Iterates through all neighbors, and creates a list (neighbor_list)
    #of the neighbors w/highest degree.

    def place_next_monitor2(self, node, prob):
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

        #take the set difference between the max-degree neighbors we just found
        #and the set of all nodes that have previously been monitors
        neighbor_set = set(neighbor_list) - self.monitor_set

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