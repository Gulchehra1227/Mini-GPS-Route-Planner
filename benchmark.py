import random
import time
from algorithms import (
    bellman_ford,
    bfs_fewest_stops,
    dijkstra_heap,
    dijkstra_list_scan,
    floyd_warshall,
)
from graph import CampusGraph


def generate_random_graph(num_vertices: int, extra_edges_per_node: int = 3, seed: int = 42) -> CampusGraph:
    rng = random.Random(seed)
    g = CampusGraph()
    names = [f"Building_{i}" for i in range(num_vertices)]
    for name in names:
        g.add_place(name)

    # Ensure connectivity via a spanning chain
    for i in range(num_vertices - 1):
        g.add_road(names[i], names[i + 1], rng.randint(10, 200))

    # Add random edges
    for i in range(num_vertices):
        for _ in range(extra_edges_per_node):
            j = rng.randrange(num_vertices)
            if i != j:
                g.add_road(names[i], names[j], rng.randint(10, 200))
    return g


def run_benchmarks() -> None:
    print(f"{'V':>6} | {'BFS (ms)':>10} | {'Dij-Heap (ms)':>13} | {'Dij-List (ms)':>13} | {'Bellman-Ford (ms)':>17} | {'Floyd-Warshall (ms)':>19}")
    print("-" * 92)

    for v in [50, 150, 300, 600]:
        g = generate_random_graph(v)
        start, goal = "Building_0", f"Building_{v - 1}"

        t0 = time.perf_counter()
        bfs_fewest_stops(g, start, goal)
        t_bfs = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        _, d_heap = dijkstra_heap(g, start, goal)
        t_heap = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        _, d_list = dijkstra_list_scan(g, start, goal)
        t_list = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        _, d_bf = bellman_ford(g, start, goal)
        t_bf = (time.perf_counter() - t0) * 1000

        assert d_heap == d_list == d_bf, "Shortest distance mismatch!"

        if v <= 300:
            t0 = time.perf_counter()
            floyd_warshall(g)
            t_fw = f"{(time.perf_counter() - t0) * 1000:.2f}"
        else:
            t_fw = "skipped (O(V^3))"

        print(f"{v:>6} | {t_bfs:>10.3f} | {t_heap:>13.3f} | {t_list:>13.3f} | {t_bf:>17.3f} | {t_fw:>19}")


if __name__ == "__main__":
    run_benchmarks()