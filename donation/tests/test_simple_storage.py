import pytest
from brownie import accounts, SimpleStorage, config


@pytest.fixture
def account():
    return accounts[0]


@pytest.fixture()
def contract(account):
    return SimpleStorage.deploy({'from': account})


def test_store_value(contract, account):
    contract.saveData("Hello", {'from': account})
    assert "Hello" == contract.retrieveAt(0)
