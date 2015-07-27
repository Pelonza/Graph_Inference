import sys, random
import networkx as nx

class localLDN():
    def __init__(self,graph,i):
        self.monitor_set = set()
        self.g = graph 
        self.g_i = nx.Graph()
        random.seed(i)

#chooses node at random
    def start(self):
        node = random.choice(self.g.nodes())
        self.g_i.add_node(node)
        neighbors = self.g.neighbors(node)
        for n in neighbors:
            self.g_i.add_edge(n, node)
        self.monitor_set.add(node)

    #finds the neighbor node with the lowest degree    
    def get_lowest(self):
        lowest_degree= min([self.g_i.degree(x) for x in self.g_i.nodes() if x
            not in self.monitor_set])
        lowest_nodes = [y for y in self.g_i.nodes() if (self.g_i.degree(y)
            == lowest_degree and y not in self.monitor_set)]
        #if the lowest degree is found print this
        if lowest_nodes:
            next_mon = random.choice(lowest_nodes)
        #continues to search for lowest degree node until it is found
        else:
            print "had to get a new one"
            next_mon = random.choice([z for z in self.g.nodes() if z not in
                self.monitor_set])
            print "Next monitor is:", next_mon
        self.monitor_set.add(next_mon)
        return next_mon

    #finds all the neighbor edges and highlights them
    #in a list
    def add_edges(self,node):
        neighbors = self.g.neighbors(node)
        for n in neighbors:
            self.g_i.add_edge(n, node)

    def go(self):
        m = self.get_lowest()
        self.add_edges(m)

    def main(self,stop):
        self.start()
        for i in range(stop):
            self.go()

##################
#main#############

#Produces graph in Gephi
if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print "Usage: " + sys.argv[0] + " graph.gexf + stop_num"
        sys.exit()

    else:
        g = nx.read_gexf(sys.argv[1], node_type=int)
        infer = localLDN(g)
        infer.main(int(sys.argv[2]))
        print infer.g_i.number_of_nodes()
