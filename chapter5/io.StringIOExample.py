# two ways of writing text to files:
# 1. a file object's write() method
# 2. print() function
import sys
import io

print("An error message", file=sys.stdout)
sys.stdout.write("Another error message\n")

sys.stdout = io.StringIO
#  sys.stdout = sys.__stdout__
#  sys.stdout.getvalue()
