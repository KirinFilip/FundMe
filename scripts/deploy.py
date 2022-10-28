from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    getAccount,
    deployMocks,
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
)


def deployFundMe():
    account = getAccount()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        priceFeedAddress = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deployMocks()
        priceFeedAddress = MockV3Aggregator[-1].address
    print("Deploying FundMe Contract")
    fundMe = FundMe.deploy(priceFeedAddress, {"from": account})
    return fundMe


def main():
    deployFundMe()
