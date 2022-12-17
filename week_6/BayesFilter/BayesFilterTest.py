from GridWorldMDP import GridWorldMDP
from BayesFilter import BayesFilter

M = 5 # rows
N = 5 # columns
initial_position = (0,0)
initial_state = initial_position[0]*N+initial_position[1]
mdp = GridWorldMDP(M, N, initial_state)

# construct all states(S), transition probabilities(TP), observation probabilities(OP) required for Bayesian Filter
S = []
A = []
TP = {}
OP = {}

# states
for x in range(M):
	for y in range(N):
		S.append((x,y))

# actions
A = ['L', 'R', 'U', 'D', 'S']

# transition probabilities
for s in S:
	for a in A:
		for s_next in S:
			TP[(s,a,s_next)] = calculate_transition_probability(s,a,s_next)


def calculate_transition_probability(s, a, s_next):
