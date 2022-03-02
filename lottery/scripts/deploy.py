from brownie import Lottery

from scripts.helpers import get_account


def deploy():
    account = get_account()
    result = Lottery.deploy({'from': account})
    print(result)


def main():
    deploy()
