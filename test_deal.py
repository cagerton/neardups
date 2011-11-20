#!/usr/bin/python

from nltk.text import Text
from nltk.tokenize import word_tokenize
from nltk.tokenize import regexp_tokenize
from nltk.probability import FreqDist
from bitarray import bitarray

from glob import glob

import hashlib


print "hi there"



class SimHasher():

    @staticmethod
    def hashes_for_files(filenames):
        """Returns a map of filenames to sim-hashes"""
        map = {}
        for filename in filenames:
            f = open("test.txt", "r")
            raw_text = f.read()
            f.close
            #


    @staticmethod
    def simhash(raw_text):
        """Compute the simhash value for a string."""
        fdist = FreqDist()
        for word in regexp_tokenize(raw_text, pattern=r'\w+([.,]\w+)*|\S+'):
            fdist.inc(word.lower())

        v = [0] * 128

        for word in fdist:
            projection = bitarray()
            projection.fromstring(hashlib.md5(word).digest())
            #print "\tw:%s, %d" % (word, fdist[word])
            #print "\t\t 128 bit hash: " + str(b)

            for i in xrange(128):
                if projection[i]:
                    v[i] += fdist.get(word)
                else:
                    v[i] -= fdist.get(word)


        hash_val = bitarray(128)

        for i in xrange(128):
            if v[i] > 0:
                hash_val[i] = True
        return hash_val

h = SimHasher.simhash(raw_text)

print "\nAnd the final bitvector for this string is:"
print str(h)


