from util import GermaNetUtil

dir = './'
file_word_embedding = '../data/de.vec'
output_words = 'output-words.txt'
output_tree = 'output-tree.txt'
output_codes = 'output-codes.txt'

util = GermaNetUtil(dir, file_word_embedding)

print("----------- loading tree -----------------------")
tree = util.load_tree(output_words)

print("----------- writing parent location codes ------")
tree.write_parent_location_code(output_codes)

print("----------- writing tree -----------------------")
tree.write_tree(output_tree)


words = []
leafs = []
with open('output-tree.txt', 'r') as f:
	for line in f.readlines():
		words.append(line[:-1])
		if len(line[:-1].split()) == 1:
			leafs.append(line[:-1])

codes = []
with open('output-codes.txt', 'r') as f:
	for line in f.readlines():
		codes.append(line.split()[0])

print("tree:")
print("nodes="+str(len(codes)))
print("leafs="+str(len(leafs)))
print("max-depth="+str(tree.depth))