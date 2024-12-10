from collections import defaultdict, deque
import heapq
import random

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.heur = {}
        self.weight = {}
        self.and_nodes = set()
        self.or_nodes = set()
        self.oracle_path = {}
    
    def addEdge(self, u, v, weight=1):
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.weight[(u,v)] = weight
        self.weight[(v,u)] = weight
    
    def set_heur(self, node, val):
        self.heur[node] = val
    
    def print_graph(self):
        for node, neigh in self.graph.items():
            nlist=','.join(neigh) if neigh else 'None'
            print(f"{node}: {nlist}")

    def bms(self, start, goal, max_iter=1000):
        bestpath = None
        best_pathlen = float('inf')
        for _ in range(max_iter):
            curr = start
            path = [start]
            visited = {start}
            while curr !=goal and len(self.graph[curr]) > 0:
                neigh = [n for n in self.graph[curr] if n not in visited]
                if not neigh:
                    break
                curr = random.choice(neigh)
                path.append(curr)
                visited.add(curr)
            
            if curr == goal and len(path) < best_pathlen:
                bestpath = path
                best_pathlen = len(path)
        return bestpath if bestpath else []
    
    def bfs(self, start, goal):
        queue = deque([[start]])
        visited = {start}
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node == goal:
                return path
            for neigh in self.graph[node]:
                if neigh not in visited:
                    visited.add(neigh)
                    newpath = list(path)
                    newpath.append(neigh)
                    queue.append(newpath)
        return[]
    
    def dfs(self, start, goal):
        stack = [(start, [start])] 
        visited = set() 
        while stack:  
            node, path = stack.pop() 
            if node not in visited: 
                if node == goal:  
                    return path 
                visited.add(node) 
                for neigh in reversed(self.graph[node]):  
                    stack.append((neigh, path + [neigh])) 
        return [] 

    def hillclimb(self, start, goal):  
        curr = start 
        path = [start] 
        while curr != goal:  
            neigh = self.graph[curr] 
            if not neigh:  
                break 
            next_node = min(neigh, key=lambda x: self.heur.get(x, float('inf'))) 
            if self.heur.get(next_node, float('inf')) >= self.heur.get(curr, float('inf')):  
                break 
            curr = next_node 
            path.append(curr) 
        return path if path[-1] == goal else [] 


    def branch_bound(self, start, goal):
        queue = [(0,start,[start])]
        visited = set()
        while queue:
            cost, node, path = heapq.heappop()
            if node == goal:
                return path
            if node not in visited:
                visited.add(node)
                for neigh in self.graph[node]:
                    if neigh not in visited:
                        newcost = cost + self.weight.get((node,neigh),1)
                        heapq.heappush(queue,(newcost,neigh, path + [neigh]))
        return []

    def branch_bound_heur(self, start, goal):  
        queue = [(self.heur.get(start, 0), 0, start, [start])]   
        visited = set() 
        while queue:  
            est, cost, node, path = heapq.heappop(queue) 
            if node == goal:  
                return path 
            if node not in visited:  
                visited.add(node)  
                for neigh in self.graph[node]:  
                    if neigh not in visited:  
                        newcost = cost + self.weight.get((node, neigh), 1) 
                        estimate = newcost + self.heur.get(neigh, 0) 
                        heapq.heappush(queue, (estimate, newcost, neigh, path + [neigh])) 
        return [] 

    def a_star(self, start, goal): 
        queue = [(self.heur.get(start, 0), 0, start, [start])]   
        visited = set() 
        while queue: 
            estimate, cost, node, path = heapq.heappop(queue) 
            if node == goal: 
                return path 
            if node not in visited:  
                visited.add(node) 
                for neigh in self.graph[node]: 
                    if neigh not in visited:  
                        newcost = cost + self.weight.get((node, neigh), 1) 
                        estimate = newcost + self.heur.get(neigh, 0) 
                        heapq.heappush(queue, (estimate, newcost, neigh, path + [neigh])) 
        return [] 
    
    def beam_search(self, start, goal, width=2): 
        paths = [[start]] 
        while paths: 
            newpaths = [] 
            for path in paths: 
                node = path[-1] 
                if node == goal: 
                    return path  
                for neigh in self.graph[node]: 
                    if neigh not in path: 
                        newpath = path + [neigh] 
                        newpaths.append(newpath) 
            newpaths.sort(key=lambda x: self.heur.get(x[-1], float('inf'))) 
            paths = newpaths[:width] 
        return [] 
    
    def branch_bound_heur(self, start, goal):  
        queue = [(self.heur.get(start, 0), 0, start, [start])]   
        visited = set() 
        while queue:  
            est, cost, node, path = heapq.heappop(queue) 
            if node == goal:  
                return path 
            if node not in visited:  
                visited.add(node)  
                for neigh in self.graph[node]:  
                    if neigh not in visited:  
                        newcost = cost + self.weight.get((node, neigh), 1) 
                        estimate = newcost + self.heur.get(neigh, 0) 
                        heapq.heappush(queue, (estimate, newcost, neigh, path + [neigh])) 
        return [] 

    def branch_bound_extended(self, start, goal): 
        queue = [(0, start, [start])] 
        bestcost = {start: 0} 
        while queue: 
            cost, node, path = heapq.heappop(queue) 
            if node == goal: 
                return path 
            for neigh in self.graph[node]:  
                newcost = cost + self.weight.get((node, neigh), 1) 
                if neigh not in bestcost or newcost < bestcost[neigh]: 
                    bestcost[neigh] = newcost 
                    heapq.heappush(queue, (newcost, neigh, path + [neigh])) 
        return [] 

    def ao_star(self, start, goal):
        
        def calculate_cost(node, visited) :
            if node == goal:
                return 0, [node]
            if node in visited:
                return float('inf'), []
            
            visited.add(node)
            
            if node in self.and_nodes:
               
                total_cost = 0
                total_path = [node]
                for neighbor in self.graph[node]:
                    cost, path = calculate_cost(neighbor, visited.copy())
                    total_cost += cost + self.weight.get((node, neighbor), 1)
                    total_path.extend(path)
                return total_cost, total_path
            else:
               
                min_cost = float('inf')
                best_path = []
                for neighbor in self.graph[node]:
                    cost, path = calculate_cost(neighbor, visited.copy())
                    total_cost = cost + self.weight.get((node, neighbor), 1)

                    if total_cost < min_cost:
                        min_cost = total_cost
                        best_path = [node] + path

                return min_cost, best_path
        
        _, path = calculate_cost(start, set())
        return path if path else []

    def best_first(self, start, goal): 
        queue = [(self.heur.get(start, 0), start, [start])] 
        visited = set() 
        while queue: 
            heuristic, node, path = heapq.heappop(queue) 
            if node == goal: 
                return path  
            if node not in visited:  
                visited.add(node) 
                for neigh in self.graph[node]: 
                    if neigh not in visited: 
                        heapq.heappush(queue, (self.heur.get(neigh, float('inf')), neigh, path + [neigh]))  
        return [] 

    def oracle(self, start, goal, path=None): 
        if path is not None: 
            self.oracle_path[(start, goal)] = path 
        return self.oracle_path.get((start, goal), []) 

    def oracle_cost(self, start, goal, path=None, cost=None): 
        if path is not None and cost is not None: 
            self.oracle_path[(start, goal)] = (path, cost) 
        return self.oracle_path.get((start, goal), ([], float('inf'))) 


    
    
g = Graph()
edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('D', 'G'), ('E', 'G'), ('F', 'G')]
for edge in edges:
    g.addEdge(*edge)

heuristics = {'A': 4, 'B': 3, 'C': 3, 'D': 1, 'E': 1, 'F': 1, 'G': 0}
for node, value in heuristics.items():
    g.set_heur(node, value)

g.print_graph()

start, goal = 'A','G'
#path = g.bms(start, goal) 
path = g.bfs(start, goal)
print(f"{start}: {' -> '.join(path)}")