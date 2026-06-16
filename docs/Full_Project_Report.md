# Complete Technical Report: Hybrid Truck-Drone Delivery Optimization

## 1. Project Overview

This project focuses on the optimization of a hybrid truck-drone delivery system. The problem studied in the project is known as the Traveling Salesman Problem with Drone, abbreviated as TSP-D.

In a classical Traveling Salesman Problem, a single vehicle starts from a depot, visits all customers exactly once, and returns to the depot with minimum travel cost. In TSP-D, the problem becomes more complex because there are two delivery resources:

* one truck,
* one drone.

The truck follows the main road-based route and also acts as a mobile depot for the drone. The drone can be launched from the truck, serve a customer, and return to the truck at a later rendezvous point. Therefore, the project does not only optimize the customer visiting order, but also decides how customers should be assigned between the truck and the drone.

The main objective of the project is to minimize the total operational cost of the delivery system.

The total operational cost includes:

* truck travel cost,
* drone flight cost,
* waiting or synchronization cost between the truck and the drone.

The project implements and compares three heuristic/metaheuristic approaches:

| Method  | Purpose                                                 |
| ------- | ------------------------------------------------------- |
| HGA     | Hybrid Genetic Algorithm baseline                       |
| GRASP   | Benchmark comparison method                             |
| HGA-SHC | Proposed enhanced method using Stochastic Hill Climbing |

The proposed contribution of the project is the integration of Stochastic Hill Climbing into a Hybrid Genetic Algorithm framework. This enhanced method is called HGA-SHC.

---

## 2. Problem Definition

The TSP-D system consists of:

* a depot,
* one truck,
* one drone,
* multiple customer nodes.

Each customer must be served exactly once. A customer can either be visited directly by the truck or served by the drone.

A drone delivery operation usually has three parts:

1. The drone is launched from the truck at a launch node.
2. The drone visits a customer.
3. The drone returns to the truck at a rendezvous node.

This creates an important synchronization problem. If the truck arrives at the rendezvous point earlier than the drone, the truck must wait. If the drone arrives earlier, the drone must wait. This waiting time is included as a cost component.

Therefore, the problem includes both routing and assignment decisions.

Routing decision:

* In which order should the customers be visited?

Assignment decision:

* Which customers should be served by the truck?
* Which customers should be served by the drone?

The difficulty of the problem increases rapidly as the number of customers increases. For this reason, exact optimization methods become inefficient for larger instances. Therefore, heuristic and metaheuristic algorithms are used.

---

## 3. Objective Function

The objective of the project is to minimize the total operational cost.

The general cost structure is:

```text
Total Cost = Truck Travel Cost + Drone Travel Cost + Waiting Cost
```

Truck travel cost represents the cost of the truck route.

Drone travel cost represents the cost of the drone flight from a launch node to a customer and then to a rendezvous node.

Waiting cost represents the synchronization penalty if the truck or the drone arrives earlier and has to wait.

A lower total cost means a better solution.

---

## 4. Constraints Considered in the Project

The implemented model considers the main constraints of a truck-drone delivery system:

1. Every customer must be served exactly once.
2. The truck must start from the depot.
3. The truck must return to the depot.
4. The drone can only be launched from the truck.
5. The drone must return to the truck at a rendezvous point.
6. The drone route must respect its endurance/range limitation.
7. Truck and drone operations must be synchronized.
8. The generated route must remain feasible.

The project uses generated customer coordinates in a coordinate plane. Distances are calculated using Euclidean distance.

---

## 5. Technologies and Tools Used

The project is implemented in Python.

Main tools and technologies:

| Tool / Technology | Purpose                                          |
| ----------------- | ------------------------------------------------ |
| Python            | Main programming language                        |
| NumPy             | Numerical operations and array-based computation |
| Matplotlib        | Plotting benchmark and performance results       |
| Jupyter Notebook  | Visual analysis and plotting experiments         |
| GitHub            | Version control and project sharing              |
| Markdown          | Documentation, README, and report writing        |
| CSV / TXT files   | Storing validation and benchmark results         |

The project is modularized into separate folders for solvers, utilities, experiments, documentation, data, and notebooks.

---

## 6. Project Folder Structure

The project is organized as follows:

```text
tspd-project/
│
├── README.md
├── requirements.txt
├── main.py
├── .gitignore
│
├── tspd/
│   ├── __init__.py
│   └── tspd_utils.py
│
├── solvers/
│   ├── __init__.py
│   ├── hga_solver.py
│   ├── hga_shc.py
│   └── grasp_solver.py
│
├── experiments/
│   ├── __init__.py
│   ├── main_benchmark.py
│   └── validation_benchmark.py
│
├── data/
│   ├── results.txt
│   ├── validation_results.csv
│   └── validation_summary.md
│
├── docs/
│   └── Problem faced.md
│
├── notebooks/
│   └── plot.ipynb
│
└── public/
    └── flowchart image
```

Each folder has a specific role.

The `tspd/` folder contains the mathematical and utility functions.

The `solvers/` folder contains the optimization algorithms.

The `experiments/` folder contains scripts for running benchmark and validation experiments.

The `data/` folder stores result outputs.

The `docs/` folder contains additional documentation about problems faced during implementation.

The `notebooks/` folder is used for plotting and visual analysis.

The `public/` folder contains images used in the README or presentation.

---

## 7. Module-by-Module Explanation

### 7.1 `main.py`

This is the main entry point of the project.

When the user runs:

```bash
python main.py
```

the benchmark process starts. It calls the benchmark runner and executes the implemented algorithms on generated customer node sets.

The purpose of this file is to provide a simple starting point for running the project.

---

### 7.2 `tspd/tspd_utils.py`

This file contains the core utility functions of the project.

Main responsibilities:

* generating customer nodes,
* computing distance matrices,
* creating initial tours,
* evaluating truck-drone route cost,
* applying the split procedure.

Important functions include:

| Function                    | Purpose                                                        |
| --------------------------- | -------------------------------------------------------------- |
| `generate_nodes()`          | Generates depot and customer coordinates                       |
| `compute_distance_matrix()` | Computes Euclidean distances between nodes                     |
| `get_nn_tour()`             | Creates a nearest-neighbor initial tour                        |
| `split_procedure()`         | Evaluates a giant tour by assigning truck and drone operations |

The `split_procedure()` function is one of the most important parts of the project. It takes a giant tour and calculates the total cost by considering possible truck and drone operations.

---

### 7.3 `solvers/hga_solver.py`

This file implements the standard HGA baseline.

HGA stands for Hybrid Genetic Algorithm.

The basic idea of HGA is to maintain a population of candidate solutions. Each candidate solution represents a possible customer visiting order, also called a giant tour.

The HGA process generally includes:

1. Initial population generation.
2. Fitness evaluation.
3. Parent selection.
4. Crossover.
5. Mutation.
6. Population update.
7. Best solution tracking.

In this project, HGA is used as the baseline algorithm. The performance of the proposed HGA-SHC method is compared against this baseline.

---

### 7.4 `solvers/hga_shc.py`

This file implements the proposed HGA-SHC method.

HGA-SHC means Hybrid Genetic Algorithm with Stochastic Hill Climbing.

The purpose of HGA-SHC is to improve the standard HGA by adding a local refinement stage.

The logic is:

1. HGA performs global search.
2. HGA generates candidate solutions.
3. SHC performs local improvements on candidate solutions.
4. The best refined solution is kept.

SHC uses small random neighborhood changes. In the current implementation, the main neighborhood operator is random swap.

A random swap means that two customer positions in the giant tour are selected randomly and their positions are exchanged.

If the new solution has a lower cost, it is accepted. In some cases, a non-improving solution may also be accepted with a small probability. This helps reduce the risk of being trapped in a local optimum.

The main SHC-related parameters are:

| Parameter              | Meaning                                        |
| ---------------------- | ---------------------------------------------- |
| SHC iteration number   | Number of local search attempts                |
| Acceptance probability | Probability of accepting a non-improving move  |
| Neighborhood operator  | Type of local modification, mainly random swap |
| Population size        | Number of candidate solutions in HGA           |
| HGA iteration number   | Number of genetic algorithm iterations         |

The advantage of HGA-SHC is better local refinement.

The disadvantage is higher runtime because additional local search is performed.

---

### 7.5 `solvers/grasp_solver.py`

This file implements the GRASP benchmark algorithm.

GRASP stands for Greedy Randomized Adaptive Search Procedure.

GRASP is used as a comparison method. It builds routes using greedy logic, but with some randomness. Instead of always selecting the nearest possible node, it selects from a restricted candidate list.

The purpose of including GRASP is to compare the proposed method with a different heuristic approach.

In this project, GRASP is especially useful as a benchmark because it behaves differently from population-based genetic algorithms.

---

### 7.6 `experiments/main_benchmark.py`

This file runs the main benchmark comparison.

It executes:

* HGA,
* GRASP,
* HGA-SHC.

All algorithms are tested on the same generated node sets. This is important for fairness. If different algorithms are tested on different customer coordinates, the comparison would not be valid.

The benchmark records and prints cost values for different customer sizes.

Example node sizes:

```text
5, 10, 100, 200
```

The purpose of this file is to compare the algorithms under the same conditions.

---

### 7.7 `experiments/validation_benchmark.py`

This file was added for final validation and reproducibility analysis.

It runs a faster validation benchmark using fixed random seeds.

The purpose of fixed seeds is reproducibility. Since HGA, GRASP, and SHC contain random operations, the results may change in every run. Fixed seeds make the experiments repeatable.

This file evaluates the algorithms using multiple metrics:

* best cost,
* average cost,
* standard deviation,
* average runtime,
* improvement percentage over HGA.

It produces two output files:

```text
data/validation_results.csv
data/validation_summary.md
```

This validation benchmark supports the final project requirements:

* benchmark testing,
* validation and refinement,
* performance evaluation,
* robustness analysis,
* reproducibility.

---

### 7.8 `data/results.txt`

This file stores benchmark outputs.

It is used to keep a record of the cost values obtained from the main benchmark tests.

---

### 7.9 `data/validation_results.csv`

This file stores detailed validation results in CSV format.

It includes results for multiple customer sizes, algorithms, seeds, costs, and runtimes.

CSV format is useful because the data can be opened in Excel, Google Sheets, or Python for further analysis.

---

### 7.10 `data/validation_summary.md`

This file summarizes the validation benchmark results in Markdown format.

It includes average cost, best cost, standard deviation, runtime, and improvement percentage.

This file is useful for directly copying results into the README or final report.

---

### 7.11 `docs/Problem faced.md`

This file explains implementation challenges and design decisions.

One of the main challenges was computational complexity. A naive route evaluation approach can become very expensive for large instances. To reduce this problem, the project uses optimized route evaluation ideas such as distance prefix sums and limited lookahead.

This improves scalability and makes the project more practical for larger node sizes.

---

### 7.12 `notebooks/plot.ipynb`

This notebook is used for plotting benchmark results.

It can be used to create:

* cost comparison charts,
* runtime comparison charts,
* improvement percentage charts,
* convergence-style visualizations.

The notebook is not the main execution file, but it is useful for visual analysis.

---

## 8. Algorithmic Workflow

The operational workflow of the proposed HGA-SHC method is:

```text
Start
↓
Generate customer nodes
↓
Compute distance matrix
↓
Initialize population
↓
Apply HGA operations
    - selection
    - crossover
    - mutation
↓
Apply split procedure
    - truck-drone allocation
    - cost evaluation
↓
Apply SHC local refinement
    - random swap
    - local cost comparison
    - possible acceptance of new solution
↓
Update best solution
↓
Return final cost
```

This workflow combines global search and local search.

HGA provides global exploration.

SHC provides local refinement.

Together, they try to produce lower-cost truck-drone routes.

---

## 9. Explanation of Main Concepts

### 9.1 TSP-D

TSP-D means Traveling Salesman Problem with Drone.

It is a routing problem where a truck and a drone work together to serve customers.

The goal is to minimize total delivery cost.

---

### 9.2 Giant Tour

A giant tour is a sequence of all customer nodes.

Example:

```text
Depot → 4 → 2 → 7 → 1 → 5 → Depot
```

At first, this sequence does not decide which customers are served by truck or drone. The split procedure later divides this tour into truck and drone operations.

---

### 9.3 Split Procedure

The split procedure evaluates a giant tour and decides how to divide it between the truck and drone.

It checks possible drone operations and calculates the total cost.

It considers:

* truck travel distance,
* drone travel distance,
* drone endurance,
* launch and rendezvous points,
* waiting cost.

---

### 9.4 HGA

HGA stands for Hybrid Genetic Algorithm.

It is a population-based search method.

It creates many candidate solutions and improves them over generations.

Main operators:

* selection,
* crossover,
* mutation.

HGA is good for global search, but it may still become trapped around local optima.

---

### 9.5 SHC

SHC stands for Stochastic Hill Climbing.

It is a local search method.

It starts from an existing solution and makes small random changes. If the new solution is better, it is accepted.

In this project, SHC mainly uses random swap as the neighborhood operator.

SHC improves local refinement but increases runtime.

---

### 9.6 GRASP

GRASP stands for Greedy Randomized Adaptive Search Procedure.

It is a heuristic algorithm that combines greedy construction with randomness.

It is used as a benchmark comparison method in this project.

---

## 10. How to Install and Run the Project

### Step 1: Clone the repository

```bash
git clone <repository-url>
cd tspdddd-2
```

### Step 2: Create a virtual environment

For macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the main benchmark

```bash
python main.py
```

This runs the main benchmark and compares HGA, GRASP, and HGA-SHC.

### Step 5: Run the validation benchmark

```bash
python -m experiments.validation_benchmark
```

This generates reproducibility and validation results.

Expected output files:

```text
data/validation_results.csv
data/validation_summary.md
```

---

## 11. Benchmark Testing

The project includes benchmark testing to compare the implemented methods.

The compared algorithms are:

* HGA,
* GRASP,
* HGA-SHC.

The same generated customer nodes are used for all algorithms. This ensures fair comparison.

The benchmark evaluates total cost values for different customer sizes.

The general interpretation is:

* HGA-SHC performs similarly to HGA on small instances.
* HGA-SHC can slightly improve cost on larger instances.
* GRASP may perform competitively on small instances but can become worse as the problem size increases.
* HGA-SHC requires more runtime because of the additional SHC local search stage.

---

## 12. Validation and Reproducibility

The validation benchmark was added to make the results more reliable.

Since the algorithms include random components, a single run is not enough to evaluate performance. Therefore, the validation benchmark uses fixed random seeds.

The validation process measures:

| Metric             | Meaning                                    |
| ------------------ | ------------------------------------------ |
| Best Cost          | Best solution found                        |
| Average Cost       | Average solution quality across runs       |
| Standard Deviation | Stability or robustness of the algorithm   |
| Average Runtime    | Computational time                         |
| Improvement vs HGA | Percentage improvement of HGA-SHC over HGA |

The improvement percentage is calculated as:

```text
Improvement (%) = ((HGA Cost - HGA-SHC Cost) / HGA Cost) × 100
```

If the improvement value is positive, HGA-SHC produced a lower cost than HGA.

The validation results show that HGA-SHC improves average solution quality compared to the HGA baseline on the tested generated instances. However, runtime increases because SHC performs extra local neighborhood exploration.

This creates a quality-runtime trade-off.

---

## 13. Convergence Analysis

Convergence analysis explains how the algorithm improves solution quality over iterations.

In a standard HGA, the algorithm may improve quickly at first, but after some iterations it may stabilize. This means that the algorithm may become trapped near a local optimum.

HGA-SHC tries to reduce this problem by adding SHC after the genetic search stage.

SHC explores neighboring solutions using random modifications. When it finds a better neighbor, it updates the current solution.

Therefore, HGA-SHC can continue improving the cost even after the HGA phase starts to stabilize.

This does not mean the algorithm guarantees a global optimum. HGA-SHC is still a heuristic/metaheuristic method. It aims to find good-quality solutions efficiently, not mathematically guaranteed optimal solutions.

---

## 14. What Was Done in the Project

The project work can be summarized as follows:

1. The TSP-D problem was selected as the optimization problem.
2. The mathematical structure of the truck-drone delivery system was analyzed.
3. Customer node generation and distance matrix computation were implemented.
4. A split procedure was implemented to evaluate truck-drone delivery costs.
5. A standard HGA baseline was implemented.
6. A GRASP benchmark algorithm was implemented.
7. A proposed HGA-SHC algorithm was implemented.
8. The project was modularized into folders such as `solvers`, `tspd`, `experiments`, and `data`.
9. Main benchmark tests were run on generated instances.
10. Validation benchmark testing was added using fixed random seeds.
11. Performance metrics were calculated.
12. Results were exported as CSV and Markdown files.
13. The README and final report were updated.
14. The project was pushed to GitHub.

---

## 15. Course Requirement Mapping

| Course Requirement        | Project Evidence                                                                                           |
| ------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Coding Phase I            | Core data structures, utility functions, distance matrix generation, and split procedure were implemented. |
| Coding Phase II           | Initial tests were performed on generated TSP-D instances and logic errors were corrected.                 |
| Coding Phase III          | The proposed HGA-SHC algorithm was finalized and integrated.                                               |
| Benchmark Testing         | HGA, GRASP, and HGA-SHC were compared on generated benchmark instances.                                    |
| Validation and Refinement | Runtime, best cost, average cost, standard deviation, and improvement percentage were calculated.          |
| Performance Evaluation    | The proposed method was evaluated in terms of solution quality, runtime, and robustness.                   |

---

## 16. Main Findings

The main findings of the project are:

1. HGA-SHC can improve the solution quality compared to the standard HGA baseline.
2. The improvement is more visible as the problem size increases.
3. GRASP is useful as a benchmark method, but it may produce worse results on larger instances.
4. SHC improves local refinement capability.
5. The additional SHC stage increases runtime.
6. Therefore, HGA-SHC creates a trade-off between better route quality and higher computational time.
7. Fixed-seed validation improves reproducibility and makes the comparison more reliable.

---

## 17. Limitations

The current implementation has some limitations:

1. The benchmark uses generated customer coordinates instead of official benchmark datasets from the original article.
2. SHC mainly uses random swap as the local neighborhood operator.
3. The split procedure evaluates cost but does not fully visualize truck and drone routes separately.
4. The project focuses on a simplified truck-drone model.
5. More advanced local search operators such as 2-opt, relocation, or drone-aware reassignment could improve the solution quality.
6. More extensive testing with larger benchmark datasets could make the results stronger.

---

## 18. Future Work

Future improvements may include:

1. Adding official benchmark datasets if available.
2. Adding route visualization for truck and drone paths.
3. Adding convergence plots over iterations.
4. Testing more random seeds.
5. Using stronger local search operators such as 2-opt and relocation.
6. Adding multi-drone support.
7. Improving the drone assignment mechanism.
8. Exporting detailed truck-drone schedules.
9. Creating a simple web interface for visualization.
10. Comparing the method with additional metaheuristics.

---

## 19. Final Conclusion

This project implemented a hybrid truck-drone delivery optimization system for the Traveling Salesman Problem with Drone.

The main contribution is the proposed HGA-SHC method, which combines the global search ability of a Hybrid Genetic Algorithm with the local refinement ability of Stochastic Hill Climbing.

The benchmark and validation results show that HGA-SHC can improve solution quality compared to the standard HGA baseline. However, this improvement comes with higher runtime because SHC performs additional local search.

Therefore, the proposed method is useful when better route quality is more important than the fastest execution time.

Overall, the project successfully demonstrates the design, implementation, benchmarking, validation, and analysis of a metaheuristic optimization approach for hybrid truck-drone delivery systems.
