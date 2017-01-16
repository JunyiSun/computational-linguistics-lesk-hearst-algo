import sys
sys.path.append('/u/csc485h/include/a3')
from Asst3 import nyt_big, nyt_mini, DefaultNpPattern
from nltk.corpus import wordnet as wn
import re
from multiprocessing import Pool
import argparse
import random
from hearst import *

def g(indexes, sents='mini'):
    BaselineNpChunkRule = ChunkRule(DefaultNpPattern, 'Default rule for NP chunking')
    NpChunker = RegexpChunkParser([BaselineNpChunkRule])
    sentences = eval('nyt_' + sents).tagged_sents()
    for index in indexes:
        parse_tree = NpChunker.parse(sentences[index])
        print(index)
        print("{}\n".format(flattenTree(parse_tree)))

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

def f(string, sents='big'):
    BaselineNpChunkRule = ChunkRule(DefaultNpPattern, 'Default rule for NP chunking')
    NpChunker = RegexpChunkParser([BaselineNpChunkRule])
    sentences = eval('nyt_' + sents).tagged_sents()
    count = 0
    for sent in sentences:
        count += 1
        try:
            parse_tree = NpChunker.parse(sent)
            if string in str(parse_tree):
                print(parse_tree)
                next = raw_input()
                if next.strip() == 'y':
                    pass
                else:
                    return
        except TypeError:
            pass
