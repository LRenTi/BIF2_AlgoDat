import tree as t
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python program.py filename")
        return

    filename = sys.argv[1]
    keys = t.read_keys_from_file(filename)
    root = t.build_binary_search_tree(keys)

    # AVL-Eigenschaften überprüfen
    is_avl = t.check_avl(root)

    # Statistiken berechnen
    min_key, max_key, sum_keys, num_nodes = t.calculate_statistics(root)
    avg_key = sum_keys / num_nodes

    # Ausgabe
    print("AVL:", "yes" if is_avl else "no")
    print("min:", min_key, "max:", max_key, "avg:", avg_key)

if __name__ == "__main__":
    main()
