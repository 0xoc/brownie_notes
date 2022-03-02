from brownie import Lottery, MockV3Aggregator, config, network
import os
from scripts.helpers import get_account


def deploy():
    account = get_account()
    active_network = network.show_active()

    if active_network == "mainnet-fork":
        priceFeedAddress = config.get('networks').get(active_network).get('price_feed_address')
        result = Lottery.deploy(priceFeedAddress, {'from': account})
        return result
    else:
        raise Exception("Only mainnet fork for now")


def main():
    deploy()
