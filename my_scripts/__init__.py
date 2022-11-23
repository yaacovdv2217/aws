numbers = [2, 5, 3, 2]

newList = []
sumN = 0
for n in range(0, len(numbers)):
    sumN += numbers[n]
    newList.append(sumN)
print(newList)


new_list = []

for i in range(len(numbers)):
    new_list.append(numbers[i] + sum(numbers[:i]))
print(new_list)
