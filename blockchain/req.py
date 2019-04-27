import requests
import json
import sys
import random
import time

NODE = ["http://127.0.0.1:5000","http://127.0.0.1:5001","http://127.0.0.1:5002"]
# CHA = ["http://127.0.0.1:6000", "http://127.0.0.1:6001"]
USR = ["1qaz2wsx3edc", "2wsx3edc4rfv", "3edc4rfv5tgb"]
CHR = ["4rfv5tgb6yhn", "5tgb6yhn7ujm"]
user_str = ["Doing the ice bucket challenge! It was freezing cold, but it's for a good cause! Donate to ALS here, the money goes to a really great cause and even a little bit can be a big help! http://www.alsa.org. I dare you to beat my Donation of $%d!",
            "I'm participating in the Ice bucket challenge (http://www.alsa.org)! Can you beat my donation of $%d?"]
user_val = [20,30,50]
charity_str = ["We used $%d to %s!", "With $%d that all of you have donated, we can now %s!"]
charity_val = ["buy lifesaving equipment for multiple families in need", "bring more funding to research in this area"]

def get(base_url, url, params):
    try:
        r= requests.get(url = base_url + url, params = params)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:  # This is the correct syntax
        print(e)
        sys.exit(1)
    return r

def post(base_url, url, data):
    try:
        r = requests.post(url = base_url + url, data=data)
        print("in post, data is {}".format(data))
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:  # This is the correct syntax
        print(e)
        sys.exit(1)
    return r


def chain(url):
    PARAMS = {}
    r = get(url ,"/chain", PARAMS)
    data = r.json()
    return data

def mine(url):
    PARAMS = {}
    r = get(url , "/mine", PARAMS)
    data = r.json()
    return data

def txn(url, sender, recipient, amount, payload=""):
    DATA = {"sender" : str(sender), "recipient" : str(recipient), "amount": int(amount), "payload" : payload}
    r = post(url, "/transactions/new", DATA)
    # print(r)
    data = r.json()
    return data

def register(url, nodes):
    DATA = {"nodes" : nodes}
    print(nodes)
    r = post(url, "/nodes/register", DATA)
    print(r)
    data = r.json()
    return data

def resolve(url):
    PARAMS = {}
    r = get(url, "/nodes/resolve", PARAMS)
    data = r.json()
    return data

# def nodes_register

def decision(probability):
    return random.random() < probability


if __name__ == "__main__":

    register(NODE[0], [NODE[1],NODE[2]])
    register(NODE[1], [NODE[2],NODE[0]])
    register(NODE[2], [NODE[0],NODE[1]])
    while True:
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
        # time.sleep(5)






    # block = chain(URL1)
    # print(block)
    # m = mine(URL1)
    # print(m)
    # t = txn(URL1, "fa636804f3054f84aa0f53dfa031b71b", "some-other-addr", 1, "THIS WAS GENERATED TEXT THAT WE PUT INTO THE BLOCK CHAIN")
    # print(t)
