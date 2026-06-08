import math
import random

# Constants from Paper-12
TRUCK_SPEED = 40.0 / 60.0
DRONE_SPEED = 40.0 / 60.0
ENDURANCE = 20.0
SERVICE_TIME_TRUCK = 1.0
SERVICE_TIME_DRONE = 1.0
C1, C2 = 1.0, 1.0
WAIT_COST_TRUCK, WAIT_COST_DRONE = 2.0, 1.0

def generate_nodes(num_nodes, seed=42):
    random.seed(seed)
    return [(5, 5)] + [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(num_nodes)]

def compute_distance_matrix(nodes):
    n = len(nodes)
    return [[math.hypot(nodes[i][0]-nodes[j][0], nodes[i][1]-nodes[j][1]) for j in range(n)] for i in range(n)]

def get_nn_tour(dist_matrix):
    n = len(dist_matrix); unvisited = set(range(1, n)); curr = 0; tour = [0]
    while unvisited:
        nxt = min(unvisited, key=lambda x: dist_matrix[curr][x])
        tour.append(nxt); unvisited.remove(nxt); curr = nxt
    return tour + [0]

def split_procedure(giant_tour, dist_matrix):
    n = len(giant_tour)
    pref = [0.0] * n
    for i in range(1, n):
        pref[i] = pref[i-1] + dist_matrix[giant_tour[i-1]][giant_tour[i]]

    dp = [float('inf')] * n
    dp[0] = 0

    for i in range(n - 1):
        if dp[i] == float('inf'): continue
        
        # 1. Direct Truck Edge
        direct_cost = C1 * dist_matrix[giant_tour[i]][giant_tour[i+1]]
        if dp[i] + direct_cost < dp[i+1]:
            dp[i+1] = dp[i] + direct_cost
        
        # OPTIMIZATION 3: Drone Edge with Early Exit
        max_k = min(i + 15, n)
        
        for j in range(i + 1, max_k - 1):
            # Drone flies i -> j -> k
            dist_i_j = dist_matrix[giant_tour[i]][giant_tour[j]]
            for k in range(j + 1, max_k):
                d_dist = dist_i_j + dist_matrix[giant_tour[j]][giant_tour[k]]
                d_time = d_dist / DRONE_SPEED + SERVICE_TIME_DRONE
                
                if d_time > ENDURANCE: continue # Early exit
                
                full_t_dist = pref[k] - pref[i]
                rem_edges = dist_matrix[giant_tour[j-1]][giant_tour[j]] + dist_matrix[giant_tour[j]][giant_tour[j+1]]
                add_edge = dist_matrix[giant_tour[j-1]][giant_tour[j+1]]
                t_dist = full_t_dist - rem_edges + add_edge
                t_time = t_dist / TRUCK_SPEED + SERVICE_TIME_TRUCK
                
                cost = (C1 * t_dist) + (C2 * d_dist) + \
                       (max(0, d_time - t_time) * WAIT_COST_TRUCK) + \
                       (max(0, t_time - d_time) * WAIT_COST_DRONE)
                
                if dp[i] + cost < dp[k]:
                    dp[k] = dp[i] + cost
                        
    return dp[n-1]