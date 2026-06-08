# Problems Faced & Implementation Challenges

## 1. The Multi-Vehicle Synchronization Problem
The core challenge of the Traveling Salesman Problem with Drone (TSP-D) is coordinating two vehicles with vastly different constraints.
- **Problem**: Early versions of the code restricted the drone to skipping only one customer at a time.
- **Approaches Considered**:
  - *Simple Triplet Logic*: Restricting drone deliveries to a simple (launch, delivery, rendezvous) sequence where the truck moves directly from launch to rendezvous. This was discarded as it failed to capture the efficiency of the "multi-node" truck travel allowed in the paper.
  - *Multi-Node Auxiliary Graph (Final Choice)*: Constructing a directed graph where an edge from node $i$ to node $k$ represents the optimal cost of the truck visiting a sequence of nodes while the drone delivers to a customer $j$.

## 2. The Computational Bottleneck ($O(N^3)$ Complexity)
As the node count reached 100, the execution time became unsustainable.
- **Problem**: The `split_procedure` was re-calculating truck distances and shortest paths thousands of times inside nested loops.
- **Approaches Considered**:
  - *NetworkX Library*: Using a high-level graph library for shortest paths. While accurate, the overhead was too high for the 100-node benchmark.
  - *Prefix Sums & Dynamic Programming (Final Choice)*: Pre-calculating a distance array to allow $O(1)$ distance lookups and using a list-based DP array for the shortest path.
  - *Lookahead Limiting*: Restricting the rendezvous search to a specific number of nodes ahead, based on the drone's endurance constraint ($E$).

## 3. Deterministic vs. Stochastic Local Search
A major point of comparison was how to "educate" the solutions found by the Genetic Algorithm.
- **Problem**: Deterministic moves (like simple swaps) often get stuck in "local optima" where no single swap can improve the cost further.
- **Approaches Considered**:
  - *Deterministic Operators*: Applying 16 specific move operators (relocation, 2-opt, etc.) as described in the paper.
  - *Stochastic Hill Climbing (IE Team Proposal)*: Replacing fixed rules with random swaps and a probabilistic acceptance criterion. This allows the algorithm to occasionally accept a "worse" move to eventually find a much better global solution.

## 4. The Initialization Problem (Random vs. Heuristic)
The starting state of the population determines how quickly the algorithm converges.
- **Problem**: Randomly generated tours for 100 nodes are highly inefficient and require thousands of generations to "untangle."
- **Approaches Considered**:
  - *Random Initialization*: Generating a set of random shuffles. This resulted in extremely high costs for 100 nodes.
  - *Nearest Neighbor (NN) Heuristic (Final Choice)*: Starting with a tour where the truck always visits the closest unvisited customer. This provided a "clean" starting point, allowing the HGA and HSC to focus on optimizing drone synchronization rather than basic truck routing.

## 5. Mathematical Modeling of Costs
The total operational cost $Z$ had to account for both movement and idle time.
- **Objective Function**:
$$Z = \sum_{e \in TD} \mathcal{C}_1 d_{ij} + \sum_{\langle i,j,k \rangle \in DD} \mathcal{C}_2(d_{ij}' + d_{jk}') + \text{WaitingCost}$$
- **Waiting Cost Logic**: Correcting the implementation to properly penalize the truck for arriving early at a rendezvous point ($W_T$) and the drone for having to hover while waiting for the truck ($W_D$).

