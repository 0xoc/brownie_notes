from brownie import SimpleStorage, Donation, network, config

from scripts.dev_utils import get_account, get_price_feed_contract


def deploy_simple_storage():
    account = get_account()
    result = SimpleStorage.deploy({'from': account})
    print("Deploy Result")
    print(result)


def deploy_donation():
    account = get_account()
    print("[DEPLOY] account: ", account)
    active_network = network.show_active()
    price_feed = get_price_feed_contract(account, active_network)
    print("[DEPLOY] price feed: ", price_feed)
    publish_source = config.get('networks').get(active_network).get('verify')
    return Donation.deploy(price_feed, {'from': account}, publish_source=publish_source)


def main():
    deploy_donation()
