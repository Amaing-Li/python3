# 2017-5-24
# notice: it will not work well in python2.7
numbers = []  # hold all the input numbers
total = 0
lowest = None
highest = None

while True:
    try:
        line = input("enter a number or Enter to finish: ")  # accept data from the console
        if not line:  # no data entered
            break
        number = int(line)
        numbers.append(number)
        total += number
        if lowest is None or lowest > number:
            lowest = number
        if highest is None or highest < number:
            highest = number
    except ValueError as err:
        print(err)

print("numbers: ", numbers)
if numbers:
    print("count =", len(numbers), "sum =", total, "lowest =", lowest, "highest =", highest, "mean =",
          total / len(numbers))
