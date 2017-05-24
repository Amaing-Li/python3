import random


def get_forenames_and_surnames():
    forenames = []
    surnames = []
    for names, filename in ((forenames, "forenames.txt"), (surnames, "surnames.txt")):
        for name in open(filename, encoding="utf-8"):
            names.append(name.rstrip())
    return forenames, surnames


fornames, surnames = get_forenames_and_surnames()
fh = open("test-names1.txt", "w", encoding="utf-8")

limit = 100
years = list(range(1970, 2013)) * 3
# len(years),len(forenames),len(surnames) should > limit
for year, forename, surname in zip(random.sample(years, limit), random.sample(fornames, limit),
                                   random.sample(surnames, limit)):
    name = "{0} {1}".format(forename, surname)
    fh.write("{0:.<25}.{1}\n".format(name, year))
