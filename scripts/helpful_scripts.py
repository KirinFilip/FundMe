from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIROMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development", "ganache-local"]


def getAccount(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS
        or network.show_active() in FORKED_LOCAL_ENVIROMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def deployMocks():
    print(f"Active network is {network.show_active()}")
    print("Deploying mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(18, Web3.toWei(2000, "ether"), {"from": getAccount()})
    print("Mocks deployed!")
