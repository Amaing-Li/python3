import sys

sites = {}
for filename in sys.argv[1:]:
    for line in open(filename):
        i = 0
        while True:
            site = None
            i = line.find("http://", i)
            if i > -1:
                i += len("http://")
                for j in range(i, len(line)):
                    if not (line[j].isalnum() or line[j] in ".-"):
                        site = line[i:j].lower()
                        break
                if site and "." in site:
                    # can not use sites[site].add(filename),
                    #  because this raise a KeyError exception the first time a new site is encountered
                    sites.setdefault(site, set()).add(filename)
                i = j
            else:
                break

for site in sorted(sites):
    print("{0} is  referred to in:".format(site))
    for filename in sorted(sites[site], key=str.lower):
        print("    {0}".format(filename))
