import random as rd 
import itertools
import sys

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

	def show_preferences(self):
		print(self.prefs)

#-------------------------------------------
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