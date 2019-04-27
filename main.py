# from geth import DevGethProcess
#
# geth = DevGethProcess('testing') #set second arg to another dir if needed
# geth.start()
#
# print(geth.rpc_port)
# print(geth.accounts)


import time
from web3 import Web3,  HTTPProvider

class user(object):
    """docstring for user."""

    def __init__(self, pub, pri):
        super(user, self).__init__()
        self.pub = pub
        self.pri = pri



user1pub = "0xb9bF03dE1115B0197caD3085f76f97295C2e6B49"
user1pri = "4A3890A5C332B9653D70D7F8AEDD5BB0E35B75BED34D9262FA90E51F0F1EE05B"
user1 = user(user1pub, user1pri)
user2pub = "0xed44353540d85EfD8350bbDdf531655CB845AA18"
user2pri = "FBB7FBD077FE3BD2DE7D230DC13B0E935514BE6FC9A1CAF54423360620E1278B"
user2 = user(user2pub, user2pri)
acc1pub = "0x94E8D0113ada765473A4F01b100aC5193f1B6756"
acc1pri = "8A405DD3F966B4E6E3E64E3BD6A3804D0F9083D18F3B927386C6C34937EFC71E"
acc1 = user(acc1pub, acc1pri)

w3 = Web3(HTTPProvider("https://mainnet.infura.io/v3/a4a175e2abed49449a2bcd819e57fc56"))
# w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/a4a175e2abed49449a2bcd819e57fc56"))
w3.eth.enable_unaudited_features()

print(w3.eth.blockNumber)
w3_last_block = w3.eth.getBlock('latest')
w3_prev_tran = w3_last_block['transactions'][0]
print("the first transaction is " + str(w3_prev_tran))
print(w3.eth.getTransaction(w3_prev_tran))

print(w3_last_block)

print(w3.eth.coinbase)

# user1 = w3.eth.account.create('user1')
# print("addr: {}, private key: {}.".format(user1.address, user1.privateKey.hex()))
signed_txn = w3.eth.account.signTransaction(
    dict(
        nonce=w3.eth.getTransactionCount(w3.eth.coinbase),
        gasPrice=w3.eth.gasPrice,
        gas=100000,
        to=user2.pub,
        value=1,
        data=b'',
    ),
    user1.pri
)

print(w3.eth.sendRawTransaction( signed_txn.rawTransaction))

print("attempt to facilitate transaction between two users.")
print("w3:")
print(w3.eth.accounts)

tran = w3.eth.sendTransaction(
    {"from": w3.eth.accounts[0],
    "to": w3.eth.accounts[0],
    "value": 10}
)
print(tran)
