# Table of Contents
* **[Install the package](#install-the-package)**    
* **[GermaNet](#germanet)**    
* **[Experiment 1:  Training and evaluating nball embeddings](#experiment-1--training-and-evaluating-nball-embeddings)**    
* **[Experiment 2: Observe neighbors of word-sense using nball embeddings](#experiment-2-observe-neighbors-of-word-sense-using-nball-embeddings)**     
* **[NBalls for other languages](#nballs-for-other-languages)**   
* **[Cite](#cite)**   

# Install the package

* for Ubuntu platform please first install python3-tk
```
sudo apt-get install python3-tk
```

* for Ubuntu or Mac platform type:

```
$ git clone https://github.com/gnodisnait/nball4tree.git
$ cd nball4tree
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

```

* Download the [german word embedding](https://fasttext.cc/docs/en/crawl-vectors.html) file 

## Setup GermaNet

* Install [Mongo DB](https://docs.mongodb.com/manual/installation/#mongodb-community-edition-installation-tutorials)
* Unzip `data/GermaNet.zip`
* Unzip `data/mongo_dump_germanet.zip`
* Restore database    
    ```bash
    $ mongorestore --db germanet dump/germanet/
    ```

# GermaNet
#### 1) Shell command for creating german input files for nball training:
    
    $ python germanet.py --generate_files data/ --germanet_xml_path data/GermaNet/ --w2v data/w2v.vec
    % --generate_files: output directory for storing generated files
    % --germanet_xml_path: the path to the GermaNet XML files
    % --w2v: file of pre-trained word embeddings 
    

#### 2) Shell command for validating tree file:
    
    $ python germanet.py --validate_tree data/ws_child.txt --log data/validation.log
    % --validate_tree: the tree file to validate, which was generated in 1)
    % --log: log file containing the result of the validation
    
   
#### 3) Shell command for generating tsv files for tensorflow:
Can be used to compare neighbors in word embedding and neighbors in nball (experiment 2).

    $ python germanet.py --export_tensorflow data/ --w2v data/w2v.vec --ws_child data/ws_child.txt
    % --export_tensorflow: output directory for storing tsv files
    % --w2v: file of pre-trained word embeddings
    % --ws_child: the tree file generated in 1)



# Experiment 1:  Training and evaluating nball embeddings
## Experiment 1.1: Training nball embeddings
Shell command for running the nball construction and training process:
```
% you need to create an empty file nball.txt for output

$ python nball.py --train_nball /Users/<user-name>/data/glove/nball.txt --w2v /Users/<user-name>/data/glove/glove.6B.50d.txt  --ws_child /Users/<user-name>/data/glove/wordSenseChildren47634.txt  --ws_catcode /Users/<user-name>/data/glove/glove.6B.catcode.txt  --log log.txt
% --train_nball: output file of nball embeddings
% --w2v: file of pre-trained word embeddings
% --ws_child: file of parent-children relations among word-senses
% --ws_catcode: file of the parent location code of a word-sense in the tree structure
% --log: log file, shall be located in the same directory as the file of nball embeddings
```
The training process can take around 6.5 hours. 


## Experiment 1.2: Checking whether tree structures are perfectly embedded into word-embeddings
* main input is the output directory of nballs created in Experiment 1.1
* shell command for running the nball construction and training process
```
$ python nball.py --zero_energy <output-path> --ball <output-file> --ws_child /Users/<user-name>/data/glove/wordSenseChildren.txt
% --zero_energy <output-path> : output path of the nballs of Experiment 1.1, e.g. ```/Users/<user-name>/data/glove/data_out```
% --ball <output-file> : the name of the output nball-embedding file
% --ws_child /Users/<user-name>/data/glove/wordSenseChildren.txt: file of parent-children relations among word-senses
```
The checking process can take around 2 hours.
* result

If zero-energy is achieved, a big nball-embedding file will be created ```<output-path>/<output-file>```
otherwise, failed relations and word-senses will be printed.

** Test result at Mac platform:
![img|630x420](https://github.com/gnodisnait/nball4tree/blob/master/pic/success_result.png)
** Test result at Ubuntu platform:
![](https://github.com/gnodisnait/nball4tree/blob/master/pic/ubuntu_result.png)
 
- [nball embeddings with 47634 balls](https://drive.google.com/file/d/1TC5h8PXKQz4rQ4hsFYlWSFsyuoxlkutf/view?usp=sharing)

- [nball embeddings with 54310 balls](https://drive.google.com/file/d/1tOJWK08mMx-uUOFxaIGEKqiQLLahKglj/view?usp=sharing)

# Experiment 2: Observe neighbors of word-sense using nball embeddings
* [pre-trained nball embeddings](https://drive.google.com/file/d/176FZwSaLB2MwTOWRFsfxWxMmJKQfoFRw/view?usp=sharing)
```
$ python nball.py --neighbors handeln.v.2 handeln.v.5 Teil.n.2 Teil.n.3 Teil.n.4 Teil.n.5 Gerät.n.1 Gerät.n.2 --ball data/nball.txt --num 12
% --neighbors: list of word-senses
% --ball: file location of the nball embeddings
% --num: number of neighbors
```

* **Result**:
```json5
loading balls....
50673  balls are loaded

{   
    'handeln.v.2': [   'handeln.v.3',
                       'handeln.v.5',
                       'agieren.v.3',
                       'urteilen.v.2',
                       'entsorgen.v.1',
                       'denken.v.1',
                       'denken.v.2',
                       'wehren.v.1',
                       'denken.v.4',
                       'denken.v.10',
                       'ausdrücken.v.2',
                       'beurteilen.v.1'],

    'handeln.v.5': [   'handeln.v.3',
                       'handeln.v.2',
                       'agieren.v.3',
                       'urteilen.v.2',
                       'entsorgen.v.1',
                       'denken.v.5',
                       'ausdrücken.v.2',
                       'einordnen.v.4',
                       'denken.v.2',
                       'evakuieren.v.1',
                       'evakuieren.v.2',
                       'wehren.v.1'],

    'Teil.n.2': [      'Profiverein.n.1',
                       'Hauptstadtverein.n.1',
                       'Ring.n.5',
                       'Traditionsklub.n.1',
                       'Reich.n.1',
                       'TÜV.n.1',
                       'Lesering.n.1',
                       'Traditionsverein.n.1',
                       'Zweitligaverein.n.1',
                       'Tennisklub.n.1',
                       'Drogenring.n.1',
                       'Albverein.n.1'],

    'Teil.n.3': [      'Kern.n.1',
                       'Funke.n.2',
                       'Rußpartikel.n.1',
                       'Zündfunke.n.1',
                       'Seitenkette.n.1',
                       'Kohlepartikel.n.1',
                       'Atomhülle.n.1',
                       'Einsprengsel.n.1',
                       'Sternenstaub.n.1',
                       'Fremdkörper.n.2',
                       'C-Atom.n.1',
                       'Quark.n.3'],

    'Teil.n.4': [      'Kokosnuss.n.1',
                       'Kürbis.n.2',
                       'Banane.n.1',
                       'Ölfrucht.n.1',
                       'Stachelbeere.n.1',
                       'Tollkirsche.n.1',
                       'Johannisbeere.n.1',
                       'Kochbanane.n.1',
                       'Scheinfrucht.n.1',
                       'Flaschenkürbis.n.1',
                       'Ecker.n.1',
                       'Beere.n.2'],

    'Teil.n.5': [      'Kern.n.5',
                       'Weltproduktion.n.2',
                       'Radioproduktion.n.1',
                       'Produktion.n.2',
                       'Ausrüstungsgegenstand.n.1',
                       'Eigenproduktion.n.2',
                       'Hörspielproduktion.n.2',
                       'Seltenheit.n.1',
                       'Opernproduktion.n.2',
                       'Erfolgsproduktion.n.1',
                       'Scheibe.n.4',
                       'Gemeinschaftsproduktion.n.1'],

    'Gerät.n.1': [     'Elektroschocker.n.1',
                       'Infanteriewaffe.n.1',
                       'Maschine.n.2',
                       'Apparat.n.2',
                       'Verbrennungsmaschine.n.1',
                       'Impulsgenerator.n.1',
                       'Verbrennungsmotor.n.1',
                       'Schiffsdieselmotor.n.1',
                       'Selbstlader.n.1',
                       'Selbstladepistole.n.1',
                       'Gasgenerator.n.1',
                       'Sportwaffe.n.1'],

    'Gerät.n.2': [     'Handgerät.n.2',
                       'Testgerät.n.1',
                       'Musikgerät.n.1',
                       'Wahlgerät.n.1',
                       'Kultgerät.n.1',
                       'Tauchgerät.n.1',
                       'Trainingsgerät.n.1',
                       'Kabel.n.1',
                       'Leitungsdraht.n.1',
                       'Kunststoffseil.n.1',
                       'Militärgerät.n.1',
                       'Heizdraht.n.1']
}
```


# NBalls for other languages

* [This code has been used to generate nball embeddings for Arabic, Chinese, Hindi, and Russian languages. Click me to get the Jupyter scripts](https://github.com/p3ml/ai_language_technology)

# Cite

If you use the code, please cite the following paper:

Tiansi Dong, Chrisitan Bauckhage, Hailong Jin, Juanzi Li, Olaf Cremers, Daniel Speicher, Armin B. Cremers, Joerg Zimmermann (2019). *Imposing Category Trees Onto Word-Embeddings Using A Geometric Construction*. **ICLR-19** The Seventh International Conference on Learning Representations, May 6 – 9, New Orleans, Louisiana, USA.

