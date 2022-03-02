from scripts.helpers import get_account
from scripts.deploy import deploy
import pytest
from brownie.exceptions import VirtualMachineError

@pytest.fixture()
def contract():
    return deploy()

@pytest.fixture()
def account():
    return get_account()

def test_start_lottery_by_owner_should_pass(contract, account):
    contract.startLottery({'from': account})

def test_start_lottery_twice_should_fail(contract, account):
    contract.startLottery({'from': account})
    
    with pytest.raises(VirtualMachineError):
        contract.startLottery({'from': account})
    
def test_start_lottery_not_owner_should_fail(contract):
    account = get_account(1)
    with pytest.raises(VirtualMachineError):
        contract.startLottery({'from': account})
    