#Erik Rye, Nick Juliano
import networkx as nx
import math
import high_neighbor_degree_condition1
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
    alg1monitors, alg1nodes, alg1edges = [],[],[]
    for i in range(numRuns):
        print "Starting {}/{} for {}".format(i+1,numRuns,graphdic[graph])
        mo, no, ed = [],[],[]
        HNDc = high_neighbor_degree_condition1.HND(graph,i)
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
            if tally>=math.log(graph.number_of_nodes()):
                HNDc.add_neighbors(monitor)
                monitor, tally = HNDc.pick_start(tally)
            if len(HNDc.monitor_set) in l:
                mo.append(len(HNDc.monitor_set))
                no.append(HNDc.result_graph.number_of_nodes())
                ed.append(HNDc.result_graph.number_of_edges())
                l.remove(len(HNDc.monitor_set))
        alg1monitors.append(mo)
        alg1nodes.append(no)
        alg1edges.append(ed)
        print "{}: {}/{} runs complete".format(graphdic[graph], i+1,numRuns)

    alg1_mon_tuples = zip(*alg1monitors)
    alg1_node_tuples = zip(*alg1nodes)
    alg1_edge_tuples = zip(*alg1edges)

    alg1_avg_mon = [np.mean(x) for x in alg1_mon_tuples]
    alg1_avg_nodes = [np.mean(x) for x in alg1_node_tuples]
    alg1_avg_edges = [np.mean(x) for x in alg1_edge_tuples]

    alg1_mon_percent = [float(x)/original_num_nodes * 100 for x in alg1_avg_mon]
    alg1_node_percent = [float(x)/original_num_nodes * 100 for x in alg1_avg_nodes]
    alg1_edge_percent = [float(x)/original_num_edges * 100 for x in alg1_avg_edges]

    outfile=open(graphdic[graph]+'alg1c1_mon_percent_ over'+str(numRuns)+' Runs', 'w')
    json.dump(alg1_mon_percent, outfile)
    outfile.close()
    outfile=open(graphdic[graph]+'alg1c1_node_percent_ over'+str(numRuns)+' Runs', 'w')
    json.dump(alg1_node_percent, outfile)
    outfile.close()
    outfile=open(graphdic[graph]+'alg1c1_edge_percent_ over'+str(numRuns)+' Runs', 'w')
    json.dump(alg1_edge_percent, outfile)
    outfile.close()
