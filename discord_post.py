import requests
import json

def post(token, channel, data):
    res = requests.post(
        f"https://discordapp.com/api/channels/{channel}/messages",
        json.dumps({'content' : data }),
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        },
    )
    res=res.json()    
    # print(res)
    return res['id']

def delete(token, channel, message):
    res = requests.delete(
        f"https://discordapp.com/api/channels/{channel}/messages/{message}",
        headers={
            "Authorization": f"Bot {token}"
        },
    )
    print(res.text)

def update(token, channel, message, data):
    res = requests.patch(
        f"https://discordapp.com/api/channels/{channel}/messages/{message}",
        json.dumps({'content' : data }),
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        },
    )
    print(res)

# embed = {
#     "name": "",
#     "value": "",
#     "inline": false,
# }
def post_embed(token, channel, embed):
    res = requests.post(
        f"https://discordapp.com/api/channels/{channel}/messages",
        json.dumps({'payload' : embed }),
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        },
    )
    res=res.json()    
    return res['id']