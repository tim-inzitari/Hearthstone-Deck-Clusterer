import os
import glob

def deleteFiles(path, fileType):
	files = glob.glob('{}*.{}'.format(path, fileType))
	for f in files:
		try:
			os.remove(f)
		except OSError as e:
			print("Error: %s : %s" % (f, e.strerror))	