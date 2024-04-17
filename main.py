import tree as t
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python program.py mainTree.txt subTree.txt")
        return

    mainTreeFilename = sys.argv[1]
    subTreeFilename = sys.argv[2]
    nodes = []

    # Main Tree bauen
    mainTreeKeys = t.read_keys_from_file(mainTreeFilename)
    mainTreeRoot = t.build_binary_search_tree(mainTreeKeys)

    # Subtree bauen
    subTreeKeys = t.read_keys_from_file(subTreeFilename)
    subTreeRoot = t.build_binary_search_tree(subTreeKeys)

    # Check ob Subtree ein Subtree von Main Tree ist
    isSubtree = t.isSubtree(mainTreeRoot, subTreeRoot)

    # AVL-Eigenschaften überprüfen
    is_avl = t.check_avl(mainTreeRoot)

    # Statistiken berechnen
    min_key, max_key, sum_keys, num_nodes = t.calculate_statistics(mainTreeRoot)
    if num_nodes != 0:
        avg_key = sum_keys / num_nodes
    else:
        avg_key = 0

    # Ausgabe
    print("AVL:", "yes" if is_avl else "no")
    print("min:", min_key, "max:", max_key, "avg:", avg_key)

    # Wenn nur ein Eintrag im subtree ist, beginne mit Einfacher Suche
    # Wenn nur ein Eintrag im subtree ist, beginne mit Einfacher Suche
    if len(subTreeKeys) == 1:
        t.simpleSearch(mainTreeRoot, subTreeRoot, nodes)

    # Ansonsten Ausgabe ob Subtree ein Subtree vom Maintree ist
    elif isSubtree:
        print("Subtree found")
    else:
        print("Subtree not found")

if __name__ == "__main__":
    main()
