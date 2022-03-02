from brownie import Lottery

from scripts.helpers import get_account


def deploy():
    account = get_account()
    result = Lottery.deploy({'from': account})
    return result


def main():
    deploy()
