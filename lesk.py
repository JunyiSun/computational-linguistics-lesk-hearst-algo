#import sys
#sys.path.insert(0, '/u/csc485h/include/a3/nltk/corpora')
#import wordnet as wn
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

sentence = 'A salad/N with greens/N and tomato/N is a healthful addition/N to any meal/N, but add an avocado/N and you have something really special/Adj.'
stop = set(stopwords.words('english') + ['something', 'thing'])
wnl = WordNetLemmatizer()

def lesk(word, word_bag):
	print(word)
	B = []
	for item in word_bag:
		vocab = item.split('/')[0]
		if not vocab == word.split('/')[0]:
			B.append(vocab)
			synset = wn.synsets(vocab)
			for syn in synset:
				meaning = syn.definition()
				mean_bag = meaning.split() 
				mean_bag = [wnl.lemmatize(x.strip(';,.()')) for x in mean_bag if x not in stop]
				try:
					ex = syn.examples()[0]
					ex_bag = ex.split()
					ex_bag = [wnl.lemmatize(x.strip(';,.()')) for x in ex_bag if x not in stop]
					B.extend(ex_bag)
				except:
					pass
				B.extend(mean_bag)
				
	#print(B)
	
	senses = []
	word_synset = wn.synsets(word.split('/')[0])
	for word_syn in word_synset:
		sense_mean = word_syn.definition()
		sense_mean_bag = sense_mean.split()
		sense_mean_bag = [wnl.lemmatize(y.strip(';,.()')) for y in sense_mean_bag if y not in stop]
		
		senses.append(sense_mean_bag)
		
	#print(senses)

	best_sense = 0
	max_overlap = 0
	max_overlap_list = []
	to_be_print = ''
	for index, sense in enumerate(senses):
		overlap = compute_overlap(sense, B)
		overlap_num = overlap[0]
		to_be_print = to_be_print  + word.split('/')[0] + '#' + str(index+1) +  '\t' + word_synset[index].definition() + '\t' + str(overlap_num) + '\t' + ','.join(p for p in overlap[1]) + '\n' 
		if overlap_num > max_overlap:
			max_overlap = overlap_num
			best_sense = word.split('/')[0] + '#' + str(index+1)
			max_overlap_list = overlap[1]
	print(best_sense)
	print(to_be_print)
	#print(max_overlap, max_overlap_list)

def compute_overlap(sense, B):
	count = 0
	overlap_list = []
	for item in sense:
		if item in B:
			count = count+1
			overlap_list.append(item)
	return count, overlap_list


if __name__ == '__main__':
    sentence_split = sentence.split()
    word_bag = []
    for word in sentence_split:
    	if '/' in word:
    		word_bag.append(word.strip('.,'))
    for word in word_bag:
    	lesk(word, word_bag)



