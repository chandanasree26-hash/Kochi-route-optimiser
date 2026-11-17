import sys

from data import build_kochi_transit_network


def get_station_catalog(g):
    """Returns a sorted list of station tuples (id, name, line_category)."""
    catalog = []
    for sid, info in g.nodes.items():
        if sid.startswith('M'):
            category = "Metro Blue Line"
        elif sid.startswith('W'):
            category = "Water Metro"
        elif sid.startswith('P'):
            category = "Pink Line (Proposed)"
        else:
            category = "Other"
        catalog.append((sid, info['name'], category))
    return catalog

def print_station_catalog(catalog):
    print("\n" + "=" * 60)
    print("           AVAILABLE STATIONS & HUBS (36 Stations)")
    print("=" * 60)
    
    categories = ["Metro Blue Line", "Water Metro", "Pink Line (Proposed)"]
    num = 1
    station_map = {}
    
    for cat in categories:
        print(f"\n--- {cat} ---")
        cat_stations = [s for s in catalog if s[2] == cat]
        for sid, name, _ in cat_stations:
            print(f"  {num:2d}. [{sid:<3}] {name}")
            station_map[num] = sid
            num += 1
            
    print("=" * 60)
    return station_map

def find_station(user_input, g, catalog, number_map):
    """Matches user input by number, station ID, or station name."""
    query = user_input.strip()
    if not query:
        return None

    # 1. Match by catalog number (1-36)
    if query.isdigit():
        idx = int(query)
        if idx in number_map:
            return number_map[idx]

    # 2. Match by exact station ID (e.g., M1, W3, P2) - case insensitive
    query_upper = query.upper()
    if query_upper in g.nodes:
        return query_upper

    # 3. Match by station name (exact or substring)
    query_lower = query.lower()
    matches = [sid for sid, name, _ in catalog if query_lower in name.lower()]
    
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        # Check for exact name match first
        for sid in matches:
            if g.nodes[sid]['name'].lower() == query_lower:
                return sid
        print(f"  Multiple matches found for '{query}':")
        for m in matches:
            print(f"    - [{m}] {g.nodes[m]['name']}")
        print("  Please be more specific or use the station ID / number.")
        return None

    return None

def prompt_station(prompt_text, g, catalog, number_map):
    while True:
        val = input(prompt_text).strip()
        if val.lower() in ('q', 'quit', 'exit'):
            return None
        if val.lower() == 'list':
            print_station_catalog(catalog)
            continue
            
        sid = find_station(val, g, catalog, number_map)
        if sid:
            print(f"  -> Selected: [{sid}] {g.nodes[sid]['name']}")
            return sid
        else:
            print("  Station not recognized. Type station name, ID (e.g. M1, W7), number, 'list', or 'q' to quit.")

def print_route(result, title="OPTIMAL ROUTE"):
    if not result:
        print(f"\n--- {title} ---")
        print("No route found between the selected stations.\n")
        return
        
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    print(f"Mode: {'Fastest Travel Time' if result['optimized_for'] == 'time' else 'Fewest Line Transfers'}")
    print(f"Algorithm: {result['algorithm'].upper()}")
    print("-" * 60)
    
    # Step-by-step route visualization
    stations = result['path']
    print(f"Journey Steps ({len(stations)} stations):")
    for idx, station in enumerate(stations, start=1):
        if idx == 1:
            print(f"   [START] {station}")
        elif idx == len(stations):
            print(f"   [DEST]  {station}")
        else:
            print(f"     |-->  {station}")
            
    print("-" * 60)
    print(f"Total Estimated Time : {result['time_cost_mins']} minutes")
    print(f"Line Transfers       : {result['transfers']}")
    print(f"Search Efficiency    : {result['nodes_explored']} nodes explored in {result['execution_time_ms']} ms")
    print(f"{'=' * 60}\n")

def main():
    print("\n" + "#" * 60)
    print("     KOCHI METRO & TRANSIT INTERACTIVE ROUTE OPTIMISER")
    print("#" * 60)
    
    g = build_kochi_transit_network()
    catalog = get_station_catalog(g)
    number_map = print_station_catalog(catalog)
    
    print("\nTip: You can enter station by Number (1-36), ID (e.g. M1, W7), or Name (e.g. Aluva).")
    print("Type 'list' anytime to re-display the station list, or 'q' to quit.\n")
    
    while True:
        # 1. Origin Station
        start_id = prompt_station("\nEnter Origin / FROM station: ", g, catalog, number_map)
        if not start_id:
            print("Exiting optimizer. Safe travels!")
            break

        # 2. Destination Station
        while True:
            end_id = prompt_station("Enter Destination / TO station: ", g, catalog, number_map)
            if not end_id:
                break
            if end_id == start_id:
                print("  Origin and Destination cannot be the same! Please select a different station.")
                continue
            break
            
        if not end_id:
            print("Exiting optimizer. Safe travels!")
            break

        # 3. Optimization Preference
        print("\nChoose Optimization Preference:")
        print("  1. Fastest Route (Shortest Time)")
        print("  2. Fewest Transfers (Least Line Changes)")
        print("  3. Compare Both (Fastest vs Fewest Transfers)")
        
        pref = input("Select option [1/2/3, default=1]: ").strip()
        
        if pref == '2':
            res = g.route(start_id, end_id, algorithm='astar', optimize_for='transfers')
            print_route(res, "OPTIMIZED FOR FEWEST TRANSFERS")
        elif pref == '3':
            res_fast = g.route(start_id, end_id, algorithm='astar', optimize_for='time')
            res_transfers = g.route(start_id, end_id, algorithm='dijkstra', optimize_for='transfers')
            print_route(res_fast, "OPTION A: FASTEST ROUTE (TIME-OPTIMIZED)")
            print_route(res_transfers, "OPTION B: FEWEST TRANSFERS")
        else:
            res = g.route(start_id, end_id, algorithm='astar', optimize_for='time')
            print_route(res, "FASTEST ROUTE (A* SEARCH)")

        again = input("Would you like to search another route? (y/n, default=y): ").strip().lower()
        if again in ('n', 'no', 'q', 'quit'):
            print("\nThank you for using Kochi Metro Transit Optimizer. Goodbye!")
            break

if __name__ == "__main__":
    if "--cli" in sys.argv:
        main()
    else:
        try:
            from app import KochiMetroOptimizerApp
            print("Launching Kochi Metro Transit Optimizer GUI (Tkinter)...")
            print("To run in terminal CLI mode instead, execute: python main.py --cli\n")
            app = KochiMetroOptimizerApp()
            app.mainloop()
        except Exception as e:
            print(f"Notice: Could not start graphical interface ({e}). Falling back to CLI mode...")
            main()


