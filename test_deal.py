#!/usr/bin/python

from nltk.text import Text
from nltk.tokenize import word_tokenize
from nltk.tokenize import regexp_tokenize
from nltk.probability import FreqDist
from bitarray import bitarray
import os
import sys

from glob import glob
import hashlib

do_debug = True
def debug(msg):
  if do_debug:
    sys.stderr.write(msg + "\n")

print "hi there"

class SimHasher():
    """LSH is safe and fun for kids!"""

    def __init__(self):
      self.hashes = {}

    def index_dir(self, dir_name):
        """Tries to check out all the files in a directory"""
        """assumes there are no directories in the directory of interest, only
        text files we want to process."""

        for root, dir, files in os.walk(dir_name):
          self.hashes.update(
              self.get_hashes_for_files( 
                  [os.path.join(root,file) for file in files]))

    def get_hashes(self):
      return self.hashes

    def __str__(self):
      hashes = self.get_hashes()
      return "\n".join(["%s: %s" % (f, hashes[f]) for f in
          hashes.keys()[:20]])

    def is_near_dup(self, new_doc_name, k=3):
      """returns true iff this document has a near duplicate already
      in the corpus used to initialize this simhasher"""

      f = open(new_doc_name)
      this_hash = SimHasher.simhash(f.read())
      f.close()

      for (old_doc_name, other_hash) in self.get_hashes().iteritems():
        c = (this_hash^other_hash).count()
        debug("bits differ %s vs %s: %d" % (new_doc_name, old_doc_name, c))
        if c <= k: 
          return True
      return False
      
    @staticmethod
    def get_hashes_for_files(filenames):
        """Returns a map of filenames to sim-hashes"""
        map = {}
        for filename in filenames:
            f = open(filename, "r")
            raw_text = f.read()
            f.close
            map[filename]=SimHasher.simhash(raw_text)
        return map

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
        hash_val.setall(False)

        for i in xrange(128):
            if v[i] > 0:
                hash_val[i] = True
        return hash_val


#print "\nAnd the final bitvector for this string is:"
#h = SimHasher.simhash(raw_text)
#print str(h)

#---------------------------------------------------------------------

## What we would do to implement this properly: 
#list of files
#simhash for each file
#put first d bits of simhashes in some tables, if len(list of files) is roughly 2^d
#have the tables point to lists that have all the simhashes that start with those d bits
#
#then, for a new document, to see if there are any near duplicates already in the system, we compute the simhash, look up the first D bits in the table to get the list, and see if any simhash in that list matches the simhash of this document, and if any *do*, then we return T, ow F.
#
### What we can do for starters: 
#filenames -> simhashes
#
## Starters 2



