weights = [23,26,20,18,32,27,29,26,30,27]
values = [505,352,258,120,354,414,498,545,173,543]
capacity = 67

def knapsack_dynamic_programming(weights, values, capacity):
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Preenchendo a tabela
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    
    # Determinando quais itens foram selecionados
    w = capacity
    selected_items = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)
            w -= weights[i - 1]
    
    selected_items.reverse()  # Para obter a ordem original
    return dp[n][capacity], selected_items

# Exemplo de uso
max_value, items = knapsack_dynamic_programming(weights, values, capacity)
print("Valor máximo (Programação Dinâmica):", max_value)
print("Itens selecionados (Programação Dinâmica):", items)