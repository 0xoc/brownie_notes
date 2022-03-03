import brownie
from scripts.helpers import get_account, get_contract
from scripts.deploy import deploy
import pytest
from brownie.exceptions import VirtualMachineError
from brownie import interface


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

    with brownie.reverts():
        contract.startLottery(
            {"from": account, "gas_limit": 50000, "allow_revert": True}
        )


def test_start_lottery_not_owner_should_fail(contract):
    account = get_account(1)
    with brownie.reverts():
        contract.startLottery({"from": account, "gasLimit": 50000})


def test_get_entrance_min_amount_eth_should_pass(contract):
    min_amount = contract.getEntryMinEth()
    assert min_amount > 0


def test_bet_more_than_min_eth_should_pass(contract, account):
    min_amount = contract.getEntryMinEth()
    contract.startLottery({"from": account})
    contract.bet({"from": account, "value": min_amount})

    participant = contract.participants.call(0)
    weight = contract.participantWeight.call(participant)

    assert participant == account
    assert weight == min_amount


def test_bet_not_started_game_should_fail(contract, account):
    min_amount = contract.getEntryMinEth()
    with brownie.reverts():
        contract.bet({"from": account, "value": min_amount, "gasLimit": 50000})


def test_bet_under_min_eth_should_fail(contract, account):
    contract.startLottery({"from": account})
    with brownie.reverts():
        contract.bet({"from": account, "value": 1, "gasLimit": 50000})


def test_end_game_not_started_should_fail(contract, account):
    with brownie.reverts():
        contract.endLottery({"from": account, "gasLimit": 50000})


def test_end_game_not_owner_should_fail(contract, account):
    contract.startLottery({"from": account})
    other = get_account(1)
    with brownie.reverts():
        contract.endLottery({"from": other, "gasLimit": 50000})


# def test_get_random_number(contract, account):
#     link = get_contract("link_token")
#     link.transfer(contract.address, 0.1 * 10**18, {"from": account})
#     tx = contract.getRandomNumber({"from": account})
#     tx.wait(2)
#     assert contract.randomResult.call() != 0
