'''
Title of Program
    XXXX.py
    
CSXXXX


Created on Jan 20, 2015

@author: Erik Rye
'''
import matplotlib.pyplot as plt
import networkx as nx
import randomwalk
import sys
import numpy as np
#graph_path = sys.argv[1]
#estimate = sys.argv[2]

#file to write stats to
stats = open('walk.stats.dat', 'w')

#reads the graph in gephi gephi gephi
graph = nx.read_gexf("/users/erik/desktop/MA4404/ba.gexf", node_type=int)

stop = graph.number_of_nodes()/2 + 50
original_num_nodes = graph.number_of_nodes()
original_num_edges = graph.number_of_edges()
original_clustering = nx.average_clustering(graph)
original_components = nx.number_connected_components(graph)
original_avg_deg = float(2*original_num_edges)/original_num_nodes

overall_monitors, overall_nodes, overall_edges, overall_components = [],[],[],[]
for i in range(0,50):
    monitors, nodes, edges, components = [],[],[], []
    for number_of_monitors in range(50,stop,50):
        #instantiates an instance of the graph inference class
        #random seed is the second number
        yut = randomwalk.RW(graph, i)
        monitor = yut.pick_start()
        while not yut.stop(number_of_monitors):
#prints everything found thus far            yut.add_neighbors(monitor)
#prints everything found thus far            monitor = yut.place_next_monitor(monitor)
#prints everything found thus far
        print "\n***************************************"

        print "Original Graph Statistics"
        print "Number of nodes:", original_num_nodes
        print "Number of edges:", original_num_edges 
        print "Number of connected components:", original_components
        print "Average degree:", original_avg_deg
        
        print "\n***************************************"

        print "Inferred Graph Statistics:"
        print "Number of monitors used:", len(yut.monitor_set)
        print "Found", yut.result_graph.number_of_nodes(), "nodes"
        print "Found", yut.result_graph.number_of_edges(), "edges"

        monitors.append(len(yut.monitor_set))
        nodes.append(yut.result_graph.number_of_nodes())
        edges.append(yut.result_graph.number_of_edges())
        components.append(nx.number_connected_components(yut.result_graph))

    overall_monitors.append(monitors)
    overall_nodes.append(nodes)
    overall_edges.append(edges)
    overall_components.append(components)

#zip function compiles into list
monitor_tuples = zip(*overall_monitors)
node_tuples = zip(*overall_nodes)
edge_tuples = zip(*overall_edges)
component_tuples = zip(*overall_components)

average_monitors = [np.mean(x) for x in monitor_tuples]
average_nodes = [np.mean(x) for x in node_tuples]
average_edges = [np.mean(x) for x in edge_tuples]
average_components = [np.mean(x) for x in component_tuples]

stats.write('Algorithm 1 Average:\n')

#calculate percentages from values
mon_percent = [float(x)/original_num_nodes * 100 for x in average_monitors]
node_percent = [float(x)/original_num_nodes * 100 for x in average_nodes]
edge_percent = [float(x)/original_num_edges * 100 for x in average_edges]

stats.write('Average % nodes: ' + str(node_percent[-1]) + '\n')
stats.write('Average % edges: ' + str(edge_percent[-1]) + '\n')
stats.write('Average # components: ' + str(average_components[-1]) + '\n')

#Sets specifications for graph
#nodes
fig = plt.figure()
fig.suptitle('Average % of nodes discovered')
ax = fig.add_subplot(111)
ax.set_xlabel('% node monitors')
ax.set_ylabel('% nodes discovered')
ax.axis([0,50,0,100])
ax.plot(mon_percent, node_percent, 'bs')
plt.grid(True)
plt.savefig('randomwalk_nodes.pdf')
plt.show()

#sets specifications for graph
#edges
fig = plt.figure()
fig.suptitle('Average % of edges discovered')
ax = fig.add_subplot(111)
ax.set_xlabel('% node monitors')
ax.set_ylabel('% edges discovered')
ax.axis([0,50,0,100])
ax.plot(mon_percent,edge_percent, 'bs')
plt.grid(True)
plt.savefig('randomwalk_edges.pdf')
plt.show()
