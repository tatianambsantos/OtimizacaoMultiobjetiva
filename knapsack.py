import random
import time

# Save it into a file and read it
# First load the n and Q
# Then, for each item, load each profit pi and weight wi

def read_knapsack_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        n = int(lines[0].strip())  # número de itens
        Q = int(lines[1].strip())  # capacidade da mochila
        profits = list(map(int, lines[2].strip().split()))  # lucros dos itens
        weights = list(map(int, lines[3].strip().split()))  # pesos dos itens
    return n, Q, profits, weights

n, Q, profits, weights = read_knapsack_data('knapsack_data.txt')

# Model the solution representation as an array (or list) of booleans or binary numbers
# Create a constructive heuristic function to build a random initial solution, given timelimit of t seconds (otherwise, just return an empty solution)

def random_constructive_heuristic(n, Q, profits, weights, time_limit):
    start_time = time.time()
    solution = [0] * n
    total_weight = 0
    total_profit = 0
    i = 0

    while time.time() - start_time < time_limit and i < n:
        if random.random() > 0.5 and total_weight + weights[i] <= Q:
            solution[i] = 1  # Caso o item i seja adicionado à solução, marcamos na lista
            total_weight += weights[i]
            total_profit += profits[i]
        i += 1
    
    return solution, total_weight, total_profit

sol_random, weight_random, profiit_random = random_constructive_heuristic(n, Q, profits, weights, time_limit=0.5)

# Exibir solução
print("Items selected:")
for i, item in enumerate(sol_random):
    if item == 1:
        print(f"Item {i+1} - Profit: {profits[i]}, Weight: {weights[i]}")

print(f"Total weight: {weight_random}")
print(f"Total Profit: {profiit_random}")

# Create a constructive heuristic function which is smarter to build an initial solution. Also respect a given timelimit of t seconds (otherwise, just return an empty solution)
# Consideramos a razão lucro/peso para incluir os itens na mochila. Prioridade para maior razão.

def smart_constructive_heuristic(n, Q, weights, profits, time_limit):
    start_time = time.time()
    solution = [0] * n
    total_weight = 0
    total_profit = 0
    i = 0

    # Mantemos o índice original e ordenamos pela razão lucro/peso
    items = [(i, profits[i], weights[i]) for i in range(n)]

    items.sort(key=lambda x: x[1] / x[2], reverse=True)

    while time.time() - start_time < time_limit and i < n:
        if total_weight + items[i][2] <= Q:
            solution[items[i][0]] = 1
            total_weight += items[i][2]
            total_profit += items[i][1]
        i += 1

    return solution, total_weight, total_profit

sol_heuristic, weight_heuristic, profit_heuristic = smart_constructive_heuristic(n, Q, weights, profits, time_limit=0.5)

# Exibir solução
print("Items selected:")
for i, item in enumerate(sol_heuristic):
    if item == 1:
        print(f"Item {i+1} - Profit: {profits[i]}, Weight: {weights[i]}")

print(f"Total weight: {weight_heuristic}")
print(f"Total Profit: {profit_heuristic}")


# Model the objective space XE as with an evaluation function that receives a complete solution as parameter and returns a number or an Evaluation object carrying a number
# Generate 10 different initial solutions and compare them. Which of the two constructive methods is better on average?


def evaluate_solution(solution, profits):
    return sum(p for p, s in zip(profits, solution) if s == 1)

# Comparação de soluções
def compare_solutions(n, Q, weights, profits, time_limit, num_solutions=10):
    random_solutions = []
    smart_solutions = []

    for _ in range(num_solutions):
        random_sol, _, _ = random_constructive_heuristic(n, Q, weights, profits, time_limit)
        smart_sol, _, _ = smart_constructive_heuristic(n, Q, weights, profits, time_limit)
        
        random_eval = evaluate_solution(random_sol, profits)
        smart_eval = evaluate_solution(smart_sol, profits)
        
        random_solutions.append(random_eval)
        smart_solutions.append(smart_eval)

    avg_random = sum(random_solutions) / num_solutions
    avg_smart = sum(smart_solutions) / num_solutions

    return avg_random, avg_smart

# Comparando as soluções
avg_random, avg_smart = compare_solutions(n, Q, weights, profits, time_limit=0.5)

print(f"Avaliação média (heurística aleatória): {avg_random}")
print(f"Avaliação média (heurística inteligente): {avg_smart}")
