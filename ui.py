import tkinter as tk
from tkinter import ttk
from algorithms import (
    bellman_ford,
    bfs_fewest_stops,
    dfs_reachable,
    dijkstra_heap,
    floyd_warshall,
)
from graph import build_sample_campus


class CampusGPSApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Mini Campus GPS Route Planner")
        self.root.geometry("620x420")

        self.campus = build_sample_campus()
        self.nodes, self.all_pairs = floyd_warshall(self.campus)
        self.node_idx = {name: i for i, name in enumerate(self.nodes)}

        controls = ttk.Frame(root, padding=12)
        controls.pack(fill=tk.X)

        ttk.Label(controls, text="Start:").grid(row=0, column=0, padx=(0, 6), sticky=tk.W)
        self.start_var = tk.StringVar(value="Main Gate")
        ttk.Combobox(controls, textvariable=self.start_var, values=self.nodes, state="readonly", width=22).grid(
            row=0, column=1, padx=(0, 12)
        )

        ttk.Label(controls, text="Destination:").grid(row=0, column=2, padx=(0, 6), sticky=tk.W)
        self.goal_var = tk.StringVar(value="Canteen")
        ttk.Combobox(controls, textvariable=self.goal_var, values=self.nodes, state="readonly", width=22).grid(
            row=0, column=3, padx=(0, 12)
        )

        ttk.Button(controls, text="Find Route", command=self.find_route).grid(row=0, column=4)

        self.output = tk.Text(root, wrap=tk.WORD, padx=12, pady=12, font=("Consolas", 10))
        self.output.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        self.find_route()

    def find_route(self) -> None:
        start = self.start_var.get()
        goal = self.goal_var.get()

        bfs_path, stops = bfs_fewest_stops(self.campus, start, goal)
        dij_path, dij_cost = dijkstra_heap(self.campus, start, goal)
        bf_path, bf_cost = bellman_ford(self.campus, start, goal)
        fw_cost = self.all_pairs[self.node_idx[start]][self.node_idx[goal]]
        reachable_count = len(dfs_reachable(self.campus, start))

        lines = [
            f"Route: {start} -> {goal}",
            "-" * 48,
            f"BFS (fewest stops):    {' -> '.join(bfs_path)} ({stops} stops)",
            f"Dijkstra (min-heap):   {' -> '.join(dij_path)} ({dij_cost:.1f} m)",
            f"Bellman-Ford check:    {' -> '.join(bf_path)} ({bf_cost:.1f} m)",
            f"Floyd-Warshall lookup: {fw_cost:.1f} m",
            f"DFS reachable places:  {reachable_count}",
        ]

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "\n".join(lines))


def run_ui() -> None:
    root = tk.Tk()
    CampusGPSApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_ui()