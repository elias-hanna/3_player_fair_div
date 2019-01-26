import random as rd 
import itertools
import sys
import numpy as np


from agent import Agent
from agent import Allocation

def removeObj(Hs,os):
    H = []
    #print os
    for o in Hs:
        if(not(o in os)):
            H.append(o)
    return H
        
def run_OS(agents, nb_objects):
    non_allocated_objects = [i  for i in range(nb_objects)]
    a = Allocation(agents,nb_objects)
    return OS(agents, non_allocated_objects, 1, a)
    # non_allocated_objects = [i  for i in range(nb_objects)]
    # l=1
    # while(len(non_allocated_objects) > 0):
        
    #     H0 = agents[0].H(non_allocated_objects,l)
    #     H1 = agents[1].H(non_allocated_objects,l)
    #     H2 = agents[2].H(non_allocated_objects,l)
    #     Hs = []
    #     for obj_a0 in H0:
    #         for obj_a1 in H1:
    #             for obj_a2 in H2:
    #                 Hs.append([obj_a0, obj_a1, obj_a2])    
                     
    #     i=0
    #     while( i < len(Hs)):
    #         h = Hs[i]
    #         if(h[0]!=h[1] and h[1]!=h[2]):
    #             i+=1
    #         else:
    #             Hs.remove(h)
        
    #     for h in Hs:   
    #         if h[0] != h[1] and h[1] != h[2]:
    #             if h[0] in non_allocated_objects and h[1] in non_allocated_objects and h[2] in non_allocated_objects: 
    #                 a.allocate([h[0], h[1], h[2]])
    #                 removeObj(non_allocated_objects,[h[0], h[1], h[2]])
        
    #     l += 1
    return a

def OS(agents, non_allocated_objects, l, from_alloc):
    a = []
   # print "l:"
   # print l
   # print "alloc"
   # print non_allocated_objects

    if(len(non_allocated_objects) > 0):
        
        H0 = agents[0].H(non_allocated_objects,l)
        H1 = agents[1].H(non_allocated_objects,l)
        H2 = agents[2].H(non_allocated_objects,l)
        Hs = []
        for obj_a0 in H0:
            for obj_a1 in H1:
                for obj_a2 in H2:
                    Hs.append([obj_a0, obj_a1, obj_a2])    
        i=0
        while( i < len(Hs)):
            h = Hs[i]
            if(h[0]!=h[1] and h[1]!=h[2] and h[0]!=h[2] ):
                i+=1
            else:
                Hs.remove(h)
        
       # print Hs

        if len(Hs)==0:
            return a + OS(agents,   non_allocated_objects,   l+1,    from_alloc)
        elif len(Hs)==1:
            h=Hs[0]
            copy_alloc = from_alloc.copy()
            copy_alloc.allocate([h[0], h[1], h[2]])
            return  a + OS(agents,   removeObj(non_allocated_objects,[h[0], h[1], h[2]]),   l+1,    copy_alloc)
        
        
        for h in Hs:   
            if h[0] != h[1] and h[1] != h[2]:
                if h[0] in non_allocated_objects and h[1] in non_allocated_objects and h[2] in non_allocated_objects:
                    copy_alloc = from_alloc.copy()
                    copy_alloc.allocate([h[0], h[1], h[2]])
                    a = a + OS(agents,   removeObj(non_allocated_objects,[h[0], h[1], h[2]]),   l,   copy_alloc) 
                    #removeObj(non_allocated_objects,[h[0], h[1], h[2]])
        #print a
        return a
    else:
        #print "r"
        #from_alloc.show()
        return [from_alloc]