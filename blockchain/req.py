import requests
import json
import sys
import random
import time


# facebook apis
HOST = "https://graph.facebook.com"
APP_ID = "424918614950476"

APP_PERMISSION = [
    "EAAGCdhMaQkwBAJflwzOZC5ZBCU0JgEbh00ovPMOSn3dQthodb6XJWCC3E0KRUb5ipQ1ZCtQQ3ZCeHlFwxZBRMtTTvttkdsABmzTMMl0gnhv4FAhPxNQvuZCjuEtoPmIMGNkSU0i2vdxB2E2fkel2mW9D5nq8FBUszSVUGYWZCGNDL5Dk3ZApHf0T0Ahku0oY6kHZBwtcECLA8L7JjZCBTtizpZA",
    "EAAGCdhMaQkwBAJjgnTKERAW4oCwyZCTpPsVphatekBt9jxqiY8Mb8vchHddC4wPrkgkon1b2cw7HqYT8RI7t7ZBAZAWXB2kefqTeZC2FxZBGrnr9JyZC5ZAEXolVPH2KEOShftlYxGRow93IGZCY3l42AaCHJyGeQbMp9PxFeyRwhaSh9q1uHi1zZB1wmlHhnDv9VSV0ZALNmFq8pZBxDmMRabC",
    "EAAGCdhMaQkwBAKqJmYu2cdFtWzt2sr7ZCb4YKKsUXomivWtijkyhjQ2ebQE4VWwo2yOCiqbIQ8MS2CXKaioZCrE6vKKTIarsBJzNIFVJr6C3CANR3VOOUxU2eswHnChSCukJVjkHeZBP8NH7yL2Pk6TetGA2byzJadTElVKPkTG2w1N3sUks2oz1Xi2Ins8ShgJwqAjb4Lz80sh8PcA"
]

# constants
NODE = ["http://127.0.0.1:5000","http://127.0.0.1:5001","http://127.0.0.1:5002"]
# CHA = ["http://127.0.0.1:6000", "http://127.0.0.1:6001"]
# user ids in the blockchain
USR = ["1qaz2wsx3edc", "2wsx3edc4rfv", "3edc4rfv5tgb"]
CHR = ["4rfv5tgb6yhn"] #, "5tgb6yhn7ujm"]
# parsing of blockchain into readible text
user_str = ["Doing the ice bucket challenge! It was freezing cold, but it's for a good cause! Donate to ALS here, the money goes to a really great cause and even a little bit can be a big help! http://www.alsa.org. I dare you to beat my Donation of $%d!",
            "I'm participating in the Ice bucket challenge (http://www.alsa.org)! Can you beat my donation of $%d?"]
user_val = [20,30,50]
charity_str = ["We used $%d to %s!", "With $%d that all of you have donated, we can now %s!"]
charity_val = ["buy lifesaving equipment for multiple families in need", "bring more funding to research in this area"]

# generic get HTML
def get(base_url, url, params):
    try:
        r= requests.get(url = base_url + url, params = params)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:  # This is the correct syntax
        print(e)
        sys.exit(1)
    return r

# generic post HTML
def post(base_url, url, data):
    try:
        r = requests.post(url = base_url + url, data=data)
        print("in post, data is {}".format(data))
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:  # This is the correct syntax
        print(e)
        sys.exit(1)
    return r

# show the chain
def chain(url):
    PARAMS = {}
    r = get(url ,"/chain", PARAMS)
    data = r.json()
    return data

# mine the blockchain
def mine(url):
    PARAMS = {}
    r = get(url , "/mine", PARAMS)
    data = r.json()
    return data

# make a transaction
def txn(url, sender, recipient, amount, payload=""):
    DATA = {"sender" : str(sender), "recipient" : str(recipient), "amount": int(amount), "payload" : payload}
    r = post(url, "/transactions/new", DATA)
    # print(r)
    data = r.json()
    return data

# register nodes
def register(url, nodes):
    DATA = {"nodes" : nodes}
    print(nodes)
    r = post(url, "/nodes/register", DATA)
    print(r)
    data = r.json()
    return data

# resolve consensus
def resolve(url):
    PARAMS = {}
    r = get(url, "/nodes/resolve", PARAMS)
    data = r.json()
    return data

# decision for probability, return True if probability
def decision(probability):
    return random.random() < probability

# facebook api not really working, Dont know where to put the token
def get_app_per(permissions):
    PARAMS = {}
    r = get(HOST, "/v3.2/" + APP_ID + "/accounts/test-users", PARAMS)
    data = r.json()
    return data


if __name__ == "__main__":

    #register the nodes
    register(NODE[0], [NODE[1],NODE[2]])
    register(NODE[1], [NODE[2],NODE[0]])
    register(NODE[2], [NODE[0],NODE[1]])
    while True:
        # iterate through each node
        for node in NODE:
            mine(node)
            resolve(node)
            if decision(0.7):
                # Donation
                donation = random.randint(20,50)
                data = random.choice(user_str)
                txn(node, random.choice(USR), random.choice(CHR), donation, data % donation)
                mine(node)
                chain(node)
            else:
                # charity
                charity = random.randint(40,100)
                char_val = random.choice(charity_val)
                char_str = random.choice(charity_str)
                data = char_str % (charity, char_val)
                txn(node, random.choice(CHR), 0, charity, data)
                mine(node)
                chain(node)
            # post to facebook

            # sleep for simulation
            time.sleep(random.randint(20,60))
    # get_app_per()
