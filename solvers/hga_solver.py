import random
from tspd.tspd_utils import split_procedure, get_nn_tour

def hga_solve(nodes, dist_matrix, iterations=100, pop_size=20):
    # Population init with NN and small variations 
    population = []
    base_tour = get_nn_tour(dist_matrix)
    for _ in range(pop_size):
        tour = list(base_tour)
        if random.random() > 0.5: # Add small noise to some individuals
            i, j = random.sample(range(1, len(tour)-1), 2)
            tour[i], tour[j] = tour[j], tour[i]
        cost = split_procedure(tour, dist_matrix)
        population.append((cost, tour))
    
    for _ in range(iterations):
        population.sort(key=lambda x: x[0])
        p1, p2 = random.choices(population[:pop_size//2], k=2)
        
        # Simple Crossover
        pt = random.randint(1, len(nodes)-1)
        child = p1[1][:pt]
        for node in p2[1]:
            if node not in child: child.append(node)
        if child[-1] != 0: child.append(0)
        
        cost = split_procedure(child, dist_matrix)
        population.append((cost, child))
        population = sorted(population, key=lambda x: x[0])[:pop_size]
        
    return population[0][0]