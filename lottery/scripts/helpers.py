from brownie import accounts, network


def get_account():
    for accoount in accounts:
        print("Accoutn ", accoount);
    return accounts[0]


