# Mini GPS Route Planner for the University Campus

A Python Data Structures 2 project that models a university campus map as a weighted graph and compares graph traversal, single-source shortest path, and all-pairs shortest path algorithms alongside priority-queue and hash-table data structures.

**Live Web Demo:** https://mini-gps-route-planner.vercel.app

## Project Structure

* `main.py` — Main menu entry point to launch the interactive CLI route planner or run benchmarks.
* `graph.py` — `CampusGraph` adjacency-list implementation with $O(1)$ average case-insensitive place lookup (`dict`) and sample campus map builder.
* `algorithms.py` — Implementations of BFS (`bfs\_fewest\_stops`), DFS (`dfs\_reachable`), Dijkstra with a binary min-heap (`dijkstra\_heap`), Dijkstra with a plain list scan (`dijkstra\_list\_scan`), Bellman-Ford (`bellman\_ford`), and Floyd-Warshall (`floyd\_warshall`).
* `planner.py` — Interactive command-line interface comparing routes, stop counts, and distances across algorithms.
* `benchmark.py` — Correctness cross-checks and runtime benchmarks across growing graph sizes ($V = 50, 150, 300, 600$).
* `tests.py` — Automated `unittest` suite covering place lookup, graph traversals, shortest paths, negative weights/cycles, and algorithm consistency.

## How to Run

From inside the `campus\_gps` folder:

```bash
python main.py
python benchmark.py
python -m unittest discover -s . -p "tests.py" -v
```

## Data Structures \& Algorithm Trade-offs

|Component / Algorithm|Data Structure / Approach|Time Complexity|Notes|
|-|-|-|-|
|Place lookup|Python `dict` (`lookup`)|$O(1)$ average|Resolves place names case-insensitively before running queries.|
|Campus map|Adjacency list (`dict` of lists)|$O(V + E)$ space|Efficient for sparse campus walkways and roads.|
|Fewest stops|BFS (`collections.deque`)|$O(V + E)$|Finds minimum edge hops on unweighted steps.|
|Reachability|DFS (recursive + visited set)|$O(V + E)$|Explores reachable places from a starting location.|
|Shortest path (heap)|Dijkstra + binary min-heap (`heapq`)|$O((V + E) \\log V)$|Fast single-source shortest path for non-negative edge weights.|
|Shortest path (list scan)|Dijkstra + linear minimum scan|$O(V^2)$|Included in benchmarks to show why a heap outperforms scanning unvisited nodes.|
|Negative weights / check|Bellman-Ford|$O(V \\cdot E)$|Supports negative edge weights and detects negative-weight cycles.|
|All-pairs shortest paths|Floyd-Warshall|$O(V^3)$|High precomputation cost, fast matrix lookups once computed on smaller maps.|



