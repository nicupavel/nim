# NIM
Nature Inspired Methods:
 - HillClimbing
 - Simulated Annealing Hill Climbing
 - Genetic Algorithm with variations
 - Particle Swarm Optimisation

# Evaluator functions
 - Rastrigin
 - Griewangk
 - Rosenbrock
 - Sixhump
 
 http://www.geatbx.com/docu/fcnindex-01.html#P140_6155


# Method Comparison 
 30 runs each for a maximum of 5000 evaluation functions calls


| Algo       | Rastrigin  |            |            | Griewangk  |            |            | Rosenbrock |            |            | Sixhump    |            |            |
|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|
|            | 5          | 10         | 30         | 5          | 10         | 30         | 5          | 10         | 30         | 5          | 10         | 30         |
| GA         |       2.08 |       7.90 |     162.61 |       0.09 |       0.24 |       4.18 |       3.04 |      12.55 |     111.82 |      -1.03 |      -1.02 |      -1.03 |
|    Std Dev |       1.38 |       3.02 |      21.41 |       0.06 |       0.17 |       1.95 |       1.78 |      16.17 |      65.74 |       0.01 |       0.02 |       0.01 |
| GA Hybrid  |       0.44 |      20.00 |     352.25 |       0.22 |      10.58 |     438.80 |       1.17 |      24.35 |    3402.52 |      -1.03 |      -1.03 |      -1.03 |
|    Std Dev |       0.63 |       5.60 |      26.55 |       0.12 |       5.50 |      60.51 |       1.16 |      15.52 |     829.96 |       0.00 |       0.00 |       0.00 |
| PSO        |       0.07 |       2.89 |      36.82 |       0.02 |       0.08 |       0.01 |       0.06 |       3.05 |      28.97 |      -1.03 |      -1.03 |      -1.03 |
|    Std Dev |       0.25 |       1.53 |       9.45 |       0.01 |       0.04 |       0.01 |       0.02 |       1.01 |      14.04 |       0.00 |       0.00 |       0.00 |

