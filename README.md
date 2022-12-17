# Icecream-Gridworld
Exploring RL algorithms like Value Iteration, Policy Iteration, Path Planning(RRT, PRM) etc. on an AI powered robot.      

Most of the work is in collaboration with 5 other teammates as part of Computational Robotics course at UCLA, including the following writup.

## Week 1:
The grid dimensions, obstacles, icecream stops, road stops, and intial position are defined.
The script lists/defines:
- All states, which is equivalent to every spot on the grid
- All transitions, which are mathematically defined as [State, action, State] and include transitions that have non-zero probability
- Number of transitions: 3125
- Number of non-zero probabilty transitions: 73 (around 2.3% of transitions non-zero probability)

With no direction from sensors, or probablistic movements give, a "move" function is built to take the initial square and amount of desired moves, and move the piece randomly according to the calculated non-zero probabilty transitions in that state for the amount of listed moves. Each time a move happens, the possible transitions for that state are listed.

## Week 2:
This week the script was redesigned to take in an action, and generate probabilites for transtions while playing the game. The game also prints the observation after a transition, but it should note that this cannot be computed when it reaches an ice cream store as the distance = 0 and 1/0 is not possible, so when this happens it simply prints "at ice cream store". There is also now a GUI that displays the grid and where the robot, ice cream store, barriers, and road is. Movement are made by typing in input like u,d,l,r,s for up, down , left, right, stay.

We need to come up with a more general function/script that can take in any list of States, Actions, Probabilities, and Observations as this can only handle specific scenarios.

## Week 3:
This week learned about the complexity of adding multiple agents to the system. Everytime an agent is added to the system, the state space, and action space increases expontentially for n agents by S' = |S|^n and A' = |A|^n, and also the transistion increases by P^3N. Computational complexity also increases even more rapidly for policy and value iteration as more actions and more states are multiplied by each other resulting in a compuding exponential increase in computation. For this reason basis functions are used, which can help to simplify the problem, however choosing the correct basis functions is key to discovering good/optimal policies yet requiring less computation.

## Week 4:

Added BFS and DFS function. Still would like to include graphical representation of path choosing while iterating to see processes, and potentially create RRT method.

## Week 5:

Implemented rrt method to solve the chess night problem. You can insert any starting position and any desired position and the algorithm will solve one way to get to that state. The action space for the knight is defined as:
A={UpUpRight,UpUpLeft,LeftLeftUp,LeftLeftDown,DownDownLeft,DownDownRight,RightRightDown,RightRightUp}
The biggest troubles occured in orginally keeping track of paths already traversed and retracing back when there was no further state to explore for a given state. It should be noted that it is in no way an optimal way to get to a desired state, but more of a "brute force" approach. It should be noted that if we try to add some reward or incentivization for moving in the general direction, it both complicates the algorithem (as the iterations that were incentivised to taken or not taken have to be noted) and may not necessarily work. For example when the night is close to the state sometimes a farter distance in squares away from the reward is less close in terms of states to the reward. For larger systems this is less at play.

## Week 6:

Bayes Filter was implemented. This filter was implemented by taking a function which samples observations and creates a functions which generates a probaility of the observations, giving assumed states. Where the assuemed state and given observations overlap the most bassed on Gausssian distributions is how the Believed state for a given time t Bel(t) gets updated. The state estimation system is useful for real life scenarios with sensors which provide a given observation. In computation it is easy to know the exact stae, becuase you are determining the dynamics and position with code, but in real life not know a state observations are needed, and state estimations like Bayesian filters are useful.

## Week 7:
Kalman Filter:
The Kallman filter is useful for being able to tolerate statistical noise while producing current state estimates based on the noise using normal (Gaussian) probability distributions. It first does a prediction of current state variables and its assumed variablilities. after an observation occurs, it compare the value against its prediction, and updates the satte estimate accordingly using weights. 

## Week 8:
Reinforcement Learning

## Week 9:
Imitation Learning: This weeks focus was on the final project, using imitation learning, specifically behavioral cloning to implement a character prediction algorithm. See readme in week9 for details on how to operate.