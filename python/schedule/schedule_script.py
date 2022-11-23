import schedule
import time


def do_nothing():

    while True:
        schedule.every(5).seconds.do(do_nothing)
        schedule.run_pending()
        time.sleep(5)
        answer = input("Hi we are removing those Resources do you approve? ")
        if answer == "yes":
            print(f"Thanks, start deleting" + str({}))
            break
        if answer == "no":
            print("Okay, Thanks for letting us Know")
        break


do_nothing()