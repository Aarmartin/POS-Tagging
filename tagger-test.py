# Aaron Martin
# 11/26
#
# Program for testing a set of words against training data probabilities to attempt to determine that words part of speech
#
# Example:
# Input:
# word1
# word2
# word3
#
# Output:
# word1/NN (noun)
# word2/JJ (adjective)
# word3/MD (modal/auxiliary verb)
#
#	1. Read in mode (simple or rule-based)
#	2. Read in training file and separate line by line and testing file and separate line by line
#	3. Convert training data into a dictionary (word tag;pval becomes ["word" : [ "tag" : pval ] ]
#	4. Parse testing data line by line
#		a. For each line (word) grab its context (previous word and next word)
#		b. Determine its tag given the context
#			i.   Grab highest probability tag of word (mode 0)
#			ii.  If the word has been encountered before, run the word and context words against a list of rules for known words (Tune in a tag) (mode 1)
#				*. Grab highest probability tag and compare it to contexet tags
#			iii. If the word has not been encountered before, run the word spelling and context against a list of rules for unknown words (Establish a new tag) (mode 1)
#				*. Check spelling and context tags	
#			iv.  If a determination can not be made for either, set as NN (noun)
#		c. Print word and its best fit tag

import sys
import operator
import re

# Method for determining the proper tag on a given word
# Takes in the word and its input context
# If mode is 0, top tag value
# If mode is 1, assess with rules
def setTag(masterDict, mode, word, previous, after):

	# Check if simple mode
	if mode == 0:
		# If word has been seen before and has a tag
		if word in masterDict.keys():
			# Return tag with highest probability
			return findTop(masterDict[word])
		else:
			# Default to NN
			return "NN"

	# Initialize context tags to None in case they are not found to have tags
	previousTag = None
	afterTag = None

	# If previous word has been found and has a tag, record it
	if previous in masterDict.keys():
		previousTag = findTop(masterDict[previous])

	# If next word has been found and has a tag, record it
	if after in masterDict.keys():
		afterTag = findTop(masterDict[after])

	# If word has been seen before and has a tag
	if word in masterDict.keys():

		# Process probability tag against known rule list
		tag = knownTest(word, findTop(masterDict[word]), previous, previousTag, after, afterTag)
		# Establishes best known tag by changing probability value to maximum
		masterDict[word][tag] = 1
		return tag

	# If word has not been seen before
	else:

		# Process unknown word against unknown rule list
		tag = unknownTest(word, previous, previousTag, after, afterTag)

		# If a known rule has been used to edit that tag, establish it as best known tag and returning it
		if tag is not None:
			masterDict[word] = {}
			masterDict[word][tag] = 1
			return tag
		# If still not found or caught by any rules, default to NN
		else:
			return "NN"

# List of rules for words with unknown tags
def unknownTest(word, previous = "", previousTag = "", after="", afterTag=""):

	# If it contains a number, tag as CD
	if bool(re.search(r"\d", word)):
		return "CD"

	# If it precedes with very, ends with -ish or -some or contains a hyphen, tag as JJ
	if previous == "very" or word.endswith("ish") or word.endswith("some") or bool(re.search(r"-", word)):
		return "JJ"

	# If the first letter is uppercase, tag as NNP
	if word[0].isupper():
		return "NNP"

	# If it ends with -en or -ed, tag as VBD
	if word.endswith("en") or word.endswith("ed"):
		return "VBD"

	# If it ends with -es or -s, tag with NNS
	if word.endswith("es") or word.endswith("s"):
		return "NNS"

	# If it ends with -ing, tag with VBG
	if word.endswith("ing"):
		return "VBG"

	# If it ends with -ly, tag with RB
	if word.endswith("ly"):
		return "RB"

	return None

# List of rules for words with known tags
def knownTest(word, wordTag, previous = "", previousTag = "", after = "", afterTag = ""):

	# Initialize tag as the tag with the top value score
	tag = wordTag

	# If it succeeds TO and was originally caught as a noun, edit to VB
	if wordTag == "NN" and previousTag == "TO":
		tag = "VB"

	# If it succeeds a proper noun and was caught as a proper noun plural, edit to NNP
	if wordTag == "NNPS" and previousTag == "NNP":
		tag = "NNP"

	# If it succeeds a determiner and was caught as a verb, edit to a noun
	if wordTag == "VB" and previousTag == "DT":
		tag = "NN"

	# If it succeeds an auxiliary verb and was caught as a VBP, edit to a regular VB
	if wordTag == "VBP" and previousTag == "MD":
		tag = "VB"

	# If it succeeds a plural noun and was caught or changed to a VB (often found from the previous edit), edit to VBP
	if wordTag == "VB" and previousTag == "NNS":
		tag = "VBP"

	# If it succeeds TO and was caught as a VBP, edit to regular VB
	if wordTag == "VBP" and previousTag == "TO":
		tag = "VB"

	return tag


# Making a sub-dictionary object that contains a list of tags and their respective probabilities (Function is called for each unique word)
# Ex. [ "JJ;0.75", "NN;0.25" ]
def makeDict(tags):
	tagDict = {}

	for tag in tags:
		# "JJ;0.75" -> [ "JJ", "0.75" ]
		parts = tag.split(";")

		# [ "JJ", "0.75" ] -> "JJ" : 0.75
		tagDict[parts[0]] = parts[1]

	return tagDict

# Method to find the tag with the highest associated Probability Value (Function is called on a specific word)
# Ex. [ "JJ" : 0.75, "NN" : 0.25 ]
def findTop(tags):
	maxn = int(0)
	maxt = ""

	# tags.keys() = [ "JJ", "NN" ]
	for tag in tags.keys():

		# Grab tag's probability value
		# tags["JJ"] = 0.75
		fval = float(tags[tag])

		# If value is higher than current max value, set to new max value
		if(fval > maxn):
			maxn = fval
			maxt = tag

	return maxt

def main(argv):

	# Set mode
	mode = int(argv[1])

	# Open each file in Read mode and set each line as an element in a list
	ftrain = open(argv[2], "r")
	ftrainl = ftrain.readlines()

	ftest = open(argv[3], "r")
	ftestl = ftest.readlines()

	# Dict object for keeping track of each unique word and its tag probabilities
	# [ "word1" : [ "JJ" : 0.02, "NN" : 0.98 ],
	#   "word2" : [ "JJ" : 0.75, "NN" : 0.25 ] ]
	masterDict = {}

	# For loop used for initializing dictionary with all unique words and their associated tag probabilities
	for line in ftrainl:

		# Input line from training data split on " "
		# "word1 JJ;0.75 NN;0.25" -> ["word1", "JJ;0.75", "NN;0.25"]
		parts = line.split()

		# Make a tag dictionary out of the entire line of tags (excluding the first item, which is the word itself)
		# [ "JJ;0.75", "NN;0.25" ] -> [ "JJ" : 0.75, "NN" : 0.25 ]
		tags = makeDict(parts[1:])
		
		# Associate the tag dictionary with its word in the master dictionary
		# "word" : [ "JJ" : 0.75, "NN" : 0.25 ]
		masterDict[parts[0]] = tags

	# For loop used for printing out calculated tag while providing context for each word
	for i, line in zip(range(len(ftestl)), ftestl):

		# Remove newline character from test word
		line = line[:-1]

		# Establish previous word and remove newline character
		previous = ftestl[i - 1]
		previous = previous[:-1]

		# Establish next word and remove newline character (try statement for when limit of words is reached)
		try:
			after = ftestl[i + 1]
			after = after[:-1]
		except:
			after = None

		# Calculate tag using methods above
		tag = setTag(masterDict, mode, line, previous, after)

		# Output
		print(line + "/" + tag)

	ftest.close()

	ftrain.close()

main(sys.argv)
