#car game
command = ""
started = False
while True:
    command = input("> ").lower()
    if command == "start":
        if started:
            print("car already started")
        else:
            started = True
            print("Car started...")

    elif command == "stop":
        if not started:
            print("car is already stopped!")
        else:
            started = False
            print("Car Stopped...")

    elif command == "help":
        print(f"""
start - to start the car
stop - to stop the car
quit - to quit
        """)
    elif command == "quit":
        break
    else:
        print("I don't understand that")
