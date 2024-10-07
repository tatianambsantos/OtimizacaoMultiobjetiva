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

# Função para gerar uma solução inicial aleatória válida para o problema da mochila
def generate_random_solution(weights, capacity, inclusion_prob=0.7):
    random.seed(time.time())  # Inicializa a semente com o tempo atual
    n = len(weights)
    solution = [0] * n  # Inicialmente, nenhum item está na mochila
    total_weight = 0

    # Cria uma lista com os índices dos itens embaralhada para inclusão aleatória
    indices = list(range(n))
    random.shuffle(indices)

    for i in indices:
        # Adiciona um fator de probabilidade para incluir o item
        if random.random() < inclusion_prob:  # Só inclui o item com a probabilidade definida
            if total_weight + weights[i] <= capacity:
                solution[i] = 1  # Inclui o item na mochila
                total_weight += weights[i]
    
    return solution

# Calcula o lucro e o peso
def evaluate_solution(solution, profits, weights, Q):
    total_profit = sum(p * s for p, s in zip(profits, solution))
    total_weight = sum(w * s for w, s in zip(weights, solution))
    if total_weight > Q:
        return 0, total_weight  # Se excerder a capacidade retorna 0
    return total_profit, total_weight

# Create a neighborhood structure and two neighborhood exploration techniques (example: best improvement and first improvement)

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

# Best Improvement: Explora todas as soluções vizinhas e pega a melhor
def best_improvement(solution, profits, weights, Q):
    current_profit, _ = evaluate_solution(solution, profits, weights, Q)
    best_solution = solution[:]
    best_profit = current_profit
    neighbors = get_neighbors(solution)
    for neighbor in neighbors:
        neighbor_profit, _ = evaluate_solution(neighbor, profits, weights, Q)
        if neighbor_profit > best_profit:
            best_solution = neighbor
            best_profit = neighbor_profit
    return best_solution

# Generate multiple initial solutions with some randomness (example, 1000)

def local_search_experiment(profits, weights, Q, num_solutions=1000):
    fi_times = []
    fi_profits = []
    bi_times = []
    bi_profits = []

    for _ in range(num_solutions):
        solution = generate_random_solution(weights, Q)

        # First Improvement
        start_time = time.time()
        fi_solution = first_improvement(solution, profits, weights, Q)
        fi_time = time.time() - start_time
        fi_profit, _ = evaluate_solution(fi_solution, profits, weights, Q)
        
        fi_times.append(fi_time)
        fi_profits.append(fi_profit)

        # Best Improvement
        start_time = time.time()
        bi_solution = best_improvement(solution, profits, weights, Q)
        bi_time = time.time() - start_time
        bi_profit, _ = evaluate_solution(bi_solution, profits, weights, Q)
        
        bi_times.append(bi_time)
        bi_profits.append(bi_profit)

    # Compute averages
    avg_fi_time = sum(fi_times) / len(fi_times)
    avg_fi_profit = sum(fi_profits) / len(fi_profits)

    avg_bi_time = sum(bi_times) / len(bi_times)
    avg_bi_profit = sum(bi_profits) / len(bi_profits)

    print(f"First Improvement: Average Time = {avg_fi_time:.6f}s, Average Profit = {avg_fi_profit}")
    print(f"Best Improvement: Average Time = {avg_bi_time:.6f}s, Average Profit = {avg_bi_profit}")
    
    # Compare results
    if avg_fi_profit > avg_bi_profit:
        print("First Improvement performs better in terms of profit.")
    else:
        print("Best Improvement performs better in terms of profit.")
    
    if avg_fi_time < avg_bi_time:
        print("First Improvement is faster.")
    else:
        print("Best Improvement is faster.")

# Run the local search experiment
local_search_experiment(profits, weights, Q)

# Now, choose some Local Search technique, such as Hill Climbing (for BI, FI or RS) or RDM
# Generate multiple initial solutions with some randomness (example, 1000)
# Apply each of the two Local Search on them, for each generated solution
# Compute de Average cost and Computational time taken for each of the two local searches

# Hill Climbing (Best Improvement)
def hill_climbing_bi(solution, profits, weights, Q):
    current_profit, _ = evaluate_solution(solution, profits, weights, Q)
    while True:
        neighbors = get_neighbors(solution)
        best_solution = solution[:]
        best_profit = current_profit
        for neighbor in neighbors:
            neighbor_profit, _ = evaluate_solution(neighbor, profits, weights, Q)
            if neighbor_profit > best_profit:
                best_solution = neighbor
                best_profit = neighbor_profit
        if best_profit > current_profit:
            solution = best_solution
            current_profit = best_profit
        else:
            break  # Para se nenhuma melhora for encontrada
    return solution

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


# Experimento de busca local para comparar técnicas
def local_search_comparison(profits, weights, Q, num_solutions=1000):
    hc_bi_times, hc_bi_profits = [], []
    hc_fi_times, hc_fi_profits = [], []

    for _ in range(num_solutions):
        solution = generate_random_solution(weights, Q)

        # Hill Climbing BI
        start_time = time.time()
        hc_bi_solution = hill_climbing_bi(solution, profits, weights, Q)
        hc_bi_time = time.time() - start_time
        hc_bi_profit, _ = evaluate_solution(hc_bi_solution, profits, weights, Q)
        hc_bi_times.append(hc_bi_time)
        hc_bi_profits.append(hc_bi_profit)

        # Hill Climbing FI
        start_time = time.time()
        hc_fi_solution = hill_climbing_fi(solution, profits, weights, Q)
        hc_fi_time = time.time() - start_time
        hc_fi_profit, _ = evaluate_solution(hc_fi_solution, profits, weights, Q)
        hc_fi_times.append(hc_fi_time)
        hc_fi_profits.append(hc_fi_profit)

    # Média dos resultados
    avg_hc_bi_time = sum(hc_bi_times) / len(hc_bi_times)
    avg_hc_bi_profit = sum(hc_bi_profits) / len(hc_bi_profits)

    avg_hc_fi_time = sum(hc_fi_times) / len(hc_fi_times)
    avg_hc_fi_profit = sum(hc_fi_profits) / len(hc_fi_profits)

    # Resultados
    print(f"Hill Climbing BI: Average Time = {avg_hc_bi_time:.6f}s, Average Profit = {avg_hc_bi_profit}")
    print(f"Hill Climbing FI: Average Time = {avg_hc_fi_time:.6f}s, Average Profit = {avg_hc_fi_profit}")

    # Comparar os melhores
    if avg_hc_fi_profit > avg_hc_bi_profit:
        print("First Improvement performs better in terms of profit than Best Improvement.")
    else:
        print("Best Improvement performs better in terms of profit than First Improvement.")
    
    if avg_hc_fi_time < avg_hc_bi_time:
        print("Hill Climbing is faster than Random Descent.")
    else:
        print("Random Descent is faster than Hill Climbing.")
    return hc_bi_profits, hc_fi_profits, hc_bi_times, hc_fi_times

# Executar o experimento
hc_bi_profits, hc_fi_profits, hc_bi_times, hc_fi_times = local_search_comparison(profits, weights, Q)
