
import copy
import numpy as np
from collections import deque

class Solver():

	def __init__(self, mdp):
		self.mdp = mdp

	def valueIteration(self, H, Gamma):
		Nstates = self.mdp.Nstates
		Nactions = self.mdp.Nactions

		policy = [0 for i in range(Nstates)]

		step = 0
		ValueFxn = np.zeros(Nstates)
		ValueFxnNext = np.zeros(Nstates)
		
		while step < H:
			for state in range(Nstates):
				maxValue = float('-inf')
				maxAction = -1
				for action in range(Nactions):
					curr_sum = 0.0
					for nxt_state in range(Nstates):
						T_p = self.mdp.getTransitionProbability(state, action, nxt_state)
						R = self.mdp.getReward(state, action, nxt_state)
						# if R!=0:
						# 	print(R, T_p)
						curr_sum = curr_sum + (T_p * (R+Gamma*ValueFxn[nxt_state]))
					if curr_sum > maxValue:
						# print(maxValue)
						maxValue = curr_sum
						maxAction = action

				ValueFxnNext[state] = max(maxValue, 0.0)
				policy[state] = int(maxAction)

			ValueFxn = copy.deepcopy(ValueFxnNext)
			step = step+1
			self.mdp.visualiseValue(ValueFxn, step)
		
		return policy


	def policyIteration(self, Theta, Gamma):
		Nstates = self.mdp.Nstates
		Nactions = self.mdp.Nactions

		# Initialization
		value = np.zeros(Nstates)
		newValue = np.zeros(Nstates)
		policy = [0 for i in range(Nstates)]

		while True:
			# Policy Evaluation
			while True:
				delta = 0
				for s in range(Nstates):
					v = value[s]
					action = policy[s]
					val = 0
					for s_next in range(Nstates):
						T_p = self.mdp.getTransitionProbability(s, action, s_next)
						R = self.mdp.getReward(s, action, s_next)
						val = val + T_p*(R + Gamma*value[s_next])

					newValue[s] = val
					delta = max(delta, abs(v-newValue[s]))

				value = copy.deepcopy(newValue)
				if delta < Theta:
					break

			# Policy Improvement
			policy_stable = True
			for s in range(Nstates):
				b = policy[s]
				maxValue = float('-inf')
				maxAction = -1
				for a in range(Nactions):
					val = 0
					for s_next in range(Nstates):
						T_p = self.mdp.getTransitionProbability(s, a, s_next)
						R = self.mdp.getReward(s, a, s_next)
						val = val + T_p*(R + Gamma*value[s_next])

					if val>maxValue:
						maxValue = val
						maxAction = a

				policy[s] = maxAction
				if b != policy[s]:
					policy_stable = False

			if policy_stable:
				break

		return policy

	def BFS(self, start_state, goal_state):
		mdp = self.mdp
		Q = deque()
		Q.append(start_state)
		Visited = np.zeros(mdp.Nstates)
		Visited[start_state] = 1 # mark state visited
		while Q:
			curr_state = Q.popleft()
			if curr_state==goal_state:
				print("FOUND")
				return 1
			for state in mdp.getValidNextStates(curr_state):
				if !Visited[state]:
					Q.append(state)
					Visited[state]=1

		print("NOT-FOUND")
		return 0




