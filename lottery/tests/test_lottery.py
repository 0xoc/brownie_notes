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
    contract.startLottery({"from": account})


def test_start_lottery_twice_should_fail(contract, account):
    contract.startLottery({"from": account})

    with pytest.raises(VirtualMachineError):
        contract.startLottery({"from": account})


def test_start_lottery_not_owner_should_fail(contract):
    account = get_account(1)
    with pytest.raises(VirtualMachineError):
        contract.startLottery({"from": account})


def test_get_entrance_min_amount_eth_should_pass(contract):
    min_amount = contract.getEntryMinEth()
    assert min_amount > 0


def test_bet_more_than_min_eth_should_pass(contract, account):
    min_amount = contract.getEntryMinEth()
    contract.startLottery({"from": account})
    contract.bet({"from": account, "value": min_amount})
    contract.bet({"from": account, "value": 2 * min_amount})

    participant = contract.participants.call(0)
    participant2 = contract.participants.call(1)
    weight = contract.participantWeight.call(participant)

    assert participant == participant2
    assert participant == account
    assert weight == 3 * min_amount


def test_bet_not_started_game_should_fail(contract, account):
    min_amount = contract.getEntryMinEth()
    with pytest.raises(VirtualMachineError):
        contract.bet({"from": account, "value": min_amount})


def test_bet_under_min_eth_should_fail(contract, account):
    contract.startLottery({"from": account})
    with pytest.raises(VirtualMachineError):
        contract.bet({"from": account, "value": 1000})
