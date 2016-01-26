#Eric Rye, Nick Juliano

#This will create plots for every graph you select "True" to.  You can select multiple graphs at the same time.  It will plot them on separate graphs.
#Only change the "True"'s and the "numRuns"

#You can change the name of the plots that are saved on lines 129 and 142.
#You can have the plots show as they finish by unblocking lines 128 and 141.

import matplotlib.pyplot as plt
import networkx as nx
import RandomPlacementDumb
import RandomPlacementSmart
import randomwalk
import randomwalk_smart
import numpy as np
graphdic={}

#RPD,RPS,RW,RWS
#This variable controls how many runs the plot is averaged over:
numRuns = 5

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

    RPDmonitors, RPDnodes, RPDedges = [],[],[]
    RPSmonitors, RPSnodes, RPSedges,  = [],[],[]
    RWmonitors, RWnodes, RWedges = [],[],[]
    RWSmonitors, RWSnodes, RWSedges,  = [],[],[]

#RandomPlacementDumb
    for i in range(numRuns):
        print "Starting {}/{}".format(i+1,numRuns)
        rpdmonitors, rpdnodes, rpdedges = [],[],[]
        yut = RandomPlacementDumb.RP(graph, i)
        monitor = yut.pick_start()
        l=range(50,stop,50)
        while not yut.stop(stop):
            yut.add_neighbors(monitor)
            monitor = yut.pick_start()
            if len(yut.monitor_set) in l:
                rpdmonitors.append(len(yut.monitor_set))
                rpdnodes.append(yut.result_graph.number_of_nodes())
                rpdedges.append(yut.result_graph.number_of_edges())
                l.remove(len(yut.monitor_set))

#RandomPlacementSmart
    for i in range(numRuns):
        print "Starting {}/{}".format(i+1,numRuns)
        rpsmonitors, rpsnodes, rpsedges = [],[],[]
        yut = RandomPlacementSmart.RP(graph, i)
        monitor = yut.pick_start()
        l=range(50,stop,50)
        while not yut.stop(stop):
            yut.add_neighbors(monitor)
            monitor = yut.pick_start()
            if len(yut.monitor_set) in l:
                rpsmonitors.append(len(yut.monitor_set))
                rpsnodes.append(yut.result_graph.number_of_nodes())
                rpsedges.append(yut.result_graph.number_of_edges())
                l.remove(len(yut.monitor_set))

#RandomWalk
        if graphdic[graph]!='General Relativity':
            rwmonitors, rwnodes, rwedges = [],[], []
            yut = randomwalk.RW(graph, i)
            monitor = yut.pick_start()
            l=range(50,stop,50)
            while not yut.stop(stop):
                yut.add_neighbors(monitor)
                monitor = yut.place_next_monitor(monitor)
                if len(yut.monitor_set) in l:
                    rwmonitors.append(len(yut.monitor_set))
                    rwnodes.append(yut.result_graph.number_of_nodes())
                    rwedges.append(yut.result_graph.number_of_edges())
                    l.remove(len(yut.monitor_set))

#RandomwalkSmart
        rwsmonitors, rwsnodes, rwsedges = [],[], []
        yut = randomwalk_smart.RW(graph, i)
        monitor = yut.pick_start()
        l=range(50,stop,50)
        while not yut.stop(stop):
            yut.add_neighbors(monitor)
            monitor = yut.place_next_monitor(monitor)
            if len(yut.monitor_set) in l:
                rwsmonitors.append(len(yut.monitor_set))
                rwsnodes.append(yut.result_graph.number_of_nodes())
                rwsedges.append(yut.result_graph.number_of_edges())
                l.remove(len(yut.monitor_set))

        RPDmonitors.append(rpdmonitors)
        RPDnodes.append(rpdnodes)
        RPDedges.append(rpdedges)

        RPSmonitors.append(rpsmonitors)
        RPSnodes.append(rpsnodes)
        RPSedges.append(rpsedges)

        RWmonitors.append(rwmonitors)
        RWnodes.append(rwnodes)
        RWedges.append(rwedges)

        RWSmonitors.append(rwsmonitors)
        RWSnodes.append(rwsnodes)
        RWSedges.append(rwsedges)

        print "{}: {}/{} runs complete".format(graphdic[graph], i+1,numRuns)

    RPD_mon_tuples = zip(*RPDmonitors)
    RPD_node_tuples = zip(*RPDnodes)
    RPD_edge_tuples = zip(*RPDedges)

    RPS_mon_tuples = zip(*RPSmonitors)
    RPS_node_tuples = zip(*RPSnodes)
    RPS_edge_tuples = zip(*RPSedges)

    RW_mon_tuples = zip(*RWmonitors)
    RW_node_tuples = zip(*RWnodes)
    RW_edge_tuples = zip(*RWedges)

    RWS_mon_tuples = zip(*RWSmonitors)
    RWS_node_tuples = zip(*RWSnodes)
    RWS_edge_tuples = zip(*RWSedges)

#RPD
    RPDaverage_monitors = [np.mean(x) for x in RPD_mon_tuples]
    RPDaverage_nodes = [np.mean(x) for x in RPD_node_tuples]
    RPDaverage_edges = [np.mean(x) for x in RPD_edge_tuples]
#RPS
    RPSaverage_monitors = [np.mean(x) for x in RPS_mon_tuples]
    RPSaverage_nodes = [np.mean(x) for x in RPS_node_tuples]
    RPSaverage_edges = [np.mean(x) for x in RPS_edge_tuples]
#RW
    RWaverage_monitors = [np.mean(x) for x in RW_mon_tuples]
    RWaverage_nodes = [np.mean(x) for x in RW_node_tuples]
    RWaverage_edges = [np.mean(x) for x in RW_edge_tuples]
#RWS
    RWSaverage_monitors = [np.mean(x) for x in RWS_mon_tuples]
    RWSaverage_nodes = [np.mean(x) for x in RWS_node_tuples]
    RWSaverage_edges = [np.mean(x) for x in RWS_edge_tuples]
#RPD
    RPD_mon_percent = [float(x)/original_num_nodes * 100 for x in RPDaverage_monitors]
    RPD_node_percent = [float(x)/original_num_nodes * 100 for x in RPDaverage_nodes]
    RPD_edge_percent = [float(x)/original_num_edges * 100 for x in RPDaverage_edges]
#RPS
    RPS_mon_percent = [float(x)/original_num_nodes * 100 for x in RPSaverage_monitors]
    RPS_node_percent = [float(x)/original_num_nodes * 100 for x in RPSaverage_nodes]
    RPS_edge_percent = [float(x)/original_num_edges * 100 for x in RPSaverage_edges]
#RW
    if graphdic[graph]!='General Relativity':
        RW_mon_percent = [float(x)/original_num_nodes * 100 for x in RWaverage_monitors]
        RW_node_percent = [float(x)/original_num_nodes * 100 for x in RWaverage_nodes]
        RW_edge_percent = [float(x)/original_num_edges * 100 for x in RWaverage_edges]
#RWS
    RWS_mon_percent = [float(x)/original_num_nodes * 100 for x in RWSaverage_monitors]
    RWS_node_percent = [float(x)/original_num_nodes * 100 for x in RWSaverage_nodes]
    RWS_edge_percent = [float(x)/original_num_edges * 100 for x in RWSaverage_edges]
