from algorithms import (
    bellman_ford,
    bfs_fewest_stops,
    dfs_reachable,
    dijkstra_heap,
    floyd_warshall,
)
from graph import build_sample_campus


def main() -> None:
    campus = build_sample_campus()
    nodes, all_pairs = floyd_warshall(campus)
    node_idx = {name: i for i, name in enumerate(nodes)}

    print("=== Mini Campus GPS Route Planner ===")
    print("Available places:", ", ".join(nodes))

    while True:
        start = input("\nStart place (or 'quit'): ").strip()
        if start.lower() == "quit":
            break
        goal = input("Destination place: ").strip()

        s_canon = campus.resolve_place(start)
        t_canon = campus.resolve_place(goal)
        if not s_canon or not t_canon:
            print("Place not found. Check spelling against the list above.")
            continue

        bfs_path, stops = bfs_fewest_stops(campus, s_canon, t_canon)
        dij_path, dij_cost = dijkstra_heap(campus, s_canon, t_canon)
        bf_path, bf_cost = bellman_ford(campus, s_canon, t_canon)
        fw_cost = all_pairs[node_idx[s_canon]][node_idx[t_canon]]

        print(f"\nRoute from {s_canon} -> {t_canon}:")
        print(f"  BFS (fewest stops):    {' -> '.join(bfs_path)} ({stops} stops)")
        print(f"  Dijkstra (min-heap):   {' -> '.join(dij_path)} ({dij_cost:.1f} m)")
        print(f"  Bellman-Ford check:    {' -> '.join(bf_path)} ({bf_cost:.1f} m)")
        print(f"  Floyd-Warshall lookup: {fw_cost:.1f} m")
        print(f"  Reachable from start (DFS): {len(dfs_reachable(campus, s_canon))} places")


if __name__ == "__main__":
    main()