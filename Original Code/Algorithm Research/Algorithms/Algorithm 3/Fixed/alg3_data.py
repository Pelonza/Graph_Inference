#Eric Rye, Nick Juliano

#This will create plots for every graph you select "True" to.  You can select multiple graphs at the same time.  It will plot them on separate graphs.
#Only change the "True"'s and the "numRuns"

#You can change the name of the plots that are saved on lines 129 and 142.
#You can have the plots show as they finish by unblocking lines 128 and 141.

import matplotlib.pyplot as plt
import networkx as nx
import alg3_fix_unscrewup
import json
import numpy as np
graphdic={}


#This variable controls how many runs the plot is averaged over:
numRuns = 50

if False:
    ERgraph = nx.read_gexf("ER_random-1.gexf", node_type=int)
    graphdic[ERgraph] = 'Erdos-Renyi'
if False:
    BAgraph = nx.read_gexf("barabasi.gexf", node_type=int)
    graphdic[BAgraph]='Barabassi-Albert'
if True:
    FBgraph = nx.read_gexf("facebook_combined.gexf", node_type=int)
    graphdic[FBgraph]='Facebook'
if False:
    GRgraph = nx.read_gexf("General_Relativity.gexf", node_type=int)
    graphdic[GRgraph]='General Relativity'

for probability in [.5,.75]:
    for graph in graphdic.keys():
        print graphdic[graph] + ": start, p="+str(probability)
        stop = graph.number_of_nodes()/2 + 50
        original_num_nodes = graph.number_of_nodes()
        original_num_edges = graph.number_of_edges()
        alg3monitors, alg3nodes, alg3edges, alg3components = [],[],[],[]
        for i in range(numRuns):
            mo, no, ed = [],[],[]
            for num_monitors in range(50,stop,50):
                alg3 = alg3_fix_unscrewup.alg3(graph,i)
                monitor = alg3.pick_start()
                while not alg3.stop(num_monitors):
                    alg3.add_neighbors(monitor)
                    monitor = alg3.place_next_monitor(monitor,probability)

                mo.append(len(alg3.monitor_set))
                no.append(alg3.result_graph.number_of_nodes())
                ed.append(alg3.result_graph.number_of_edges())

            alg3monitors.append(mo)
            alg3nodes.append(no)
            alg3edges.append(ed)
            print "{}: {}/50 runs complete, @ p={}".format(graphdic[graph], i+1,probability)

        alg3_mon_tuples = zip(*alg3monitors)
        alg3_node_tuples = zip(*alg3nodes)
        alg3_edge_tuples = zip(*alg3edges)

        alg3_avg_mon = [np.mean(x) for x in alg3_mon_tuples]
        alg3_avg_nodes = [np.mean(x) for x in alg3_node_tuples]
        alg3_avg_edges = [np.mean(x) for x in alg3_edge_tuples]

        alg3_mon_percent = [float(x)/original_num_nodes * 100 for x in alg3_avg_mon]
        alg3_node_percent = [float(x)/original_num_nodes * 100 for x in alg3_avg_nodes]
        alg3_edge_percent = [float(x)/original_num_edges * 100 for x in alg3_avg_edges]

        outfile=open(graphdic[graph]+'alg3_p='+str(probability)+'_mon_percent_ over'+str(numRuns)+' Runs', 'w')
        json.dump(alg3_mon_percent, outfile)
        outfile.close()
        outfile=open(graphdic[graph]+'alg3_p='+str(probability)+'_node_percent_ over'+str(numRuns)+' Runs', 'w')
        json.dump(alg3_node_percent, outfile)
        outfile.close()
        outfile=open(graphdic[graph]+'alg3_p='+str(probability)+'_edge_percent_ over'+str(numRuns)+' Runs', 'w')
        json.dump(alg3_edge_percent, outfile)
        outfile.close()
