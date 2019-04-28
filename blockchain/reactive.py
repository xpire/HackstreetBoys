import requests
import json
import sys
import random
import time
from req import *

if __name__ == "__main__":

    #assumes the blockchain is already running
    # choose any node (say the first one)
    node = NODE[0]
    mine(node)
    resolve(node)

    # Donation
    donation = 8070
    data = "Congratulations AJ McLean, for donating ${} towards an amazing cause {}! Feel free to support the cause and more through this link: {}.".format(donation, "The ALS Ice Bucket Challenge",node)  #TODO
    txn(node, "AJ McLean", CHR[0], donation, data)
    mine(node)
    chain(node)
    # post to facebook
    fbPost(PAGE_ID,data)
    # sleep for simulation
    # time.sleep(random.randint(20,60))
    exit()
    # get_app_per()
