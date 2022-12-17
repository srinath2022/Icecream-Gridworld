from abc import ABC, abstractmethod


class MDP(ABC):

	def __init__(self, Ns, Na):
		self.Nstates = Ns
		self.Nactions = Na
		pass

	# get i th State
	@abstractmethod
	def getState(self, i):
		pass

	# get i th Action
	@abstractmethod
	def getAction(self, i):
		pass

	# Transition probability for triplet (state_i, action_j, state_k)
	@abstractmethod
	def getTransitionProbability(self, i, j, k):
		pass

	# Next state we get when we try to take an acton 
	@abstractmethod
	def getNextState(self, i , j):
		pass

	# The reward you get when transitioning from state i to state k by taking action j
	@abstractmethod
	def getReward(self, i , j, k):
		pass

	# drawing function to visualise our MDP
	@abstractmethod
	def visualise(self):
		pass
