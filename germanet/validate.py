from pygermanet import load_germanet
import numpy as np
from germanet.tree import Tree

germanet = load_germanet()
num_nodes = 0
words = {}
leaf_nodes = []
errors = 0

def __load_tree(file, log):
    """
    Creates and fills tree from the input file.

    :param file: file containing word-sense parents and their children
    :param log: log file
    """
    global words, errors

    tree = Tree()
    with open(file, 'r') as f:

        for line in f:
            parent, children = line.split()[0], len(line.split()) > 1 and line.split()[1:] or None

            # validation step 1: check for duplicate nodes
            if parent in words:
                if words[parent] >= 2:
                    log.write("validation error: synset '"+parent+"' appears more than 2 times!\n")
                    errors += 1
                else:
                    words[parent] += 1
            elif parent != '*root*':
                words[parent] = 1

            __add_children(tree, parent, children, log)

def __add_children(tree, parent, children, log):
    """
    Reads children from the file and adds them in the tree to the parent node.

    :param tree: Tree
    :param parent: parent node
    :param children: children nodes
    :param log: log file
    """
    global num_nodes, leaf_nodes, errors

    parent_node = None
    if parent == "*root*":
        parent_node = tree.root
    else:
        parent_node = __search(tree, parent)
        if parent_node is None:
            log.write("validation error: synset '"+parent+"' is not in tree\n")
            errors += 1
            return

    if children is None:
        leaf_nodes.append(parent_node)
        return

    for child in children:
        added = parent_node.add_child(child)
        if added is not None:
            num_nodes += 1

def __search(tree, target_node_name):
    """
    Searches for the target node in BFS order.
    :param tree: Tree
    :param target_node_name: synset / word-sense
    :return: parent node or None if it could not find node with target_node_name
    """
    q = [tree.root]
    while len(q) > 0:
        node = q.pop()
        for child in node.children:
            if child.word == target_node_name:
                return child
            q.insert(0, child)
    return None


def __validate_tree(file, log):
    """
    Function for validating the tree recreated tree structure.

    :param file: file containing word-sense parents and their children
    :param log: log file
    """
    global num_nodes, words, errors

    log.write("loading tree\n")
    __load_tree(file, log)
    log.write("finished loading tree\n")
    if len(words.keys()) != (num_nodes):
        diff = abs(len(words.keys()) - num_nodes ) # exclude *root*
        log.write("validation error: missing nodes "+str(diff)+"\n")
        errors += 1

def __validate_file(file, log):
    """
    Validates file by checking for duplicates.

    :param file: file containing word-sense parents and their children
    :param log: log file
    """
    global errors

    synsets = {}
    with open(file , 'r') as f:
        for line in f:
            for synset in line.split():
                if synset in synsets:
                    synsets[synset] += 1
                else:
                    synsets[synset] = 1

    log.write("checking for irregular occurrences of word senses\n")

    for syn in synsets:
        if synsets[syn] > 2:
            log.write("validation error: synset '"+syn+"' appears more than twice!\n")
            errors += 1
        elif synsets[syn] == 1 and not syn == "*root*":
            log.write("validation error: synset '"+syn+"' appears only once!\n")
            errors += 1


def __validate_hypernyms(log):
    """
    Compares the hypernyms of all leaf nodes with the hypernyms in germanet.

    :param log: log file
    """
    global leaf_nodes, germanet, errors
    for leaf in leaf_nodes:
        paths_germanet = germanet.synset(leaf.word).hypernym_paths
        path = [leaf.word]
        node = leaf.parent
        while node is not None:
            path.insert(0, node.word)
            node = node.parent
        if not __is_equal(path, paths_germanet):
            log.write("validation error: synset '"+leaf.word+"' has wrong path -> ["+ ",".join(path) +"]\n")
            errors += 1

def __is_equal(path_tree, paths_germanet):
    """
    Compares if hypernym path in tree and hypernym path(s) in germanet are equal.

    :param path_tree: path in tree
    :param paths_germanet: path in germanet
    :return: True if paths are equal, otherwise False
    """
    if len(paths_germanet) > 0 and isinstance(paths_germanet[0], list):
        for path in paths_germanet:
            if len(path) != len(path_tree):
                continue
            if __eq(path_tree, path):
                return True
    elif __eq(path_tree, paths_germanet):
        return True

    return False

def __eq(path1, path2):
    p = []
    for syn in path2[1:]:
        p.append(syn.__str__()[7:-1])
    return np.array_equal(path1[1:], p)

def validate(file, logfile):
    global num_nodes, words, errors
    num_nodes = 0
    words = {}
    with open(logfile, 'a+') as log:
        log.write("Step 1: validate file\n")
        log.write("------------------------------\n")
        __validate_file(file, log)
        log.write("\nStep 2: validate tree\n")
        log.write("------------------------------\n")
        __validate_tree(file, log)
        log.write("\nStep 3: validate hypernyms\n")
        log.write("------------------------------\n")
        __validate_hypernyms(log)
        log.write("Finished validating. Total errors="+str(errors)+"\n")
        if errors == 0:
            log.write("The tree-structure in '"+file+"' seems to be valid!\n")