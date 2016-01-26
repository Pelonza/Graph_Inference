#Eric Rye, Nick Juliano

#This will create plots for every graph you select "True" to.  You can select multiple graphs at the same time.  It will plot them on separate graphs.
#Only change the "True"'s and the "numRuns"

#You can change the name of the plots that are saved on lines 129 and 142.
#You can have the plots show as they finish by unblocking lines 128 and 141.

import matplotlib.pyplot as plt
import networkx as nx
import RandomPlacementDumb
import high_neighbor_degree_fixed
import sys,time
import numpy as np
graphdic={}


#This variable controls how many runs the plot is averaged over:
numRuns = 1

if True:
    ERgraph = nx.read_gexf("ER_random-1.gexf", node_type=int)
    graphdic[ERgraph] = 'Erdos-Renyi'
if True:
    BAgraph = nx.read_gexf("barabasi.gexf", node_type=int)
    graphdic[BAgraph]='Barabassi-Albert'
if True:
    FBgraph = nx.read_gexf("facebook_combined.gexf", node_type=int)
    graphdic[FBgraph]='Facebook'
if True:
    GRgraph = nx.read_gexf("General_Relativity.gexf", node_type=int)
    graphdic[GRgraph]='General Relativity'


for graph in graphdic.keys():
    print graphdic[graph] + ": start"
    stop = graph.number_of_nodes()/2 + 50
    original_num_nodes = graph.number_of_nodes()
    original_num_edges = graph.number_of_edges()
    original_clustering = nx.average_clustering(graph)
    original_components = nx.number_connected_components(graph)
    original_avg_deg = float(2*original_num_edges)/original_num_nodes
    
    overall_monitors, overall_nodes, overall_edges, overall_components = [],[],[],[]
    alg1monitors, alg1nodes, alg1edges, alg1components = [],[],[],[]
    
    for i in range(numRuns):
        print "Starting {}/{}".format(i+1,numRuns)
        monitors, nodes, edges, components = [],[],[], []
        yut = RandomPlacementDumb.RP(graph, i)
        monitor = yut.pick_start()
        l=range(50,stop,50)
        while not yut.stop(stop):
            yut.add_neighbors(monitor)
            monitor = yut.pick_start()
            if len(yut.monitor_set) in l:
                monitors.append(len(yut.monitor_set))
                nodes.append(yut.result_graph.number_of_nodes())
                edges.append(yut.result_graph.number_of_edges())
                components.append(nx.number_connected_components(yut.result_graph))
                l.remove(len(yut.monitor_set))

        mo, no, ed, co = [],[],[],[]
        alg1 = high_neighbor_degree_fixed.HND(graph,i)
        monitor = alg1.pick_start()
        l=range(50,stop,50)
        while not alg1.stop(stop):
            alg1.add_neighbors(monitor)
            monitor = alg1.place_next_monitor(monitor)
            if len(alg1.monitor_set) in l:
                mo.append(len(alg1.monitor_set))
                no.append(alg1.result_graph.number_of_nodes())
                ed.append(alg1.result_graph.number_of_edges())
                co.append(nx.number_connected_components(alg1.result_graph))
                l.remove(len(alg1.monitor_set))


        overall_monitors.append(monitors)
        overall_nodes.append(nodes)
        overall_edges.append(edges)
        overall_components.append(components)
        alg1monitors.append(mo)
        alg1nodes.append(no)
        alg1edges.append(ed)
        alg1components.append(co)
        print "{}: {}/{} runs complete".format(graphdic[graph], i+1,numRuns)

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

    fig = plt.figure()
    fig.suptitle('Average % of nodes discovered')
    ax = fig.add_subplot(111)
    ax.set_xlabel('% node monitors')
    ax.set_ylabel('% nodes discovered')
    ax.axis([0,50,0,100])
    ax.plot(mon_percent, node_percent, 'g^',label="RPD")
    ax.plot(alg1_mon_percent, alg1_node_percent, 'bs', label='p=0')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True)
    #plt.show()
    plt.savefig(graphdic[graph]+'_alg1fixed_RPD_nodes_over'+str(numRuns)+'Runs.pdf')

    fig = plt.figure()
    fig.suptitle('Average % of edges discovered')
    ax = fig.add_subplot(111)
    ax.set_xlabel('% node monitors')
    ax.set_ylabel('% edges discovered')
    ax.axis([0,50,0,100])
    ax.plot(mon_percent,edge_percent, 'g^',label="RDS")
    ax.plot(alg1_mon_percent,alg1_edge_percent, 'bs', label='p=0')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True)
    #plt.show()
    plt.savefig(graphdic[graph]+'_alg1fixed_RPD_edges_over'+str(numRuns)+'Runs.pdf')
    print graphdic[graph] + ": complete"

