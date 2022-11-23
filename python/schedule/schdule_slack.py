import schedule
import time
import requests


def do_nothing():
    answer = input("Hi we are removing those Resources do you approve? ")
    if answer == "yes":
        print(f"Thanks, start deleting" + str({}))
    if answer == "no":
        print("Okay, Thanks for letting us Know")
    schedule.every().day.at("11:33").do(do_nothing)
    while True:
        schedule.run_pending()
        time.sleep(1)


def send_message(message):
    slack_url = "https://hooks.slack.com/services/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"
    payload_obj = '{"text": "%s", "icon_emoji": ":monkey:"}' % message
    response = requests.post(slack_url, payload_obj)
    return response.text


send_message(message=f" :" + str(do_nothing()))
