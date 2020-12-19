# Aaron Martin
# 11/26
#
# Program that takes in training data as a list of words and their intended parts of speech, and uses that data to calculate probabilities for each word what it's likelyhood is that it would be used as the part of speech
#
# Example:
# Input:
# word1/NN
# word2/NN
# word1/JJ
# word1/NNP
# word2/MD
# word3/NNPS
#
# Output:
# word1 P(NN) = 1/3, P(JJ) = 1/3, P(NNP) = 1/3
# word2 P(NN) = 1/2, P(MD) = 1/2
# word3 P(NNPS) = 1
#
#	1. Parse training file line by line
#		a. For each line, use regex to split it on proper '/' (not escaped \/)
#		b. If the word has not been encountered, add it to a dictionary
#		c. If the associated tag has not been encountered for that word, add it to a dictionary at that word in the dictionary (nested dicionary)
#		d. Increment value for each appearence in training data
#	2. Parse created dictionary through each word
#		a. grab total count of all tags associated with that word
#		b. For each word, Parse each of its tags
#			i.  Grab the tags count and add one to it
#			ii. Divide that value by the total tag count and the list size of unique tags
#		c. Print the word and each of its tag probabilities on one line

import sys
import re

# Method used for determining status of a word's tag value, and incrementing its count (Called on specific tags)
def dictEdit(masterDict, key, val):

	# If a word as not been found before, add it to the dictionary, with its value as another dictionary (for the tags)
	# [ "word" : {} ]
	if key not in masterDict.keys():
		masterDict[key] = {}

	# With the word now in place, if it does not yet have a count value (has not been encountered before) default it to 0
	# [ "word" : [ "tag" : 0 ] ]
	if val not in masterDict[key].keys():
		masterDict[key][val] = 0

	# Increment that tag's count by one
	# [ "word" : [ "tag" : 1 ] ]
	masterDict[key][val] += 1

def main(argv):

	# Open the training file and split each line as an element in a list
	f = open(argv[1], "r")
	fl = f.readlines()

	# Dict object for keeping track of each individual word and its associated tag value counts
	masterDict = {}

	# For loop for iterating over each word and tag in the training data
	for line in fl:

		# Remove newline character
		line = line[:-1]

		# Establish intended / to be split on (not escaped slashes like \/)
		parts = re.match(r"(.*)(?<!\\)/(.*)", line)

		# Grab word and tag values from regex capture groups
		word = parts.group(1)
		tag = parts.group(2)

		# Use dictEdit method to update status of dictionary at location [word][tag]
		try:
			dictEdit(masterDict, word, tag)
		except:
			print(line)

	# For loop for iterating over every unique word to print its calculated probabilities
	for key in masterDict.keys():

		# Print initial word first
		print(key, end=" ")

		tagCount = 0

		# For loop for iterating over list of tags in the respective words tag values to grab total tag count
		for tag in masterDict[key].keys():
			tagCount += masterDict[key][tag]

		# For loop used for calculating probability and printing output to output file for each tag in the words tag list
		for tag in masterDict[key].keys():
			# Numerator value tag count + 1
			num = masterDict[key][tag] + 1
			# Denominator value total tag count + len of list of tags
			den = tagCount + 21
			# Divinding values
			p = num/den
			# Output
			print(tag + ";" + str("{0:.5f}".format(p)), end=" ")
		print()

main(sys.argv)
