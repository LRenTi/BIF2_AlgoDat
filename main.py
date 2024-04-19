import tree as t
from graphviz import Digraph
import argparse
import os

def draw_tree(root, filename):
    path = "images/"
    
    filename = filename[:-4]
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    dot = Digraph()
    add_edges(root, dot)
    dot.render(filename, format="png", cleanup=True, directory=path)
    print("Tree visualization saved as:", path + filename + ".png")

def add_edges(node, dot):
    if node is not None:
        dot.node(str(node.key))
        if node.left is not None:
            dot.edge(str(node.key), str(node.left.key))
            add_edges(node.left, dot)
        if node.right is not None:
            dot.edge(str(node.key), str(node.right.key))
            add_edges(node.right, dot)
            
    
def main():
    # Arguments parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--plot", action="store_true", help="Plot the tree")
    parser.add_argument("mainTreeFilename", help="Input filename of the Main Tree")
    parser.add_argument("subTreeFilename", help="Input filename of the Sub Tree")
    args = parser.parse_args()
    
    tree = t.AVLTree() # Create an empty AVL tree
    nodes = []

    t.print_balance_factors(tree.root) # Print the balance factors of the tree
    
    if tree.is_avl(): # Check if the tree is AVL
        print("AVL: yes")
    else:
        print("AVL: no")
        
    print("min:", tree.min_key(), ", max:", tree.max_key(), ", avg:", tree.avg_key())

    if args.plot: # Plot the tree
        draw_tree(tree.root, args.mainTreefilename)

    # Main Tree bauen
    mainTreeRoot = t.buildTree(args.mainTreeFilename)

    # Subtree bauen
    subTreeRoot = t.buildTree(args.subTreeFilename)

    # Check ob Subtree ein Subtree von Main Tree ist
    isSubtree = t.isSubtree(mainTreeRoot, subTreeRoot)

    # Wenn nur ein Eintrag im subtree ist, beginne mit Einfacher Suche
    if len(subTreeRoot) == 1:
        t.simpleSearch(mainTreeRoot, subTreeRoot, nodes)

    # Ansonsten Ausgabe ob Subtree ein Subtree vom Maintree ist
    elif isSubtree:
        print("Subtree found")
    else:
        print("Subtree not found")

if __name__ == "__main__":
    main()