# CompRobotics209as
Computational Robotics EC

## Gridworld: Defining The state space, action space, transitions and Visualization
The grid dimensions, obstacles, icecream stops, road stops, and intial position are defined. This script can be easily modified to change grid dimensions, number of obstacles/stores/stops, initial posistion, chance of error in transistions, and transisiton probabilities. This was designed to be used as an available basis model to help visualize and modify the Gridworld problem, however the capability it provides for adaption for this specific problem cannot be used for all MDP problems. The MDP spaces (S, A, P, O) would have to be recreated and visualiztion modified in order to be more widely availble which was not the intent of the program. 

The script lists/defines:
- All states, which is equivalent to every spot on the grid
- All transitions, which are mathematically defined as [State, action, State] and include transitions that have non-zero probability
- Harmonic mean distance (H) from ice cream stores
- Number of possible transitions: 3125
- Number of non-zero probabilty transitions: 73 (around 2.3% of transitions non-zero probability)
- Which transition user attempted, if there was a barrier, if there was an error in transition causing an uninteneded transition (caused by uncertainity in transitions, set prob_error to 0 if desired to have no erri) 

With no direction from sensors, or probablistic movements give, a "move" function is built to take the initial square and amount of desired moves, and move the piece randomly according to the calculated non-zero probabilty transitions in that state for the amount of listed moves. Each time a move happens, the possible transitions for that state are listed.

The script was redesigned to take in an action, and generate probabilites for transtions while playing the game. The game also prints the observation after a transition, but it should note that this cannot be computed when it reaches an ice cream store as the distance = 0 and 1/0 is not possible, so when this happens it simply prints "at ice cream store". There isa GUI that displays the grid and where the robot, ice cream store, barriers, and road is. Movement are made by typing in input  u,d,l,r,s for up, down , left, right, stay.

The display was designed to have easy access to be able to import policies based on various algorithms later learned in the class to test their feasability and be able to visualize how the robot is navigating with said policy.

## How to Run 
- Navigate to Gridworld visualization.py
- Change initial variables in the first lines if you want to change the setup (obstacles, transition error, ice cream spot, road spots, dimensionality of gridworld), otherwise they will be default setup from class problem with .1 transition error.
- Run the script. Additionally, if desired insert an algorthmic policy where you would like to control the actions of the based on either the observation or actual state where th design will output states as [x,y] positions starting at [0,0] in bottom left, and will take in actions as the string "Up", "Down", "Left", "Right", "Stay"
- In the trerminal where it lists "desired input action is:" type u, d, l, r, s, or q for up, down , left, right, stay, or quit respectively. The robot is displayed in green, road obstacles in red, barrieiers in grey, and ice cream stores in pink.
