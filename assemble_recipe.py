#!/usr/bin/python
import json
import io
import re
import math
import sys
import getopt

def main(argv):

	try:
		opts, args = getopt.getopt(argv, 'hdi:l:o:', ['help'])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	
	inFiles = list()
	lFiles = list()
	outFileName = ''

	global _debug
	_debug = 0
	global translations
	translations = dict()

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt == '-d':
			_debug = 1
		elif opt in ("-i"):
			inFiles.append(arg)
		elif opt in ("-l"):
			lFiles.append(arg)
		elif opt in ("-o"):
			if outFileName != '':
				print 'More than one output file specified, security stop.'
				usage()
				sys.exit(2)
		   	else:
		   		outFileName = arg

	if len(inFiles) == 0:
		inFiles.append('recipe.json')
		print 'No input file specified. Using default "recipe.json".'
	if outFileName == '':
		print 'No output file specified. Using default "recipe.html".'
		outFileName = 'recipe.html'


	for lFile in lFiles:
		readPropFile(lFile)

	print 'Begin writing recipes to', outFileName
	with io.open(outFileName, 'w') as outFile:
		outFile.write(u'<!DOCTYPE html>\n<html>\n<head>\n<title>Recipes</title>\n</head><body>')
		for inFileName in inFiles:
			processJson(inFileName, outFile)
		outFile.write(u'</body>\n</html>')

def processJson(inFileName, outFile):
	print 'Parsing', inFileName

	with io.open(inFileName, 'r') as inFile:
		jsonFileContent = json.load(inFile)
		count = 0
		for inJson in jsonFileContent:
			printRecipe(outFile, inJson)
			count += 1
	print count, 'recipes processed.\n'
		

def printRecipe(outFile, inJson):
	output = inJson['output'];
	outputName = inJson['output_name']
	outputCount = inJson['output_count']

	recipeType = inJson['type']

	inputs = inJson['inputs']

	cols = 0
	lines = len(inputs)

	for line in inputs:
		if len(line) > cols:
			cols = len(line)

	if _debug:
		print '---Recipe:---'
		print 'File contains', recipeType, 'recipe with', lines, 'lines and', cols, 'columns.'
		print 'Output:', outputCount, 'of', output
		print ''

	outFile.write(u'\n<table>\n\t<tr><th colspan="' + str(cols + 2) + '">')
	if recipeType == 'shaped':
		outFile.write(u'Shaped ')
	if recipeType == 'shapeless':
		outFile.write(u'Shapeless ')
	outFile.write(u'Crafting: ')
	outFile.write(outputName)
	outFile.write(u'</th></tr>');

	didWriteResult = 0
	

	for l in xrange(0,lines):
		line = inputs[l]
		outFile.write(u'\n\t<tr>')
		if _debug:
			print 'Recipe line:', line
		for item in line:
			printItem(outFile, item)

		if (not didWriteResult) and ((l + 1) > math.floor(lines/2)):
			printArrow(outFile)
			printItem(outFile, output)
			didWriteResult = 1
		else:
			printPlaceholder(outFile)
		outFile.write(u'\n\t</tr>')
	outFile.write(u'\n</table>')
	if _debug:
		print ''

def printItem(outFile, inputItem):
	if inputItem == '':
		outFile.write(u'\n\t\t<td></td>')
	else:
		item = re.split(':', inputItem)
		if len(item) != 3:
			nSpace = 'minecraft'
			nKind = item[0]
			nName = item[1]
		else:
			nKind = item[0]
			nSpace = item[1]
			nName = item[2]

		urlLink = u''
		urlImg = u''
		if nSpace == 'minecraft':
			urlImg = u'https://github.com/Team-IO/taam/wiki/images/recipes/vanilla/' + nName + '.png'
			
			if(nKind == 'item'):
				urlLink = u'http://minecraft.gamepedia.com/Items'
			if(nKind == 'block'):
				urlLink = u'http://minecraft.gamepedia.com/Blocks'
			
		if nSpace == 'taam':
			urlImg = u''
			if(nKind == 'item'):
				urlImg = u'https://raw.githubusercontent.com/Team-IO/taam/master/resources/assets/taam/textures/items/' + nName + '.png'
			if(nKind == 'block'):
				urlImg = u'https://github.com/Team-IO/taam/wiki/images/recipes/taam/' + nName + '.png'
			
			urlLink = u''
			if nName.startswith('ingot.'):
				urlLink = u'https://github.com/Team-IO/taam/wiki/Ores-%26-Ingots#' + nName
			if nName.startswith('material.'):
				urlLink = u'https://github.com/Team-IO/taam/wiki/Materials#' + nName
			if nName.startswith('part.'):
				urlLink = u'https://github.com/Team-IO/taam/wiki/Parts#' + nName
			if nName.startswith('tool.'):
				urlLink = u'https://github.com/Team-IO/taam/wiki/Tools#' + nName
		nDisplay = getName(nSpace, nKind, nName)

		outFile.write(u'\n\t\t<td><a href="')
		outFile.write(urlLink)
		outFile.write(u'"><img src="')
		outFile.write(urlImg)
		outFile.write(u'" width="16" height="16" alt="')
		outFile.write(nDisplay)
		outFile.write(u'" title="')
		outFile.write(nDisplay)
		outFile.write(u'" /></a></td>')

def printArrow(outFile):
	outFile.write(u'\n\t\t\t<td><img src="https://github.com/Team-IO/taam/wiki/images/recipes/arrow.png" width="22" height="15" alt="Arrow" /></td>')

def printPlaceholder(outFile):
	outFile.write(u'\n\t\t\t<td colspan="2"></td>')

def readPropFile(lFile):
	print 'Reading language file', lFile
	with io.open(lFile, 'r') as propFile:
		count = 0
		lines = propFile.readlines()
		for line in lines:
			if line.startswith('#'):
				continue
			element = re.split('=', line, 1)
			if len(element) == 2:
				translations[element[0]]=element[1].strip();
				count += 1
	print count, 'translations loaded.\n'
	return translations

def getName(nSpace, nKind, nName):
	if nKind == 'item':
		search = u'item'
	else:
		search = u'tile'
	if nSpace != 'minecraft':
		search = search + '.' + nSpace
	search = search + '.' + nName + '.name'
	if _debug:
		print search
	if search in translations:
		return translations[search]
	else:
		return search

if __name__ == "__main__":
	main(sys.argv[1:])