import json
import requests


def block_kit():
    webhook_slack = "https://hooks.slack.com/services/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"

    payload_obj = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Do you approve? \n*"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Approve"
                        },
                        "style": "primary",
                        "value": "click_me_123"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Deny"
                        },
                        "style": "danger",
                        "value": "click_me_123"
                    }
                ]
            }
        ]
    }

    r = requests.post(webhook_slack, json.dumps(payload_obj))
    return r.text


block_kit()

# def send_message(message):
#     slack_url = "https://hooks.slack.com/services/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"
#     payload_obj = '{"text": "%s"}' % message
#     response = requests.post(slack_url, payload_obj)
#     return response
