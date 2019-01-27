import random as rd 
import itertools
import sys
import numpy as np


from agent import Agent
from agent import Allocation

def run_TR(agents, nb_objects):
    objects = [i for i in range(nb_objects)]
    allocs = TR(agents, objects)
    allocations = []
    for al in allocs:
    	allocations.append(Allocation(agents, nb_objects, al))
    return allocations
    
def TR(agents, objects):
	al = [[list(),list(),list()], [list(),list(),list()], [list(),list(),list()]]
	nb_objects = len(objects)
	
	# Changing the starting agent
	for first_agent in range(0, len(agents)):
		objects_copy = objects.copy()
		# For odd number l <= N
		for l in range(0, nb_objects):
			# For each agent
			for m in range(0, len(agents)):
				Hml = agents[(first_agent + m)%3].H(objects_copy, l)
				# If H returns empty list
				if not Hml:
					al[first_agent] = None
					break
				last = agents[(m+1)%3].last_from_list(objects_copy)
				objects_copy.remove(last)
				al[first_agent][m].append(last)
			else:
				continue
			break

	return al