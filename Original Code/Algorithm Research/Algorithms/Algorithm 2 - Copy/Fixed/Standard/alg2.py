#Eric Rye, Nick Juliano
import networkx as nx
import alg2_helper
import sys
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
    alg2monitors, alg2nodes, alg2edges = [],[],[]
    for i in range(numRuns):
        print "Starting {}/50".format(i)
        mo, no, ed, co = [],[],[],[]
        alg2 = alg2_helper.alg2(graph,i)
        monitor = alg2.pick_start()
        l=range(50,stop,50)
        while not alg2.stop(stop):
            alg2.add_neighbors(monitor)
            monitor = alg2.place_next_monitor(monitor)
            print len(alg2.monitor_set)
            if len(alg2.monitor_set) in l:
                mo.append(len(alg2.monitor_set))
                no.append(alg2.result_graph.number_of_nodes())
                ed.append(alg2.result_graph.number_of_edges())
                co.append(nx.number_connected_components(alg2.result_graph))
                l.remove(len(alg2.monitor_set))
        alg2monitors.append(mo)
        alg2nodes.append(no)
        alg2edges.append(ed)
        print "{}: {}/50 runs complete".format(graphdic[graph], i+1)

    alg2_mon_tuples = zip(*alg2monitors)
    alg2_node_tuples = zip(*alg2nodes)
    alg2_edge_tuples = zip(*alg2edges)

    alg2_avg_mon = [np.mean(x) for x in alg2_mon_tuples]
    alg2_avg_nodes = [np.mean(x) for x in alg2_node_tuples]
    alg2_avg_edges = [np.mean(x) for x in alg2_edge_tuples]

    alg2_mon_percent = [float(x)/original_num_nodes * 100 for x in alg2_avg_mon]
    alg2_node_percent = [float(x)/original_num_nodes * 100 for x in alg2_avg_nodes]
    alg2_edge_percent = [float(x)/original_num_edges * 100 for x in alg2_avg_edges]

    outfile=open(graphdic[graph]+'alg2_mon_percent_ over'+str(numRuns)+' Runs', 'w')
    json.dump(alg2_mon_percent, outfile)
    outfile.close()
    outfile=open(graphdic[graph]+'alg2_node_percent_ over'+str(numRuns)+' Runs', 'w')
    json.dump(alg2_node_percent, outfile)
    outfile.close()
    outfile=open(graphdic[graph]+'alg2_edge_percent_ over'+str(numRuns)+' Runs', 'w')
    json.dump(alg2_edge_percent, outfile)
    outfile.close()
