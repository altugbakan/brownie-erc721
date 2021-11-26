from brownie import network, config
import pytest
import random

from scripts.deploy import deploy, create
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
    get_contract,
)


def test_can_create_collectible_unit():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    collectible = deploy(account)
    fund_with_link(
        collectible, account, config["networks"][network.show_active()]["fee"]
    )
    random_number = random.randrange(0, 100)

    # Act
    created_collectible = create(collectible, account)
    requestID = created_collectible.events["requestedCollectible"]["requestID"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestID, random_number, collectible.address, {"from": account}
    )

    # Assert
    assert collectible.tokenCounter() == 1
    assert collectible.tokenIDToBreed(0) == random_number % 3
