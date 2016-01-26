import matplotlib.pyplot as plt
import matplotlib.colors as colors
import networkx as nx
import numpy as np
import json
graphdic={}
numRuns=50

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
    if graphdic[graph]!='General Relativity':
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
#Alg3 p=0.25
    infile=open(graphdic[graph]+'alg3_p=0.25_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    alg3_mon_percent_p25=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg3_p=0.25_node_percent_ over'+str(numRuns)+' Runs', 'r')
    alg3_node_percent_p25=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg3_p=0.25_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    alg3_edge_percent_p25=json.load(infile)
    infile.close()
#Alg3 p=0.5
    infile=open(graphdic[graph]+'alg3_p=0.5_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    alg3_mon_percent_p5=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg3_p=0.5_node_percent_ over'+str(numRuns)+' Runs', 'r')
    alg3_node_percent_p5=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg3_p=0.5_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    alg3_edge_percent_p5=json.load(infile)
    infile.close()
#Alg3 p=0.75
    infile=open(graphdic[graph]+'alg3_p=0.75_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    alg3_mon_percent_p75=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg3_p=0.75_node_percent_ over'+str(numRuns)+' Runs', 'r')
    alg3_node_percent_p75=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg3_p=0.75_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    alg3_edge_percent_p75=json.load(infile)
    infile.close()
#Alg2
    infile=open(graphdic[graph]+'alg2_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    alg2_mon_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg2_node_percent_ over'+str(numRuns)+' Runs', 'r')
    alg2_node_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg2_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    alg2_edge_percent=json.load(infile)
    infile.close()
#Alg2c1
    infile=open(graphdic[graph]+'alg2c1_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    alg2c1_mon_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg2c1_node_percent_ over'+str(numRuns)+' Runs', 'r')
    alg2c1_node_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg2c1_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    alg2c1_edge_percent=json.load(infile)
    infile.close()
#Alg2c2
    infile=open(graphdic[graph]+'alg2c2_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    alg2c2_mon_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg2c2_node_percent_ over'+str(numRuns)+' Runs', 'r')
    alg2c2_node_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg2c2_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    alg2c2_edge_percent=json.load(infile)
    infile.close()
#Alg2c12L
    infile=open(graphdic[graph]+'alg2c12L_mon_percent_ over'+str(numRuns)+' Runs', 'r')
    alg2c12L_mon_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg2c12L_node_percent_ over'+str(numRuns)+' Runs', 'r')
    alg2c12L_node_percent=json.load(infile)
    infile.close()
    infile=open(graphdic[graph]+'alg2c12L_edge_percent_ over'+str(numRuns)+' Runs', 'r')
    alg2c12L_edge_percent=json.load(infile)
    infile.close()
#########################
    fig = plt.figure()
    fig.suptitle('Average % of nodes discovered')
    ax = fig.add_subplot(111)
    ax.set_xlabel('% node monitors')
    ax.set_ylabel('% nodes discovered')
    ax.axis([0,50,0,100])

    ax.plot(ideal_mon_percent, ideal_node_percent,'black', label='Ideal')

    ax.plot(alg1_mon_percent, alg1_node_percent,'red',label='Alg1')
    ax.plot(alg1c1_mon_percent, alg1c1_node_percent,'darkred',linestyle='-.',label='Alg1c1')
    ax.plot(alg1c2_mon_percent, alg1c2_node_percent,'firebrick',linestyle='--', label='Alg1c2')
    ax.plot(alg1c12L_mon_percent, alg1c12L_node_percent,'orange', label='Alg1c12L')

    ax.plot(alg2_mon_percent, alg2_node_percent,'green',label='Alg2')
    ax.plot(alg2c1_mon_percent, alg2c1_node_percent,'lime',linestyle='-.',label='Alg2c1')
    ax.plot(alg2c2_mon_percent, alg2c2_node_percent,'olive',linestyle='--', label='Alg2c2')
    ax.plot(alg2c12L_mon_percent, alg2c12L_node_percent,'yellowgreen',label='Alg2c12L')

    ax.plot(alg3_mon_percent_p25, alg3_node_percent_p25,'mediumblue', label='Alg3 p=0.25')
    ax.plot(alg3_mon_percent_p5, alg3_node_percent_p5,'darkblue',linestyle='-.', label='Alg3 p=0.50')
    ax.plot(alg3_mon_percent_p75, alg3_node_percent_p75,'lightseagreen',linestyle='--', label='Alg3 p=0.75')

    if graphdic[graph]!='General Relativity':
        ax.plot(RW_mon_percent, RW_node_percent,'fuchsia',linestyle='--', label='RW')
    ax.plot(RWS_mon_percent, RWS_node_percent,'plum', label='RWS')
    ax.plot(RPD_mon_percent, RPD_node_percent,'mediumvioletred', label='RPD')
    ax.plot(RPS_mon_percent, RPS_node_percent,'magenta',linestyle='-.', label='RPS')

    plt.legend(loc=4, fontsize=7)
    plt.grid(True)
    plt.savefig(graphdic[graph]+'_AllInOne+others_nodes_over_50_Runs.png')
    plt.close()

    fig = plt.figure()
    fig.suptitle('Average % of edges discovered')
    ax = fig.add_subplot(111)
    ax.set_xlabel('% node monitors')
    ax.set_ylabel('% edges discovered')
    ax.axis([0,50,0,100])

    ax.plot(ideal_mon_percent, ideal_edge_percent,'black', label='Ideal')

    ax.plot(alg1_mon_percent, alg1_edge_percent,'red', label='Alg1')
    ax.plot(alg1c1_mon_percent, alg1c1_edge_percent,'darkred',linestyle='-.', label='Alg1c1')
    ax.plot(alg1c2_mon_percent, alg1c2_edge_percent,'firebrick',linestyle='--', label='Alg1c2')
    ax.plot(alg1c12L_mon_percent, alg1c12L_edge_percent,'orange',label='Alg1c12L')

    ax.plot(alg2_mon_percent, alg2_edge_percent,'green',label='Alg2')
    ax.plot(alg2c1_mon_percent, alg2c1_edge_percent,'lime',linestyle='-.',label='Alg2c1')
    ax.plot(alg2c2_mon_percent, alg2c2_edge_percent,'olive',linestyle='--', label='Alg2c2')
    ax.plot(alg2c12L_mon_percent, alg2c12L_edge_percent,'yellowgreen', label='Alg2c12L')

    ax.plot(alg3_mon_percent_p25, alg3_edge_percent_p25,'mediumblue', label='Alg3 p=0.25')
    ax.plot(alg3_mon_percent_p5, alg3_edge_percent_p5,linestyle='-.',color='darkblue', label='Alg3 p=0.5')
    ax.plot(alg3_mon_percent_p75, alg3_edge_percent_p75,linestyle='--',color='lightseagreen', label='Alg3 p=0.75')

    if graphdic[graph]!='General Relativity':
        ax.plot(RW_mon_percent, RW_edge_percent,'fuchsia',linestyle='--', label='RW')
    ax.plot(RWS_mon_percent, RWS_edge_percent,'plum',label='RWS')
    ax.plot(RPD_mon_percent, RPD_edge_percent, color='mediumvioletred',label='RPD')
    ax.plot(RPS_mon_percent, RPS_edge_percent,linestyle='-.',color= 'magenta',label='RPS')

    plt.legend(loc=4, fontsize=7)
    plt.grid(True)
    plt.savefig(graphdic[graph]+'_AllInOne+Others_edges_over_50_Runs.png')
    plt.close()
