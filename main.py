import random


MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.6
REPRODUCTION_RATE = 0.3


P = [60, 100, 120]
W = [10, 20, 30]
M = 50


def generate_initial_population(count):
    """Generate the initial set of individuals."""
    solutions = []
    for _ in range(count):
        solutions.append([random.choice([0, 1]) for _ in P])

    return solutions


def compute_fitness(individual):
    """Computes fitness of a solution."""
    fitness_score = sum([x * value for x, value in zip(individual, P)])

    total_weight = sum([x * weight for x, weight in zip(individual, W)])

    if total_weight > M:
        fitness_score = 0

    return fitness_score


def select_parents(population):
    """Select parents using tournament selection."""
    parents = []
    random.shuffle(population)

    if compute_fitness(population[0]) > compute_fitness(population[1]):
        parents.append(population[0])
    else:
        parents.append(population[1])

    if compute_fitness(population[2]) > compute_fitness(population[3]):
        parents.append(population[2])
    else:
        parents.append(population[3])

    return parents


def mutate(individuals):
    """Mutate the chromosome of an individual."""
    for individual in individuals:
        for i in range(len(individual)):
            if random.random() < MUTATION_RATE:
                # Flip the bit
                individual[i] = ~individual[i]


def cross_over(parents):
    """One-point cross over the chromosome from two parents."""
    n = len(parents[0]) // 2

    child1 = parents[0][:n] + parents[1][n:]
    child2 = parents[1][:n] + parents[0][n:]

    return [child1, child2]


def next_generation(population):
    next_gen = []
    while len(next_gen) < len(population):
        children = []

        # we run selection and get parents
        parents = select_parents(population)

        # reproduction
        if random.random() < REPRODUCTION_RATE:
            children = parents
        else:
            # crossover
            if random.random() < CROSSOVER_RATE:
                children = cross_over(parents)

            # mutation
            if random.random() < MUTATION_RATE:
                mutate(children)

        next_gen.extend(children)

    return next_gen[:len(population)]


def compute_average_fitness(population):
    """Compute average value for fitness of entire population."""
    avg_fitness = sum([compute_fitness(individual) for individual \
            in population]) / len(population)
    return avg_fitness


def solve_knapsack():
    """Solve the knapsack program using genetic algorithm."""
    population = generate_initial_population(4)

    for i in range(500):
        avg_fitness = compute_average_fitness(population)
        print(f"Generation {i+1}: Average Fitness = {avg_fitness}")
        print("-" * 50)

        population = next_generation(population)

    population = sorted(population, key=lambda x: compute_fitness(x), reverse=True)
    return population[0]


if __name__ == "__main__":
    solve_knapsack()
