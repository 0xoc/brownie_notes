from brownie import (
    accounts,
    network,
    MockV3Aggregator,
    LinkToken,
    VRFCoordinatorMock,
    Contract,
    config,
)


FORKS = [
    "mainnet-fork",
]

DEVELOPMENT = [
    "development",
]


def get_account(index=0):
    print("main key ", config["wallets"]["main"])
    if network.show_active() == "rinkeby":
        accounts.add(config["wallets"]["main"])
        accounts.add(config["wallets"]["second"])
    return accounts[index]


contract_map = {
    "price_feed_address": MockV3Aggregator,
    "link_token": LinkToken,
    "vrf_coordinator": VRFCoordinatorMock,
}


def get_contract(name):
    contract_type = contract_map[name]
    if network.show_active() in DEVELOPMENT:
        if len(contract_type) <= 0:
            deploy_mocks()
        return contract_type[-1]
    else:
        address = config["networks"][network.show_active()][name]
        return Contract.from_abi(contract_type._name, address, contract_type.abi)


def deploy_mocks():
    account = get_account()
    MockV3Aggregator.deploy(8, 3000 * 10**18, {"from": account})
    link = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link, {"from": account})
