import argparse
from germanet.util import GermaNetUtil
from germanet.validate import validate
from germanet.export_tensorflow import export


def main():
	parser = argparse.ArgumentParser()

	# commands for generating input files
	parser.add_argument('--generate_files')
	parser.add_argument('--germanet_xml_path')
	parser.add_argument('--w2v')

	# commands for validating tree file
	parser.add_argument('--validate_tree')
	parser.add_argument('--log')

	# commands for generating tsv files for tensorflow
	parser.add_argument('--export_tensorflow')
	#parser.add_argument('--w2v')
	parser.add_argument('--ws_child')

	## parses commands
	args = parser.parse_args()

	# generates germanet input files
	if args.generate_files and args.germanet_xml_path and args.w2v:

		if not args.germanet_xml_path.endswith('/'):
			args.germanet_xml_path = args.germanet_xml_path + '/'
		if not args.generate_files.endswith('/'):
			args.generate_files = args.generate_files + '/'

		input = 'germanet.py --generate_files {} --germanet_xml_path {} --w2v {}'.format(args.generate_files, args.germanet_xml_path, args.w2v)
		print(input)
		generate_germanet(args.germanet_xml_path, args.w2v, args.generate_files)


	if args.validate_tree and args.log:
		input = 'germanet.py --validate_tree {} --log {}'.format(args.validate_tree, args.log)
		print(input)
		validate(args.validate_tree, args.log)


	if args.export_tensorflow and args.w2v and args.ws_child:

		if not args.export_tensorflow.endswith('/'):
			args.export_tensorflow = args.export_tensorflow + '/'

		input = 'germanet.py --export_tensorflow {} --w2v {} --ws_child {}'.format(args.export_tensorflow, args.w2v, args.ws_child)
		print(input)
		export(args.w2v, args.ws_child, args.export_tensorflow)

def generate_germanet(dir, file_word_embedding, out_dir):
	if not out_dir.endswith('/'):
		out_dir = out_dir + '/'

	output_w2v = out_dir+'ws_w2v.vec'
	output_words = out_dir+'ws_words.txt'
	output_tree = out_dir+'ws_child.txt'
	output_codes = out_dir+'ws_catcode.txt'

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

if __name__ == "__main__":
	main()
