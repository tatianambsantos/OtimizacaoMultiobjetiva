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
        profits = []
        weights = []
        for line in lines[2:]:
            if line.strip() == "":  # Verificar se há uma linha vazia (fim do arquivo)
                break
            profit, weight = map(int, line.split())  # Cada linha tem lucro e peso
            profits.append(profit)
            weights.append(weight)
    return n, Q, profits, weights

n, Q, profits, weights = read_knapsack_data('knapsack_data_big.txt')

# Create a constructive heuristic function to build a greedy randomized initial solution, given parameter α and timelimit of t seconds
# (otherwise, just return an empty solution)
# Heurística gulosa randomizada para gerar solução inicial
def greedy_randomized_solution(n, profits, weights, capacity, alpha, time_limit):
    start_time = time.time()
    solution = [0] * n
    remaining_capacity = capacity
    total_profit = 0
    items = list(range(n))
    while items and time.time() - start_time < time_limit:
        # Seleção gulosa randomizada
        candidates = [(i, profits[i] / weights[i]) for i in items if weights[i] <= remaining_capacity]
        if not candidates:
            break
        candidates.sort(key=lambda x: x[1], reverse=True)
        num_candidates = max(1, int(alpha * len(candidates)))
        selected_item = random.choice(candidates[:num_candidates])[0]
        solution[selected_item] = 1
        remaining_capacity -= weights[selected_item]
        total_profit += profits[selected_item]
        items.remove(selected_item)
    return solution, capacity-remaining_capacity, total_profit

greedy_sol, greedy_sol_weight, greedy_sol_profit = greedy_randomized_solution(n, profits, weights, Q, alpha=0.2, time_limit=2.0)

# Exibir solução
print("Items selected:")
for i, item in enumerate(greedy_sol):
    if item == 1:
        print(f"Item {i+1} - Profit: {profits[i]}, Weight: {weights[i]}")
print(f"Total weight: {greedy_sol_weight}")
print(f"Total Profit: {greedy_sol_profit}")


# What value of α is the best one? Try a hundred possibilities, from 0.00, 0.01, ..., 0.98, 0.99, 1.00
# Encontrar o melhor valor de alpha (entre 0 e 1)
def find_best_alpha(n, profits, weights, capacity, alpha_values=100, time_limit=1):
    best_alpha = 0
    best_profit = float('-inf')
    for alpha in [i / alpha_values for i in range(alpha_values + 1)]:
        solution, w, prof = greedy_randomized_solution(n, profits, weights, capacity, alpha, time_limit)
        if prof > best_profit:
            best_profit = prof
            best_alpha = alpha
    return best_alpha, best_profit

best_alpha, best_prof = find_best_alpha(n, profits, weights, Q)
print(f"Best alpha: {best_alpha}, Best profit: {best_prof}")
#Best alpha: 0.12 / Best profit: 348886

# After selecting the best α, generate 10 different initial solutions and compare them with some purely greedy (α = 0) and purely random
# (α = 1) strategies. Which of the constructive methods is better on average?

# Gerar múltiplas soluções com o melhor alpha
def generate_solutions(n, profits, weights, capacity, alpha, num_solutions=10, time_limit=1):
    total_weight = 0
    total_profit = 0
    solutions = []
    for _ in range(num_solutions):
        sol, weight, prof = greedy_randomized_solution(n, profits, weights, capacity, alpha, time_limit)
        total_weight += weight
        total_profit += prof
        solutions.append((sol, weight, prof))
    mean_weight = total_weight / num_solutions
    mean_prof = total_profit / num_solutions
    return mean_weight, mean_prof

def compare_strategies(n, profits, weights, capacity, best_alpha, num_solutions=10, time_limit=1):

    greedy_solution, greedy_weight, greedy_profit = greedy_randomized_solution(n, profits, weights, capacity, 0.0, time_limit)
    random_solution, random_weight, random_profit = greedy_randomized_solution(n, profits, weights, capacity, 1.0, time_limit)
    best_alpha_weight, best_alpha_profit = generate_solutions(n, profits, weights, capacity, best_alpha, num_solutions, time_limit)

    # Exibir os resultados
    print("\nSolução puramente gulosa:")
    print(f"Peso na mochila: {greedy_weight}, Lucro: {greedy_profit}")

    print("\nSolução puramente aleatória:")
    print(f"Peso na mochila: {random_weight}, Lucro: {random_profit}")

    print("\nMédia das soluções com o melhor alpha encontrado:")
    print(f"Peso na mochila: {best_alpha_weight}, Lucro: {best_alpha_profit}")

    return

compare_strategies(n, profits, weights, Q, best_alpha)