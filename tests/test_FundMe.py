import pytest
from brownie import FundMe, network, accounts
from scripts.deploy import deployFundMe
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIROMENTS, getAccount


def test_owner():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    account = getAccount
    fundme = deployFundMe()
    # Act
    # Assert
    assert fundme.i_owner() == accounts[0]


def test_fund():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    account = getAccount
    fundme = deployFundMe()
    # Act
    tx = fundme.fund({"from": account, "value": 500 * 10e18})
    tx.wait(1)
    # Assert
    assert fundme.addressToAmountFunded(account.address) == 500 * 10e18
