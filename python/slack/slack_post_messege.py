import os
from slack import WebClient
from slack.errors import SlackApiError

# ID of channel you want to post message to
SLACK_API_TOKEN = 'TXFocsqowoV0aElXRCdf21k7'
channel_id = "C044SDYMZ6X"
client = WebClient(token=os.environ['SLACK_API_TOKEN'])
try:
    # Call the conversations.list method using the WebClient
    result = client.chat_postMessage(
        channel=channel_id,
        text="Hello world!"
        # You could also use a blocks[] array to send richer content
    )
    # Print result, which includes information about the message (like TS)
    print(result)

except SlackApiError as e:
    print(f"Error: {e}")
