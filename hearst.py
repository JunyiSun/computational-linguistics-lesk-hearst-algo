#!/usr/bin/env python
import sys
import re
sys.path.append('/u/csc485h/include/a3') 
from Asst3 import nyt_big, nyt_mini, DefaultNpPattern
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
stop = set(stopwords.words('english')+ ['other', 'especially', 'such', 'including'])


# nyt_big  is the full POS-tagged 2004 NY Times corpus. 
# nyt_mini is the first 100K lines of nyt_big. 
# Use nyt_big for your final submission. You can use nyt_mini
# for testing and debugging your code during code development.
# DefaultNpPattern is a simple baseline pattern for NP chunking

# create a chunk parser with the default pattern for NPs
from nltk.chunk.regexp import *
BaselineNpChunkRule = ChunkRule(DefaultNpPattern, 
                                'Default rule for NP chunking')
NpPattern = BaselineNpChunkRule
NpChunker = RegexpChunkParser([BaselineNpChunkRule], 
                              chunk_label='NP')

indicator = ['such as', 'such', 'other', 'including', 'especially']

NP = '(\(NP(\s([a-zA-Z0-9.])+/[A-Z]+)*(\s([a-zA-Z0-9.])+/[A-Z]+)\))'
conditionalCOMMA = '(\s\s,/,)?'
conditionalNP = '((\s\s,/,\s\s)(\(NP(\s([a-zA-Z0-9.])+/[A-Z]+)*(\s([a-zA-Z0-9.])+/[A-Z]+)\)))*'
conditionalANDORNP = '(\s\s(and/CC|or/CC)\s\s(\(NP(\s([a-zA-Z0-9.])+/[A-Z]+)*(\s([a-zA-Z0-9.])+/[A-Z]+)\)))?'

suchas = '(\s\s)(such/JJ  as/IN)\s\s'
list1 = [NP, conditionalCOMMA, suchas, NP, conditionalNP, conditionalANDORNP]
pattern1 = ''.join(list1)

pat2 = '(\(NP such/JJ(\s([a-zA-Z0-9.])+/[A-Z]+)*(\s([a-zA-Z0-9.])+/[A-Z]+)\))  as/IN  '
list2 = [pat2, NP, conditionalNP, conditionalANDORNP]
pattern2 = ''.join(list2)


other = '\s\s((and/CC|or/CC)\s\s)?(\(NP other/JJ ([a-zA-Z0-9.])+/[A-Z]+(\s([a-zA-Z0-9.])+/[A-Z]+)?\))'
list3 = [NP, conditionalNP, other]
pattern3 = ''.join(list3)

including = '(\s\s)(including/VBG)\s\s'
list4 = [NP, conditionalCOMMA, including, NP, conditionalNP, conditionalANDORNP]
pattern4 = ''.join(list4)

especiallyNP = '(\s\s)\(NP especially/RB(\s([a-zA-Z0-9.])+/[A-Z]+)*(\s([a-zA-Z0-9.])+/[A-Z]+)\)'
list5 = [NP, conditionalCOMMA, especiallyNP, conditionalNP, conditionalANDORNP]
pattern5 = ''.join(list5)


def get_parsed(s):
	p = NpChunker.parse(s)
	pstr = str(p)
	plist = pstr.splitlines()
	#print(plist)
	return ''.join(plist)

def get_words(parsed, search_result):
	extracted = parsed[search_result.start():search_result.end()]
	#print(extracted)
	group = extracted.split("  ")
	NP_group = []
	for index, item in enumerate(group):
		if 'NP' in item:
			NP_group.append(group[index])
	#print(NP_group)

	words = []
	for element in NP_group:
		compound = element.strip('(NP) ')
		subs = compound.split()
		temp = ''
		for sub in subs:
			if (len(temp) == 0):
				temp = temp + wnl.lemmatize(sub.split('/')[0])
			else:
				temp = temp + ' ' + wnl.lemmatize(sub.split('/')[0])
		words.append(temp)
	#print(words)
	return words


def do_pattern1(parsed):
	search_result1 = re.search(pattern1, parsed)
	if search_result1:
		words1 = get_words(parsed, search_result1)
		super_word = process_compound(words1[0])
		for np in words1[1:]:
			print_hyperonym(np, super_word)
			


def do_pattern2(parsed):
	search_result2 = re.search(pattern2, parsed)
	if search_result2:
		words2 = get_words(parsed, search_result2)
		try: 
			super_word = process_compound(words2[0].split(' ', 1)[1])
		except:
			super_word = words2[0]
		for np in words2[1:]:
			print_hyperonym(np, super_word)
			
    
def do_pattern3(parsed):
	search_result = re.search(pattern3, parsed)
	if search_result:
		words = get_words(parsed, search_result)
		try:
			super_word = process_compound(words[len(words)-1].split(' ', 1)[1])
		except:
			super_word = words[len(words)-1]
		for np in words[0:len(words)-1]: 
			print_hyperonym(np, super_word)

def do_pattern4(parsed):
	search_result4 = re.search(pattern4, parsed)
	if search_result4:	
		words = get_words(parsed, search_result4)
		super_word = process_compound(words[0])

		for np in words[1:]:
			print_hyperonym(np, super_word)

			

def do_pattern5(parsed):
	search_result = re.search(pattern5, parsed)
	if search_result:
		words = get_words(parsed, search_result)
		try:
			super_word = process_compound(words[0].split(' ', 1)[1])
		except:
			super_word = words[0]
		for np in words[1:]:
			print_hyperonym(np, super_word)

def print_hyperonym(np, super_word):

	word = process_compound(np)
	#print('HYPONYM(' + word + ', ' + super_word + ')')
	check(word, super_word)
	if len(super_word.split()) > 1:
		try:
			super_super_word = super_word.rsplit(' ', 1)[1]
			check(word, super_super_word)
			#print('HYPONYM(' + word + ', ' + super_super_word + ')')
		except:
			pass


def check(word, super_word):
	super_syn = wn.synsets(super_word)
	word_syn = wn.synsets(word)

	if len(super_syn) == 0 or len(word_syn) == 0:
		print('4', end="")
		#print('Case 4')
		print('HYPONYM(' + word + ', ' + super_word + ')')

	found = False
	if len(super_syn) > 0 and len(word_syn) > 0:
		for s, w in ((s1, w1) for s1 in super_syn for w1 in word_syn):
			inner_found = False 
			for result in w.lowest_common_hypernyms(s) :
				if result is s:
					#print('Case 1')
					print('1', end="")
					print('HYPONYM(' + word + ', ' + super_word + ')')
					found = True
					inner_found = True
					break
				if result is w:
					#print('Case 2')
					print('2', end="")
					print('HYPONYM(' + word + ', ' + super_word + ')')
					found = True
					inner_found = True
					break
			if inner_found:
				break
		if not found:
			print('3', end="")
			print('HYPONYM(' + word + ', ' + super_word + ')')
				
					

					
def process_compound(np):
	split_list = np.split()
	if len(split_list) <= 1:
		return np
	if len(wn.synsets(np)) > 0 or len(wn.synsets(split_list[0])) > 0 and split_list[0] not in stop :
		#print(np)
		return np
	else:
		found = False
		start = 1
		while not found and start < len(split_list)-1:
			sub = ' '.join(split_list[start:])
			#print(sub)
			if len(wn.synsets(sub)) > 0 or len(wn.synsets(split_list[start])) > 0 and split_list[start] not in stop : 
				found = True
			else:
				start = start + 1
		return ' '.join(split_list[start:])



if __name__ == '__main__':
	# just for the purpose of illustration, print the output of the 
	# NP Chunker for the first 3 sentences of nyt_mini
	
	for index, s in enumerate(nyt_big.tagged_sents()):    # here is big!!!
	#if True:
		#s = nyt_mini.tagged_sents()[97090]
		#print(s)
		
		sentence = ' '.join(t[0] for t in s)
		if any(x in sentence for x in indicator):

			try:
				#print(sentence)
				parsed = get_parsed(s)
				#print(parsed)
				do_pattern1(parsed)
				do_pattern2(parsed)
				do_pattern3(parsed)
				do_pattern4(parsed)
				do_pattern5(parsed)
			except:
				pass
	
''' some util functions to count the occurrance of each case and confidence
def p(filename='output.txt'):
    d = {'1': [], '3': [], '2': [], '4': []}
    file = open(filename)
    for line in file:
        if len(line.split()) == 4:
            l = line.split()
            d[l[3]].append((l[0], l[1], l[2]))
    import pdb; pdb.set_trace()
    for i in d:
        print("\n\nSentence for {}".format(i))
        for j in random.sample(d[i], 50):
            print("{:40} {:40} {:10}".format(j[0], j[1], j[2]))
'''