# Deck Clusterer   

A python script for converting Hearthstone deck codes from a csv to declarations of their archetypes in csv format.

## Requirements    
Language that must be installed    
* Python 3.8+   

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
```
cd CSVs/   
python getCSVsThreaded
