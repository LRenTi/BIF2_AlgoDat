class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return TreeNode(key)
        elif key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return self.balance(node)

    def balance_factor(self, node):
        return self.height(node.right) - self.height(node.left)

    def height(self, node):
        if node is None:
            return -1
        return max(self.height(node.left), self.height(node.right)) + 1

    def balance(self, node):
        if self.balance_factor(node) > 1:
            if self.balance_factor(node.right) < 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        elif self.balance_factor(node) < -1:
            if self.balance_factor(node.left) > 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        return node

    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        return left_child

    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        return right_child

    def is_avl(self):
        node = self.root
        if node is None:
            return True
        if abs(self.balance_factor(node)) > 1:
            return False
        return self._is_avl(node.left) and self._is_avl(node.right)

    def _is_avl(self, node):
        if node is None:
            return True
        if abs(self.balance_factor(node)) > 1:
            return False
        return self._is_avl(node.left) and self._is_avl(node.right)

    def min_key(self):
        node = self.root
        if node is None:
            return None
        while node.left:
            node = node.left
        return node.key
    
    def max_key(self):
        node = self.root
        if node is None:
            return None
        while node.right:
            node = node.right
        return node.key

    def avg_key(self):
        total, count = self._avg_key(self.root)
        return total / count if count > 0 else 0

    def _avg_key(self, node):
        if node is None:
            return 0, 0
        left_total, left_count = self._avg_key(node.left)
        right_total, right_count = self._avg_key(node.right)
        total = left_total + right_total + node.key
        count = left_count + right_count + 1
        return total, count

def print_balance_factors(node):
    if node is None:
        return
    print_balance_factors(node.left)
    print("bal({}) = {}".format(node.key, AVLTree().balance_factor(node)), end='')
    
    if abs(AVLTree().balance_factor(node)) > 1:
        print(" (AVL violation!)")
    else:
        print()
        
    print_balance_factors(node.right)
