'''

Created by Karl Schmitt, Nicholas Juliano, Brittany Reynolds, Erin Moore, Ralucca Gera, and Erik
Original Created on Jan 25, 2015
Commit Date 7/27/2015

You may contact the primary author at:
karl <dot> schmitt <at> valpo <dot> edu

Copyright (C) 2015, Karl R. B. Schmitt & Ralucca Gera

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


'''

import argparse
import networkx as nx
#import matplotlib.pyplot as plt
#import matplotlib
import json
import numpy as np
import sys
import importlib
import os


def main(args):

    #Print the args/namespace to confirm everything got entered that I thought got entered.
    print args

    #sys.path.append('C:\\Users\\kschmit1\\Documents\\GitHub\\Graph_Infer\\Networks')
    #sys.path.append('C:\\Users\\kschmit1\\Documents\\GitHub\\Graph_Infer\\Clean_Algorithms')
    #print sys.path
    
    graphdic={} #Empty graph dictionary to load in graphs for inference on.
    algsM={}; #Empty dictionary which will import each inference algorithm
    
    if args.printalgs:
        #Print the list of valid short argument names
        print "Valid Algorithm are:"
        print "Algorithms with 'r' require a parameter for restarting"
        print "Algorithms with 'p' require a parameter for probability"
        print "Cannot currently run algorithms with both a 'p' and 'r' in same call"
        print "UBDn      : Upper Bound Discovery for nodes"
        print "UBDe      : Upper Bound Discovery for edges"
        print "FDD       : Fake-Degree Discovery. Fake Degree is # of unseen neighbors"
        print "FDD_r     : Fake-Degree Discovery. Includes restart after 2 monitors with no new nodes added"
        print "HGD_LS    : Highest Global Degree, Least Seen"
        print "HGD_LS_r  : Highest Global Degree, Least Seen, restart after 2 with no new info."
        print "HC_p      : Hill-Climbing with Probablistic Restart"
        print "HC_pL     : Hill-Climbing with Probablistic Restart, walk < log(#nodes)"
        print "HC_pF     : Hill-Climbing with Probablistic Restart, 1/2 neighbors monitors"
        print "HC_pLF    : Hill-Climbing with Prob. Restart, walk < log(#nodes), 1/2 neighbors monitors"
        print "HLD_p     : Highest Local Degree, restart if no monitorless neighbors**Might have error"
        print "HLD_L     : Highest Local Degree, restart if walk > log(#nodes)"
        print "HLD_F     : Highest Local Degree, restart if 1/2 neighbors have monitors"
        print "HLD_LF    : Highest Local Degree, restart if walk> log(#nodes) or 1/2 neighbors"
        print "HLD_pL    : Highest Local Degree Probablistic Restart, walk < log(#nodes)**Might have error"
        print "HLD_pF    : Highest Local Degree Probablistic Restart, 1/2 neighbors monitors**Might have error"
        print "HLD_pLF   : Highest Local Degree Probablistic Restart, walk < log(#nodes), 1/2 neighbors monitors**Might have error"
        print "RPS       : Random Placement Smart, (no placement on monitors)"
        print "RPD       : Random Placement Dumb, could place on monitor (don't use this)"
        print "RWS       : Random Walk Smart, walk can't choose neighbors w/ monitors"
        print "RWD       : Random Walk Dumb, walk can choose neighbors w/ monitors"
        
        
        
        
        return
    elif not args.graph_name:
        #Makes sure there's one graph to run on.
        
        print "No input graphs defined. Defaulting to barabasi."
        try:
            args.graph_name.append('barabasi')
        except:
            sys.exit("Could not import any graph!")
            
    elif args.alg_name:
        try:           
            filename=args.alg_name[0]+'.py'
            for root,dirs,names in os.walk(args.algpath):
                if filename in names:
                    sys.path.append(root)
        except:
            print "Couldn't find a path to the first algorithm name"
        for alg in args.alg_name:
            try:
                #tmpstr='Clean_Algorithms.HC_p.py'
                algsM[alg]=importlib.import_module(alg)           
            except:
                print "Could not import a module (v1) for Algorithm: ", alg
        
        #Error check to make sure we actually loaded an algorithm.
        if len(algsM)==0:
            try:
                #args.alg_name.append('UBDn')
                algsM[alg]=__import__('FDD')
                print "No valid algorithm input could load. Using FDD"
            except:
                sys.exit("Could not import any algorithm module")
                
    elif not args.alg_name:
        #If no algorithms specified on input line, default to UBDn
        print "No algorithm selected. Defaulting to upper bound, nodes"
        try:
            args.alg_name.append('UBDn')
            algsM[alg]=__import__('UBDn')
        except:
            sys.exit("Could not import any algorithm module")

    #This loops through each graph
    for grph in args.graph_name:
        #Read in the graph to work on.
        try:
            filename=grph+'.gexf'
            for root,dirs,names in os.walk(args.inpath):
                if filename in names:
                    #print os.path.join(root,filename)
                    graphdic[grph]=nx.read_gexf(os.path.join(root,filename))
        except:
            #If we couldn't read the graph in. Give error, and go to next graph
            print "Could not read in graph ", grph
            print "Check file existence, and if in .gexf format"
            continue

        #Running display of status
        print grph + ": start"

        #Compute basic properties and stop condition(s) for graph.
        original_num_nodes = graphdic[grph].number_of_nodes()
        original_num_edges = graphdic[grph].number_of_edges()
        step= int(graphdic[grph].number_of_nodes()/200) #This gives us 2 data points for each % of nodes
        stop = int(graphdic[grph].number_of_nodes()/2 + step) #This stops 1% after 50

        #Check to make sure step/stop are non-zero
        step=max(step,1)
        stop=max(stop,1)

        print "Step: ", step
        print "Stop: ", stop

        #Initialize dictionaries to hold results for each algorithm for monitors, nodes and edges
        algs_mon, algs_node, algs_edge={},{},{}
        for alg in algsM.keys():
            algs_mon[alg]=[]
            algs_node[alg]=[]
            algs_edge[alg]=[]

        #This loops over each trial run.
        for trial in range(args.trials):
            print "Starting Run: {}/{} for {}".format(trial+1,args.trials,grph)

            #Dictionaries to hold in trial values per algorithm.
            mon,node,edge={},{},{}
            infer_objs={}
            curr_mon={}
            
            #Initialize dictionaries for algorithms.
            for alg in algsM.keys():
                mon[alg]=[]
                node[alg]=[]
                edge[alg]=[]
                
                #Build the inference objects/initialize
                infer_objs[alg]=algsM[alg].Alg(graphdic[grph],trial)
                
                #Pick the first monitor, and add it's neighbors.
                curr_mon[alg]=infer_objs[alg].pick_start()
                infer_objs[alg].add_neighbors(curr_mon[alg])
                
                #print "Checking Nodes:", infer_objs[alg].graph.number_of_nodes()
                #print "Checking Nodes:", infer_objs[alg].result_graph.number_of_nodes()
                #print len(mon[alg]), len(node[alg]), len(edge[alg])
                #print "startmon: ", curr_mon[alg]
                #print "Degree is: ", infer_objs[alg].graph.degree(curr_mon[alg])
            

            for ii in range(step,stop,step):

                #Place monitors on 0.5% of the graph.
                for jj in range(step):
                    for alg in algsM.keys():
                        curr_mon[alg]=infer_objs[alg].place_next_monitor(curr_mon[alg], args.params)
                        infer_objs[alg].add_neighbors(curr_mon[alg])

                #Store the data for this 0.5% of the graph
                for alg in algsM.keys():
                    node[alg].append(infer_objs[alg].result_graph.number_of_nodes())
                    mon[alg].append(ii)
                    edge[alg].append(infer_objs[alg].result_graph.number_of_edges())

                #Output a percent complete message for comfort.
                tmp_compl=int(float(ii)*2/original_num_nodes*100)
                print "{}: Run {}/{}: {} complete".format(grph, trial+1, args.trials, tmp_compl)
                #print curr_mon['UBDn']
        
            #End loop to place all monitors
                

            #Save to json, and to multi-trial data structure.
            for alg in algsM.keys():

                #Save all the counts
                algs_mon[alg].append(mon[alg])
                algs_node[alg].append(node[alg])
                algs_edge[alg].append(edge[alg])
                
                if not args.printless:
                    #Output the monitor counts.
                    mon_per=[float(x)/original_num_nodes*100 for x in mon[alg]]
                    outfile=open(args.out_path+alg+'_mon_per_'+grph+'_Trial'+str(trial)+'.json','w')
                    json.dump(mon_per,outfile)
                    outfile.close()

                    #Output the node counts.          
                    node_per=[float(x)/original_num_nodes*100 for x in node[alg]]
                    outfile=open(args.out_path+alg+'_node_per_'+grph+'_Trial'+str(trial)+'.json','w')
                    json.dump(node_per,outfile)
                    outfile.close()

                    #Output the edge counts.
                    edge_per=[float(x)/original_num_edges*100 for x in edge[alg]]
                    outfile=open(args.out_path+alg+'_edge_per_'+grph+'_Trial'+str(trial)+'.json','w')
                    json.dump(edge_per,outfile)
                    outfile.close()

            print "{}: {}/{} runs complete".format(grph, trial+1,args.trials)

        #End loop over multiple trials.
            
        #Check for flag to output averages of all trials.
        if args.mkavg:
            #mon_tuples, node_tuples, edge_tuples={},{},{}
            for alg in algsM.keys():

                #Output averaged monitors
                mon_tuples=zip(*algs_mon[alg])               
                mon_avg=[np.mean(x) for x in mon_tuples]
                mon_avg_per=[float(x)/original_num_nodes*100 for x in mon_avg]
                outfile=open(args.out_path+alg+'_mon_per_avg_'+grph+'_'+str(args.trials)+'Runs.json','w')
                json.dump(mon_avg_per,outfile)
                outfile.close()

                #Output averaged nodes
                node_tuples=zip(*algs_node[alg])               
                node_avg=[np.mean(x) for x in node_tuples]
                node_avg_per=[float(x)/original_num_nodes*100 for x in node_avg]
                outfile=open(args.out_path+alg+'_node_per_avg_'+grph+'_'+str(args.trials)+'Runs.json','w')
                json.dump(node_avg_per,outfile)
                outfile.close()
                outfile=open(args.out_path+alg+'_node_avg_'+grph+'_'+str(args.trials)+'Runs.json','w')
                json.dump(node_avg,outfile)
                outfile.close()
                
                #Output average node std. dev.
                node_std=[np.std(x) for x in node_tuples]
                #node_std_per=[float(x)/original_num_nodes*100 for x in node_std]
                outfile=open(args.out_path+alg+'_node_std_'+grph+'_'+str(args.trials)+'Runs.json','w')
                json.dump(node_std,outfile)
                outfile.close()

                #Output averaged edges
                edge_tuples=zip(*algs_edge[alg])
                edge_avg=[np.mean(x) for x in edge_tuples]
                edge_avg_per=[float(x)/original_num_edges*100 for x in edge_avg]
                outfile=open(args.out_path+alg+'_edge_per_avg_'+grph+'_'+str(args.trials)+'Runs.json','w')
                json.dump(edge_avg_per,outfile)
                outfile.close()
                outfile=open(args.out_path+alg+'_edge_avg_'+grph+'_'+str(args.trials)+'Runs.json','w')
                json.dump(edge_avg,outfile)
                outfile.close()
                
                #Output average edge std. dev.
                edge_std=[np.std(x) for x in edge_tuples]
                #edge_std_per=[float(x)/original_num_edges*100 for x in edge_std]
                outfile=open(args.out_path+alg+'_edge_std_'+grph+'_'+str(args.trials)+'Runs.json','w')
                json.dump(edge_std,outfile)
                outfile.close()

    #End Loop over multiple graphs

    #--------------
    #Here's where I should go through and do plots or such. This could also go inside the graph loop.
    #Have to load back in the correct data for plotting. 
    #--------------


    

if __name__=="__main__":

    parser=argparse.ArgumentParser(description='Command line graph inference', add_help=True)

    #This could be changed to support opening the files on input. But might cause dictionary issues later.
    parser.add_argument('-g', action="append", dest="graph_name", type=str, help='Input Graph(s) in .gexf format')
    parser.add_argument('-i', action="store", type=str, dest='inpath', default=os.getcwd(), help='Path to input graphs')
    parser.add_argument('-I', action="store", type=str, dest='algpath', default=os.getcwd(),help='Path to algorithms')
    parser.add_argument('-a', action="append", dest="alg_name", type=str, help='Algorithms to use')
    parser.add_argument('-p', action="append", dest="params", help='Parameters passed to each Algorithm')
    parser.add_argument('-o', action="store",dest="out_path", type=str, default='', help='Path to output files to')
    parser.add_argument('-t', action="store", dest="trials", type=int, default=1, help='Number of trials to run. Default=1')
    parser.add_argument('-z', action="store_true", dest="viz", default=False, help='Create dynamic visualization. Slow!!')
    parser.add_argument('-f', action="store_true", dest="mkplot", default=False, help='Output a plot of results')
    parser.add_argument('-m', action="store_true", dest="mkavg", default=False, help='Average all the trials in an Algorithm')
    parser.add_argument('-n', action="store_true", dest="printalgs", default=False, help='Print list of valid algorithm names')
    parser.add_argument('-L', action="store_true", dest="printless", default=False, help='Do not output individual trial values')

    args=parser.parse_args()

    main(args)
