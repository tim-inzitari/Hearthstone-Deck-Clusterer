# Deck Clusterer   

A python script for converting Hearthstone deck codes from a csv to declarations of their archetypes in csv format.

## Requirements    
Language that must be installed    
* Python 3.7+   

Packages that can must be installed   
This can be done by following instructions in **Setup**          
* [python-hearthstone](https://github.com/hearthsim/python-hearthstone)
* MatPlotLib
* Scikit-learn
* [python-hearthstone](https://github.com/hearthsim/hsdata)
* PySimpleGui
* scikit-learn
* pandas
* [Python Imaging Library](https://pillow.readthedocs.io)
* [backports.csv](https://pypi.python.org/pypi/backports.csv)
* [Requests](http://docs.python-requests.org)
* BeautifulSoup4


## Setup   

Clone this repository first, then clone the hs-card-tiles repo [https://github.com/HearthSim/hs-card-tiles](https://github.com/HearthSim/hs-card-tiles) within the `DeckClusterer` directory.   

```
git clone https://github.com/HearthSim/hs-card-tiles
```

Then properly install a Python version of atleast 3.8   
Then at the **first install, and after every Hearthstone Patch, Card Change, Or addition of Hero Portrait/Cardback**   
run `setup.py` found in the `setup` directory.

```
cd setup   
python setup.py    
```

This will update the card database, hearthstone library, and pull the most recent card tiles.   

### USAGE

To run the Clustering or Classification Program
```
python main.py
```   
and follow instructions on the GUI   
   
To Generate CSVs from Battlefy Data:    
`STARTDATE` format: "MM-DD-YYYY" **Note, 24 hour time so enter the Monday for a full weekend**   
`ENDDATE` format: "MM-DD-YYYY" **Note UCT Timezone so enter the Monday for a full weekend**   

```
cd CSVs/   
python getCSVsThreaded STARTDATE ENDDATE   
```

## CSV formatting

### Input   
The first line in the CSV file will be the schema for the rest of the file. It will be a comma separated list of arguments with the same length as the rest of the rows of the file. Leave unused fields blank, and use "K" for keys (which will group the decklists and control what the image file is named as), and "D" for deck codes to be parsed by the script.

For example, a schema of `K,D,D,D,D` in the first line of the csv will indicate that the followings lines have the form "Name/Key, Deck Code #1, Deck Code #2, Deck Code #3, Deck Code #4", which a schema of "K,,D" will indicate the form of "Name/Key, \[Irrelevant\], Deck Code" and the program will group deck codes corresponding to the same key to the same deck image.

If the schema is not specified, a schema of `K,D,D,D,...` will be assumed.   

Example input:
```
K,D,D,D,D
Akron,AAECAf0GBO0Fws4Cl9MCzfQCDYoB8gX7BrYH4Qf7B40I58sC8dAC/dACiNIC2OUC6uYCAA==,AAECAaoICCCZAvPCAsLOAqvnAvbsAqfuAs30Agu9AdMB2QfwB7EIkcECrMICm8sClugClO8CsPACAA==,AAECAQcC08MCn9MCDkuRBv8HsgibwgK+wwLKwwLJxwKbywLMzQLP5wKq7AKb8wLF8wIA,AAECAZICAv4BmdMCDkBf/QL3A+YFxAaFCOQIoM0Ch84CmNICntIChOYC1+8CAA==
```     
also accepts full deck codes.   

### Output    
For all modes     
Outport will be of form:
`K,D,D,D,D,...`   
followed by the team name and deck calssification one each line    

Example output:
```
K,D,D,D,D`   
Akron, Highlander mage, OTK dh, Enrage warrior, Zoo warlock   
```   
Clustering Portion also outputs a csv of Labels that can be used for later classification usages into
`outputs/labels/NEW_labels/` this should be renamed for easier use.   