import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import json
graphdic={}

numRuns=5

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
#Alg1
    infile=open(graphdic[graph]+'alg1_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    alg1_mon_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg1_node_percent_ over'+str(numRuns)+' Runs', 'r')
    alg1_node_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg1_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    alg1_edge_percent=json.load(infile)
    infile.close()
#Alg1c1
    infile=open(graphdic[graph]+'alg1c1_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    alg1c1_mon_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg1c1_node_percent_ over'+str(numRuns)+' Runs', 'r')
    alg1c1_node_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg1c1_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    alg1c1_edge_percent=json.load(infile)
    infile.close()
#Alg1c2
    infile=open(graphdic[graph]+'alg1c2_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    alg1c2_mon_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg1c2_node_percent_ over'+str(numRuns)+' Runs', 'r')
    alg1c2_node_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg1c2_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    alg1c2_edge_percent=json.load(infile)
    infile.close()
#Alg1c12L
    infile=open(graphdic[graph]+'alg1c12L_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    alg1c12L_mon_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg1c12L_node_percent_ over'+str(numRuns)+' Runs', 'r')
    alg1c12L_node_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg1c12L_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    alg1c12L_edge_percent=json.load(infile)
    infile.close()
#RPD
    infile=open(graphdic[graph]+'_RPD_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    RPD_mon_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'_RPD_node_percent_ over'+str(numRuns)+' Runs', 'r')
    RPD_node_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'_RPD_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    RPD_edge_percent=json.load(infile)
    infile.close()
#RPS
    infile=open(graphdic[graph]+'_RPS_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    RPS_mon_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'_RPS_node_percent_ over'+str(numRuns)+' Runs', 'r')
    RPS_node_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'_RPS_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    RPS_edge_percent=json.load(infile)
    infile.close()
#RW
    infile=open(graphdic[graph]+'_RW_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    RW_mon_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'_RW_node_percent_ over'+str(numRuns)+' Runs', 'r')
    RW_node_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'_RW_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    RW_edge_percent=json.load(infile)
    infile.close()
#RWS
    infile=open(graphdic[graph]+'_RWS_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    RWS_mon_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'_RWS_node_percent_ over'+str(numRuns)+' Runs', 'r')
    RWS_node_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'_RWS_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    RWS_edge_percent=json.load(infile)
    infile.close()
#ideal
    infile=open(graphdic[graph]+'ideal_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    ideal_mon_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'ideal_node_percent_ over'+str(numRuns)+' Runs', 'r')
    ideal_node_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'ideal_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    ideal_edge_percent=json.load(infile)
    infile.close()

    fig = plt.figure()
    fig.suptitle('Average % of nodes discovered')
    ax = fig.add_subplot(111)
    ax.set_xlabel('% node monitors')
    ax.set_ylabel('% nodes discovered')
    ax.axis([0,50,-30,30])

    ax.plot(RW_mon_percent, [alg1_node_percent[x]-RW_node_percent[x] for x in range(len(RW_node_percent))],'o', label='Alg1')
    ax.plot(RW_mon_percent, [alg1c1_node_percent[x]-RW_node_percent[x] for x in range(len(RW_node_percent))],'^', label='Alg1c1')
    ax.plot(RW_mon_percent, [alg1c2_node_percent[x]-RW_node_percent[x] for x in range(len(RW_node_percent))],'8', label='Alg1c2')
    ax.plot(RW_mon_percent, [algc12L_node_percent[x]-RW_node_percent[x] for x in range(len(RW_node_percent))],'s', label='Alg1c12L')
    ax.plot(RW_mon_percent, [RPD_node_percent[x]-RW_node_percent[x] for x in range(len(RW_node_percent))],'p', label='RPD')
    ax.plot(RW_mon_percent, [RPS_node_percent[x]-RW_node_percent[x] for x in range(len(RW_node_percent))],'*', label='RPS')

    ax.plot(RW_mon_percent, [RWS_node_percent[x]-RW_node_percent[x] for x in range(len(RW_node_percent))],'h', label='RWS')
    ax.plot(RW_mon_percent, [ideal_node_percent[x]-RW_node_percent[x] for x in range(len(RW_node_percent))],'+', label='ideal')

    plt.legend(loc='best', fontsize=10)
    plt.grid(True)
    #plt.show()
    plt.savefig(graphdic[graph]+'_AllInOne_nodes_over_5_Runs.png')
    plt.close()

    fig = plt.figure()
    fig.suptitle('Average % of edges discovered')
    ax = fig.add_subplot(111)
    ax.set_xlabel('% node monitors')
    ax.set_ylabel('% edges discovered')
    ax.axis([0,50,-30,30])

    ax.plot(alg1_mon_percent, [alg1_edge_percent[x]-RW_edge_percent[x] for x in range(len(alg1_edge_percent))],'o', label='Alg1')
    ax.plot(alg1c1_mon_percent, [alg1c1_edge_percent[x]-RW_edge_percent[x] for x in range(len(alg1_edge_percent))],'^', label='Alg1c1')
    ax.plot(alg1c2_mon_percent, [alg1c2_edge_percent[x]-RW_edge_percent[x] for x in range(len(alg1_edge_percent))],'8', label='Alg1c2')
    ax.plot(alg1c12L_mon_percent, [alg1c12L_edge_percent[x]-RW_edge_percent[x] for x in range(len(alg1_edge_percent))],'s', label='Alg1c12L')
    ax.plot(RPD_mon_percent, [RPD_edge_percent[x]-RW_edge_percent[x] for x in range(len(alg1_edge_percent))],'p', label='RPD')
    ax.plot(RPS_mon_percent, [RPS_edge_percent[x]-RW_edge_percent[x] for x in range(len(alg1_edge_percent))],'*', label='RPS')

    ax.plot(RWS_mon_percent, [RWS_edge_percent[x]-RW_edge_percent[x] for x in range(len(alg1_edge_percent))],'h', label='RWS')
    ax.plot(ideal_mon_percent, [ideal_edge_percent[x]-RW_edge_percent[x] for x in range(len(alg1_edge_percent))],'+', label='ideal')

    plt.legend(loc='best', fontsize=10)
    plt.grid(True)
    #plt.show()
    plt.savefig(graphdic[graph]+'_AllInOne_edges_over_5_Runs.png')
    plt.close()
