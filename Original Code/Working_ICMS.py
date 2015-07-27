'''
Title of Program
    XXXX.py
    
CSXXXX


Created on Jan 20, 2015

@author: Erik Rye
'''
 
import numpy as np
import algorithm3_mod as algorithm3_mod
import algorithm3 as algorithm3
import networkx as nx
#import matplotlib.pyplot as plt
import sys
import time

#file to write stats to
stats = open('statistics.dat', 'w')

#reads the graph in, adjust for desired graph on your machine
graph = nx.read_gexf("web-Stanford.gexf", node_type=int)

#This tells Python we want to stop at the interval of 50 after 
#half of the nodes have been used as monitors
stop = graph.number_of_nodes()/2 + 50
original_num_nodes = graph.number_of_nodes()
original_num_edges = graph.number_of_edges()
original_avg_deg = float(2*original_num_edges)/original_num_nodes

mon_dict,node_dict,edge_dict = {},{},{}


#--------------------------------
'''
This section runs a loop over several restart probabilities.
Not needed for our testing??

#adjust desired probabilities here
# .25, .5, 75 would be range(1,4), for example
for prob in range(1,4):
    prob /= float(4)
    print "\n#################################"
    print "Begininng probability p = ", prob
    print "#################################"
    time.sleep(2)
    '''
#------------------------------


overall_monitors, overall_nodes, overall_edges, overall_components = [],[],[],[]
overall_monitors2, overall_nodes2, overall_edges2, overall_components2 = [],[],[],[]


#change the second number for # of iterations
# This runs multiple trials of the inference algorithm... 
# This needs to be run multiple times once we institute a random choice between equal degrees/seen
for i in range(0,1):
    print "Beginning round: ", i
    time.sleep(2)
    monitors, nodes, edges, components = [],[],[],[]
    nodes_percent_fnd, edges_percent_fnd, comp_fnd=[],[],[]
    monitors2, nodes2, edges2, components2 = [],[],[],[]
    nodes_percent_fnd2, edges_percent_fnd2, comp_fnd2=[],[],[]
    #Defining everything that you start off with     
    print "\n***************************************"
    print "Original Graph Statistics"
    print "Number of nodes:", original_num_nodes
    print "Number of edges:", original_num_edges 
    print "Average degree:", original_avg_deg
    print "\n***************************************"

    #presenting the number of monitors used and how many edges and nodes
    yut = algorithm3.alg30(graph, i)
    monitor = yut.pick_start()
    for number_of_monitors in range(50,stop,50):
        #yut.monitor_set_list=[]
        while not yut.stop(number_of_monitors):
            yut.add_neighbors(monitor)
            monitor = yut.place_next_monitor(monitor, 0.75)


        #print "Inferred Graph Statistics:"
        #print "Number of monitors used:", len(yut.monitor_set)
        #print "Found", yut.result_graph.number_of_nodes(), "nodes"
        #print "Found", yut.result_graph.number_of_edges(), "edges"
        #calculating found data into percents
        nodes_percent_fnd.append(float(yut.result_graph.number_of_nodes())/graph.number_of_nodes() * 100)
        #print "Found", nodes_percent_fnd[-1], "percent of the nodes"
        edges_percent_fnd.append(float(yut.result_graph.number_of_edges())/graph.number_of_edges() * 100)
        #print "Found", edges_percent_fnd[-1], "percent of the edges"
        #create the plots of percentage of nodes and edges
        comp_fnd.append(nx.number_connected_components(yut.result_graph))
        #print "Found", comp_fnd[-1]
        #monitor_list = []
        #monitor_list.append(yut.monitor_set)
    
        monitors.append(len(yut.monitor_set))
        #yut.monitor_set_list.append(yut.monitor_set)
        nodes.append(yut.result_graph.number_of_nodes())
        edges.append(yut.result_graph.number_of_edges())
        components.append(nx.number_connected_components(yut.result_graph))

    foo = algorithm3_mod.alg3(graph, i)
    monitor = foo.pick_start()
    for number_of_monitors in range(50,stop,50):
        while not foo.stop(number_of_monitors):
            foo.add_neighbors(monitor)  
            monitor = foo.place_next_monitor2()


        #print "Inferred Graph Statistics:"
        #print "Number of monitors used:", len(yut.monitor_set)
        #print "Found", yut.result_graph.number_of_nodes(), "nodes"
        #print "Found", yut.result_graph.number_of_edges(), "edges"
        #calculating found data into percents
        nodes_percent_fnd2.append(float(foo.result_graph.number_of_nodes())/graph.number_of_nodes() * 100)
        #print "Found", nodes_percent_fnd2[-1], "percent of the nodes"
        edges_percent_fnd2.append(float(foo.result_graph.number_of_edges())/graph.number_of_edges() * 100)
        #print "Found", edges_percent_fnd2[-1], "percent of the edges"
        #create the plots of percentage of nodes and edges
        comp_fnd2.append(nx.number_connected_components(foo.result_graph))
        #print "Found", comp_fnd2[-1]
        #monitor_list = []
        #monitor_list.append(yut.monitor_set)
    
        monitors2.append(len(foo.monitor_set))
        #yut.monitor_set_list.append(yut.monitor_set)
        nodes2.append(foo.result_graph.number_of_nodes())
        edges2.append(foo.result_graph.number_of_edges())
        components2.append(nx.number_connected_components(foo.result_graph))
        
#    overall_monitors.append(monitors)
#    overall_nodes.append(nodes)
#    overall_edges.append(edges)
#    overall_components.append(components)

    #write the last iteration graph at the max number of monitors once per p
#    nx.write_gexf(yut.result_graph,
#            "C:\Users\breynol2\Documents\Example" + ".gexf")
#the zip function merges the lists together
#monitor_tuples = zip(*overall_monitors)
#node_tuples = zip(*overall_nodes)
#edge_tuples = zip(*overall_edges)
#component_tuples = zip(*overall_components)
   
#average_monitors = [np.mean(x) for x in monitor_tuples]
#average_nodes = [np.mean(x) for x in node_tuples]
#average_edges = [np.mean(x) for x in edge_tuples]
#average_components = [np.mean(x) for x in component_tuples]
    
#Calculates average percentage of nodes, edges, and components found
#mon_percent = [float(x)/original_num_nodes * 100 for x in average_monitors]
#node_percent = [float(x)/original_num_nodes * 100 for x in average_nodes]
#edge_percent = [float(x)/original_num_edges * 100 for x in average_edges]
    
#Prints these results
    #stats.write("Prob = " + str(prob) + '\n')
#    stats.write("Average percent of nodes found = " + str(node_percent[-1]) + '\n')
#    stats.write("Average percent of edges found = " + str(edge_percent[-1]) + '\n')
#    stats.write("Average components found = " + str(average_components[-1]) + '\n')

    #mon_dict[prob] = mon_percent
    #node_dict[prob] = node_percent 
    #edge_dict[prob] = edge_percent 


stats.close()