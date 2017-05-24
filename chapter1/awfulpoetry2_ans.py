# 2017-5-24 limingming
import random
import sys

lines = 5  # default value
if len(sys.argv) > 1:
    try:
        temp = int(sys.argv[1])
        if 1 <= temp <= 10:
            lines = temp
        else:
            print("lines must be 1-10 inclusive")
    except ValueError as err:
        print("usage: awfulpoetry2_ans.py [lines]")

articles = ["the", "a"]
subjects = ["cat", "dog", "man", "woman"]
verbs = ["sang", "ran", "jumped"]
adverbs = ["loudly", "quietly", "well", "badly"]

for _ in range(lines):
    article = random.choice(articles)
    subject = random.choice(subjects)
    verb = random.choice(verbs)
    adverb = random.choice(adverbs)

    if random.randint(0, 1) == 0:
        print(article, subject, verb)
    else:
        print(article, subject, verb, adverb)
