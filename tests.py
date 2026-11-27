import unittest
from algorithms import (
    bellman_ford,
    bfs_fewest_stops,
    dfs_reachable,
    dijkstra_heap,
    dijkstra_list_scan,
    floyd_warshall,
)
from graph import CampusGraph, build_sample_campus


class TestCampusGPS(unittest.TestCase):
    def setUp(self) -> None:
        self.campus = build_sample_campus()

    def test_case_insensitive_place_lookup(self) -> None:
        self.assertEqual(self.campus.resolve_place("  main gate "), "Main Gate")
        self.assertEqual(self.campus.resolve_place("CANTEEN"), "Canteen")
        self.assertIsNone(self.campus.resolve_place("Nonexistent Hall"))

    def test_bfs_fewest_stops(self) -> None:
        path, stops = bfs_fewest_stops(self.campus, "Main Gate", "Admin Building")
        self.assertEqual(path, ["Main Gate", "Admin Building"])
        self.assertEqual(stops, 1)

    def test_dfs_reachability(self) -> None:
        reachable = dfs_reachable(self.campus, "Main Gate")
        self.assertEqual(len(reachable), len(self.campus.places()))

    def test_shortest_paths_agree_on_sample_campus(self) -> None:
        start, goal = "North Gate", "Canteen"
        _, dij_h_cost = dijkstra_heap(self.campus, start, goal)
        _, dij_l_cost = dijkstra_list_scan(self.campus, start, goal)
        _, bf_cost = bellman_ford(self.campus, start, goal)
        nodes, matrix = floyd_warshall(self.campus)

        idx_s = nodes.index(start)
        idx_g = nodes.index(goal)
        fw_cost = matrix[idx_s][idx_g]

        self.assertEqual(dij_h_cost, 410.0)
        self.assertEqual(dij_l_cost, dij_h_cost)
        self.assertEqual(bf_cost, dij_h_cost)
        self.assertEqual(fw_cost, dij_h_cost)

    def test_bellman_ford_negative_edge_and_cycle(self) -> None:
        g = CampusGraph()
        g.add_road("A", "B", 5, bidirectional=False)
        g.add_road("B", "C", -2, bidirectional=False)
        g.add_road("A", "C", 10, bidirectional=False)

        path, cost = bellman_ford(g, "A", "C")
        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(cost, 3.0)

        # Introduce a negative cycle: C -> B with weight -5 makes B -> C -> B total -7
        g.add_road("C", "B", -5, bidirectional=False)
        with self.assertRaises(ValueError):
            bellman_ford(g, "A", "C")


if __name__ == "__main__":
    unittest.main()