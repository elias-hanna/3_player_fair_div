import random as rd 
import itertools
import sys
import numpy as np


from agent import Agent
from agent import Allocation

def run_BU(agents, nb_objects):
    non_allocated_objects = [i  for i in range(nb_objects)]
    a = Allocation(agents,nb_objects)
    return BU(agents, non_allocated_objects, 1, a)

def BU(agents, non_allocated_objects, l, from_alloc):