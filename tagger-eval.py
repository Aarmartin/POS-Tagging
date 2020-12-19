# Aaron Martin
# 11/26
#
# Program to compare result of testing data POS tagging against a key with the correct POS values and outputing the accurracy and confusion matrix
#
# Example:
# Test Input:
# word1/NN
# word2/JJ
# word3/MD
# Key Input:
# word1/NN
# word/JJ
# word3/WDT
#
# Output:
# NN NN 1
# JJ JJ 1
# MD WDT 1
# Accuracy: 0.66667
#
#	1. Read in key and testing file
#	2. Parse both files at the same time line by line
#		a. For each line (word) in each file, split it on the intended '/' (not escaped \/)
#		b. Check to ensure the files are talking about the same word
#		c. Check to see if the tag values match, and increment an ongoing sum of the number of correct pairs by one if they do
#		d. Store each good tag pair in a dictionary object with its value the count of its number of occurrences (NN NN, JJ JJ, NNP NNP, etc.)
#		e. Store each conflicting tag pair in a dict object with its value the count of its occurrences (NN NNP, JJ NN, IN WDT, etc.)
#	3. Print all of the good pairs in alphabeetically sorted order
#	4. Print all of the conflicting pairs in alphabetically sorted order
#	5. Print the accuracy between the two (correct/total)

import sys
import re

def main(argv):

	# Open Key and Test Files for Reading
	ftest = open(argv[2], "r")
	ftrue = open(argv[1], "r")

	# Split the files line by line into lists
	ftestl = ftest.readlines()
	ftruel = ftrue.readlines()

	# Correct keeps track of the number of matching pairs
	correct = 0

	# GPairs is a dictionary of tuples to keep track of each correct pair
	gpairs = {}

	# Pairs is a dictionary of tuples to keep track of each conflicting (incorrect) pair
	pairs = {}

	# For each test value and true value (with iterator i) in each line list
	for i, test, true in zip(range(len(ftruel)), ftestl, ftruel):

		# Split the key for the test and true values word/tag -> [word, tag]
		#te = test.split("/")
		#tr = true.split("/")

		testm = re.match(r"(.*)(?<!\\)/(.*)", test)
		truem = re.match(r"(.*)(?<!\\)/(.*)", true)

		te = []
		te.append(testm.group(1))
		te.append(testm.group(2))

		tr = []
		tr.append(truem.group(1))
		tr.append(truem.group(2))

		# Debug/Testing code
		'''
		previous = ftruel[i - 1]
		pr = previous.split("/")

		try:
			after = ftruel[i + 1]
			af = after.split("/")
		except:
			af = ["BROKEN", "BROKEN"]
		'''
		# Eliminate the newline character
		#te[1] = te[1][:-1]
		#tr[1] = tr[1][:-1]

		# Debug/Testing code
		'''
		pr[1] = pr[1][:-1]
		af[1] = af[1][:-1]
		'''

		# If the test word and key word do not match, synchronization has been broken and an error has occurred
		if(te[0] != tr[0]):
			print("Sync Broke")
		else:

			# Check to see if the test tag and gold tag match
			if(te[1] == tr[1]):

				# Push correct pair into a tuple
				gpair = (te[1], tr[1])

				# If that correct pairing has already occurred, increment its count, otherwise add it to the list of good pairs
				if gpair in gpairs.keys():
					gpairs[gpair] += 1
				else:
					gpairs[gpair] = 1

				# Increment correct count
				correct += 1
			else:

				# Push conflicting pair into a tuple
				pair = (te[1], tr[1])

				# If that conflic has already occurred, increment its count, otherwise add it to list of conflicts
				if pair in pairs.keys():
					pairs[pair] += 1
				else:
					pairs[pair] = 1

				# Debug/Testing code
				'''				
				if len(te[0]) > 8:
					tabber = "\t"
				elif len(te[0]) > 4:
					tabber = "\t\t"
				else:
					tabber = "\t\t\t"

				print("Test word: " + te[0] + tabber + "Tagged as: " + te[1] + "\tCorrect Tag: " + tr[1])
				if bool(re.search(r"NOT FOUND", te[1])):
					print("Tag was not found")
				'''

	for gpair in sorted(gpairs):
		print(gpair[0], gpair[1], ":", gpairs[gpair])

	for pair in sorted(pairs):
		print(pair[0], pair[1], ":", pairs[pair])
	
	print("Accuracy: " + str(correct/len(ftruel)))
	'''
	sorted_pairs = sorted(pairs.items(), key=lambda x: x[1], reverse=True)

	for pair in sorted_pairs:
		print(pair[0][0], pair[0][1], pair[0][2], pair[0][3], ";", pair[1])
	'''


main(sys.argv)
