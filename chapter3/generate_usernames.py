#!/usr/bin/env python3
import sys
import collections

# 1601:Albert:Lukas:Montgomeery:Legal
# 4730:Nadelle::Landale:Warehousing

ID,FORENAME,MIDDLENAME,SURNAME,DEPARTMENT=range(5)
User = collections.namedtuple("User","username forename middlename surname id")

def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} file1 [file2 [... fileN]]".format(sys.argv[0]))
        sys.exit()

    usernames = set()
    users = {} # dictionary
    for filename in sys.argv[1:]:
        for line in open(filename, encoding="utf8"):
            line = line.rstrip()
            if line: # ignore blank lines
                user = process_line(line, usernames)
                users[(user.surname.lower(), user.forename.lower(), user.id)] = user # key-value
    print_users(users)

def process_line(line,usernames):
    fields = line.split(":") # ID,FORENAME,MIDDLENAME,SURNAME,DEPARTMENT=range(5)
    username = generate_username(fields,usernames)
    user = User(username,fields[FORENAME],fields[MIDDLENAME],fields[SURNAME],fields[ID])
    return user

def generate_username(fields,usernames):
    # username = first letter of forename + first letter of middlename + suername
    username = ((fields[FORENAME][0] + fields[MIDDLENAME][:1]+fields[SURNAME]).replace("-","").replace("'",""))
    username = original_name = username[:8].lower()
    count =1
    while username in usernames:
        username="{0}{1}".format(original_name,count) # for the same username, plus 1 to be distinct
        count +=1
    usernames.add(username)
    return username

def print_users(users):
    namewidth = 32
    usernamewidth = 9
    print("{0:<{nw}} {1:^6} {2:{uw}}".format("Name","ID","Username",nw=namewidth,uw=usernamewidth))
    print("{0:-<{nw}} {0:-<6} {0:-<{uw}}".format("",nw=namewidth,uw=usernamewidth))
    for key in sorted(users):
        user = users[key]
        initial = ""
        if user.middlename:
            initial=" "+user.middlename[0]
        name = "{0.surname}, {0.forename}{1}".format(user,initial)
        print("{0:.<{nw}} ({1.id:4}) {1.username:{uw}}".format(name,user,nw=namewidth,uw=usernamewidth))

main()

# output
# Name                               ID   Username
# -------------------------------- ------ ---------
# Landale, Nadelle................ (4730) nlandale
# Li, Amaing M.................... (1234) amli
# Montgomeery, Albert L........... (1601) almontgo

