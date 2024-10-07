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


# Calcula o lucro e o peso
def evaluate_solution(solution, profits, weights, Q):
    total_profit = sum(p * s for p, s in zip(profits, solution))
    total_weight = sum(w * s for w, s in zip(weights, solution))
    if total_weight > Q:
        return 0, total_weight  # Se excerder a capacidade retorna 0
    return total_profit, total_weight

# Neighborhood structure: bit flip
def get_neighbors(solution):
    neighbors = []
    for i in range(len(solution)-1):
        neighbor = solution[:]
        neighbor[i] = 1 - neighbor[i]
        neighbor[i+1] = 1 - neighbor[i+1]
        neighbors.append(neighbor)
    return neighbors

# First Improvement: explora as soluções vizinhas e aceita a primeira melhora
def first_improvement(solution, profits, weights, Q):
    current_profit, cur_weight = evaluate_solution(solution, profits, weights, Q)
    neighbors = get_neighbors(solution)
    i = 0
    for neighbor in neighbors:
        neighbor_profit, w = evaluate_solution(neighbor, profits, weights, Q)
        # print(f"iteration: {i}, neighbor_profit: {neighbor_profit}, current profit: {current_profit}, neighbor weight: {w}, current weight: {cur_weight}")
        i += 1
        if neighbor_profit > current_profit:
            return neighbor
    return solution  # Se não encontrar melhora retorna a solução corrente

# Hill Climbing (First Improvement)
def hill_climbing_fi(solution, profits, weights, Q):
    current_profit, _ = evaluate_solution(solution, profits, weights, Q)
    
    while True:
        neighbors = get_neighbors(solution)
        improvement_found = False  # Indicador para saber se houve melhoria

        for neighbor in neighbors:
            neighbor_profit, _ = evaluate_solution(neighbor, profits, weights, Q)
            
            if neighbor_profit > current_profit:
                solution = neighbor
                current_profit = neighbor_profit
                improvement_found = True  # Marcamos que encontramos uma melhoria
                break  # Saímos do loop para aceitar a primeira melhoria

        if not improvement_found:
            break  # Paramos se não houver mais melhorias

    return solution

# Função GRASP completa
def grasp_knapsack(n, profits, weights, capacity, iterations, alpha=0.3):
    best_solution = None
    best_profit = 0
    
    for _ in range(iterations):
        # Fase de construção
        solution, greedy_sol_weight, greedy_sol_profit = greedy_randomized_solution(n, profits, weights, capacity,  alpha=0.12, time_limit=2.0)
        
        # Fase de busca local
        refined_solution = hill_climbing_fi(solution, profits, weights, capacity)
        
        # Avaliação da solução
        profit, weight = evaluate_solution(refined_solution, profits, weights, capacity)
        
        if profit > best_profit:
            best_profit = profit
            best_solution = refined_solution
    
    return best_solution, best_profit


solution, profit = grasp_knapsack(n, profits, weights, Q, iterations=10000)
print(f"Best solution found by GRASP: {solution}")
print(f"Profit: {profit}")
