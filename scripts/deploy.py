from brownie import Collectible, network, config

from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
    get_contract,
    get_opensea_uri,
)


def deploy(account=get_account()):
    return Collectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )


def create(collectible, account=get_account()):
    tx = collectible.createCollectible({"from": account})
    tx.wait(1)
    return tx


def main():
    account = get_account()

    # Deploy the NFT contract
    print("Deploying NFT contract...")
    collectible = deploy(account)
    print("Deployed.")

    # Fund the NFT contract with LINK
    print("Funding contract with LINK...")
    fund_with_link(
        collectible.address, account, config["networks"][network.show_active()]["fee"]
    )
    print("Funded.")

    # Mint an NFT
    print("Minting an NFT...")
    create(collectible, account)
    print("Minted.")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(
            f"You can view your NFT at {get_opensea_uri(collectible.address, collectible.tokenCounter())}"
        )
