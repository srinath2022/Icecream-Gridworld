

class BayesFilter:
	# T   : Transition probabilities - a dictionary of (s,a,s') -> p
	# S   : List of all states
	# OP  : Observation Probabilities - a dictionary of (|S|*|O| -> p) entries
	# s_i : Initial state of the agent
	def __init__(self, TP, S, OP, s_i):
		# Belief : Mapping from state to probability
		self.Belief = dict.fromkeys(S, 0)
		self.Belief[s_i] = 1
		self.TP = TP
		self.S = S
		self.OP = OP

	# Update belief based on the action taken
	def read_action(a):
		updatedBelief = dict.fromkeys(self.S, 0)
		for state in self.S:
			for probable_curr_state in self.S:
				if self.Belief[probable_curr_state] != 0:
					updatedBelief[state] += self.TP[(probable_curr_state, a, state)] * self.Belief[probable_curr_state]

		self.Belief = updatedBelief

	# Update belief based on the observation
	def read_observation(o):
		for state in self.S:
			self.Belief[state] = self.Belief[state] * self.OP[(state, o)]

		# normalise
		factor=1.0/sum(self.Belief.itervalues())
		for state in self.S:
			self.Belief[state] = self.Belief[state] * factor

	# Get State Estimate : for visualisation
	def get_state_estimate():
		return self.Belief

