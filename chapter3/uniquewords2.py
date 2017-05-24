import string
import sys
import collections

words = collections.defaultdict(int)
strip = string.whitespace + string.punctuation + string.digits + "\"'"
for filename in sys.argv[1:]:
    for line in open(filename):
        for word in line.lower().split():
            word = word.strip(strip)
            if len(word) > 2:
                # can not words[word] += 1
                # because this will raise a KeyError exception the first time a new word is encountered
                words[word] += 1
for word in sorted(words):
    print("'{0}' occurs {1} times".format(word, words[word]))
