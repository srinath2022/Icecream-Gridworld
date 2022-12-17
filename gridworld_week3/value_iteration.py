
#Inputs to Import
#States: list S = [S]
#Action: list A = [A]
#Transition Probabilities: list [S, A, S', Probability], only need non-zero probabilities
#Reward with transition: list [S, A, S', Reward]
#Discount factor: rho (float)

from typing import DefaultDict

#Example of S,A, P, R, rho in poker where you can only get 2,3,4 on draw, and you can't exceed 5 (instead of 21) reward is equal to number you stay at
S = [0, 2, 3, 4, 5, 'Done']
A = ['hit', 'stay']
P = [[0, 'hit', 2, 1/3], [0, 'hit', 3, 1/3], [0, 'hit', 4, 1/3], [0,'stay', 'Done', 1], [2,'hit', 4, 1/3], [2,'hit', 5, 1/3], [2,'hit', 'Done', 1/3], [2,'stay','Done', 1], [3,'hit',5, 1/3], [3,'hit','Done', 2/3], [3,'stay', 'Done', 1], [4, 'hit', 'Done', 1], [4,'stay','Done', 1], [5, 'hit', 'Done', 1] ,[5,'stay', 'Done', 1]]
R = [[2,'stay', 2, 2], [3,'stay', 3, 3], [4,'stay', 4, 4],[4,'stay', 4, 4], [5,'stay', 5, 5]] #[S, A, S', Reward Value], only include transition that get reward
rho = 1 #no diminishing returns for time taken

value_prev = []
value_new =  []
#initalize no value to all states
for state in S:
    value_prev.append(0)
    value_new.append(0)



def value_iteration(S):
    iteration = 1
    for state in S:
        max_value = 0
        for action in A: #with only one move what is the best value to pull (calculated from value which is propagted from reward)
            calc_value_action = 0 # summing the value for the action in state
            for transition in P:
                reward_available = False #check to see if there is a possible reward associated with state and action, state
                if (transition[0] == state) and (transition[1] == action):
                    for reward in R:
                        if (reward[0] == state) and (reward[1] == action) and (reward[2] == transition[2]):
                            calc_value_action = reward[3] * transition[3] + calc_value_action
                            reward_available = True
                if reward_available == False: #if there is no reward for state action next state, add value of next state time probability times reward
                    value_from_next_state = value_prev[S.index(transition[2])] #find value associatd with next state
                    calc_value_action = calc_value_action + (rho * transition[3] * value_from_next_state)
            if calc_value_action > max_value:
                max_value = calc_value_action
        value_new[S.index[state]] = max_value
    
    iteration += 1
