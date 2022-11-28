def emoji_converter(message):
    words = message.split(" ")
    emojis = {
        ":)": "😃",
        ":(": "🙁"
    }
    output = ""
    for word in words:
        output += emojis.get(word, word) + " "
    return output


message = input("> ")
print(emoji_converter(message))

"https://hooks.slack.com/services/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"

"https://hooks.slack.com/services/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"
