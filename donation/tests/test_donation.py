import pytest
from scripts.deploy import deploy_donation

from scripts.dev_utils import get_account


@pytest.fixture
def account():
    return get_account()


@pytest.fixture()
def contract(account):
    return deploy_donation()


def test_donate(contract, account):
    amount = 4000000000000000
    contract.donate({'from': account, 'value': amount})
    funder_address = contract.funders.call(0)
    funder_amount = contract.fundersAmount.call(funder_address)

    assert funder_address == account
    assert funder_amount == amount

