'''
This code has the matplotlib things we have been using to plot data.
Currently it's set up for 8 algorithms, but if you are only displaying 
one data set, everything can be pared down.

Key things are:
Importing the correct JSON file name (this have not been adjusted)
Creating the plots with matplotlib
Creating all the axes etc.
Showing the plot.

Code written/adjusted by Brittany Reynolds, 2015
'''

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sys
import time
import json

graph_name="ER_random-1" #name to call it by
Graph_Name= "Facebook"  #name you want on top of plot
alg_name1="UBDn"
alg_name2="HLD_r"
alg_name3="HC"
alg_name4="HGD_LS"
alg_name5="HGD_LS_r2"
alg_name6="FDD"
alg_name7="FDD_r2"
alg_name8="RPS"

infile=open('JSON_Files/mon_percent_'+graph_name, 'r')
monplotlist=json.load(infile)
infile.close()

infile=open('JSON_Files/'+alg_name1+'_nodes_percent_fnd_'+graph_name, 'r')
nodes_percent_fnd=json.load(infile)
infile.close()

infile=open('JSON_Files/'+alg_name2+'_nodes_percent_fnd_'+graph_name, 'r')
nodes_percent_fnd2=json.load(infile)
infile.close()

infile=open('JSON_Files/'+alg_name3+'_nodes_percent_fnd_'+graph_name, 'r')
nodes_percent_fnd3=json.load(infile)
infile.close()

infile=open('JSON_Files/'+alg_name4+'_nodes_percent_fnd_'+graph_name, 'r')
nodes_percent_fnd4=json.load(infile)
infile.close()

infile=open('JSON_Files/'+alg_name5+'_nodes_percent_fnd_'+graph_name, 'r')
nodes_percent_fnd5=json.load(infile)
infile.close()

infile=open('JSON_Files/'+alg_name6+'_nodes_percent_fnd_'+graph_name, 'r')
nodes_percent_fnd6=json.load(infile)
infile.close()

infile=open('JSON_Files/'+alg_name7+'_nodes_percent_fnd_'+graph_name, 'r')
nodes_percent_fnd7=json.load(infile)
infile.close()

infile=open('JSON_Files/'+alg_name8+'_nodes_percent_fnd_'+graph_name, 'r')
nodes_percent_fnd8=json.load(infile)
infile.close()



#print len(monplotlist)
#print len(nodes_percent_fnd)
#print len(nodes_percent_fnd2)
#print len(nodes_percent_fnd3)
#print len(edges_percent_fnd)
#print len(edges_percent_fnd2)
#print len(edges_percent_fnd3)

#Plot1 = plt.plot(monplotlist, nodes_percent_fnd, 'ro', color='red', label='Nodes1')
#Plot2 = plt.plot(monplotlist, nodes_percent_fnd2, 'ro', color='blue', label='Nodes2')
#Plot3 = plt.plot(monplotlist, nodes_percent_fnd3, 'ro', color='green', label='Nodes3')
Plot1 = plt.plot(monplotlist, nodes_percent_fnd, 'g*', label='Nodes1')
Plot2 = plt.plot(monplotlist, nodes_percent_fnd2, 'mx', label='Nodes2')
Plot3 = plt.plot(monplotlist, nodes_percent_fnd3, 'bx', label='Nodes3')
Plot4 = plt.plot(monplotlist, nodes_percent_fnd4, 'm+', label='Nodes4')
Plot5 = plt.plot(monplotlist, nodes_percent_fnd5, 'b+', label='Nodes5')
Plot6 = plt.plot(monplotlist, nodes_percent_fnd6, 'mo', label='Nodes6')
Plot7 = plt.plot(monplotlist, nodes_percent_fnd7, 'b.', label='Nodes7')
Plot8 = plt.plot(monplotlist, nodes_percent_fnd8, 'g*', label='Nodes8')

red_dot,=Plot1
blue_dot,=Plot2
green_dot,=Plot3
yellow_dot,=Plot4
magenta_dot,=Plot5
cyan_dot,=Plot6
black_dot,=Plot7
orange_dot,=Plot8
fontsize=20
Plot1+Plot2+Plot3+Plot4+Plot5+Plot6+Plot7+Plot8  #+Plot7+Plot8+Plot9+Plot10+Plot11+Plot12
plt.axis([19,50,79, 100.5])
plt.legend([red_dot, blue_dot, green_dot, yellow_dot, magenta_dot, cyan_dot, black_dot, orange_dot,], [ alg_name1, alg_name2, alg_name3,alg_name4,"HGD_LS_wR", "FDD" ,"FDD_wR",alg_name8,], loc=4)
#plt.suptitle(Graph_Name, fontsize=24)
plt.xlabel('% of nodes covered with monitors', fontsize=24)
plt.ylabel('% found', fontsize=24)
#grid('on')
#myaxes.xaxis.grid(True)
#myaxes.set_axisbelow(True)
#ax = plt.gca()
#ax.grid(True)
#ax.axhline(0,color='black',lw=2)
#ax.grid(b=True, which='major',color='b', linestyle='-')
ax = plt.gca()
ax.grid(True)
plt.show()







