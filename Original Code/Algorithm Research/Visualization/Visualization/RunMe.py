import matplotlib.pyplot as plt
import networkx as nx
import randomwalk1
import HND_condition12L
import math
import sys,time

###README###
#all the "if True/False:" statements are just switches.  True is on, False is off.  For graphs only pick one, for visualizations you can pick one or many.


#Erdos-Renyi
if True:
    G = nx.erdos_renyi_graph(100,.3) #(nodesize, p)

#Barabasi-Albert
if False:
    G = nx.barabasi_albert_graph(100,2) #(nodesize, m)

#Graphs too big for me to run (Facebook requires 9GB of available RAM):
#G = nx.read_gexf("ER_random-1.gexf", node_type=int)
#G = nx.read_gexf("barabasi.gexf", node_type=int)
#G = nx.read_gexf("facebook_combined.gexf", node_type=int)
#G = nx.read_gexf("General_Relativity.gexf", node_type=int)

#Setting up the plot
cf = plt.figure(1, figsize=(8,8))
pos = nx.graphviz_layout(G)
ax = cf.add_axes((0,0,1,1))
for n in G:
    G.node[n]['draw'] = nx.draw_networkx_nodes(G,pos,nodelist=[n], with_labels=False,node_size=200,alpha=0.2,node_color='w')
plt.ion()
plt.show()
ax = plt.gca()
canvas = ax.figure.canvas
background = canvas.copy_from_bbox(ax.bbox)

#Set number of monitors
stop = G.number_of_nodes()

#Random Walk (dumb) 
if True:     
    yut = randomwalk1.RW(G, 1)
    monitor = yut.pick_start()
    G.node[monitor]['draw'].set_color('r')
    G.node[monitor]['draw'].set_alpha('1.0')
    while not yut.stop(stop):
        plt.pause(.1)
        neighbors=yut.add_neighbors(monitor)
        for neighbor in neighbors:
            n=G.node[neighbor]['draw']
            if neighbor not in yut.monitor_set:
                n.set_color('b')
                n.set_alpha(.5)
                e=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,neighbor)],width=.2,alpha=1,color='b')
                ax.draw_artist(n)
                ax.draw_artist(e)
        monitor1 = yut.place_next_monitor(monitor)
        m=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,monitor1)],width=1,alpha=1,color='r')
        monitor=monitor1
        a=G.node[monitor]['draw']
        a.set_color('r')
        a.set_alpha('1.0')
        ax.draw_artist(a)
        ax.draw_artist(m)

        
        
        
        
#ALGORITHM1 WITH CONDITION 1 (NOTE THAT LOG(100)=2!!!)
if False:
    HNDc = HND_condition12L.HND(G,1)
    tally=0
    monitor, tally = HNDc.pick_start(tally)
    G.node[monitor]['draw'].set_color('g')
    G.node[monitor]['draw'].set_alpha('1.0')
    while not HNDc.stop(stop):
        plt.pause(.1)
        neighbors=HNDc.add_neighbors(monitor)
        for neighbor in neighbors: 
            n=G.node[neighbor]['draw']
            if neighbor not in HNDc.monitor_set:
                n.set_color('b')
                n.set_alpha(.5)
                ax.draw_artist(n)
                e=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,neighbor)],width=.2,alpha=1,color='b')
        monitor1, tally = HNDc.place_next_monitor(monitor,tally)
        m=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,monitor1)],width=1,alpha=1,color='r')
        ax.draw_artist(m)
        monitor=monitor1
        a=G.node[monitor]['draw']
        a.set_color('g')
        a.set_alpha('1.0')
        ax.draw_artist(a)
        if tally>=math.log(G.number_of_nodes()): 
            neighbors=HNDc.add_neighbors(monitor)
            for neighbor in neighbors:
                n=G.node[neighbor]['draw']
                if neighbor not in HNDc.monitor_set:
                    n.set_color('b')
                    n.set_alpha(.5)
                    e=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,neighbor)],width=.2,alpha=1,color='b')
                    ax.draw_artist(n)
                    ax.draw_artist(e)
            monitor1, tally = HNDc.pick_start(tally)
            m=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,monitor1)],width=1,alpha=1,color='r')
            monitor=monitor1
            a=G.node[monitor]['draw']
            a.set_color('r')
            a.set_alpha('1.0')
            ax.draw_artist(a)
            ax.draw_artist(m)
        
        
        
#ALGORITHM1 WITH CONDITION 2       
if False:
    HNDc = HND_condition12L.HND(G,1)
    tally=0
    monitor, tally = HNDc.pick_start(tally)
    G.node[monitor]['draw'].set_color('g')
    G.node[monitor]['draw'].set_alpha('1.0')
    while not HNDc.stop(stop):
        plt.pause(.1)
        neighbors=HNDc.add_neighbors(monitor)
        for neighbor in neighbors:
            n=G.node[neighbor]['draw']
            if neighbor not in HNDc.monitor_set:
                n.set_color('b')
                n.set_alpha(.5)
                ax.draw_artist(n)
                e=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,neighbor)],width=.2,alpha=1,color='b')
                ax.draw_artist(e)
        
        monitor1, tally = HNDc.place_next_monitor(monitor,tally)
        m=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,monitor1)],width=1,alpha=1,color='r')
        ax.draw_artist(m)
        monitor=monitor1
        a=G.node[monitor]['draw']
        a.set_color('g')
        a.set_alpha('1.0')
        ax.draw_artist(a)
        if (HNDc.seen['Total']-len(HNDc.seen.keys()))>G.number_of_nodes():
            neighbors=HNDc.add_neighbors(monitor)
            for neighbor in neighbors:
                n=G.node[neighbor]['draw']
                if neighbor not in HNDc.monitor_set:
                    n.set_color('b')
                    n.set_alpha(.5)
                    ax.draw_artist(n)
                    e=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,neighbor)],width=.2,alpha=1,color='b')
            monitor1, tally = HNDc.pick_start(tally)
            m=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,monitor1)],width=1,alpha=1,color='r')
            ax.draw_artist(m)
            monitor=monitor1
            a=G.node[monitor]['draw']
            a.set_color('r')
            a.set_alpha('1.0')
        
        
        
#ALGORITHM1 WITH CONDITION1&2        
if False:       
    HNDc = HND_condition12L.HND(G,1)
    tally=0
    monitor, tally = HNDc.pick_start(tally)
    G.node[monitor]['draw'].set_color('g')
    G.node[monitor]['draw'].set_alpha('1.0')
    while not HNDc.stop(stop):
        plt.pause(.1)
        neighbors=HNDc.add_neighbors(monitor)
        for neighbor in neighbors: 
            n=G.node[neighbor]['draw']
            if neighbor not in HNDc.monitor_set:
                n.set_color('b')
                n.set_alpha(.5)
                ax.draw_artist(n)
                e=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,neighbor)],width=.2,alpha=1,color='b')
        monitor1, tally = HNDc.place_next_monitor(monitor,tally)
        m=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,monitor1)],width=1,alpha=1,color='r')
        ax.draw_artist(m)
        monitor=monitor1
        a=G.node[monitor]['draw']
        a.set_color('g')
        a.set_alpha('1.0')
        ax.draw_artist(a)
        if tally>=math.log(G.number_of_nodes()) or ((HNDc.seen['Total']-len(HNDc.seen.keys()))>G.number_of_nodes()): 
            neighbors=HNDc.add_neighbors(monitor)
            for neighbor in neighbors:
                n=G.node[neighbor]['draw']
                if neighbor not in HNDc.monitor_set:
                    n.set_color('b')
                    n.set_alpha(.5)
                    e=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,neighbor)],width=.2,alpha=1,color='b')
                    ax.draw_artist(n)
                    ax.draw_artist(e)
            monitor1, tally = HNDc.pick_start(tally)
            #m=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,monitor1)],width=1,alpha=1,color='r')
            monitor=monitor1
            a=G.node[monitor]['draw']
            a.set_color('r')
            a.set_alpha('1.0')
            ax.draw_artist(a)
            ax.draw_artist(m)

