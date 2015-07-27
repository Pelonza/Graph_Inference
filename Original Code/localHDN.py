import sys, random
import networkx as nx


class localHDN():
    def __init__(self,graph,i):
        self.monitor_set = set()
        self.g = graph #This saves the copy of the graph we are searching. 
        self.g_i = nx.Graph() # Creates a graph structure that is "empty"
        random.seed(i)

    #chooses node at random    
    def start(self):
        node = random.choice(self.g.nodes())
        self.g_i.add_node(node)
        neighbors = self.g.neighbors(node)
        for n in neighbors:
            self.g_i.add_edge(n, node)
        self.monitor_set.add(node)

    #finds the neigbor node with the highest degree    
    def get_highest(self):
        highest_degree= max([self.g_i.degree(x) for x in self.g_i.nodes() if x
            not in self.monitor_set])
        highest_nodes = [y for y in self.g_i.nodes() if (self.g_i.degree(y)
            == highest_degree and y not in self.monitor_set)]
        #if the highest degree is found print this
        if highest_nodes:
            next_mon = random.choice(highest_nodes)
        #continues to search for highest degree node until it is found    
        else:
            print "had to get a new one"
            next_mon = random.choice([z for z in self.g.nodes() if z not in
                self.monitor_set])
            print "Next monitor is:", next_mon
        self.monitor_set.add(next_mon)
        return next_mon

    #finds all of the neighbor edges and highlights them
    #makes a list
    def add_edges(self,node):
        neighbors = self.g.neighbors(node)
        for n in neighbors:
            self.g_i.add_edge(n, node)

    def go(self):
        m = self.get_highest()
        self.add_edges(m)

    def main(self,stop):
        self.start()
        for i in range(stop):
            self.go()

##################
#main#############

#Prints graph in Gephi

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print "Usage: " + sys.argv[0] + " graph.gexf + stop_num"
        sys.exit()

    else:
        g = nx.read_gexf(sys.argv[1], node_type=int)
        #stop_num=sys.argv[2]
        infer = localHDN(g)
        infer.main(stop_num)
