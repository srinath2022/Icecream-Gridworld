from GridWorldMDP import GridWorldMDP
from Solver import Solver

agent_state = 7*10+8
mdp = GridWorldMDP(10, 10, agent_state)

# Policy Iteration
solver = Solver(mdp)
policy = solver.policyIteration(0.2, 0.9)
mdp.startAgent(policy, 15)

# Value Iteration
# solver = Solver(mdp)
# iterations = 10
# policy = solver.valueIteration(iterations, 0.8)
# mdp.startAgent(policy, 20)

# while True:
# 	mdp.visualise()
# 	moves = ['l', 'r', 'u', 'd', 's']
# 	move = input('Please enter a action for the robot (l,r,u,d,s):')
# 	if move == 'q':
# 		break
# 	if move in moves:
# 		mdp.takeAction(moves.index(move))
# 	else:
# 		print('Invalid action')