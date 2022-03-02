from brownie import (
    Lottery,
    config,
    network,
)
import os
from scripts.helpers import get_account, get_contract


def deploy():
    account = get_account()
    active_network = network.show_active()
    network_settings = config["networks"][active_network]

    # get contracts
    price_feed = get_contract("price_feed_address")
    vrf_coordinator = get_contract("vrf_coordinator")
    link_token = get_contract("link_token")

    key_hash = network_settings["key_hash"]
    vrf_fee = network_settings["vrf_fee"]

    result = Lottery.deploy(
        price_feed.address,
        vrf_coordinator.address,
        link_token.address,
        key_hash,
        vrf_fee,
        {"from": account},
    )
    return result


def main():
    deploy()
