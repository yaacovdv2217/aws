def find_max(numbers):
    maximum = numbers[0]
    for number in numbers:
        if number > maximum:
            maximum = number
    return maximum


numbers = [3, 5, 7, 10]
print(max(numbers))
