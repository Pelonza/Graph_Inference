# This is the main file which calls each of the algorithms.
# See 'main' for interface and command-line parser.
# NOTE: While this saves the data, it is into a file-format readable by python only.
# These can be imported directly back into python for later plotting in a python script.
#
# To use this file, you need to go in and modify several lines to the appropriate
# algorithm, trials, probability and graph-name. Other files do not require changes.
 
import numpy as np
import Fake_Degree_Discovery_Revised as myalg
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import json
import sys
import time

#algorithm run with
alg_name="FDD_Revised"
#alg_name="UBD_n"

#Number of trials to run
num_trials=1

#default probability
prob=0.75 


#reads the graph in, adjust for desired graph on your machine
#graph_name="barabasi"
graph_name="General_Relativity"
#graph_name="facebook_combined"
#graph_name="ER_random-1"
#graph_name="wiki-Vote"


graph = nx.read_gexf("Graph_Files/"+graph_name+".gexf", node_type=int)

#Use these two lines when you want to read a directed network as an undirected one.
#graph1 = nx.read_gexf("Graph_Files/"+graph_name+".gexf", node_type=int)
#graph = graph1.to_undirected()


#This tells Python we want to stop at the interval of 50 after 
#half of the nodes have been used as monitors
stop = graph.number_of_nodes()/2 + 50
original_num_nodes = graph.number_of_nodes()
original_num_edges = graph.number_of_edges()
original_avg_deg = float(2*original_num_edges)/original_num_nodes

mon_dict,node_dict,edge_dict = {},{},{}

#--------------------------------
# This runs multiple trials of the inference algorithm... 
# This needs to be run multiple times once we institute a random choice between equal degrees/seen
#--------------------------------

for i in range(0,num_trials):
    #print "Beginning round: ", i
    time.sleep(2)
    monitors, nodes, edges, components = [],[],[],[]
    nodes_percent_fnd, edges_percent_fnd, comp_fnd=[],[],[]
    mon_percent=[]
    
    #Notice it calls "myalg" and "alg" ... so IF algorithm module has a function/definition for 'alg', need to only change imported module.
    yut = myalg.alg(graph, i)
    monitor = yut.pick_start()
    monitor_set_list=[] #Will hold which monitors got added each 50, in case we need for tracking/info.
    
    for number_of_monitors in range(50,stop,50):
    #for number_of_monitors in range(50,200,50): #For testing purposes to not run to full stop on big graphs.
        print "In for-loop at:", number_of_monitors

        #Adds number of monitors that this loop counts by (50 right now)
        while not yut.stop(number_of_monitors):
            yut.add_neighbors(monitor)
            
            #This line may need to be changed, depending on monitor placing method
            monitor = yut.place_next_monitor(monitor, prob)
            
            #tracks which nodes were added to the monitor set
            monitor_set_list.append(yut.monitor_set)
        
        #calculating found data into percents
        nodes_percent_fnd.append(float(yut.result_graph.number_of_nodes())/original_num_nodes * 100)
        edges_percent_fnd.append(float(yut.result_graph.number_of_edges())/original_num_edges * 100)
        comp_fnd.append(nx.number_connected_components(yut.result_graph))
        mon_percent.append(float(number_of_monitors)/original_num_nodes*100)

        nodes.append(yut.result_graph.number_of_nodes())
        edges.append(yut.result_graph.number_of_edges())
        components.append(nx.number_connected_components(yut.result_graph))

    #End loop that iterates through adding monitors.

      
    #Output each of the data variables into python readable files (NOT human-readable or importable elsewhere)
    outfile=open('Erin_Output/'+alg_name+'_mon_percent_'+graph_name+'_Trial'+str(i),'w') #Repeat for nodes, edges, compns below
    json.dump(mon_percent, outfile)
    outfile.close()

    outfile=open('Graph_Infer_Output/'+alg_name+'_nodes_percent_fnd_'+graph_name+'_trial_'+str(i), 'w')
    json.dump(nodes_percent_fnd, outfile)
    outfile.close()

    outfile=open('Graph_Infer_Output/'+alg_name+'_edges_percent_fnd_'+graph_name+'_trial_'+str(i), 'w')
    json.dump(edges_percent_fnd, outfile)
    outfile.close()

    #outfile=open('Graph_Infer_Output/'+alg_name+'_comp_fnd_'+graph_name, 'w')
    #json.dump(comp_fnd, outfile)
    #outfile.close()
    
    '''
    
    #Use this for directed graphs
    
    outfile=open('Graph_Infer_Output/mon_percent_'+graph_name, 'w')
    json.dump(mon_percent, outfile)
    outfile.close()
    
    outfile=open('Graph_Infer_Output/'+alg_name+'_nodes_percent_fnd_'+graph_name+'_directed', 'w')
    json.dump(nodes_percent_fnd, outfile)
    outfile.close()

    outfile=open('Graph_Infer_Output/'+alg_name+'_edges_percent_fnd_'+graph_name+'_directed', 'w')
    json.dump(edges_percent_fnd, outfile)
    outfile.close()

    outfile=open('Graph_Infer_Output/'+alg_name+'_comp_fnd_'+graph_name+'_directed', 'w')
    json.dump(comp_fnd, outfile)
    outfile.close()
    
 








