


class Graph:
    def __init__(self, nVertices, edges):
        self.edges = edges
        self.nVertices = nVertices

    def _copyEdges(self):
        edgesCopy = []
        for e in self.edges:
            edgesCopy.append(e)
        return edgesCopy

    def isDAG(self):
        # Kahn Algorithm for topological sort (adjusted just for cycle detection)
        # L = []
        S = []
        edges = self._copyEdges()

        # Init S to be the vertices that have no incoming edge.
        for v in range(self.nVertices):
            incoming = [e for e in edges if e[1] == v]
            if len(incoming) == 0:
                S.append(v)

        while len(S) > 0:
            v = S.pop(0)
            # L.append(v)

            neighbors = [(e,e[1]) for e in edges if e[0] == v]
            for e, u in neighbors:
                edges.remove(e)

                incoming = [e for e in edges if e[1] == u]
                if len(incoming) == 0:
                    S.append(u)

        
        if len(edges) > 0: # If there are edges remaining, graph has at least 1 cycle
            return False
        else:
            return True