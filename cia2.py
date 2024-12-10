from enum import Enum
from typing import List, Optional

class NodeType(Enum):
    OR = "OR"
    AND = "AND"
    LEAF = "LEAF"

class Node:
    def __init__(self, name: str, node_type: NodeType, score: float = 0):
        self.name = name
        self.node_type = node_type
        self.score = score
        self.children: List[Node] = []
        self.parent: Optional[Node] = None
        self.best_child: Optional[Node] = None

    def add_child(self, child: 'Node'):
        self.children.append(child)
        child.parent = self

class AOStarMinimax:
    def __init__(self):
        self.root = self._create_game_tree()

    def _create_game_tree(self):
        root = Node("A", NodeType.OR, 15)
        b = Node("B", NodeType.AND, 12)
        c = Node("C", NodeType.AND, 9)
        d = Node("D", NodeType.OR, 7)
        e = Node("E", NodeType.OR, 14)
        f = Node("F", NodeType.LEAF, 18)
        g = Node("G", NodeType.LEAF, 11)
        h = Node("H", NodeType.LEAF, 5)
        i = Node("I", NodeType.LEAF, 13)
        j = Node("J", NodeType.LEAF, 10)
        k = Node("K", NodeType.LEAF, 8)

        root.add_child(b)
        root.add_child(c)
        b.add_child(d)
        b.add_child(e)
        d.add_child(f)
        d.add_child(g)
        e.add_child(h)
        e.add_child(i)
        c.add_child(j)
        c.add_child(k)

        return root

    def minimax(self, node: Node, depth: int, max_player: bool):
        if node.node_type == NodeType.LEAF:
            print(f"Depth {depth} - {'max' if max_player else 'min'} evaluates {node.score}")
            return node.score

        if max_player:
            max_eval = float('-inf')
            for child in node.children:
                eval = self.minimax(child, depth + 1, False)
                max_eval = max(max_eval, eval)
            print(f"Depth {depth} - max evaluates {max_eval}")
            return max_eval
        else:
            min_eval = float('inf')
            for child in node.children:
                eval = self.minimax(child, depth + 1, True)
                min_eval = min(min_eval, eval)
            print(f"Depth {depth} - min evaluates {min_eval}")
            return min_eval

    def alpha_beta_pruning(self, node: Node, depth: int, max_player: bool, alpha: float, beta: float):
        if node.node_type == NodeType.LEAF:
            print(f"Depth {depth} - {'max' if max_player else 'min'} evaluates {node.score}")
            return node.score

        if max_player:
            max_eval = float('-inf')
            for child in node.children:
                eval = self.alpha_beta_pruning(child, depth + 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    print(f"Depth {depth} - Pruning at max node")
                    break
            print(f"Depth {depth} - max evaluates {max_eval}")
            return max_eval
        else:
            min_eval = float('inf')
            for child in node.children:
                eval = self.alpha_beta_pruning(child, depth + 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    print(f"Depth {depth} - Pruning at min node")
                    break
            print(f"Depth {depth} - min evaluates {min_eval}")
            return min_eval

solver = AOStarMinimax()

print("Minimax")
minimax_result = solver.minimax(solver.root, 0, False)
print(f"Minimax Final Value: {minimax_result}\n")

print("Alpha-Beta Pruning")
alpha_beta_result = solver.alpha_beta_pruning(solver.root, 0, False, float('-inf'), float('inf'))
print(f"Alpha-Beta Pruning Final Value: {alpha_beta_result}")
