from solution import Solution

import random
from math import exp

BEST_SOLUTION_ENERGY_INIT_VALUE = 100


def make_annealing(
    n_queens: int,
    initial_temperature: float,
    final_temperature: float,
    cooling_rate: float,
    n_steps: int) -> tuple[Solution, list[int], list[int], list[int]]:
  timer = 0
  current_temperature = initial_temperature
  
  temperatures = []
  energies = []
  bad_solutions = []
  
  best_solution = Solution([], BEST_SOLUTION_ENERGY_INIT_VALUE)
  
  current_solution = Solution.default(n_queens)
  current_solution.calculate_energy()
  
  working_solution = Solution()
  working_solution.copy(current_solution)
  
  while current_temperature > final_temperature:
    n_bad_solutions = 0
    
    for _ in range(n_steps):
      is_new = False
      
      working_solution.copy(current_solution)
      working_solution.modify()
      working_solution.calculate_energy()
      
      if working_solution.energy <= current_solution.energy:
        is_new = True
      else:
        n_bad_solutions += 1

        p = exp(-(working_solution.energy - current_solution.energy) /
                current_temperature)
        
        is_new = p > random.random()
        
      if is_new:
        is_new = False
        
        current_solution.copy(working_solution)
        
        if current_solution.energy < best_solution.energy:
          best_solution.copy(current_solution)
      else:
        working_solution.copy(current_solution)

    temperatures.append(current_temperature)
    energies.append(best_solution.energy)
    bad_solutions.append(n_bad_solutions)
    
    current_temperature *= cooling_rate
    timer += 1
  
  return best_solution, temperatures, energies, bad_solutions