
import random
from Graph import Graph
import numpy as np
rng = np.random.default_rng()

# compute the distance between two states
def compute_distance(state1, state2):
	# using squared eucledian distance for chess problem
	x1 = state1[0]
	y1 = state1[1]
	x2 = state2[0]
	y2 = state2[1]
	return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)

# get the nearby valid reachable states to state
def get_valid_reachable_states(G, state, mdp):
	mdp_state = mdp.makeState(state[0], state[1])
	immediate_next_states = mdp.getValidNextStates(mdp_state)
	valid_reachable_states = []
	curr_states_in_G = G.get_vertex_set()
	for state in immediate_next_states:
		if mdp.getState(state) not in curr_states_in_G:
			valid_reachable_states.append(mdp.getState(state))
	return valid_reachable_states

# C - a list of all states - [(x,y),(x,y)]
# start - start state - (x,y)
# goal - goal state - (x,y)
def RRT(C, start, goal, mdp):
	# initialisation
	G = Graph()
	G.add_vertex(start)

	while True:
		# randomly smaple s_rand from C
		# i = random.randint(0, len(C)-1)
		# s_rand = C[i]
		igrs = rng.integers(low=[0,0], high=[20,20], size=[1,2])
		s_rand = (igrs[0][0], igrs[0][1])

		# find nearest point in V to s_rand
		s_nearest = None
		s_nearest_dist = float('inf')

		for s in G.get_vertex_set():
			dist = compute_distance(s, s_rand)
			if dist<s_nearest_dist:
				s_nearest = s
				s_nearest_dist = dist

		# make a move towards s_rand from s_nearest to get s_new
		# for chess, I am considering to check 8 nearby states of s_nearest and choose which is closer to s_rand
		s_new = None
		s_new_dist = float('inf')
		if s_nearest is not None:
			valid_reachable_states = get_valid_reachable_states(G, s_nearest, mdp)
			for s in valid_reachable_states:
				dist = compute_distance(s, s_rand)
				if dist<s_new_dist:
					s_new = s
					s_new_dist = dist


		if s_new is not None:
			G.add_vertex(s_new)
			G.add_edge(s_nearest, s_new)
			mdp.jumpToState(s_new)
			mdp.visualise()
			if s_new == goal:
				print("FOUND")
				return 1
