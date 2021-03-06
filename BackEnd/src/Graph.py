from collections import deque, namedtuple

inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')

def make_edge(start, end, cost):
    return Edge(start, end, cost)

class Graph:

    instance = None
    
    def __init__(self, edges):

        if Graph.instance == None:

            Graph.instance = self
        
            wrong_edges = [i for i in edges if len(i) not in [2, 3]]

            if wrong_edges:

                raise ValueError('Wrong edges data: {}'.format(wrong_edges))

            self.edges = [make_edge(*edge) for edge in edges]

    @staticmethod
    def getInstance(edges):
        
        if Graph.instance == None:

            Graph(edges)

        return Graph.instance

    @property
    def vertices(self):

        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends = True):

        if both_ends:

            node_pairs = [[n1, n2], [n2, n1]]

        else:

            node_pairs = [[n1, n2]]

        return node_pairs

    def remove_edge(self, n1, n2, both_ends = True):

        node_pairs = self.get_node_pairs(n1, n2, both_ends)

        edges = self.edges[:]

        for edge in edges:

            if [edge.start, edge.end] in node_pairs:

                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost, both_ends = True):

        node_pairs = self.get_node_pairs(n1, n2, both_ends)

        for edge in self.edges:

            if [edge.start, edge.end] in node_pairs:

                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start = n1, end = n2, cost = cost))

        if both_ends:

            self.edges.append(Edge(start = n2, end = n1, cost = cost))

    @property
    def neighbours(self):

        neighbours = {vertex: set() for vertex in self.vertices}

        for edge in self.edges:

            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):

        assert source in self.vertices

        distances = {vertex: inf for vertex in self.vertices}

        previous_vertices = {vertex: None for vertex in self.vertices}

        distances[source] = 0

        vertices = self.vertices.copy()

        while vertices:

            current_vertex = min(vertices, key = lambda vertex: distances[vertex])

            vertices.remove(current_vertex)

            if distances[current_vertex] == inf:

                break

            for neighbour, cost in self.neighbours[current_vertex]:

                alternative_route = distances[current_vertex] + cost

                if alternative_route < distances[neighbour]:

                    distances[neighbour] = alternative_route

                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest

        while previous_vertices[current_vertex] is not None:

            path.appendleft(current_vertex)

            current_vertex = previous_vertices[current_vertex]
            
        if path:

            path.appendleft(current_vertex)
        
        finalList = []

        for i in path:

            finalList.append(i)
        
        return distances[dest], finalList
        
    def connections(self, node, dictionary):

        finalList = []

        for i in dictionary[node]:

            finalList.append(i)

        for j in dictionary:
            
            for k in dictionary[j]:

                if node == k:

                    finalList.append(j)              

        return(finalList)

graph = Graph.getInstance([("Paraiso", "Cartago", 7),
                           ("Cartago", "Tres_Rios", 12),
                           ("Tres_Rios", "Curridabat", 6),
                           ("Tres_Rios", "Sabanilla", 8),
                           ("Curridabat", "San_Pedro", 4),
                           ("Sabanilla", "San_Pedro", 3),
                           ("Sabanilla", "Guadalupe", 3),
                           ("Sabanilla", "San_Jose", 8),
                           ("Guadalupe", "San_Pedro", 2),
                           ("San_Jose", "San_Pedro", 4),
                           ("Tres_Rios", "Zapote", 10),
                           ("Zapote", 'San_Jose', 6),
                           ("Guadalupe", "Moravia", 10),
                           ("Moravia", "Tibas", 12),
                           ("San_Jose", "Tibas", 5),
                           ("Tibas", "Santo_Domingo", 4),
                           ("Santo_Domingo", "Heredia", 5)])