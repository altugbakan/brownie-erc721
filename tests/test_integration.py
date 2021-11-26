from brownie import network, config
import pytest
import time

from scripts.deploy import deploy, create
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
)


def test_can_create_collectible_integration():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    account = get_account()
    collectible = deploy(account)
    fund_with_link(
        collectible, account, config["networks"][network.show_active()]["fee"]
    )

    # Act
    create(collectible, account)
    time.sleep(600)

    # Assert
    assert collectible.tokenCounter() == 1
