from graph import TransitGraph

def build_kochi_transit_network():
    g = TransitGraph()
    
    # ---------------------------------------------------------
    # 1. Kochi Metro - Blue Line
    # (Approximate coordinates for key stations to allow A* heuristic)
    # ---------------------------------------------------------
    metro_stations = [
        ("M1", "Aluva", 10.1098, 76.3496),
        ("M2", "Pulinchodu", 10.1000, 76.3480),
        ("M3", "Companypady", 10.0900, 76.3450),
        ("M4", "Ambattukavu", 10.0800, 76.3420),
        ("M5", "Muttom", 10.0700, 76.3390),
        ("M6", "Kalamassery", 10.0550, 76.3250),
        ("M7", "Cochin University", 10.0450, 76.3200),
        ("M8", "Pathadipalam", 10.0350, 76.3150),
        ("M9", "Edappally", 10.0250, 76.3100),
        ("M10", "Changampuzha Park", 10.0150, 76.3080),
        ("M11", "Palarivattom", 10.0055, 76.3050),
        ("M12", "JLN Stadium", 9.9980, 76.3000),
        ("M13", "Kaloor", 9.9900, 76.2950),
        ("M14", "Lissie", 9.9850, 76.2900),
        ("M15", "M.G. Road", 9.9723, 76.2818),
        ("M16", "Maharaja's College", 9.9650, 76.2840),
        ("M17", "Ernakulam South", 9.9600, 76.2900), # Transfer point to Railway
        ("M18", "Kadavanthra", 9.9620, 76.3000),
        ("M19", "Elamkulam", 9.9640, 76.3100),
        ("M20", "Vyttila", 9.9658, 76.3190), # Transfer Hub (Metro + Water Metro)
        ("M21", "Thykoodam", 9.9600, 76.3250),
        ("M22", "Petta", 9.9550, 76.3300),
        ("M23", "Vadakkekotta", 9.9520, 76.3380),
        ("M24", "SN Junction", 9.9500, 76.3410),
        ("M25", "Tripunithura Terminal", 9.9482, 76.3444),
    ]
    
    for sid, name, lat, lon in metro_stations:
        g.add_station(sid, name, lat, lon)
        
    # Add connections for Blue Line (assume ~2 mins between consecutive stations)
    for i in range(len(metro_stations) - 1):
        g.add_connection(metro_stations[i][0], metro_stations[i+1][0], 2.0, "Blue Line")

    # ---------------------------------------------------------
    # 2. Kochi Water Metro
    # ---------------------------------------------------------
    water_stations = [
        ("W1", "High Court Water Metro", 9.9822, 76.2730),
        ("W2", "Vypin Water Metro", 9.9790, 76.2427),
        ("W3", "Vyttila Water Metro", 9.9660, 76.3195), # Right next to Vyttila Metro
        ("W4", "Kakkanad Water Metro", 10.0270, 76.3353),
        ("W5", "South Chittoor", 10.0385, 76.2796),
        ("W6", "Cheranelloor", 10.0500, 76.2800),
        ("W7", "Fort Kochi", 9.9660, 76.2435),
        ("W8", "Willingdon Island", 9.9570, 76.2690),
    ]
    
    for sid, name, lat, lon in water_stations:
        g.add_station(sid, name, lat, lon)
        
    # Water Metro Routes
    g.add_connection("W1", "W2", 20.0, "Water Metro: High Court-Vypin")
    g.add_connection("W3", "W4", 25.0, "Water Metro: Vyttila-Kakkanad")
    g.add_connection("W1", "W5", 30.0, "Water Metro: High Court-South Chittoor")
    g.add_connection("W5", "W6", 15.0, "Water Metro: South Chittoor-Cheranelloor")
    g.add_connection("W1", "W7", 25.0, "Water Metro: High Court-Fort Kochi")
    g.add_connection("W1", "W8", 15.0, "Water Metro: High Court-Willingdon")
    
    # ---------------------------------------------------------
    # 3. Walking/Transfer Links (Connecting Metro and Water Metro)
    # ---------------------------------------------------------
    # Walk between Vyttila Metro (M20) and Vyttila Water Metro (W3)
    g.add_connection("M20", "W3", 3.0, "Walkway")
    
    # Walk between M.G. Road (M15) / Maharaja's (M16) and High Court (W1)
    # High court is a bit far from MG road (approx 20 mins walk or short auto ride)
    g.add_connection("M15", "W1", 15.0, "Walkway/Auto")
    g.add_connection("M16", "W1", 18.0, "Walkway/Auto")

    # Let's add a fake "Proposed Pink Line" to make route choice more interesting
    # Info Park to JLN Stadium (Phase 2 extension)
    pink_stations = [
        ("P1", "Info Park", 10.0100, 76.3600),
        ("P2", "Kakkanad Junction", 10.0200, 76.3450), # Close to Kakkanad Water Metro
        ("P3", "Palarivattom Bypass", 10.0055, 76.3150),
        # P4 will just be a connection to M12 (JLN Stadium)
    ]
    for sid, name, lat, lon in pink_stations:
        g.add_station(sid, name, lat, lon)
        
    g.add_connection("P1", "P2", 3.0, "Pink Line (Proposed)")
    g.add_connection("P2", "P3", 4.0, "Pink Line (Proposed)")
    g.add_connection("P3", "M12", 2.0, "Pink Line (Proposed)") # Connects to Blue Line at JLN Stadium
    
    # Walkway between Kakkanad Junction Pink Line and Kakkanad Water Metro
    g.add_connection("P2", "W4", 5.0, "Walkway")

    return g

if __name__ == "__main__":
    g = build_kochi_transit_network()
    print(f"Network built with {len(g.nodes)} stations.")
