# Geuss Game

secret_number = 9
guess_count = 0
guess_limit = 3
chances = 2
while guess_count < guess_limit:
    guess = int(input("Guess: "))
    print(f"you have {chances} chances left")
    guess_count += 1
    chances -= 1

    if guess == secret_number:
        print("You won!")
        break
else:
    print("Sorry you have failed")
