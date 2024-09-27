import random

ENERGY_DEFAULT_VALUE = 0

RANDINT_DEFAULT_LEFT_BOUND = 0

DELTAS_LENGHT = 4

class Solution:
  def __init__(
      self,
      plan: list[int] = [],
      energy: int = ENERGY_DEFAULT_VALUE) -> "Solution":
    self.__n_queens = len(plan)
    
    self.__plan = plan
    self.__energy = energy
    
  @classmethod
  def default(cls, n_queens: int) -> "Solution":
    solution = Solution([i for i in range(n_queens)])
    
    for _ in range(n_queens):
      solution.modify()
    
    return cls(plan=solution.__plan)
  
  def __get_random_index(self, right_bound: int) -> int:
    return random.randint(RANDINT_DEFAULT_LEFT_BOUND, right_bound - 1)
  
  def modify(self) -> None:
    i = self.__get_random_index(self.__n_queens)
    j = self.__get_random_index(self.__n_queens)
    
    while j == i:
      j = self.__get_random_index(self.__n_queens)
    
    self.__plan[i], self.__plan[j] = self.__plan[j], self.__plan[i]
  
  def calculate_energy(self) -> None:
    dx = (-1, 1, -1, 1)
    dy = (-1, 1, 1, -1)

    n_errors = 0
    
    for x in range(self.__n_queens):
      for j in range(DELTAS_LENGHT):
        tx = x + dx[j]
        ty = self.__plan[x] + dy[j]
        
        while (0 <= tx < self.__n_queens
               and 0 <= ty < self.__n_queens):
          if self.__plan[tx] == ty:
            n_errors += 1
          
          tx += dx[j]
          ty += dy[j]
          
    self.__energy = n_errors

  @property
  def plan(self) -> list[int]:
    return self.__plan[::]
  
  @plan.setter
  def plan(self, new_plan: list[int]) -> None:
    self.__plan = new_plan[::]
  
  @property
  def energy(self) -> float:
    return self.__energy
  
  @property
  def n_queens(self) -> int:
    return self.__n_queens
  
  @energy.setter
  def energy(self, new_energy_value: float) -> None:
    self.__energy = new_energy_value
    
  def copy(self, source_solution: 'Solution') -> None:
    self.__plan = source_solution.plan[::]
    self.__energy = source_solution.energy
    self.__n_queens = source_solution.n_queens
