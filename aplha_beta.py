import math

def alphabeta(depth, nodeIndex, isMaximizingPlayer, values, alpha, beta, maxDepth):
    if depth == maxDepth:
        print(f"Leaf node reached at depth {depth}, returning value: {values[nodeIndex]}")
        return values[nodeIndex]

    if isMaximizingPlayer:
        best = -math.inf
        print(f"Maximizer at depth {depth}, alpha: {alpha}, beta: {beta}")
        for i in range(2):
            value = alphabeta(depth + 1, nodeIndex * 2 + i, False, values, alpha, beta, maxDepth)
            print(f"Maximizer at depth {depth}, comparing value: {value} with best: {best}, alpha: {alpha}, beta: {beta}")
            best = max(best, value)
            alpha = max(alpha, best)
            # Alpha-Beta Pruning
            if beta <= alpha:
                print(f"Pruning at depth {depth} with alpha: {alpha} and beta: {beta}")
                break
        print(f"Maximizer at depth {depth}, selected best: {best}")
        return best
    else:
        best = math.inf
        print(f"Minimizer at depth {depth}, alpha: {alpha}, beta: {beta}")
        for i in range(2):
            value = alphabeta(depth + 1, nodeIndex * 2 + i, True, values, alpha, beta, maxDepth)
            print(f"Minimizer at depth {depth}, comparing value: {value} with best: {best}, alpha: {alpha}, beta: {beta}")
            best = min(best, value)
            beta = min(beta, best)
            # Alpha-Beta Pruning
            if beta <= alpha:
                print(f"Pruning at depth {depth} with alpha: {alpha} and beta: {beta}")
                break
        print(f"Minimizer at depth {depth}, selected best: {best}")
        return best

# Example usage:
maxDepth = 3
# New leaf node values
values = [3, 5, 2, 9, 12, 8, 6, 4]
print(f"Optimal value: {alphabeta(0, 0, True, values, -math.inf, math.inf, int(maxDepth))}")