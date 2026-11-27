class CampusGraph:
    """Weighted graph stored as an adjacency list with O(1) place lookup."""

    def __init__(self) -> None:
        self.adj: dict[str, list[tuple[str, float]]] = {}
        self.lookup: dict[str, str] = {}  # lowercase name -> canonical place name

    def add_place(self, name: str) -> None:
        clean = name.strip()
        if clean not in self.adj:
            self.adj[clean] = []
            self.lookup[clean.lower()] = clean

    def add_road(self, src: str, dst: str, weight: float, bidirectional: bool = True) -> None:
        self.add_place(src)
        self.add_place(dst)
        u = self.resolve_place(src)
        v = self.resolve_place(dst)
        self.adj[u].append((v, float(weight)))
        if bidirectional:
            self.adj[v].append((u, float(weight)))

    def resolve_place(self, query: str) -> str | None:
        return self.lookup.get(query.strip().lower())

    def neighbors(self, place: str) -> list[tuple[str, float]]:
        canonical = self.resolve_place(place)
        return self.adj.get(canonical, []) if canonical else []

    def places(self) -> list[str]:
        return sorted(self.adj.keys())


def build_sample_campus() -> CampusGraph:
    g = CampusGraph()
    roads = [
        ("Main Gate", "Admin Building", 120),
        ("Main Gate", "Library", 200),
        ("Admin Building", "Science Block", 150),
        ("Library", "Science Block", 110),
        ("Library", "Canteen", 90),
        ("Canteen", "Dormitory A", 180),
        ("Dormitory A", "Dormitory B", 100),
        ("Science Block", "Engineering Lab", 140),
        ("Engineering Lab", "Sports Complex", 220),
        ("Canteen", "Sports Complex", 250),
        ("Dormitory B", "North Gate", 130),
        ("Sports Complex", "North Gate", 160),
    ]
    for u, v, dist in roads:
        g.add_road(u, v, dist, bidirectional=True)
    return g