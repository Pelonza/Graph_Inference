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
import high_neighbor_degree
import sys,time
import numpy as np
#graph_path = sys.argv[1]
#estimate = sys.argv[2]

#file to write stats to
stats = open('walk.stats.dat', 'w')

#reads the graph in
graph = nx.read_gexf("C:\\Users\\Ralu\\Desktop\\2015\\comparingGraphsUsingk-matrixDistribution\\facebook_combined.gexf", node_type=int)

stop = graph.number_of_nodes()/2 + 50
original_num_nodes = graph.number_of_nodes()
original_num_edges = graph.number_of_edges()
original_clustering = nx.average_clustering(graph)
original_components = nx.number_connected_components(graph)
original_avg_deg = float(2*original_num_edges)/original_num_nodes

overall_monitors, overall_nodes, overall_edges, overall_components = [],[],[],[]
alg1monitors, alg1nodes, alg1edges, alg1components = [],[],[],[]
for i in range(0,50):
    monitors, nodes, edges, components = [],[],[], []
    for number_of_monitors in range(50,stop,50):
        #instantiates an instance of the graph inference class
        #random seed is the second number
        yut = randomwalk.RW(graph, i)
        monitor = yut.pick_start()
        while not yut.stop(number_of_monitors):
            yut.add_neighbors(monitor)
            monitor = yut.place_next_monitor(monitor)

        monitors.append(len(yut.monitor_set))
        nodes.append(yut.result_graph.number_of_nodes())
        edges.append(yut.result_graph.number_of_edges())
        components.append(nx.number_connected_components(yut.result_graph))

    mo, no, ed, co = [],[],[],[]
    for num_monitors in range(50,stop,50):
        alg1 = high_neighbor_degree.HND(graph,i)
        monitor = alg1.pick_start()
        while not alg1.stop(num_monitors):
            alg1.add_neighbors(monitor)
            monitor = alg1.place_next_monitor(monitor)

        mo.append(len(alg1.monitor_set))
        no.append(alg1.result_graph.number_of_nodes())
        ed.append(alg1.result_graph.number_of_edges())
        co.append(nx.number_connected_components(alg1.result_graph))


    overall_monitors.append(monitors)
    overall_nodes.append(nodes)
    overall_edges.append(edges)
    overall_components.append(components)
    alg1monitors.append(mo)
    alg1nodes.append(no)
    alg1edges.append(ed)
    alg1components.append(co)

monitor_tuples = zip(*overall_monitors)
node_tuples = zip(*overall_nodes)
edge_tuples = zip(*overall_edges)
component_tuples = zip(*overall_components)

alg1_mon_tuples = zip(*alg1monitors)
alg1_node_tuples = zip(*alg1nodes)
alg1_edge_tuples = zip(*alg1edges)
alg1_component_tuples = zip(*alg1components)


average_monitors = [np.mean(x) for x in monitor_tuples]
average_nodes = [np.mean(x) for x in node_tuples]
average_edges = [np.mean(x) for x in edge_tuples]
average_components = [np.mean(x) for x in component_tuples]
alg1_avg_mon = [np.mean(x) for x in alg1_mon_tuples]
alg1_avg_nodes = [np.mean(x) for x in alg1_node_tuples]
alg1_avg_edges = [np.mean(x) for x in alg1_edge_tuples]
alg1_avg_components = [np.mean(x) for x in alg1_component_tuples]

mon_percent = [float(x)/original_num_nodes * 100 for x in average_monitors]
node_percent = [float(x)/original_num_nodes * 100 for x in average_nodes]
edge_percent = [float(x)/original_num_edges * 100 for x in average_edges]

alg1_mon_percent = [float(x)/original_num_nodes * 100 for x in alg1_avg_mon]
alg1_node_percent = [float(x)/original_num_nodes * 100 for x in alg1_avg_nodes]
alg1_edge_percent = [float(x)/original_num_edges * 100 for x in alg1_avg_edges]
print alg1_mon_percent
print alg1_node_percent

fig = plt.figure()
fig.suptitle('Average % of nodes discovered')
ax = fig.add_subplot(111)
ax.set_xlabel('% node monitors')
ax.set_ylabel('% nodes discovered')
ax.axis([0,50,0,100])
ax.plot(mon_percent, node_percent, 'bs',label="RW")
ax.plot(alg1_mon_percent, alg1_node_percent, 'g^', label='p=0')
plt.legend(loc='best', fontsize=10)
plt.grid(True)
plt.savefig('randomwalk_p0_nodes.pdf')
plt.show()

fig = plt.figure()
fig.suptitle('Average % of edges discovered')
ax = fig.add_subplot(111)
ax.set_xlabel('% node monitors')
ax.set_ylabel('% edges discovered')
ax.axis([0,50,0,100])
ax.plot(mon_percent,edge_percent, 'bs',label="RW")
ax.plot(alg1_mon_percent,alg1_edge_percent, 'g^', label='p=0')
plt.legend(loc='best', fontsize=10)
plt.grid(True)
plt.savefig('randomwalk_p0_edges.pdf')
plt.show()
