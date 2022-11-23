price = 1000000
good_credit = True

if good_credit:
    down_payment = price * 0.1
else:
    down_payment = price * 0.2
print(f"Down Payment is: ${down_payment}")

weight = int(input("weight: "))
unit = input("(L)bs or (K)g: ")
if unit.upper() == "L":
    converted = weight * 0.45
    print(f"you are {converted} kilos")
elif unit.upper() == "K":
    converted = weight / 0.45
    print(f"you are {converted} pounds")
else:
    print("Please add a normal Letter")

