import requests
import json

# Send Slack Message Using Slack Api

message_test = "hellow"


def slack_message(message_text=None, payload_obj=None, slack_url=None):
    if not slack_url:
        slack_url = "https://hooks.slack.com/services/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"
    if not payload_obj and message_text:
        payload_obj = {"text": "\n" + str(message_text) + "\n",
                       "icon_emoji": ":monkey:"}
    requests.post(slack_url, data=json.dumps(payload_obj))
