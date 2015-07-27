
︠f5fef863-57d8-4f26-b6f8-feb804a1fa04︠
'''
NOTE: While this saves the data, it is into a file-format readable by python only.
      These can be imported directly back into python for later plotting in a python script.
      
Important lines to observe:
Line 18 -- modify to accept different algorithms
Line 28 -- modify to load/test on different graphs (from sub-folder of Graph_Files)
Line 46 -- modify for run-count per graph per algorithm
Line 56 -- may need modified depending on algorithm file/module
Line 69 -- may need modified depending on call to "place monitor" in algorithm
Line 87 -- starts saving data, currently into sub-folder of Graph_Infer_Output

'''
︡6c3c85f3-a3c7-4166-be1a-c29aa306c7b2︡{"stdout":"'\\nNOTE: While this saves the data, it is into a file-format readable by python only.\\n      These can be imported directly back into python for later plotting in a python script.\\n      \\nImportant lines to observe:\\nLine 18 -- modify to accept different algorithms\\nLine 28 -- modify to load/test on different graphs (from sub-folder of Graph_Files)\\nLine 46 -- modify for run-count per graph per algorithm\\nLine 56 -- may need modified depending on algorithm file/module\\nLine 69 -- may need modified depending on call to \"place monitor\" in algorithm\\nLine 87 -- starts saving data, currently into sub-folder of Graph_Infer_Output\\n\\n'\n"}︡
︠a079ae49-f10b-455e-baea-d0f0f0e2acdfs︠

 
import numpy as np
#import HighGlobalDegree_LeastSeen as myalg #Expects there to be a class/definition for "alg" in module.
import Fake_Degree_Discovery_Revised as myalg
#import Fake_Degree_Discovery as myalg
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import json
import sys
import time

#algorithm run with
alg_name="FDD_Revised"
#alg_name="UBD_n"


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
︡25da6635-1252-4ffc-ac40-cf2e0817d9c0︡
︠f94dee24-c746-4bbc-ad5b-ddb4a59b7dbbs︠


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

#Number of trials to run
num_trials=1
prob=0.75 #default probability

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

    #print mon_percent
    
    #out_monitor_set_list=zip(*monitor_set_list)
    
    #Output each of the data variables into python readable files (NOT human-readable or importable elsewhere)
    #outfile=open('Erin_Output/'+alg_name+'_mon_percent_'+graph_name+'_Trial'+str(i),'w') #Repeat for nodes, edges, compns below
    
    
    #outfile=open('Graph_Infer_Output/mon_percent_'+graph_name, 'w')
    #json.dump(mon_percent, outfile)
    #outfile.close()

    outfile=open('Graph_Infer_Output/'+alg_name+'_nodes_percent_fnd_'+graph_name, 'w')
    json.dump(nodes_percent_fnd, outfile)
    outfile.close()

    outfile=open('Graph_Infer_Output/'+alg_name+'_edges_percent_fnd_'+graph_name, 'w')
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
    
    '''

    #outfile=open('Graph_Infer_Output/'+alg_name+'_monitor_set_list_'+graph_name+'_Trial_'+str(i), 'w')
    #json.dump(out_monitor_set_list, outfile)
    #outfile.close()
︡2191acd1-6d94-4be3-ac14-e77dcce69659︡{"stdout":"In for-loop at:"}︡{"stdout":" 50\nIn for-loop at: 100\nIn for-loop at:"}︡{"stdout":" 150\nIn for-loop at: 200\nIn for-loop at:"}︡{"stdout":" 250\nIn for-loop at:"}︡{"stdout":" 300\nIn for-loop at:"}︡{"stdout":" 350\nIn for-loop at:"}︡{"stdout":" 400\nIn for-loop at:"}︡{"stdout":" 450\nIn for-loop at:"}︡{"stdout":" 500\nIn for-loop at:"}︡{"stdout":" 550\nIn for-loop at:"}︡{"stdout":" 600\nIn for-loop at:"}︡{"stdout":" 650\nIn for-loop at:"}︡{"stdout":" 700\nIn for-loop at:"}︡{"stdout":" 750\nIn for-loop at:"}︡{"stdout":" 800\nIn for-loop at:"}︡{"stdout":" 850\nIn for-loop at:"}︡{"stdout":" 900\nIn for-loop at:"}︡{"stdout":" 950\nIn for-loop at:"}︡{"stdout":" 1000\nIn for-loop at:"}︡{"stdout":" 1050\nIn for-loop at:"}︡{"stdout":" 1100\nIn for-loop at:"}︡{"stdout":" 1150\nIn for-loop at:"}︡{"stdout":" 1200\nIn for-loop at:"}︡{"stdout":" 1250\nIn for-loop at:"}︡{"stdout":" 1300\nIn for-loop at:"}︡{"stdout":" 1350\nIn for-loop at:"}︡{"stdout":" 1400\nIn for-loop at:"}︡{"stdout":" 1450\nIn for-loop at:"}︡{"stdout":" 1500\nIn for-loop at:"}︡{"stdout":" 1550\nIn for-loop at:"}︡{"stdout":" 1600\nIn for-loop at:"}︡{"stdout":" 1650\nIn for-loop at:"}︡{"stdout":" 1700\nIn for-loop at:"}︡{"stdout":" 1750\nIn for-loop at:"}︡{"stdout":" 1800\nIn for-loop at:"}︡{"stdout":" 1850\nIn for-loop at:"}︡{"stdout":" 1900\nIn for-loop at:"}︡{"stdout":" 1950\nIn for-loop at:"}︡{"stdout":" 2000\nIn for-loop at:"}︡{"stdout":" 2050\nIn for-loop at:"}︡{"stdout":" 2100\nIn for-loop at:"}︡{"stdout":" 2150\nIn for-loop at:"}︡{"stdout":" 2200\nIn for-loop at:"}︡{"stdout":" 2250\nIn for-loop at:"}︡{"stdout":" 2300\nIn for-loop at:"}︡{"stdout":" 2350\nIn for-loop at:"}︡{"stdout":" 2400\nIn for-loop at:"}︡{"stdout":" 2450\nIn for-loop at:"}︡{"stdout":" 2500\nIn for-loop at:"}︡{"stdout":" 2550\nIn for-loop at:"}︡{"stdout":" 2600\nIn for-loop at:"}︡{"stdout":" 2650\n\"\\n    \\n    #Use this for directed graphs\\n    \\n    outfile=open('Graph_Infer_Output/mon_percent_'+graph_name, 'w')\\n    json.dump(mon_percent, outfile)\\n    outfile.close()\\n    \\n    outfile=open('Graph_Infer_Output/'+alg_name+'_nodes_percent_fnd_'+graph_name+'_directed', 'w')\\n    json.dump(nodes_percent_fnd, outfile)\\n    outfile.close()\\n\\n    outfile=open('Graph_Infer_Output/'+alg_name+'_edges_percent_fnd_'+graph_name+'_directed', 'w')\\n    json.dump(edges_percent_fnd, outfile)\\n    outfile.close()\\n\\n    outfile=open('Graph_Infer_Output/'+alg_name+'_comp_fnd_'+graph_name+'_directed', 'w')\\n    json.dump(comp_fnd, outfile)\\n    outfile.close()\\n    \\n    \""}︡{"stdout":"\n"}︡
︠6d77fd5c-8445-4d0d-b06c-1db89c605611︠
︡c3662a89-1894-4505-98f5-ecd5e83fc6de︡
︠f9229d4d-f929-4932-bae9-2aa1e067ba7a︠









