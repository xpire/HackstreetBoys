import requests
import json
import sys
import random
import time
from req.py import *

if __name__ == "__main__":

    #assumes the blockchain is already running
    # choose any node (say the first one)
    node = NODE[0]
    mine(node)
    resolve(node)

    # Donation
    donation = 5000 #TODO
    data = "hello" #TODO
    txn(node, random.choice(USR), random.choice(CHR), donation, data)
    mine(node)
    chain(node)
    # post to facebook

    # sleep for simulation
    time.sleep(random.randint(20,60))
    # get_app_per()
