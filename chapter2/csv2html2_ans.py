import sys
import xml.sax.saxutils


# this is the main method, also the main structure of the thought
# structure: print start; print line; print end
def main():
    maxwidth, format = process_options()  # alternation
    print_start()
    count = 0
    while True:
        try:
            line = input()
            if count == 0:
                color = "lightgreen"
            elif count % 2 == 0:
                color = "white"
            else:
                color = "lightyellow"
            print_line(line, color, maxwidth, format)  # format added
            count += 1
        except EOFError:
            break
    print_end()


def process_options():
    maxwidth_arg = "maxwidth="
    format_arg = "format="
    maxwidth = 100  # default value first, alter later (thought)
    format = "0.f"  # default value, alter later (thought)
    for arg in sys.argv[1:]:
        if arg in ["-h","--help"]:
            print("""\
            usage:
            csv2html2_ans.py [maxwidth=int] [format=str] < infile.csv > outfile.html
            
            maxwidth is an optional integer; if specified, it sets the maximun
            number of characters that can be output for string fields,
            otherwise a default of {0} characters is used.
            
            format is the format to use for numbers; if not specified it defaults to "{1}".
            """.format(maxwidth,format))
            return None,None
        elif arg.startswith(maxwidth_arg):
            try:
                maxwidth = int(arg[len(maxwidth_arg):])
            except ValueError:
                pass
        elif arg.startswith(format_arg):
            format = arg[len(format_arg):]
    return maxwidth,format


def print_start():
    print("<table border='1'>")


def print_line(line, color, maxwidth,format):
    print("<tr bgcolor='{0}'>".format(color))
    numberFormat = "<td align='right'>{{0:{0}}}</td>".format(format)
    fields = extract_fields(line)
    for field in fields:
        if not field:
            print("<td></td>")
        else:
            number = field.replace(",", "")  # 123,456
            try:
                x = float(number)
                # print("<td align='right'>{0:d}</td>".format(round(x)))
                print(numberFormat.format(x))
            except ValueError:
                field = field.title()  # first letter of each word uppercase
                field = field.replace(" And ", " and ")
                #  field width
                if len(field) <= maxwidth:
                    field = xml.sax.saxutils.escape(field)  # escape &,,,and >
                else:
                    field = "{0} ...".format(xml.sax.saxutils.escape(field[:maxwidth]))
                print("<td>{0}</td>".format(field))
    print("</tr>")


def extract_fields(line):
    fields = []
    field = ""  # to hold the field string
    quote = None  # "this is a string"  quote:"
    for c in line:
        if c in "\"'":
            if quote is None:  # start of quoted string
                quote = c
            elif quote == c:  # end of quoted string
                quote = None
            else:
                field += c  # other quote inside quoted string
            continue
        if quote is None and c == ",":  # end of a field
            fields.append(field)
            field = ""
        else:
            field += c  # accumulating a field
    if field:
        fields.append(field)  # adding the last field  # the last field not end with comma(,)
    return fields


def print_end():
    print("</table>")


main()
