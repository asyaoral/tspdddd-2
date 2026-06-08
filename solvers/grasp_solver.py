import random
from tspd.tspd_utils import split_procedure

def grasp_solve(nodes, dist_matrix, iterations=50):
    best_cost = float('inf')
    n = len(nodes)
    for _ in range(iterations):
        unvisited = set(range(1, n))
        curr, tour = 0, [0]
        while unvisited:
            candidates = sorted(list(unvisited), key=lambda x: dist_matrix[curr][x])
            rcl = candidates[:max(1, len(candidates)//3)]
            nxt = random.choice(rcl)
            tour.append(nxt)
            unvisited.remove(nxt)
            curr = nxt
        tour.append(0)
        cost = split_procedure(tour, dist_matrix)
        if cost < best_cost: best_cost = cost
    return best_cost