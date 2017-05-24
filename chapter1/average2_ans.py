# limingming 2017-5-24
numbers = []  # hold all the input numbers
total = 0
lowest = None
highest = None

# indexes = []

while True:
    try:
        line = input("enter a number or Enter to finish: ")  # accept data from the console
        if not line:  # no data entered
            break

        # indexes.append(len(numbers))  # [0,1,2,3...,len(numbers)-1]

        number = int(line)
        numbers.append(number)
        total += number
        if lowest is None or lowest > number:
            lowest = number
        if highest is None or highest < number:
            highest = number
    except ValueError as err:
        print(err)

indexes = range(len(numbers) - 1)

swapped = True
while swapped:
    swapped = False
    for index in indexes:
        if index + 1 == len(numbers):
            break
        if numbers[index] > numbers[index + 1]:
            temp = numbers[index]
            numbers[index] = numbers[index + 1]
            numbers[index + 1] = temp
            swapped = True

if numbers:
    middle = int(len(numbers) / 2)
    median = numbers[middle]
    if len(numbers) % 2 == 0:
        median = (median + numbers[middle - 1]) / 2

print("numbers: ", numbers)
if numbers:
    print("count =", len(numbers), "sum =", total, "lowest =", lowest, "highest =", highest, "mean =",
          total / len(numbers), "median =", median)
