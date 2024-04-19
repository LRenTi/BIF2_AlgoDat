class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None
        
    def buildTree(self, filename, keys=[]):
        with open(filename, 'r') as file:
            for line in file:
                key = int(line.strip())
                keys.append(key)
                self.insert(key)
        return self.root

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
        if self.root is None:
            return False
        return self._is_avl(self.root)

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

# PART 2: SEARCHING

# Suche für nur einen Eintrag im Subtree
def simpleSearch(mainTreeRoot, subTreeRoot, nodes=[]):
    if mainTreeRoot is None:
        print(subTreeRoot.key, "not found!")
        return

    nodes.append(mainTreeRoot.key)

    if mainTreeRoot.key == subTreeRoot.key:
        print(subTreeRoot.key, "found:", ", ".join(map(str, nodes)))
        return

    if subTreeRoot.key < mainTreeRoot.key:
        simpleSearch(mainTreeRoot.left, subTreeRoot, nodes)
    else:
        simpleSearch(mainTreeRoot.right, subTreeRoot, nodes)
        
    nodes.pop()

# Suchfunktionen für Subtree-Suche
# Checken ob Werte ident sind
def isIdentical(mainTreeRoot, subTreeRoot):
    if subTreeRoot is None:
        return True
    
    if mainTreeRoot is None:
        return False
    
    if mainTreeRoot.key != subTreeRoot.key:
        return False
    
    return (isIdentical(mainTreeRoot.left, subTreeRoot.left) and
            isIdentical(mainTreeRoot.right, subTreeRoot.right))

# Checken ob Subtree ein Subtree von Maintree ist
def isSubtree(mainTreeRoot, subTreeRoot):
    if mainTreeRoot is None and subTreeRoot is None:
        return True
    
    if mainTreeRoot is None:
        return False
    
    if isIdentical(mainTreeRoot, subTreeRoot):
        return True
    
    return (isSubtree(mainTreeRoot.left, subTreeRoot) or
            isSubtree(mainTreeRoot.right, subTreeRoot))
