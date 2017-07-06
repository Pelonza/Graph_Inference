import matplotlib.pyplot as plt
import json
graphdic={}
numRuns=50
graphdic['sbm']='sbmgraph'
graphdic['ws'] ='wsgraph'


#==============================================================================
# 
# if True:
#     ORgraph = nx.read_gexf("oregon1_010331.gexf", node_type=int)
#     graphdic[ORgraph] = 'Oregon'
# if True:
#     CAgraph = nx.read_gexf("CA-HepPh.gexf", node_type=int)
#     graphdic[CAgraph]='CA-HepPh'
# if True:
#     ENgraph = nx.read_gexf("Enron.gexf", node_type=int)
#     graphdic[ENgraph]='Enron'
# if True:
#     BKgraph = nx.read_gexf("Brightkite.gexf", node_type=int)
#     graphdic[BKgraph]='Brightkite'
# 
#==============================================================================

for graph in graphdic.keys():
#HCp
    infile=open('HC_p_mon_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    alg1_mon_percent=json.load(infile)
    infile.close()
    infile=open('HC_p_node_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    alg1_node_percent=json.load(infile)
    infile.close()
    infile=open('HC_p_edge_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    alg1_edge_percent=json.load(infile)
    infile.close()
#HCpL
    infile=open('HC_pL_mon_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    alg1c1_mon_percent=json.load(infile)
    infile.close()
    infile=open('HC_pL_node_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    alg1c1_node_percent=json.load(infile)
    infile.close()
    infile=open('HC_pL_edge_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    alg1c1_edge_percent=json.load(infile)
    infile.close()
#HCpF
    infile=open('HC_pF_mon_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    alg1c2_mon_percent=json.load(infile)
    infile.close()
    infile=open('HC_pF_node_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    alg1c2_node_percent=json.load(infile)
    infile.close()
    infile=open('HC_pF_edge_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    alg1c2_edge_percent=json.load(infile)
    infile.close()
#HCpLF
    infile=open('HC_pLF_mon_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    alg1c12L_mon_percent=json.load(infile)
    infile.close()
    infile=open('HC_pLF_node_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    alg1c12L_node_percent=json.load(infile)
    infile.close()
    infile=open('HC_pLF_edge_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    alg1c12L_edge_percent=json.load(infile)
    infile.close()
#RP
    infile=open('RPS_mon_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    RPD_mon_percent=json.load(infile)
    infile.close()
    infile=open('RPS_node_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    RPD_node_percent=json.load(infile)
    infile.close()
    infile=open('RPS_edge_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    RPD_edge_percent=json.load(infile)
    infile.close()

#RW
    if graphdic[graph]!='General Relativity':
        infile=open('RWD_mon_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
        RW_mon_percent=json.load(infile)
        infile.close()
        infile=open('RWD_node_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
        RW_node_percent=json.load(infile)
        infile.close()
        infile=open('RWD_edge_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
        RW_edge_percent=json.load(infile)
        infile.close()
#HLD_p
    infile=open('HLD_p_mon_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    RWS_mon_percent=json.load(infile)
    infile.close()
    infile=open('HLD_p_node_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    RWS_node_percent=json.load(infile)
    infile.close()
    infile=open('HLD_p_edge_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    RWS_edge_percent=json.load(infile)
    infile.close()
#UBDn
    infile=open('UBDn_mon_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    UBDn_mon_percent=json.load(infile)
    infile.close()
    infile=open('UBDn_node_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    UBDn_node_percent=json.load(infile)
    infile.close()
    infile=open('UBDn_edge_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    UBDn_edge_percent=json.load(infile)
    infile.close()
    
#UBDe
    infile=open('UBDe_mon_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    UBDe_mon_percent=json.load(infile)
    infile.close()
    infile=open('UBDe_node_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    UBDe_node_percent=json.load(infile)
    infile.close()
    infile=open('UBDe_edge_per_avg_'+graphdic[graph]+'_'+str(numRuns)+'Runs.json', 'r')
    UBDe_edge_percent=json.load(infile)
    infile.close()

#########################
    fig = plt.figure()
    #fig.suptitle('Average % of nodes discovered')
    ax = fig.add_subplot(111)
    ax.set_xlabel('% node monitors')
    ax.set_ylabel('% nodes discovered')
    ax.axis([0,50,0,100])

    ax.plot(UBDn_mon_percent, UBDn_node_percent,'black', label='UBDn')

    ax.plot(alg1_mon_percent, alg1_node_percent,'red',label='HCp')
    ax.plot(alg1c1_mon_percent, alg1c1_node_percent,'darkred',linestyle='-.',label='HCpL')
    ax.plot(alg1c2_mon_percent, alg1c2_node_percent,'firebrick',linestyle='--', label='HCpF')
    ax.plot(alg1c12L_mon_percent, alg1c12L_node_percent,'orange', label='HCpLF')

    if graphdic[graph]!='General Relativity':
        ax.plot(RW_mon_percent, RW_node_percent,'fuchsia',linestyle='--', label='RW')
    ax.plot(RWS_mon_percent, RWS_node_percent,'plum', label='HLD_p')
    ax.plot(RPD_mon_percent, RPD_node_percent,'mediumvioletred', label='RP')

    plt.legend(loc=4, fontsize=7)
    plt.grid(True)
    plt.savefig(graphdic[graph]+'_All_Algs_nodes_50Runs.eps', format='eps', dpi=1000)
    plt.close()

    fig = plt.figure()
    #fig.suptitle('Average % of edges discovered')
    ax = fig.add_subplot(111)
    ax.set_xlabel('% node monitors')
    ax.set_ylabel('% edges discovered')
    ax.axis([0,50,0,100])

    ax.plot(UBDe_mon_percent, UBDe_edge_percent,'black', label='UBDn')

    ax.plot(alg1_mon_percent, alg1_edge_percent,'red', label='HCp')
    ax.plot(alg1c1_mon_percent, alg1c1_edge_percent,'darkred',linestyle='-.', label='HCpL')
    ax.plot(alg1c2_mon_percent, alg1c2_edge_percent,'firebrick',linestyle='--', label='HCpF')
    ax.plot(alg1c12L_mon_percent, alg1c12L_edge_percent,'orange',label='HCpLF')

    if graphdic[graph]!='General Relativity':
        ax.plot(RW_mon_percent, RW_edge_percent,'fuchsia',linestyle='--', label='RW')
    ax.plot(RWS_mon_percent, RWS_edge_percent,'plum',label='HLD_p')
    ax.plot(RPD_mon_percent, RPD_edge_percent, color='mediumvioletred',label='RP')


    plt.legend(loc=4, fontsize=7)
    plt.grid(True)
    plt.savefig(graphdic[graph]+'_All_Algs_edges_50Runs.eps', format='eps', dpi=1000)
    plt.close()
