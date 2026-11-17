import math
import heapq
from collections import defaultdict
import time

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth (specified in decimal degrees)"""
    R = 6371.0 # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

class TransitGraph:
    def __init__(self):
        self.nodes = {} # node_id -> {name, lat, lon}
        self.edges = defaultdict(list) # node_id -> [(neighbor_id, weight, line_name)]
        
    def add_station(self, station_id, name, lat, lon):
        self.nodes[station_id] = {'name': name, 'lat': lat, 'lon': lon}
        
    def add_connection(self, u, v, time_mins, line_name):
        self.edges[u].append((v, time_mins, line_name))
        self.edges[v].append((u, time_mins, line_name)) # Assuming undirected for simplicity
        
    def get_heuristic(self, node_id, target_id):
        """A* heuristic: Straight-line distance travel time (approx 35 km/h)"""
        n1 = self.nodes[node_id]
        n2 = self.nodes[target_id]
        dist_km = haversine(n1['lat'], n1['lon'], n2['lat'], n2['lon'])
        return (dist_km / 35.0) * 60.0 # Time in minutes

    def route(self, start_id, end_id, algorithm='dijkstra', optimize_for='time'):
        """
        Finds the optimal route.
        algorithm: 'dijkstra' or 'astar'
        optimize_for: 'time' or 'transfers'
        """
        start_time = time.perf_counter()
        
        # Priority queue: (f_cost, g_cost, current_node, path, current_line, transfers, segments)
        pq = [(0, 0, start_id, [start_id], None, 0, [])]
        
        # Track best g_cost to reach a node with a specific line
        best_costs = {}
        nodes_explored = 0
        
        # Transfer penalties
        TRANSFER_PENALTY_TIME = 5.0 # 5 minutes to switch lines
        TRANSFER_PENALTY_TRANSFERS = 1000.0 # Heavy penalty for 'fewest transfers' mode
        
        while pq:
            f_cost, g_cost, current, path, current_line, transfers, segments = heapq.heappop(pq)
            nodes_explored += 1
            
            if current == end_id:
                exec_time = time.perf_counter() - start_time
                
                actual_time = g_cost
                if optimize_for == 'transfers':
                    actual_time = g_cost - (transfers * TRANSFER_PENALTY_TRANSFERS) + (transfers * TRANSFER_PENALTY_TIME)
                
                return {
                    'path': [self.nodes[n]['name'] for n in path],
                    'path_ids': list(path),
                    'time_cost_mins': round(actual_time, 2),
                    'transfers': transfers,
                    'nodes_explored': nodes_explored,
                    'execution_time_ms': round(exec_time * 1000, 4),
                    'algorithm': algorithm,
                    'optimized_for': optimize_for,
                    'segments': [
                        {
                            'from_id': u,
                            'from_name': self.nodes[u]['name'],
                            'to_id': v,
                            'to_name': self.nodes[v]['name'],
                            'line': line,
                            'time_mins': t,
                            'is_transfer': is_xfer
                        }
                        for u, v, line, t, is_xfer in segments
                    ]
                }
                
            state_key = (current, current_line)
            if state_key in best_costs and best_costs[state_key] <= g_cost:
                continue
            best_costs[state_key] = g_cost
            
            for neighbor, edge_time, line_name in self.edges[current]:
                is_transfer = (current_line is not None and current_line != line_name)
                new_transfers = transfers + (1 if is_transfer else 0)
                
                step_cost = edge_time
                if is_transfer:
                    if optimize_for == 'transfers':
                        step_cost += TRANSFER_PENALTY_TRANSFERS
                    else:
                        step_cost += TRANSFER_PENALTY_TIME
                        
                new_g_cost = g_cost + step_cost
                
                # Calculate A* Heuristic (h_cost)
                h_cost = 0
                if algorithm == 'astar':
                    h_cost = self.get_heuristic(neighbor, end_id)
                    if optimize_for == 'transfers':
                        h_cost = 0 
                        
                new_f_cost = new_g_cost + h_cost
                new_segments = segments + [(current, neighbor, line_name, edge_time, is_transfer)]
                
                heapq.heappush(pq, (new_f_cost, new_g_cost, neighbor, path + [neighbor], line_name, new_transfers, new_segments))
                
        return None
