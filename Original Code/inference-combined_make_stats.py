'''
Title of Program
    XXXX.py
    
CSXXXX


Created on Jan 20, 2015

@author: Erik Rye
'''

import numpy as np
import algorithm3
import networkx as nx
import matplotlib.pyplot as plt
import sys
import time

#file to write stats to
stats = open('statistics.dat', 'w')

#reads the graph in, adjust for desired graph on your machine
graph = nx.read_gexf("C:\\Users\\Ralu\\Desktop\\2015\\ba-1.gexf", node_type=int)

#This tells Python we want to stop at the interval of 50 after 
#half of the nodes have been used as monitors
stop = graph.number_of_nodes()/2 + 50
original_num_nodes = graph.number_of_nodes()
original_num_edges = graph.number_of_edges()
original_avg_deg = float(2*original_num_edges)/original_num_nodes

mon_dict,node_dict,edge_dict = {},{},{}

#adjust desired probabilities here
# .25, .5, 75 would be range(1,4), for example
for prob in range(1,4):
    prob /= float(4)
    print "\n#################################"
    print "Begininng probability p = ", prob
    print "#################################"
    time.sleep(2)
    overall_monitors, overall_nodes, overall_edges, overall_components = [],[],[],[]
    
    #change the second number for # of iterations
    for i in range(0,1):
        print "Beginning round: ", i
        time.sleep(2)
        monitors, nodes, edges, components = [],[],[],[]
        for number_of_monitors in range(50,stop,50):
            yut = algorithm3.alg3(graph, i)
            monitor = yut.pick_start()
            while not yut.stop(number_of_monitors):
                yut.add_neighbors(monitor)
                monitor = yut.place_next_monitor(monitor, prob)

            print "\n***************************************"
            print "Original Graph Statistics"
            print "Number of nodes:", original_num_nodes
            print "Number of edges:", original_num_edges 
            print "Average degree:", original_avg_deg
            print "\n***************************************"
            print "Inferred Graph Statistics:"
            print "Number of monitors used:", len(yut.monitor_set)
            print "Found", yut.result_graph.number_of_nodes(), "nodes"
            print "Found", yut.result_graph.number_of_edges(), "edges"
            print "Found", float(yut.result_graph.number_of_nodes())/graph.number_of_nodes() * 100, "percent of the nodes"
            print "Found", float(yut.result_graph.number_of_edges())/graph.number_of_edges() * 100, "percent of the edges"
            print "Found", nx.number_connected_components(yut.result_graph)


            monitors.append(len(yut.monitor_set))
            nodes.append(yut.result_graph.number_of_nodes())
            edges.append(yut.result_graph.number_of_edges())
            components.append(nx.number_connected_components(yut.result_graph))

        overall_monitors.append(monitors)
        overall_nodes.append(nodes)
        overall_edges.append(edges)
        overall_components.append(components)

        #write the last iteration graph at the max number of monitors once per p
        nx.write_gexf(yut.result_graph,
                "C:\\Users\\Ralu\\Desktop\\2015\\inferred_graph"+str(prob) + ".gexf")

    monitor_tuples = zip(*overall_monitors)
    node_tuples = zip(*overall_nodes)
    edge_tuples = zip(*overall_edges)
    component_tuples = zip(*overall_components)
   
    average_monitors = [np.mean(x) for x in monitor_tuples]
    average_nodes = [np.mean(x) for x in node_tuples]
    average_edges = [np.mean(x) for x in edge_tuples]
    average_components = [np.mean(x) for x in component_tuples]

    mon_percent = [float(x)/original_num_nodes * 100 for x in average_monitors]
    node_percent = [float(x)/original_num_nodes * 100 for x in average_nodes]
    edge_percent = [float(x)/original_num_edges * 100 for x in average_edges]

    stats.write("Prob = " + str(prob) + '\n')
    stats.write("Average percent of nodes found = " + str(node_percent[-1]) + '\n')
    stats.write("Average percent of edges found = " + str(edge_percent[-1]) + '\n')
    stats.write("Average components found = " + str(average_components[-1]) + '\n')

    mon_dict[prob] = mon_percent
    node_dict[prob] = node_percent 
    edge_dict[prob] = edge_percent 

    



stats.close()
#points may need to be modified if more than 9 lines need to go on 1 plot
points = ['-bs', '-gH', '-kD', '-ro', '-y*', '-cv', '-rd', '-bp', '-rx']
fig = plt.figure()
fig.suptitle('Average % of nodes discovered')
ax = fig.add_subplot(111)
ax.set_xlabel('% node monitors')
ax.set_ylabel('% nodes discovered')
ax.axis([0,50,0,100])
i = 0
for k in node_dict.keys():
    ax.plot(mon_dict[k], node_dict[k],points[i],label='p =' + str(k))
    i += 1
plt.legend(loc=4, fontsize=10)
plt.grid(True)
plt.savefig('nodes.pdf')
plt.show()

fig = plt.figure()
fig.suptitle('Average % of edges discovered')
ax = fig.add_subplot(111)
ax.set_xlabel('% node monitors')
ax.set_ylabel('% edges discovered')
ax.axis([0,50,0,100])
i = 0
for k in node_dict.keys():
    ax.plot(mon_dict[k], edge_dict[k],points[i],label='p =' + str(k))
    i += 1
plt.legend(loc=4, fontsize=10)
plt.grid(True)
plt.savefig('edges.pdf')
plt.show()
