from brownie import network, accounts, config, MockV3Aggregator

FORK_CHAINS = ['mainnet-fork-dev', ]
DEV_CHAINS = ['development']


def get_account():
    if network.show_active() in DEV_CHAINS or \
            network.show_active() in FORK_CHAINS:
        print("[ACCOUNT] Using Dev account")
        return accounts[0]
    else:
        print("[ACCOUNT] Using Manual Account")
        return accounts.add(config.get('wallets').get('the_key'))


def get_price_feed_contract(account, active_network):
    if active_network == "development":
        price_feed = MockV3Aggregator.deploy(8, 265000000000, {'from': account})
    else:
        price_feed = config.get('networks').get(active_network).get('price_feed')
    return price_feed
