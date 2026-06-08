import time
from tspd.tspd_utils import generate_nodes, compute_distance_matrix
from solvers.hga_solver import hga_solve
from solvers.grasp_solver import grasp_solve
from solvers.hga_shc import hga_shc_solve

def run_benchmarks():
    sizes = [5, 10, 100,200]
    seed = 42
    
    iters_small, iters_large = 100, 500 #we can change this according to our needs  by decreaing the number of iterations it takes less time to run
    pop_size = 20 # we can change this too

    results = {"Paper": {}, "GRASP": {}, "HSC": {}}

    for size in sizes:
        nodes = generate_nodes(size, seed=seed)
        dist_matrix = compute_distance_matrix(nodes)
        iters = iters_small if size < 50 else iters_large

        # Run Algorithms
        results["Paper"][size] = hga_solve(nodes, dist_matrix, iterations=iters, pop_size=pop_size)
        results["GRASP"][size] = grasp_solve(nodes, dist_matrix, iterations=50)
        results["HSC"][size] = hga_shc_solve(nodes, dist_matrix, iterations=iters, pop_size=pop_size)

    #the ouput
    print(f"HGA algorithm cost (Z):")
    for size in sizes: print(f"On {size} node : {results['Paper'][size]:.2f}")

    print(f"\nGRASP algorithm cost (Z):")
    for size in sizes: print(f"On {size} node : {results['GRASP'][size]:.2f}")

    print(f"\nHSC algorithm cost:") # Output label per team request
    for size in sizes: print(f"On {size} node : {results['HSC'][size]:.2f}")

if __name__ == "__main__":
    run_benchmarks()