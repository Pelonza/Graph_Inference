#Eric Rye, Nick Juliano
import networkx as nx
import IdealPlacement_helper
import numpy as np
import json
graphdic={}
numRuns = 50

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
    overall_monitors, overall_nodes, overall_edges  = [],[],[]

    for i in range(numRuns):
        print "Starting {}/{}".format(i+1,numRuns)
        monitors, nodes, edges, components = [],[],[], []
        yut = IdealPlacement_helper.IP(graph, i)
        monitor = yut.pick_start()
        l=range(50,stop,50)
        while not yut.stop(stop):
            yut.add_neighbors(monitor)
            monitor = yut.pick_start()
            if len(yut.monitor_set) in l:
                monitors.append(len(yut.monitor_set))
                nodes.append(yut.result_graph.number_of_nodes())
                edges.append(yut.result_graph.number_of_edges())
                l.remove(len(yut.monitor_set))
        overall_monitors.append(monitors)
        overall_nodes.append(nodes)
        overall_edges.append(edges)
        print "{}: {}/{} runs complete".format(graphdic[graph], i+1,numRuns)

    monitor_tuples = zip(*overall_monitors)
    node_tuples = zip(*overall_nodes)
    edge_tuples = zip(*overall_edges)

    average_monitors = [np.mean(x) for x in monitor_tuples]
    average_nodes = [np.mean(x) for x in node_tuples]
    average_edges = [np.mean(x) for x in edge_tuples]

    mon_percent = [float(x)/original_num_nodes * 100 for x in average_monitors]
    node_percent = [float(x)/original_num_nodes * 100 for x in average_nodes]
    edge_percent = [float(x)/original_num_edges * 100 for x in average_edges]

    outfile=open(graphdic[graph]+'ideal_mon_percent_ over'+str(numRuns)+' Runs', 'w')
    json.dump(mon_percent, outfile)
    outfile.close()
    outfile=open(graphdic[graph]+'ideal_node_percent_ over'+str(numRuns)+' Runs', 'w')
    json.dump(node_percent, outfile)
    outfile.close()
    outfile=open(graphdic[graph]+'ideal_edge_percent_ over'+str(numRuns)+' Runs', 'w')
    json.dump(edge_percent, outfile)
    outfile.close()
