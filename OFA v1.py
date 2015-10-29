#Data collection for Optimal Flow Predictve Mdoeling

from __future__ import division
import operator
import time
from numpy import * 
import math
from gurobipy import *
import matplotlib.pyplot as plt
import random

#path = sys.path
#path.append('C:\Users\\nich8038\Documents\Research and Grants\Research\PythonModules')

import randFCNF as RN
#import CreateTSFCNetwork as CN   

def CharacterizeArcsIJK (f, m, problemID, seed, numNodes, Nodes, commodities, arcs, varcost, fixedcost, requirements, solution, arcsUsed, LPSolution):
    
    networkSupply = 0
    
    for i in Nodes:
        if requirements[i,0] > 0:
            networkSupply = networkSupply + requirements[i,0]  
    
    for i,j in arcs:
        fromNodeReq = requirements[i,0]
        toNodeReq = requirements[j,0]
        
        fromOutDegree = 0
        fromOutSupplyDegree = 0
        fromOutSupplyAmt = 0
        fromOutDemandDegree = 0
        fromOutDemandAmt = 0 
        
        for a,c in arcs.select(i,'*'):
            fromOutDegree = fromOutDegree + 1
            if requirements[c,0] > 0:
                fromOutSupplyDegree = fromOutSupplyDegree + 1
                fromOutSupplyAmt = fromOutSupplyAmt + requirements[c,0]
            elif requirements[c,0] < 0:
                fromOutDemandDegree = fromOutDemandDegree + 1
                fromOutDemandAmt = fromOutDemandAmt + requirements[c,0]                
        
        fromInDegree = 0
        fromInSupplyDegree = 0
        fromInSupplyAmt = 0
        fromInDemandDegree = 0
        fromInDemandAmt = 0 
        
        for a,c in arcs.select('*',i):
            fromInDegree = fromInDegree + 1
            if requirements[c,0] > 0:
                fromInSupplyDegree = fromInSupplyDegree + 1
                fromInSupplyAmt = fromInSupplyAmt + requirements[c,0]
            elif requirements[c,0] < 0:
                fromInDemandDegree = fromInDemandDegree + 1
                fromInDemandAmt = fromInDemandAmt + requirements[c,0]    
 
        toOutDegree = 0
        toOutSupplyDegree = 0
        toOutSupplyAmt = 0
        toOutDemandDegree = 0
        toOutDemandAmt = 0 
        
        for a,c in arcs.select(j,'*'):
            toOutDegree = toOutDegree + 1
            if requirements[c,0] > 0:
                toOutSupplyDegree = toOutSupplyDegree + 1
                toOutSupplyAmt = toOutSupplyAmt + requirements[c,0]
            elif requirements[c,0] < 0:
                toOutDemandDegree = toOutDemandDegree + 1
                toOutDemandAmt = toOutDemandAmt + requirements[c,0]                
        
        toInDegree = 0
        toInSupplyDegree = 0
        toInSupplyAmt = 0
        toInDemandDegree = 0
        toInDemandAmt = 0 
        
        for a,c in arcs.select('*',j):
            toInDegree = toInDegree + 1
            if requirements[c,0] > 0:
                toInSupplyDegree = toInSupplyDegree + 1
                toInSupplyAmt = toInSupplyAmt + requirements[c,0]
            elif requirements[c,0] < 0:
                toInDemandDegree = toInDemandDegree + 1
                toInDemandAmt = toInDemandAmt + requirements[c,0]    
        
        f.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(problemID, seed, numNodes, networkSupply, i,j,arcsUsed[i,j], solution[i,j,0], LPSolution[i,j,0], varcost[i,j,0], fixedcost[i,j], fromNodeReq, toNodeReq, fromOutDegree, fromOutSupplyDegree, fromOutSupplyAmt, fromOutDemandDegree, fromOutDemandAmt, fromInDegree,  fromInSupplyDegree, fromInSupplyAmt, fromInDemandDegree, fromInDemandAmt,toOutDegree, toOutSupplyDegree, toOutSupplyAmt, toOutDemandDegree, toOutDemandAmt, toInDegree,  toInSupplyDegree, toInSupplyAmt, toInDemandDegree, toInDemandAmt)) 








#FCNFgenerator usage:
#               (seed, model var, node count , supplyPct, demandPct, rhsMin, rhsMax, cMin, cMax, fMin, fMax, K, arcs, Sparse = -1):


rhsMin = 1000
rhsMax = 2000
cMin = 0 
cMax = 10
fMin = 20000
fMax = 60000
K = 1 


seed=2200
seedMin = seed
seedMax = seed * 10000

f = open('OSA_DATA_20131511_RANDGEM.txt','w')
f.close()
g = open('OSA_PROBS_20131511_RANDGEM.txt','w')
g.close()

arcs=[]
decision = {}
flow = {}
varcost = {}
fixedcost = {}
problemID = -1

for seed in range(seedMin,seedMax,10):
      
    problemID += 1
    
    m = Model('GenFCNF')
    m.setParam( 'OutputFlag', 0 ) 
    m.setParam( 'LogToConsole', 0 )
    m.setParam( 'LogFile', "" )   
    m.params.threads = 1
    m.params.NodefileStart = 0.5
    m.params.timeLimit = 1800

    arcs[:]=[]
    decision.clear()
    flow.clear()
    varcost.clear()
    fixedcost.clear() 
    
    random.seed(seed)
    
    nodeCnt = random.randint(15, 25)
    supplyPct = random.uniform(0.15,0.45)
    demandPct = random.uniform(0.15,0.45)   
    
    RQ = RN.FCNFgenerator(seed, m, nodeCnt, supplyPct, demandPct, rhsMin, rhsMax, cMin, cMax, fMin, fMax, K, arcs)
    commodities = range(0,K)
    arcs=tuplelist(arcs)
    noV = len(arcs)
    
    
    g = open('OSA_PROBS_20131511_RANDGEM.txt','a')
    g.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},'.format(problemID, seed, nodeCnt, len(arcs), m.NumVars,m.NumBinVars, m.NumConstrs, supplyPct, demandPct, rhsMin, rhsMax, cMin, cMax, fMin, fMax, K))
    g.close()        
    
    m.optimize()   #get optimal solution for testing...
    
    
    if m.status == 2 or m.status == 9:    
        
        g = open('OSA_PROBS_20131511_RANDGEM.txt','a')
        g.write('{},{},{},{},{},{},'.format(m.status, m.objval, m.Runtime, m.MIPgap, m.NodeCount, m.IterCount))
        g.close()            
    
        for i,j in arcs:
            for k in range(K):
                flow[i,j,k] = m.getVarByName('flow_%s_%s_%s' % (i, j, k))        #create dictionary of continuous variables
                varcost[i,j,k] = flow[i,j,k].Obj                                 #extract varcosts from model   
            decision[i,j] = m.getVarByName('decision_%s_%s' % (i,j))             #create dictionary of binary variables
            fixedcost[i,j] = decision[i,j].Obj                                   #extract fixed costs from model
    
        solution = m.getAttr('x', flow) 
        arcsUsed = m.getAttr('x', decision)
                        
        for i,j in arcs:
            for k in range(K):
                decision[i,j].vType = GRB.CONTINUOUS      
        
        m.optimize()
        
        g = open('OSA_PROBS_20131511_RANDGEM.txt','a')
        g.write('{}\n'.format(m.objval))
        g.close()      
        
        LPsolution = m.getAttr('x', flow) 
       
        f = open('OSA_DATA_20131511_RANDGEM.txt','a') 
        Nodes = range(0,nodeCnt)
        CharacterizeArcsIJK (f, m, problemID, seed, nodeCnt, Nodes, commodities, arcs, varcost, fixedcost, RQ, solution, arcsUsed, LPsolution)
        f.close()
        
    else:
        
        g = open('OSA_PROBS_20131511_RANDGEM.txt','a')
        g.write(',,,,,,\n')
        g.close()         
    
    
  