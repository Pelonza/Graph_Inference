import networkx as nx
import random, sys

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


class HND():
    def __init__(self, graph, sd):
        self.graph = graph
        random.seed(sd)
        self.result_graph = nx.Graph()
        self.monitor_set = set()

    def pick_start(self,tally):
        try:
            temp=list(set(self.result_graph.nodes()) - self.monitor_set)
            max_degree_list=maxes(temp, key=lambda mynode: self.graph.degree(mynode))
            start_node = random.choice(max_degree_list)
        except:
            start_node = random.choice([x for x in self.graph.nodes() if x not in self.monitor_set])
        self.monitor_set.add(start_node)
        self.result_graph.add_node(start_node)
        tally=0
        return start_node, tally

    def add_neighbors(self, node):
        neighbors = self.graph.neighbors(node)
        for neighbor in neighbors:
            self.result_graph.add_edge(node, neighbor)

    def place_next_monitor(self, node, tally):
        neighbors = self.graph.neighbors(node)
        max_degree, neighbor_list = 0, []
        neighbor_set = set(neighbors) - self.monitor_set
        if len(neighbor_set)< len(set(neighbors))/2:
            next_monitor, tally = self.pick_start(tally)
            return next_monitor,tally
        for neighbor in neighbor_set:
            degree = self.graph.degree(neighbor)
            if degree > max_degree:
                neighbor_list = []
                max_degree = degree
                neighbor_list.append(neighbor)
            elif degree == max_degree and len(neighbor_list) >= 1:
                neighbor_list.append(neighbor)
            else:
                continue
        if neighbor_set:
            next_monitor = random.choice(neighbor_list)
            self.monitor_set.add(next_monitor)
            tally+=1
        else:
            next_monitor, tally = self.pick_start(tally)
        return next_monitor, tally

    def stop(self, allotment):
        if allotment > self.graph.number_of_nodes():
            sys.exit(1)
        if len(self.monitor_set) < allotment:
            return False
        else:
            return True
