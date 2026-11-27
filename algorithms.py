from collections import deque
import heapq
from graph import CampusGraph


def reconstruct_path(parent: dict[str, str | None], start: str, goal: str) -> list[str]:
    if goal not in parent:
        return []
    path: list[str] = []
    curr: str | None = goal
    while curr is not None:
        path.append(curr)
        if curr == start:
            break
        curr = parent[curr]
    path.reverse()
    return path if path and path[0] == start else []


def bfs_fewest_stops(graph: CampusGraph, start: str, goal: str) -> tuple[list[str], int]:
    """Unweighted shortest path (minimum number of edges/stops)."""
    s = graph.resolve_place(start)
    t = graph.resolve_place(goal)
    if not s or not t:
        return [], -1
    if s == t:
        return [s], 0

    queue: deque[str] = deque([s])
    parent: dict[str, str | None] = {s: None}

    while queue:
        u = queue.popleft()
        if u == t:
            path = reconstruct_path(parent, s, t)
            return path, len(path) - 1
        for v, _ in graph.adj[u]:
            if v not in parent:
                parent[v] = u
                queue.append(v)
    return [], -1


def dfs_reachable(graph: CampusGraph, start: str) -> list[str]:
    """Depth-first traversal returning all reachable places from start."""
    s = graph.resolve_place(start)
    if not s:
        return []
    visited: set[str] = set()
    order: list[str] = []

    def _dfs(u: str) -> None:
        visited.add(u)
        order.append(u)
        for v, _ in graph.adj[u]:
            if v not in visited:
                _dfs(v)

    _dfs(s)
    return order


def dijkstra_heap(graph: CampusGraph, start: str, goal: str) -> tuple[list[str], float]:
    """Shortest weighted path using a binary min-heap (heapq)."""
    s = graph.resolve_place(start)
    t = graph.resolve_place(goal)
    if not s or not t:
        return [], float("inf")

    dist: dict[str, float] = {node: float("inf") for node in graph.adj}
    parent: dict[str, str | None] = {s: None}
    dist[s] = 0.0
    pq: list[tuple[float, str]] = [(0.0, s)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == t:
            return reconstruct_path(parent, s, t), d
        for v, w in graph.adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))

    return [], float("inf")


def dijkstra_list_scan(graph: CampusGraph, start: str, goal: str) -> tuple[list[str], float]:
    """Shortest weighted path scanning a plain list instead of a heap (for comparison)."""
    s = graph.resolve_place(start)
    t = graph.resolve_place(goal)
    if not s or not t:
        return [], float("inf")

    dist: dict[str, float] = {node: float("inf") for node in graph.adj}
    parent: dict[str, str | None] = {s: None}
    unvisited: set[str] = set(graph.adj.keys())
    dist[s] = 0.0

    while unvisited:
        u = min(unvisited, key=lambda node: dist[node])
        unvisited.remove(u)
        if dist[u] == float("inf") or u == t:
            break
        for v, w in graph.adj[u]:
            if v in unvisited and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u

    if dist[t] == float("inf"):
        return [], float("inf")
    return reconstruct_path(parent, s, t), dist[t]


def bellman_ford(graph: CampusGraph, start: str, goal: str) -> tuple[list[str], float]:
    """Shortest path supporting negative edge weights; raises ValueError on negative cycles."""
    s = graph.resolve_place(start)
    t = graph.resolve_place(goal)
    if not s or not t:
        return [], float("inf")

    nodes = list(graph.adj.keys())
    edges = [(u, v, w) for u in nodes for v, w in graph.adj[u]]
    dist: dict[str, float] = {node: float("inf") for node in nodes}
    parent: dict[str, str | None] = {s: None}
    dist[s] = 0.0

    for _ in range(len(nodes) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        if not updated:
            break

    for u, v, w in edges:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    if dist[t] == float("inf"):
        return [], float("inf")
    return reconstruct_path(parent, s, t), dist[t]


def floyd_warshall(graph: CampusGraph) -> tuple[list[str], list[list[float]]]:
    """All-pairs shortest path distances in O(V^3)."""
    nodes = graph.places()
    idx = {name: i for i, name in enumerate(nodes)}
    n = len(nodes)
    dist = [[float("inf")] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0.0
    for u in nodes:
        i = idx[u]
        for v, w in graph.adj[u]:
            j = idx[v]
            if w < dist[i][j]:
                dist[i][j] = w

    for k in range(n):
        for i in range(n):
            if dist[i][k] == float("inf"):
                continue
            for j in range(n):
                cand = dist[i][k] + dist[k][j]
                if cand < dist[i][j]:
                    dist[i][j] = cand

    return nodes, dist