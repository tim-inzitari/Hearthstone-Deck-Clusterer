import sys
import subprocess
import io
import os
	
def install(name):
    subprocess.call(['pip', 'install',"--upgrade", name])

if __name__ == '__main__':

	#install requirements
	thelibFolder = os.path.dirname(os.path.realpath(__file__))
	requirementPath = thelibFolder + '/requirements.txt'
	install_requires = []
	if os.path.isfile(requirementPath):
		with open(requirementPath) as f:
			install_requires = f.read().splitlines()
	for install_ in install_requires:
		install(install_)

	#update hs-card-tiles
	p = subprocess.Popen(["git", "pull", "origin", "master"], cwd="../hs-card-tiles")

	#run curl
	os.system("curl -L https://api.hearthstonejson.com/v1/latest/enUS/cards.collectible.json > ../resources/cards.collectible.json")

