
from Graph import Graph
from GridWorldMDP import GridWorldMDP
from RRT import RRT

G = Graph()

# Load chess graph
rows = 20
cols = 20
mdp = GridWorldMDP(rows, cols, 0*10+0)

for row in range(rows):
	for col in range(cols):
		# The vertex
		G.add_vertex((row, col))
		# The edges
		if(row-2>=0 and col-1>=0):
			G.add_edge((row, col), (row-2, col-1))
		if(row-1>=0 and col-2>=0):
			G.add_edge((row, col), (row-1, col-2))
		if(row+1<rows and col-2>=0):
			G.add_edge((row, col), (row+1, col-2))
		if(row+2<rows and col-1>=0):
			G.add_edge((row, col), (row+2, col-1))
		if(row+2<rows and col+1<cols):
			G.add_edge((row, col), (row+2, col+1))
		if(row+1<rows and col+2<cols):
			G.add_edge((row, col), (row+1, col+2))
		if(row-1>=0 and col+2<cols):
			G.add_edge((row, col), (row-1, col+2))
		if(row-2>=0 and col+1<cols):
			G.add_edge((row, col), (row-2, col+1))


# G.BFS((0,0), (7,7), mdp)
# G.BFS((0,0), (7,7), mdp)
RRT(G.get_vertex_set(), (0,0), (17,15), mdp)
