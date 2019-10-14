from germanet.tree import Tree

num_nodes = 0
words = {}

def __load_tree(file, log):
    global words

    tree = Tree()
    with open(file, 'r') as f:

        for line in f:
            parent, children = line.split()[0], len(line.split()) > 1 and line.split()[1:] or None

            # validation step 1: check for duplicate nodes
            if parent in words:
                if words[parent] > 1:
                    log.write("validation error: synset '"+parent+"' appears more than 2 times!")
                elif children is None: # is leaf
                    words[parent] += 1
            else:
                words[parent] = 1

            __add_children(tree, parent, children, log)

def __add_children(tree, parent, children, log):
    global num_nodes

    parent_node = None
    if parent == "*root*":
        parent_node = tree.root
    else:
        parent_node = __search_bfs([tree.root], parent)
        if parent_node is None:
            log.write("validation error: synset '"+parent+"' is not in tree")
            return

    if children is None:
        return

    for child in children:
        added = parent_node.add_child(child)
        if added is not None:
            num_nodes += 1

def __search_bfs(queue, target_node_name):
    if len(queue) == 0:
        return None
    node = queue.pop()
    for child in node.children:
        if child.word == target_node_name:
            return child
        else:
            queue.insert(0, child)
    __search_bfs(queue, target_node_name)

def __validate_tree(file, log):
    global num_nodes, words

    log.write("loading tree")
    __load_tree(file, log)
    log.write("finished loading tree")
    if len(words.keys()) != num_nodes:
        diff = abs(len(words.keys()) - num_nodes)
        log.write("validation error: missing nodes "+str(diff))

def __validate_file(file, log):
    synsets = {}
    with open(file , 'r') as f:
        for line in f:
            for synset in line.split():
                if synset in synsets:
                    synsets[synset] += 1
                else:
                    synsets[synset] = 1

    for syn in synsets:
        if synsets[syn] > 2:
            log.write("validation error: synset '"+syn+"' appears more than twice!")
        elif synsets[syn] == 1:
            log.write("validation error: synset '"+syn+"' appears only once!")

def validate(file, logfile):
    global num_nodes, words
    num_nodes = 0
    words = {}
    with open(logfile, 'w+') as log:
        log.write("Step 1: validate file")
        log.write("------------------------")
        __validate_file(file, log)
        log.write("\nStep 2: validate tree")
        log.write("------------------------")
        __validate_tree(file, log)