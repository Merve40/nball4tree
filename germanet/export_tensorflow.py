
def export(w2v, ws_child, out_dir):
    """
    Exports the word-to-vec file to tsv files as input for tensorflow.

    :param w2v: word-to-vec file
    :param ws_child: tree file
    :param out_dir: output directory for the files to generate
    """
    if not out_dir.endswith('/'):
        out_dir = out_dir+'/'

    tmeta = out_dir+'meta.tsv'
    tdata = out_dir+'data.tsv'
    words = set()
    tsv = {}
    # read data into memory
    with open(ws_child, 'r') as ws, open(w2v, 'r') as vecs:
        for line in ws:
            wsenses = [elem.split('.')[0] for elem in line.split()]
            words.update(wsenses)

        for line in vecs:
            word, vec = line.split()[0], "\t".join(line.split()[1:])
            if word in words:
                tsv[word] = vec

    # write to file
    with open(tdata, 'w+') as data, open(tmeta, 'w+') as meta:
        for key in tsv:
            tvec = tsv[key]
            data.write(tvec+'\n')
        meta.write(key+'\n')