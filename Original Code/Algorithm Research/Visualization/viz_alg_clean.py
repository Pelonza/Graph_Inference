import matplotlib.pyplot as plt
import networkx as nx
import randomwalk1
import HND_condition12L
import math
import sys,time
from collections import defaultdict

###README###
#all the "if True/False:" statements are just switches.  True is on, False is off.  For graphs only pick one, for visualizations you can pick one or many.


#Erdos-Renyi
if False:
    G = nx.erdos_renyi_graph(100,.05) #(nodesize, p)

#Barabasi-Albert
if True:
    G = nx.barabasi_albert_graph(500,2) #(nodesize, m)

if False:
    G = nx.watts_strogatz_graph(500, 4, .3, seed=None)

if False:
    G = nx.davis_southern_women_graph()

if False:
    G = nx.connected_watts_strogatz_graph(500, 4, .3, seed=None)

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
if False:
    yut = randomwalk1.RW(G, 1)
    monitor = yut.pick_start()
    G.node[monitor]['draw'].set_color('r')
    G.node[monitor]['draw'].set_alpha('1.0')
    while not yut.stop(stop):
        plt.pause(.5)
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




 #Depth First Search
if False:
    nodes = G
    visited=set()
    for start in nodes:

        if start in visited:
            continue

        visited.add(start)
        stack = [(start,iter(G[start]))]
        while stack:
            parent,children = stack[-1]
            try:
                child = next(children)
                if child not in visited:
                    nx.draw_networkx_edges(G,pos,edgelist=[(parent,x)  for x in children],width=.2,alpha=.5,color='0.8')
                    plt.pause(.1)
                    nx.draw_networkx_edges(G,pos,edgelist=[(parent,child)],width=.8,alpha=1,color='b')
                    nx.draw_networkx_nodes(G,pos,nodelist=[parent],node_color='b',alpha=1)
                    nx.draw_networkx_nodes(G,pos,nodelist=set(G[parent].keys())-visited,alpha=.5,node_color='0.8')
                    plt.pause(.1)
                    visited.add(child)
                    stack.append((child,iter(G[child])))
            except StopIteration:
                stack.pop()
    plt.pause(10)



#ALGORITHM1 WITH CONDITION 1 (NOTE THAT LOG(100)=2!!!)
if False:
    HNDc = HND_condition12L.HND(G,1)
    tally=0
    monitor, tally = HNDc.pick_start(tally)
    G.node[monitor]['draw'].set_color('g')
    G.node[monitor]['draw'].set_alpha('1.0')
    length=math.log(G.number_of_nodes())
    while not HNDc.stop(stop):
        plt.pause(1)
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
        if tally>=length:
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
if True:
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
            m=nx.draw_networkx_edges(G,pos,edgelist=[(monitor,monitor1)],width=1,alpha=1,color='r')
            monitor=monitor1
            a=G.node[monitor]['draw']
            a.set_color('r')
            a.set_alpha('1.0')
            ax.draw_artist(a)
            ax.draw_artist(m)
