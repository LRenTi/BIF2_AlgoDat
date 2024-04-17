class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def read_keys_from_file(filename):
    keys = []
    with open(filename, 'r') as file:
        for line in file:
            keys.append(int(line.strip()))
    return keys

def  build_binary_search_tree(keys):
    root = None
    for key in keys:
        root = insert(root, key)
    return root

def insert(root, key):
    if root is None:
        return TreeNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    return root

def calculate_balance_factor(node):
    if node is None:
        return 0
    return height(node.right) - height(node.left)

def height(node):
    if node is None:
        return -1
    return max(height(node.left), height(node.right)) + 1

def check_avl(root):
    if root is None:
        return True
    balance_factor = calculate_balance_factor(root)
    if abs(balance_factor) > 1:
        return False
    return check_avl(root.left) and check_avl(root.right)

def calculate_statistics(root):
    if root is None:
        return (float('inf'), float('-inf'), 0, 0)
    min_key, max_key, sum_keys, num_nodes = root.key, root.key, root.key, 1
    min_left, max_left, sum_left, num_left = calculate_statistics(root.left)
    min_right, max_right, sum_right, num_right = calculate_statistics(root.right)
    min_key = min(min_key, min_left, min_right)
    max_key = max(max_key, max_left, max_right)
    sum_keys += sum_left + sum_right
    num_nodes += num_left + num_right
    return (min_key, max_key, sum_keys, num_nodes)

#PART 2: SEARCHING

def simpleSearch(mainTreeRoot, subTreeRoot, nodes=[]):
    if mainTreeRoot is None:
        print(subTreeRoot.key, "not found!")
        return

    nodes.append(mainTreeRoot.key)

    if mainTreeRoot.key == subTreeRoot.key:
        print(subTreeRoot.key, "found:", ", ".join(map(str, nodes)))
        return

    if subTreeRoot.key < mainTreeRoot.key:  # Corrected comparison
        simpleSearch(mainTreeRoot.left, subTreeRoot, nodes)
    else:
        simpleSearch(mainTreeRoot.right, subTreeRoot, nodes)

    nodes.pop()

def isIdentical(mainTreeRoot, subTreeRoot):
    if subTreeRoot is None:
        return True
    if mainTreeRoot is None:
        return False
    if mainTreeRoot.key != subTreeRoot.key:
        return False
    return (isIdentical(mainTreeRoot.left, subTreeRoot.left) and
            isIdentical(mainTreeRoot.right, subTreeRoot.right))

def isSubtree(mainTreeRoot, subTreeRoot):
    if mainTreeRoot is None and subTreeRoot is None:
        return True
    if mainTreeRoot is None:
        return False
    if isIdentical(mainTreeRoot, subTreeRoot):
        return True
    return (isSubtree(mainTreeRoot.left, subTreeRoot) or
            isSubtree(mainTreeRoot.right, subTreeRoot))

