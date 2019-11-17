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
$ python nball.py --train_nball data/nball.txt --w2v data/ws_w2v.vec  --ws_child data/ws_child.txt --ws_catcode data/ws_catcode.txt --log data/log.txt
```

**Result:**
```
['Spezifikum.n.1', 'Zustand.n.1', 'ortsspezifisch.j.1', 'Entität.n.2', 'Stelle.n.3', 'denken.v.5', 'machen.v.7', 'wahrnehmen.v.3', 'Menge.n.2', 'klassenübergreifend.j.1', 'nehmen.v.1', 'sollen.v.3', 'handeln.v.5', 'sein.v.2', 'bekommen.v.4', 'wünschen.v.1', 'geben.v.4', 'können.v.1', 'haben.v.7', 'Dauerkontakt.v.1', 'haben.v.6', 'wissen.v.2', 'sein.v.3', 'haben.v.1', 'gefallen.v.1', 'gehen.v.7', 'stammen.v.1', 'lassen.v.5', 'müssen.v.2', 'führen.v.5', 'bekommen.v.2', 'kommen.v.2', 'vorangehen.v.1', 'aufhaben.v.3', 'können.v.2', 'sollen.v.1', 'folgen.v.5', 'fehlen.v.5', 'anschließen.v.3', 'halten.v.5', 'folgen.v.1', 'bedeuten.v.2', 'haben.v.8', 'aufhaben.v.2', 'loshaben.v.2', 'haben.v.5', 'sollen.v.2', 'sein.v.5', 'können.v.3']
*** Spezifikum.n.1 
Shifting Artefakt.n.1
Shifting Struktur.n.3
Shifting Ding.n.5
*** Zustand.n.1 
Shifting Veränderung.n.1
Shifting Veränderung.n.2
Shifting Prozess.n.1
Shifting Geschehnis.n.1
Shifting Ereignis.n.1
Shifting Beziehung.n.1
Shifting Situation.n.1
*** ortsspezifisch.j.1 
*** Entität.n.2 
Shifting Objekt.n.4
Shifting Äußerung.n.2
Shifting Kommunikation.n.1
Shifting Mitteilung.n.1
Shifting Übermittlung.n.1
Shifting Kreation.n.1
Shifting Erschaffung.n.1
Shifting Erzeugung.n.1
Shifting Bewegung.n.3
*** Stelle.n.3 
Shifting Handlung.n.2
Shifting Veranstaltung.n.1
*** denken.v.5 
*** machen.v.7 
*** wahrnehmen.v.3 
*** Menge.n.2 
Shifting Gruppe.n.1
Shifting Teilmenge.n.2
Shifting Teil.n.2
Shifting Zusammenschluss.n.1
Shifting Bauwerk.n.1
Shifting Veröffentlichung.n.2
Shifting Produkt.n.2
Shifting Vorrichtung.n.1
Shifting Stoff.n.4
Shifting Hilfe.n.2
*** klassenübergreifend.j.1 
*** nehmen.v.1 
*** sollen.v.3 
*** handeln.v.5 
*** sein.v.2 
*** bekommen.v.4 
*** wünschen.v.1 
*** geben.v.4 
*** können.v.1 
*** haben.v.7 
*** Dauerkontakt.v.1 
*** haben.v.6 
*** wissen.v.2 
*** sein.v.3 
Shifting verarbeiten.v.1
*** haben.v.1 
*** gefallen.v.1 
*** gehen.v.7 
*** stammen.v.1 
*** lassen.v.5 
*** müssen.v.2 
*** führen.v.5 
*** bekommen.v.2 
*** kommen.v.2 
*** vorangehen.v.1 
Shifting ändern.v.3
*** aufhaben.v.3 
*** können.v.2 
*** sollen.v.1 
*** folgen.v.5 
*** fehlen.v.5 
*** anschließen.v.3 
*** halten.v.5 
*** folgen.v.1 
*** bedeuten.v.2 
*** haben.v.8 
*** aufhaben.v.2 
*** loshaben.v.2
Shifting stattfinden.v.1
*** haben.v.5 
*** sollen.v.2 
*** sein.v.5 
*** können.v.3
finished training of all families

loading balls....
[417]
totally 50674  balls are loaded
updating first level children...
```

## Experiment 1.2: Checking whether tree structures are perfectly embedded into word-embeddings
* main input is the output directory of nballs created in Experiment 1.1
* shell command for running the nball construction and training process
```
$ python nball.py --zero_energy data/data_out/ --ball data/nball.txt --ws_child data/ws_child.txt
```

**Result:**
```
loading balls....
[417]
totally 50674  balls are loaded
failed families with P []
failed families with DC []
the tree structure is perfectly embedded in nball embeddings.

generating nball embedding file...
```
#### [NBall Embedding](https://drive.google.com/open?id=1Djv4EZXfp9Zpr_iCIW7u8SrdYqkk0Pr5) (6GB)


# Experiment 2: Observe neighbors of word-sense using nball embeddings
```
$ python nball.py --neighbors handeln.v.2 handeln.v.5 Teil.n.2 Teil.n.3 Teil.n.4 Teil.n.5 Gerät.n.1 Gerät.n.2 --ball data/nball.txt --num 12
% --neighbors: list of word-senses
% --ball: file location of the nball embeddings
% --num: number of neighbors
```

* **Result**:
```json5
loading balls....
50674  balls are loaded

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

