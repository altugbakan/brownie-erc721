from brownie import Collectible

from scripts.create_metadata import get_uri
from scripts.helpful_scripts import get_account, get_breed, get_opensea_uri


def set_token_uri(collectible, token_id, uri, account=get_account()):
    tx = collectible.setTokenURI(token_id, uri, {"from": account})
    tx.wait(1)


def main():
    account = get_account()
    collectible = Collectible[-1]
    for token_id in range(collectible.tokenCounter()):
        breed = get_breed(collectible.tokenIDToBreed(token_id))
        if not collectible.tokenURI(token_id).startswith("ipfs://"):
            print("Setting token URI...")
            set_token_uri(collectible, token_id, get_uri(token_id, breed), account)
            print("Set.")
            print(
                f"You can view your NFT at {get_opensea_uri(collectible.address, token_id)}"
            )
