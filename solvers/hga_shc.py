import random, math
from tspd.tspd_utils import split_procedure, get_nn_tour

def shc_education(tour, dist_matrix, iters=30):

    best_tour = list(tour)
    best_cost = split_procedure(best_tour, dist_matrix)
    for _ in range(iters):
        neighbor = list(best_tour)
        i, j = random.sample(range(1, len(neighbor)-1), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        n_cost = split_procedure(neighbor, dist_matrix)
        if n_cost < best_cost or random.random() < 0.05:
            best_tour, best_cost = neighbor, n_cost
    return best_tour, best_cost

def hga_shc_solve(nodes, dist_matrix, iterations=100, pop_size=20):
    base_tour = get_nn_tour(dist_matrix)
    population = []
    for _ in range(pop_size):
        tour = list(base_tour)
        if random.random() > 0.5:
            i, j = random.sample(range(1, len(tour)-1), 2)
            tour[i], tour[j] = tour[j], tour[i]
        _, cost = shc_education(tour, dist_matrix, 10)
        population.append((cost, tour))

    for _ in range(iterations):
        population.sort(key=lambda x: x[0])
        p1, p2 = random.choices(population[:pop_size//2], k=2)
        pt = random.randint(1, len(nodes)-1)
        child = p1[1][:pt]
        for node in p2[1]:
            if node not in child: child.append(node)
        if child[-1] != 0: child.append(0)
        
        educated_tour, cost = shc_education(child, dist_matrix)
        population.append((cost, educated_tour))
        population = sorted(population, key=lambda x: x[0])[:pop_size]
    return population[0][0]