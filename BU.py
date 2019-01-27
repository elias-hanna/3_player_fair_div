import random as rd 
import itertools
import sys
import numpy as np


from agent import Agent
from agent import Allocation

def run_BU(agents, nb_objects):
    objects = [i for i in range(nb_objects)]
    allocs = BU(agents, objects)
    allocations = []
    for al in allocs:
    	allocations.append(Allocation(agents, nb_objects, al))
    return allocations

def BU(agents, objects):
	al = [[list(),list(),list()], [list(),list(),list()], [list(),list(),list()]]
	nb_objects = len(objects)
	
	# Changing the starting agent
	for first_agent in range(0,len(agents)):
		objects_copy = objects.copy()
		for i in range(0 + first_agent, nb_objects + first_agent):
			last = agents[i%3].last_from_list(objects_copy)
			objects_copy.remove(last)
			al[first_agent][i%3 - 1].append(last)

	return al