from brownie import Collectible

from scripts.deploy import create
from scripts.helpful_scripts import fund_with_link, get_account


def main():
    account = get_account()
    collectible = Collectible[-1]
    fund_with_link(collectible.address, account)
    create(collectible, account)
    print("Collectible created.")
