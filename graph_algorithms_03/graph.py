import copy
import time
from collections import deque

class Graph:
    def __init__(self):
        self.edges = []


    def add_edge(self, k):
        self.edges.append(k)    


    def show_matrix(self, n):
        self.matrix = [[0] * n for _ in range(n)]
        for el in self.edges:
            a, b = el
            self.matrix[a-1][b-1] = 1


    def show_list(self, n):
        self.list = [[] for _ in range(n)]
        for el in self.edges:
            a, b = el
            self.list[a-1].append(b)
            

    def show_table(self):
        self.table = copy.deepcopy(self.edges)
        self.table.sort(key=lambda x: x[0])
    

    def g_print(self, representation, n):
        if representation == "matrix":
            l_matrix = []
            l_matrix.append("  | " + " ".join([str(i) for i in range(1, n+1)]))
            l_matrix.append("--+" + "-" * (n * 2))

            for el in range(1, n+1):
                l_matrix.append(f"{el} | " + " ".join([str(self.matrix[el-1][i]) for i in range(n)]))       
            
            for row in l_matrix:
                print(row)
            print()
        elif representation == "list":
            idx = 1
            for el in self.list:
                print(f"{idx}: " + " ".join(str(i) for i in el))
                idx += 1
            print()
        elif representation == "table":
            for el in self.table:
                print(f"{el[0]} -> {el[1]}")
            print()


    def find(self, representation, n, a, b, measurements):
        if measurements:
            pass
        else:
            while True:
                print("Podaj wierzchołki krawędzi")
                try:
                    a = int(input("from -> "))
                    b = int(input("to -> "))
                    if a <= 0 or b <= 0 or a > n or b > n:
                        raise ValueError
                    break 
                except ValueError:
                    print("Podano nieistniejące wierzchołki. Spróbuj ponownie\n")
                
        if representation == "matrix":
            start_time = time.time()
            if self.matrix[a-1][b-1] == 1:
                print("Krawędź istnieje w grafie")
            else:
                print("Krawędź nie istnieje w grafie")
            end_time = time.time()
            elapsed_time = end_time - start_time
        
        elif representation == "list":
            start_time = time.time()
            if b in self.list[a-1]:
                print("Krawędź istnieje w grafie")
            else:
                print("Krawędź nie istnieje w grafie")
            end_time = time.time()
            elapsed_time = end_time - start_time    
        
        elif representation == "table":
            start_time = time.time()
            if (a, b) in self.table:
                print("Krawędź istnieje w grafie")
            else:
                print("Krawędź nie istnieje w grafie")
            end_time = time.time()
            elapsed_time = end_time - start_time
        print()
        
        if measurements:
            return elapsed_time
        

    def kahn(self, representation, n, measurements):
        start_time = time.time()
        self.kahn_list = []
        in_degree = [0] * n
        
        if representation == "matrix":
            for i in range(n):
                for j in range(n):
                    if self.matrix[i][j] == 1:
                        in_degree[j] += 1
            
        elif representation == "list":
            for i in range(n):
                for el in self.list[i]:
                    in_degree[el-1] += 1
        
        elif representation == "table":
            for el in self.table:
                in_degree[el[1]-1] += 1
        
        queue = []
        for i in range(n):
            if in_degree[i] == 0:
                queue.append(i + 1)

        while queue:
            node = queue.pop(0)
            self.kahn_list.append(node)

            if representation == "matrix":
                for el in range(n):
                    if self.matrix[node-1][el] == 1:
                        in_degree[el] -= 1
                        if in_degree[el] == 0:
                            queue.append(el + 1)
            elif representation == "list":
                for el in self.list[node-1]:
                    in_degree[el-1] -= 1
                    if in_degree[el-1] == 0:
                        queue.append(el)
            elif representation == "table":  
                for el in self.table:
                    if el[0] == node:
                        in_degree[el[1]-1] -= 1
                        if in_degree[el[1]-1] == 0:
                            queue.append(el[1])
        
        if len(self.kahn_list) != n:
            print("Graf nie jest acykliczny")
        else:
            print("Kolejność topologiczna grafu: " + " ".join(str(i) for i in self.kahn_list))

        end_time = time.time()
        elapsed_time = end_time - start_time
        if measurements:
            return elapsed_time


    def tarjan(self, representation, n, measurements):
        start_time = time.time()
        visited = [False] * n
        stack = []

        def tarjan_visit(node):
            visited[node] = True
            if representation == "matrix":
                for i in range(n):
                    if self.matrix[node][i] == 1 and not visited[i]:
                        tarjan_visit(i)
            elif representation == "list":
                for neighbor in self.list[node]:
                    idx = neighbor - 1
                    if not visited[idx]:
                        tarjan_visit(idx)
            elif representation == "table":
                for edge in self.table:
                    if edge[0] == node + 1:
                        idx = edge[1] - 1
                        if not visited[idx]:
                            tarjan_visit(idx)
            stack.append(node + 1) 

        for i in range(n):
            if not visited[i]:
                tarjan_visit(i)

        result = stack[::-1]
        end_time = time.time()
        print("Kolejność topologiczna grafu:", " ".join(str(i) for i in result))    
    
        elapsed_time = end_time - start_time
        if measurements:
            return elapsed_time
        
    
    def bfs(self, representation, n):
        visited = [False] * n
        self.result = []

        def bfs_visit(start):
            queue = deque()
            queue.append(start)
            visited[start] = True

            while queue:
                node = queue.popleft()
                self.result.append(node + 1)
                if representation == "matrix":
                    for i in range(n):
                        if self.matrix[node][i] == 1 and not visited[i]:
                            queue.append(i)
                            visited[i] = True
                elif representation == "list":
                    for neighbor in self.list[node]:
                        idx = neighbor - 1
                        if not visited[idx]:
                            queue.append(idx)
                            visited[idx] = True
                elif representation == "table":
                    for edge in self.table:
                        if edge[0] == node + 1:
                            idx = edge[1] - 1
                            if not visited[idx]:
                                queue.append(idx)
                                visited[idx] = True

        for i in range(n):
            if not visited[i]:
                bfs_visit(i)

        print("Odwiedzone wierzchołki:", " ".join(str(i) for i in self.result))
    

    def dfs(self, representation, n):
        visited = [False] * n
        self.result = []

        def dfs_visit(node):
            visited[node] = True
            self.result.append(node + 1)
            
            if representation == "matrix":
                for i in range(n):
                    if self.matrix[node][i] == 1 and not visited[i]:
                        dfs_visit(i)
            elif representation == "list":
                for el in self.list[node]:
                    if not visited[el - 1]:
                        dfs_visit(el - 1)
            elif representation == "table":
                for el in self.table:
                    if el[0] == node + 1:
                        idx = el[1] - 1
                        if not visited[idx]:
                            dfs_visit(idx)

        for i in range(n):
            if not visited[i]:
                dfs_visit(i)

        print("Odwiedzone wierzchołki:", " ".join(str(i) for i in self.result))