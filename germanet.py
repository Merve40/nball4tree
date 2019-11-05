from germanet.util import GermaNetUtil

dir = 'data/'
file_word_embedding = 'data/w2v_3.vec'
output_w2v = 'data/sample_w2v.vec'
output_words = 'data/sample_words.txt'
output_tree = 'data/sample_children.txt'
output_codes = 'data/sample_catcodes.txt'

util = GermaNetUtil(dir, file_word_embedding, output_w2v)

print("----------- loading tree -----------------------")
tree = util.load_tree(output_words)

print("\n----------- writing parent location codes ------")
tree.write_parent_location_code(output_codes)
print("created "+output_codes)

print("\n----------- writing tree -----------------------")
tree.write_tree(output_tree)
print("created "+output_tree+'\n')

words = []
leafs = []
with open(output_tree, 'r') as f:
	for line in f.readlines():
		words.append(line[:-1])
		if len(line[:-1].split()) == 1:
			leafs.append(line[:-1])

codes = []
with open(output_codes, 'r') as f:
	for line in f.readlines():
		codes.append(line.split()[0])

print("tree:")
print("nodes="+str(len(codes)))
print("leafs="+str(len(leafs)))
print("max-depth="+str(tree.depth))

print("\n----------- writing new w2v file ---------------")
util.create_w2v_file(tree)
print("created "+output_w2v)
