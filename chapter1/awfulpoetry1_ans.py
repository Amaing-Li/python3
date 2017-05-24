# 2017-5-24 limingming
import random

articles = ["the", "a"]
subjects = ["cat", "dog", "man", "woman"]
verbs = ["sang", "ran", "jumped"]
adverbs = ["loudly", "quietly", "well", "badly"]

for i in range(5):
    article = random.choice(articles)
    subject = random.choice(subjects)
    verb = random.choice(verbs)
    adverb = random.choice(adverbs)

    if random.randint(0,1) ==0:
        print(article,subject,verb)
    else:
        print(article,subject,verb,adverb)