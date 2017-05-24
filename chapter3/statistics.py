import sys
import collections
import math

Statistics = collections.namedtuple("Statistics", "mean mode median std_dev")


def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} file1 [file2 [... fileN]]".format(sys.argv[0]))
        sys.exit()

    numbers = []  # to hold all the numbers
    frequencies = collections.defaultdict(int)  # default value int()
    for filename in sys.argv[1:]:
        read_data(filename, numbers, frequencies)
    if numbers:
        statistics = calculate_statistics(numbers, frequencies)
        print_results(len(numbers), statistics)
    else:
        print("no numbers found")


# update numbers and frequencies
def read_data(filename, numbers, frequencies):
    for lino, line in enumerate(open(filename, encoding="ascii"), start=1):  # lino: line no.
        for x in line.split():  # split lines on whitespace
            try:
                number = float(x)
                numbers.append(number)
                frequencies[number] += 1
            except ValueError as err:
                print("{filename}:{lino}: skipping {x}: {err}".format(**locals()))  # mapping unpacking


def calculate_statistics(numbers, frequencies):
    mean = sum(numbers) / len(numbers)
    mode = calculate_mode(frequencies, 3)  # to do optimization
    median = calculate_median(numbers)
    std_dev = calculate_std_dev(numbers, mean)
    return Statistics(mean, mode, median, std_dev)


def calculate_mode(frequencies, maximum_modes):
    highest_frequency = max(frequencies.values())
    mode = [number for number, frequency in frequencies.items() if frequency == highest_frequency]
    if not (1 <= len(mode) <= maximum_modes):
        mode = None
    else:
        mode.sort()
    return mode


def calculate_median(numbers):
    numbers = sorted(numbers)
    middle = len(numbers) // 2
    median = numbers[middle]  # start from zero
    if len(numbers) % 2 == 0:
        median = (median + numbers[middle - 1]) / 2
    return median


#      ------------------------------
#     | square{ sigma[ x-mean(x) ] }
#    |-------------------------------
#  \|             n -1
def calculate_std_dev(numbers, mean):
    total = 0
    for number in numbers:
        total += ((number - mean) ** 2)
        variance = total / (len(numbers) - 1)
        return math.sqrt(variance)


def print_results(count, statistics):
    real = "9.2f"

    if statistics.mode is None:
        modeline = ""
    elif len(statistics.mode) == 1:
        # 9.2f : width=9, precision=2, type=float
        modeline = "mode     ={0:{fmt}}\n".format(statistics.mode[0], fmt=real)
    else:
        modeline = ("mode     =[" + ", ".join(["{0:.2f}".format(m) for m in statistics.mode]) + "]\n")

    # count: width=6
    print("""\
    count    ={0:6} 
    mean     ={mean:{fmt}}
    median   ={median:{fmt}}
    {1}\
    std.dev. = {std_dev:{fmt}}""".format(count, modeline, fmt=real, **statistics._asdict()))


main()


# content of numbers.txt
# 1 2 2 2 3 4 5
# 1 2 3 4 0 1 22 11 22
# 11 22 11 21 23 23
# 1 3 3


# output
# count     = 25
# mean      = 8.12
# median    = 3.00
# mode      = [1.00, 2.00, 3.00]
# std.dev.   = 1.45
