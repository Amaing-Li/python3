import sys
import unicodedata


def print_unicode_table(words):
    print("decimal    hex    chr    {0:^40}".format("name"))  # center width=40
    print("-------   -----   ---    {0:-<40}".format(""))  # left alignment width=40

    code = ord(" ")  # unicode order
    end = min(0xD800, sys.maxunicode)

    while code < end:
        c = chr(code)
        name = unicodedata.name(c, "*** unknown ***")  # name or unknown
        ok = True
        for word in words:  # both contain
            if word not in name.lower():
                ok = False
                break
        if ok:
            print("{0:7}  {0:5X}  {0:^3c}  {1}".format(code, name.title()))
        code += 1


words = []  # hold all the command line words
if len(sys.argv) > 1:
    if sys.argv[1] in ("-h", "--help"):
        print("usage: {0} [string1 [string2 [... stringN]]]".format(sys.argv[0]))
        words = None
    else:
        for word in sys.argv[1:]:
            words.append(word.lower())

if words is not None:
    print_unicode_table(words)


# output

# decimal    hex    chr                      name
# -------   -----   ---    ----------------------------------------
#    891    37B   ͻ   Greek Small Reversed Lunate Sigma Symbol
#    892    37C   ͼ   Greek Small Dotted Lunate Sigma Symbol
#    893    37D   ͽ   Greek Small Reversed Dotted Lunate Sigma Symbol
#    975    3CF   Ϗ   Greek Capital Kai Symbol
#    976    3D0   ϐ   Greek Beta Symbol
#    977    3D1   ϑ   Greek Theta Symbol
#    978    3D2   ϒ   Greek Upsilon With Hook Symbol
#    979    3D3   ϓ   Greek Upsilon With Acute And Hook Symbol
#    980    3D4   ϔ   Greek Upsilon With Diaeresis And Hook Symbol
#    981    3D5   ϕ   Greek Phi Symbol
#    982    3D6   ϖ   Greek Pi Symbol
#    983    3D7   ϗ   Greek Kai Symbol
#   1008    3F0   ϰ   Greek Kappa Symbol
#   1009    3F1   ϱ   Greek Rho Symbol
#   1010    3F2   ϲ   Greek Lunate Sigma Symbol
#   1012    3F4   ϴ   Greek Capital Theta Symbol
#   1013    3F5   ϵ   Greek Lunate Epsilon Symbol
#   1014    3F6   ϶   Greek Reversed Lunate Epsilon Symbol
#   1017    3F9   Ϲ   Greek Capital Lunate Sigma Symbol
#   1020    3FC   ϼ   Greek Rho With Stroke Symbol
#   1021    3FD   Ͻ   Greek Capital Reversed Lunate Sigma Symbol
#   1022    3FE   Ͼ   Greek Capital Dotted Lunate Sigma Symbol
#   1023    3FF   Ͽ   Greek Capital Reversed Dotted Lunate Sigma Symbol
