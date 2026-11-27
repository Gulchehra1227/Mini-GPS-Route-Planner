from benchmark import run_benchmarks
from planner import main as run_planner


def main() -> None:
    while True:
        print("\n=== Campus GPS Route Planner ===")
        print("1. Interactive Route Planner (CLI)")
        print("2. Run Algorithm Benchmarks")
        print("3. Quit")

        choice = input("Choose an option (1-3): ").strip()
        if choice == "1":
            run_planner()
        elif choice == "2":
            run_benchmarks()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")


if __name__ == "__main__":
    main()