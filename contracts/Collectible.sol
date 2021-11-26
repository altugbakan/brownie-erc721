// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract Collectible is ERC721URIStorage, VRFConsumerBase {
    event requestedCollectible(bytes32 indexed requestID);
    event breedAssigned(uint256 indexed tokenID, Breed breed);

    mapping(uint256 => Breed) public tokenIDToBreed;
    mapping(bytes32 => address) internal requestIDToSender;

    uint256 public tokenCounter;
    bytes32 internal keyhash;
    uint256 internal fee;

    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    ) VRFConsumerBase(_vrfCoordinator, _linkToken) ERC721("Doggies", "DOG") {
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestID = requestRandomness(keyhash, fee);
        requestIDToSender[requestID] = msg.sender;
        emit requestedCollectible(requestID);
        return requestID;
    }

    function fulfillRandomness(bytes32 _requestID, uint256 _randomNumber)
        internal
        override
    {
        Breed breed = Breed(_randomNumber % 3);
        tokenIDToBreed[tokenCounter] = breed;
        emit breedAssigned(tokenCounter, breed);
        _safeMint(requestIDToSender[_requestID], tokenCounter);
        tokenCounter++;
    }

    function setTokenURI(uint256 _tokenID, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), _tokenID),
            "ERC721: caller is not owner nor approved"
        );
        _setTokenURI(_tokenID, _tokenURI);
    }
}
