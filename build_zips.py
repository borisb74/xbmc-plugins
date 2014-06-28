""" addons.xml generator """

import os
import md5

import zipfile
from xml.dom.minidom import parse

EXCLUDE_EXTS = ['.pyc', '.pyo', '.swp']

def generateZip(ADDON):
	# Parse addon.xml for version number
	dom = parse("%s/addon.xml" % ADDON)
	addon = dom.getElementsByTagName('addon')[0]
	version = addon.getAttribute('version')
	zfilename = "%s-%s.zip" % (ADDON, version)

	# Walk the directory to create the zip file
	z = zipfile.ZipFile("repo/" + ADDON + "/" + zfilename, 'w')
	for r, d, f in os.walk(ADDON):
	  for ff in f:
		skip = False

		# If it's not one of the files we're excluding
		for ext in EXCLUDE_EXTS:
		  if ff.endswith(ext):
			skip = True

		if not skip: 
		  z.write(os.path.join(r, ff), os.path.join(r, ff))
	z.close()



#ADDON='plugin.audio.afl-radio'

addons = os.listdir( "." )
for ADDON in addons:
	if ( not os.path.isdir( ADDON ) or ADDON == ".svn" or ADDON == ".git"): continue
	if ( not os.path.isfile( ADDON + "/addon.xml")): continue
	generateZip(ADDON)

#if ( __name__ == "__main__" ):
#    # start
#    Generator()