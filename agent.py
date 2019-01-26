import random as rd 
import itertools
import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()



#-------------------------------------------
class Allocation:

        def __init__(self,agents,nb_objects, alloc=None):
            self.nb_agents = len(agents)
            self.nb_objects = nb_objects
            self.agents = agents
            if alloc == None:
                self.al = [[-1] * (self.nb_objects//self.nb_agents) for i in range(self.nb_agents)] 
            else:
                self.al = alloc

        def _allocate(self,a,o):
            for obj in range(self.nb_objects//self.nb_agents):
                if self.al[a][obj] == -1:
                    self.al[a][obj] = o
                    return 1
            return -1

        def set_agents(self,agents):
            self.agents = agents

        def get_alloc(self):
            return self.al

        def copy(self):
            new_alloc = Allocation(self.agents, self.nb_objects)
            for a in range(len(self.agents)):
                for obj in range(self.nb_objects//self.nb_agents):
                    new_alloc._allocate(a,self.al[a][obj])
            return new_alloc
                
        def allocate(self,o):
            a = Allocation(self.agents,self.nb_objects)
            if(len(o)==len(self.agents)):
                for a in range(len(self.agents)):
                    self._allocate(a,o[a])
            else:
                 print("Cannot allocate, too few or too much objects")          

        def show(self):
            for a in range(self.nb_agents):
                print("Allocation agent n {0}:".format(a))
                print("-------------------")
                print("| Object |  Ranks |")
                print("-------------------")
                for o in range(self.nb_objects/self.nb_agents):
                    print("|   {0}\t |   {1}\t  |".format(self.al[a][o],self.agents[a].rank(self.al[a][o])))
                print("-------------------")
                print(" ")

        def simple_show(self):
            print(self.al)

        def compute_utility(self):
            utility = [0]*self.nb_agents
            for a in range(self.nb_agents):
                for o in range(self.nb_objects//self.nb_agents):
                    utility[a] += self.nb_objects - self.agents[a].rank(self.al[a][o])
            return utility

        def pareto_optimal(self):
            for a in range(self.nb_agents):
                for ao in range(self.nb_agents):
                    if ao!=a:
                        for o in range(self.nb_objects//self.nb_agents):
                            for o2 in range(self.nb_objects//self.nb_agents):
                                if self.agents[a].rank(self.al[a][o]) > self.agents[ao].rank(self.al[a][o]) and self.agents[a].rank(self.al[ao][o2]) < self.agents[ao].rank(self.al[ao][o2]):
                                    #print "Agents ( ", a, " , ", ao, "):  [", self.al[a][o], " , ", self.al[ao][o2], "]"
                                    return False
            return True

#-------------------------------------------
class Agent:

    def __init__(self, nb_obj, prefs = None):

        if(nb_obj % 3 != 0):
            raise ValueError('The number of object to allocate is not a multiple of 3')

        if prefs != None:
            # Initialize agents preferences with those given in arg
            self.prefs = prefs

        else:
            # Initialize the preferences of the agent over the objects (Borda style) 
            self.prefs = [None]*nb_obj;
            # Initialize lists that are used to generate a random allocation of preferences
            objects_index = list(range(0, nb_obj))
            prefs = list(range(1, nb_obj + 1))
                    
            # Assign to each item a preference
            for _ in itertools.repeat(None, nb_obj):
                # Choose an object randomly among those left
                chosen_object = objects_index[rd.randint(0, len(objects_index) - 1)]
                objects_index.remove(chosen_object)
                # Choose a pref randomly among those left
                chosen_pref = prefs[rd.randint(0, len(prefs) - 1)]
                prefs.remove(chosen_pref)
                # Assign chosen
                self.prefs[chosen_object] = chosen_pref

        ranks = self.prefs[:]
        self.ranked_obj = ranks[:]
        for i in range(len(self.ranked_obj)):
            self.ranked_obj[i] = np.argmin([x for x in ranks if x is not None]) 
            ranks[ self.ranked_obj[i]] = nb_obj + 1

    def get_prefs(self):
        return self.prefs

    def show_preferences(self):
        print(self.prefs)

    def show_ranked_obj(self):
        print(self.ranked_obj)

    def rank(self,obj):
        return self.prefs[obj]

    def top(self,V):
        top = V[0]
        for obj in V:
            if self.prefs[obj] < self.prefs[top]:
                top = obj
        return top

    def last(self,V):
        last = V[0]
        for obj in V:
            if self.prefs[obj] > self.prefs[top]:
                top = obj
        return last

    def sb(self,V):
            W = V[:]
            W.remove(self.top(W))
            return self.top(W)

    def H(self,V,l):
            h = []
            Hlist = []
            if l >=  len(self.ranked_obj):
                l= len(self.ranked_obj)-1
            for obj in V:
                for i in range(l):
                    if obj == self.ranked_obj[i]:
                        Hlist.append(obj)
            return Hlist

#-------------------------------------------
class AllAgents:

    def __init__(self, nb_obj):
        std_prefs = [i for i in range (1, nb_obj + 1)]
        all_prefs = list(itertools.permutations(std_prefs))
        self.all_agents_sets = []
        for i in range(0, len(all_prefs)):              # Agent 1
            for j in range(0, len(all_prefs)):          # Agent 2
                for k in range(0, len(all_prefs)):      # Agent 3
                    self.all_agents_sets.append([Agent(nb_obj, list(all_prefs[i])), Agent(nb_obj, list(all_prefs[j])), Agent(nb_obj, list(all_prefs[k]))])

    def show_all_preferences(self):
        print("Number of sets: " + str(len(self.all_agents_sets)))
        for i in range(0, len(self.all_agents_sets)):
            print("-------------------")
            print(str(i + 1) + "th set")
            print("Agent 1:")
            self.all_agents_sets[i][0].show_preferences()
            print("Agent 2:")
            self.all_agents_sets[i][1].show_preferences()
            print("Agent 3:")
            self.all_agents_sets[i][2].show_preferences()

    def get_all_sets(self):
        return self.all_agents_sets

#-------------------------------------------
class AllAllocations:

    def __init__(self, nb_obj):
        std_objs = [i for i in range (0, nb_obj)]
        all_objs = list(itertools.permutations(std_objs))

        # Space-time tradeoff, should we use list or dict ? 
        self.all_allocs = {}
        for i in range(0, len(all_objs)):
            add_cpt = 0
            one_alloc = list(all_objs[i])
            new_alloc = [one_alloc[x:x+len(one_alloc)//3] for x in range(0, len(one_alloc), len(one_alloc)//3)]
            for k in range(0, len(self.all_allocs)):
                if add_cpt != 2:
                    add_cpt = 0
                    for j in range(0, len(new_alloc)):
                        if add_cpt == 2:
                            break
                        if(Counter(self.all_allocs[k].get_alloc()[j]) == Counter(new_alloc[j])):
                            add_cpt += 1
                else:
                    break
            if add_cpt != 2: # We only add an allocation if its not already in the database(i.e all 3 allocations for each agent are different)
                self.all_allocs[len(self.all_allocs)] = Allocation([Agent(nb_obj),Agent(nb_obj), Agent(nb_obj)], nb_obj, new_alloc)

    def show_all_allocs(self):
        print("Number of allocs: " + str(len(self.all_allocs)))
        for i in range(0, len(self.all_allocs)):
            print("-------------------")
            print(str(i + 1) + "th alloc")
            self.all_allocs[i].simple_show()

def main():
    nb_obj = 9
    try:
        a = Agent(nb_obj)
        b = Agent(nb_obj)
    except ValueError as error:
        raise error.with_traceback(sys.exc_info()[2])

def prefs_are_not_same(a, b, c):
    if(a.get_prefs() == b.get_prefs() and a.get_prefs() == c.get_prefs() and b.get_prefs() == c.get_prefs()):
        return False
    return True

#-------------------------------------------
if __name__ == '__main__':
    main()
