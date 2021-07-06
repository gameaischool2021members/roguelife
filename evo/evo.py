import random
import numpy as np

class EvoAlg:
    def __init__(self):
        # Tuning parameters
        self.population_size = 1000
        self.truncation_selection = self.population_size // 10
        self.mutation_rate = .01

    # For the first batch
    def get_initial_population(self):
        return [np.random.rand(10) for _ in range(ea.population_size)]

    def get_new_generation(self, population):
        population.sort(reverse=True, key=lambda x: x[1])
        
        # Select best and strip off fitness
        parents = [x[0] for x in population[:self.truncation_selection]]
        new_pop = []
        
        for _ in range(self.population_size):
            temp = np.copy(parents[random.randint(0, len(parents) - 1)])
            # Mutation
            for i in range(len(temp)):
                if random.uniform(0, 1) < self.mutation_rate:
                    temp[i] = random.uniform(0, 1)
            new_pop.append(temp)
        return new_pop

# Placeholder, fitness should come from game
def fitness_function(population):
    out = []
    for individual in population:
        fitness = sum(individual) / len(individual)
        out.append((individual, fitness))
    return out

ea = EvoAlg()
pop = ea.get_initial_population()

for _ in range(100):
    pop_fit = fitness_function(pop)
    max_fit = max([i[1] for i in pop_fit])
    print(max_fit)
    pop = ea.get_new_generation(pop_fit)