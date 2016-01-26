#Erik Rye, Nick Juliano
import networkx as nx
import high_neighbor_degree_condition2L_alg2
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
        print "Starting {}/{} for {}".format(i+1,numRuns,graphdic[graph])
        mo, no, ed= [],[],[]
        HNDc = high_neighbor_degree_condition2L_alg2.HND(graph,i)
        tally=0
        monitor, tally = HNDc.pick_start(tally)
        l=range(50,stop,50)
        while not HNDc.stop(stop):
            HNDc.add_neighbors(monitor)
            monitor, tally = HNDc.place_next_monitor(monitor,tally)
            if len(HNDc.monitor_set) in l:
                mo.append(len(HNDc.monitor_set))
                no.append(HNDc.result_graph.number_of_nodes())
                ed.append(HNDc.result_graph.number_of_edges())
                l.remove(len(HNDc.monitor_set))
        alg2monitors.append(mo)
        alg2nodes.append(no)
        alg2edges.append(ed)
        print "{}: {}/{} runs complete".format(graphdic[graph], i+1,numRuns)

    alg2_mon_tuples = zip(*alg2monitors)
    alg2_node_tuples = zip(*alg2nodes)
    alg2_edge_tuples = zip(*alg2edges)

    alg2_avg_mon = [np.mean(x) for x in alg2_mon_tuples]
    alg2_avg_nodes = [np.mean(x) for x in alg2_node_tuples]
    alg2_avg_edges = [np.mean(x) for x in alg2_edge_tuples]

    alg2_mon_percent = [float(x)/original_num_nodes * 100 for x in alg2_avg_mon]
    alg2_node_percent = [float(x)/original_num_nodes * 100 for x in alg2_avg_nodes]
    alg2_edge_percent = [float(x)/original_num_edges * 100 for x in alg2_avg_edges]

    outfile=open(graphdic[graph]+'alg2c2_mon_percent_ over'+str(numRuns)+' Runs', 'w')
    json.dump(alg2_mon_percent, outfile)
    outfile.close()
    outfile=open(graphdic[graph]+'alg2c2_node_percent_ over'+str(numRuns)+' Runs', 'w')
    json.dump(alg2_node_percent, outfile)
    outfile.close()
    outfile=open(graphdic[graph]+'alg2c2_edge_percent_ over'+str(numRuns)+' Runs', 'w')
    json.dump(alg2_edge_percent, outfile)
    outfile.close()
