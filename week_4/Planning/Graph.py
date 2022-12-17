
from collections import deque

class Graph():
	def __init__(self):
		self.V = [] # Vertices
		self.E = {} # Edges : Map from a vertex to list of vertices

	def add_vertex(self, vertex):
		self.V.append(vertex)

	def get_vertex_set(self):
		return self.V

	def add_edge(self, vertex1, vertex2):
		if vertex1 in self.E:
			self.E[vertex1].append(vertex2)
		else:
			self.E[vertex1] = []
			self.E[vertex1].append(vertex2)

	# Breadth First Search
	def BFS(self, vertex_s, vertex_f, mdp):
		Q = deque()
		Q.append(vertex_s)
		Visited = dict.fromkeys(self.V, 0)
		Visited[vertex_s] = 1 # mark state visited
		while Q:
			curr_vertex = Q.popleft()
			mdp.jumpToState(curr_vertex)
			mdp.visualise()
			if curr_vertex==vertex_f:
				print("FOUND")
				return 1
			for vertex in self.E[curr_vertex]:
				if not Visited[vertex]:
					Q.append(vertex)
					Visited[vertex]=1

		print("NOT-FOUND")
		return 0

	# Depth First Search
	def DFS(self, vertex_s, vertex_f, mdp):
		S = deque()
		S.append(vertex_s)
		Visited = dict.fromkeys(self.V, 0) # 0 - unvisited, 1 - visited, 2 - current node in stack
		while S:
			curr_vertex = S[-1] # The last appended element
			Visited[curr_vertex] = 2
			mdp.jumpToState(curr_vertex)
			mdp.visualise()
			if curr_vertex==vertex_f:
				print("FOUND")
				return 1
			visited_all_child = True
			for vertex in self.E[curr_vertex]:
				if not Visited[vertex]:
					S.append(vertex)
					visited_all_child = False
					break

			if visited_all_child:
				Visited[curr_vertex]=1
				S.pop()

		print("NOT-FOUND")
		return 0
