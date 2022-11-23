import requests
import json

slack_token = "https://hooks.slack.com/services/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"
slack_channel = "#yaacov-test"
slack_icon_emoji = ':gun:'
slack_user_name = 'Double Images Monitor'


def post_message_to_slack(text, blocks=None):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': slack_channel,
        'text': text,
        'icon_emoji': slack_icon_emoji,
        'username': slack_user_name,
        'blocks': json.dumps(blocks) if blocks else None
    }).json)
