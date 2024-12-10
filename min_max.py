import math

def minimax(depth, nodeIndex, isMaximizingPlayer, values, maxDepth):
    # Terminal node (leaf nodes)
    if depth == maxDepth:
        print(f"Leaf node reached at depth {depth}, returning value: {values[nodeIndex]}")
        return values[nodeIndex]

    if isMaximizingPlayer:
        best = -math.inf
        print(f"Maximizer at depth {depth}")
        # Maximizer's choice (MAX player)
        for i in range(2):
            value = minimax(depth + 1, nodeIndex * 2 + i, False, values, maxDepth)
            print(f"Maximizer at depth {depth}, comparing value: {value} with best: {best}")
            best = max(best, value)
            print(f"Maximizer at depth {depth}, selected best: {best}")
        return best
    else:
        best = math.inf
        print(f"Minimizer at depth {depth}")
        # Minimizer's choice (MIN player)
        for i in range(2):
            value = minimax(depth + 1, nodeIndex * 2 + i, True, values, maxDepth)
            print(f"Minimizer at depth {depth}, comparing value: {value} with best: {best}")
            best = min(best, value)
            print(f"Minimizer at depth {depth}, selected best: {best}")
        return best

# The depth of the game
maxDepth = 3

# New leaf node values
values = [3, 5, 2, 9, 12, 8, 6, 4]

optimalValue = minimax(0, 0, True, values, maxDepth)
print("\nThe optimal value is:", optimalValue)