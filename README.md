# Brownie ERC721

To modify the name and the symbol of your token, open [Collectible.sol](./contracts/Collectible.sol) and change `Doggies` and `DOG` respectively.

You can find the functions about NFT metadata in [create_metadata.py](./scripts/create_metadata.py). A sample metadata can also be found in [sample_metadata.py](./metadata/sample_metadata.py).

You need a local [IPFS](https://ipfs.io/) node to publish your metadata. If you do not want to run a node, you can use [Pinata](https://www.pinata.cloud/) for an IPFS gateway. Functions for publishing to both can be found in [create_metadata.py](./scripts/create_metadata.py) and be used interchangably.