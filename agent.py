import random as rd 
import itertools
import sys
import numpy as np



#-------------------------------------------
class Allocation:

        def __init__(self,agents,nb_objects):
                self.nb_agents = len(agents)
                self.nb_objects = nb_objects
                self.agents = agents
                self.al = [[-1] * (self.nb_objects/self.nb_agents) for i in range(self.nb_agents)] 

        def _allocate(self,a,o):
                for obj in range(self.nb_objects/self.nb_agents):
                        if self.al[a][obj] == -1:
                                self.al[a][obj] = o
                                return 1
                return -1
        def copy(self):
                new_alloc = Allocation(self.agents, self.nb_objects)
                for a in range(len(self.agents)):
                        for obj in range(self.nb_objects/self.nb_agents):
                                new_alloc._allocate(a,self.al[a][obj])
                return new_alloc
                
        def allocate(self,o):
                a = Allocation(self.agents,self.nb_objects)
                if(len(o)==len(self.agents)):
                        for a in range(len(self.agents)):
                                self._allocate(a,o[a])
                else:
                     print "cannot allocate, too few objects"           

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
                        for o in range(self.nb_objects/self.nb_agents):
                                utility[a] += self.nb_objects - self.agents[a].rank(self.al[a][o])
                return utility

        def pareto_optimal(self):
                for a in range(self.nb_agents):
                        for ao in range(self.nb_objects/self.nb_agents):
                                if ao!=a:
                                        for o in range(self.nb_objects/self.nb_agents):
                                                for o2 in range(self.nb_objects/self.nb_agents):
                                                        if self.agents[a].rank(self.al[a][o]) > self.agents[ao].rank(self.al[a][o]) and self.agents[a].rank(self.al[ao][o2]) < self.agents[ao].rank(self.al[ao][o2]):
                                                                #print "Agents ( ", a, " , ", ao, "):  [", self.al[a][o], " , ", self.al[ao][o2], "]"
                                                                return False
                return True
                                
#-------------------------------------------
class Agent:

	def __init__(self, nb_obj):
		if(nb_obj % 3 != 0):
			raise ValueError('The number of object to allocate is not a multiple of 3')

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
                        self.ranked_obj[i] = np.argmin(ranks) 
                        ranks[ np.argmin(ranks)] = nb_obj + 1

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



def main():
	nb_obj = 9
	try:
		a = Agent(nb_obj)
		b = Agent(nb_obj)
	except ValueError as error:
  		raise error.with_traceback(sys.exc_info()[2])

        

#-------------------------------------------
if __name__ == '__main__':
	main()
