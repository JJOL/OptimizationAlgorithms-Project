from collections import deque, defaultdict


class Graph:
    def __init__(self, nVertices, edges):
        self.nVertices = nVertices
        self.edges = edges

        self.adjList = defaultdict(list)
        self.inDegree = [0] * nVertices
        for src, dest, w in edges:
            self.adjList[src].append(dest)
            self.inDegree[dest] += 1

    def isDAG(self):
        # Kahn Algorithm for topological sort (adjusted just for cycle detection)
        S = deque([v for v in range(self.nVertices) if self.inDegree[v] == 0])
        inDegree = self.inDegree.copy()

        visited = 0
        while len(S) > 0:
            v = S.popleft()
            visited += 1
            for u in self.adjList[v]:
                inDegree[u] -= 1
                if inDegree[u] == 0:
                    S.append(u)

        return visited == self.nVertices
    

from collections import defaultdict, deque

class DynTopoDAG:
    def __init__(self, n):
        self.n = n
        self.adj = defaultdict(list)
        # vert holds a valid topo-order; start with [0, 1, ..., n-1]
        self.vert = list(range(n))
        # pos[v] is v’s index in vert
        self.pos = {v: v for v in self.vert}

    def _recompute_pos(self):
        for idx, v in enumerate(self.vert):
            self.pos[v] = idx

    def add_edge(self, u, v):
        """Attempt to insert edge u→v. 
        Return True if DAG still valid; False and no change if it would cycle."""
        if self.pos[u] < self.pos[v]:
            # fast path
            self.adj[u].append(v)
            return True

        # slow path: potential back-edge
        limit = self.pos[u]
        seen = {v}
        stack = [v]
        R = []  # will collect all reachable ≤ limit
        while stack:
            x = stack.pop()
            if x == u:
                return False  # cycle!
            R.append(x)
            for w in self.adj[x]:
                if w not in seen and self.pos[w] <= limit:
                    seen.add(w)
                    stack.append(w)

        # reorder vert: remove R, then insert it right after u
        new_vert = []
        for x in self.vert:
            if x not in seen or x not in R:  # filter out exactly R
                new_vert.append(x)

        # find where u ended up
        idx_u = new_vert.index(u)
        # splice R in after idx_u
        new_vert[idx_u+1:idx_u+1] = R

        # commit changes
        self.vert = new_vert
        self._recompute_pos()
        self.adj[u].append(v)
        return True

    def can_add_edge(self, u, v):
        # just test without mutating
        backup_adj = {k:list(vs) for k,vs in self.adj.items()}
        backup_vert = self.vert[:]
        backup_pos = dict(self.pos)

        ok = self.add_edge(u, v)

        if not ok:
            # no mutation happened on failure path
            return False

        # revert changes
        self.adj = backup_adj
        self.vert = backup_vert
        self.pos = backup_pos
        return True