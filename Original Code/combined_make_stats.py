'''
Title of Program
    XXXX.py
    
CSXXXX


Created on Jan 20, 2015

@author: Erik Rye
'''
import randomwalk
import numpy as np
import algorithm3
import networkx as nx
import matplotlib.pyplot as plt
import sys
#allows you to work with time and convert between representations
import time
#finds and adds nodes of highest degree along with their edges to graph
import localHDN
#finds and adds nodes of lowest degree along with their edges to graph
import localLDN

#file to write stats to
stats = open('statistics.dat', 'w')

#reads the graph in, adjust for desired graph on your machine
graph = nx.read_gexf("/users/erik/desktop/MA4404/facebook_combined.gexf", node_type=int)

#This tells Python we want to stop at the interval of 50 after 
#half of the nodes have been used as monitors
stop = graph.number_of_nodes()/2 + 50
original_num_nodes = graph.number_of_nodes()
original_num_edges = graph.number_of_edges()
original_avg_deg = float(2*original_num_edges)/original_num_nodes

mon_dict,node_dict,edge_dict = {},{},{}

#adjust desired probabilities here
# .25, .5, 75 would be range(1,4), for example
for prob in range(0,5,4):
    #It divides left with the right and assign the result to left
    prob /= float(4)
    print "\n#################################"
    print "Begininng probability p = ", prob
    print "#################################"
    time.sleep(2)
    overall_monitors, overall_nodes, overall_edges, overall_components = [],[],[],[]

    
    if prob == 0:
        mlmonitors,mlnodes,mledges = [],[],[]
        for i in range(25):
            print "Beginning round: ", i
            #defines lmonitors, lnodes,ledges
            lmonitors,lnodes,ledges = [],[],[]
            for number_of_monitors in range(50,stop,50):
                l = localLDN.localLDN(graph, i)
                print number_of_monitors
                l.main(number_of_monitors)
                #adds new info to list
                lmonitors.append(len(l.monitor_set))
                lnodes.append(l.g_i.number_of_nodes())
                ledges.append(l.g_i.number_of_edges())
            
            #add new lmonitor,lnode,ledge to mlmonitor, mlnode, and mledge lists
            mlmonitors.append(lmonitors)
            mlnodes.append(lnodes)
            mledges.append(ledges)
            
#the zip function merges the lists
        mlmonitor_tuples = zip(*mlmonitors)
        mlnode_tuples = zip(*mlnodes)
        mledge_tuples = zip(*mledges)
       
        maverage_monitors = [np.mean(x) for x in mlmonitor_tuples]
        maverage_nodes = [np.mean(x) for x in mlnode_tuples]
        maverage_edges = [np.mean(x) for x in mledge_tuples]

        mlmon_percent = [float(x)/original_num_nodes * 100 for x in maverage_monitors]
        mlnode_percent = [float(x)/original_num_nodes * 100 for x in maverage_nodes]
        mledge_percent = [float(x)/original_num_edges * 100 for x in maverage_edges]
        f = open('blah.txt', 'w')
        for a in mlmon_percent:
            f.write(str(a) + ' ')
        for b in mlnode_percent:
            f.write(str(b) + ' ')
        for c in mledge_percent:
            f.write(str(c) + ' ')
        f.close
    
#Pulls data from localHDN about number of monitors
#found thus far
    if prob == 0:
        olmonitors,olnodes,oledges = [],[],[]
        for i in range(25):
            print "Beginning round: ", i
            lmonitors,lnodes,ledges = [],[],[]
            for number_of_monitors in range(50,stop,50):
                l = localHDN.localHDN(graph, i)
                print number_of_monitors
                l.main(number_of_monitors)
                lmonitors.append(len(l.monitor_set))
                lnodes.append(l.g_i.number_of_nodes())
                ledges.append(l.g_i.number_of_edges())
            
            olmonitors.append(lmonitors)
            olnodes.append(lnodes)
            oledges.append(ledges)

#the function zip merges these into a list
        omonitor_tuples = zip(*olmonitors)
        onode_tuples = zip(*olnodes)
        oedge_tuples = zip(*oledges)
       
        oaverage_monitors = [np.mean(x) for x in omonitor_tuples]
        oaverage_nodes = [np.mean(x) for x in onode_tuples]
        oaverage_edges = [np.mean(x) for x in oedge_tuples]

        omon_percent = [float(x)/original_num_nodes * 100 for x in oaverage_monitors]
        onode_percent = [float(x)/original_num_nodes * 100 for x in oaverage_nodes]
        oedge_percent = [float(x)/original_num_edges * 100 for x in oaverage_edges]
        f = open('blah.txt', 'a')
        for a in omon_percent:
            f.write(str(a) + ' ')
        for b in onode_percent:
            f.write(str(b) + ' ')
        for c in oedge_percent:
            f.write(str(c) + ' ')
        f.close

    #change the second number for # of iterations
    for i in range(25):
        print "Beginning round: ", i
        time.sleep(2)
        monitors, nodes, edges, components = [],[],[],[]
        for number_of_monitors in range(50,stop,50):
            yut = algorithm3.alg3(graph, i)
            monitor = yut.pick_start()
            while not yut.stop(number_of_monitors):
                yut.add_neighbors(monitor)
                monitor = yut.place_next_monitor(monitor, prob)


            monitors.append(len(yut.monitor_set))
            nodes.append(yut.result_graph.number_of_nodes())
            edges.append(yut.result_graph.number_of_edges())
            components.append(nx.number_connected_components(yut.result_graph))

        overall_monitors.append(monitors)
        overall_nodes.append(nodes)
        overall_edges.append(edges)
        overall_components.append(components)

        #write the last iteration graph at the max number of monitors once per p
        nx.write_gexf(yut.result_graph,
                "/users/erik/desktop/inferred_graphp"+str(prob) + ".gexf")

#merges lists together with the zip function to make one list
    monitor_tuples = zip(*overall_monitors)
    node_tuples = zip(*overall_nodes)
    edge_tuples = zip(*overall_edges)
    component_tuples = zip(*overall_components)
   
    average_monitors = [np.mean(x) for x in monitor_tuples]
    average_nodes = [np.mean(x) for x in node_tuples]
    average_edges = [np.mean(x) for x in edge_tuples]
    average_components = [np.mean(x) for x in component_tuples]
#Finds average percent of nodes, edges, and percent of monitors utilized to find
#percent of vertices and edges of the given network
    mon_percent = [float(x)/original_num_nodes * 100 for x in average_monitors]
    node_percent = [float(x)/original_num_nodes * 100 for x in average_nodes]
    edge_percent = [float(x)/original_num_edges * 100 for x in average_edges]
#Writes this for user
    stats.write("Prob = " + str(prob) + '\n')
    stats.write("Average percent of nodes found = " + str(node_percent[-1]) + '\n')
    stats.write("Average percent of edges found = " + str(edge_percent[-1]) + '\n')
    stats.write("Average components found = " + str(average_components[-1]) + '\n')

    mon_dict[prob] = mon_percent
    node_dict[prob] = node_percent 
    edge_dict[prob] = edge_percent 

roverall_monitors, roverall_nodes, roverall_edges, roverall_components = [],[],[],[]
for i in range(0,25):
    rmonitors, rnodes, redges, components = [],[],[], []
    for number_of_monitors in range(50,stop,50):
        #instantiates an instance of the graph inference class
        #random seed is the second number
        yut = randomwalk.RW(graph, i)
        monitor = yut.pick_start()
        while not yut.stop(number_of_monitors):
            yut.add_neighbors(monitor)
            monitor = yut.place_next_monitor(monitor)
#len finds the length of each list
        rmonitors.append(len(yut.monitor_set))
        rnodes.append(yut.result_graph.number_of_nodes())
        redges.append(yut.result_graph.number_of_edges())

    roverall_monitors.append(rmonitors)
    roverall_nodes.append(rnodes)
    roverall_edges.append(redges)

    
#merges lists together with the zip function to make one list
rmonitor_tuples = zip(*roverall_monitors)
rnode_tuples = zip(*roverall_nodes)
redge_tuples = zip(*roverall_edges)
raverage_monitors = [np.mean(x) for x in rmonitor_tuples]
raverage_nodes = [np.mean(x) for x in rnode_tuples]
raverage_edges = [np.mean(x) for x in redge_tuples]

#Calculates percents found of monitors, nodes, and edges to use for graphs
rmon_percent = [float(x)/original_num_nodes * 100 for x in raverage_monitors]
rnode_percent = [float(x)/original_num_nodes * 100 for x in raverage_nodes]
redge_percent = [float(x)/original_num_edges * 100 for x in raverage_edges]
stats.close()


#points may need to be modified if more than 9 lines need to go on 1 plot;
#plots all information calculated with specifications
points = ['-bs', '-gH', '-kD', '-ro', '-y*', '-cv', '-rd', '-bp', '-rx']
fig = plt.figure()
fig.suptitle('Average % of nodes discovered')
ax = fig.add_subplot(111)
ax.set_xlabel('% node monitors')
ax.set_ylabel('% nodes discovered')
ax.axis([0,50,0,100])
i = 0
for k in node_dict.keys():
    ax.plot(mon_dict[k], node_dict[k],points[i],label='p =' + str(k))
    i += 1
ax.plot(omon_percent, onode_percent, label='localHDN')
ax.plot(mlmon_percent, mlnode_percent, label='localLDN')
ax.plot(rmon_percent, rnode_percent, label='RW')
plt.legend(loc=4, fontsize=10)
plt.grid(True)
plt.savefig('nodes.pdf')
plt.show()

fig = plt.figure()
fig.suptitle('Average % of edges discovered')
ax = fig.add_subplot(111)
ax.set_xlabel('% node monitors')
ax.set_ylabel('% edges discovered')
ax.axis([0,50,0,100])
i = 0
for k in node_dict.keys():
    ax.plot(mon_dict[k], edge_dict[k],points[i],label='p =' + str(k))
    i += 1
ax.plot(omon_percent, oedge_percent, label='localHDN')
ax.plot(mlmon_percent, mledge_percent, label='localLDN')
ax.plot(rmon_percent, redge_percent, label='RW')
plt.legend(loc=4, fontsize=10)
plt.grid(True)
plt.savefig('edges.pdf')
plt.show()
