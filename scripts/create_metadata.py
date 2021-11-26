from brownie import Collectible, network
import os
import json
import requests

from metadata.sample_metadata import metadata_template
from scripts.helpful_scripts import get_breed

IPFS_ENDPOINT_URL = "http://127.0.0.1:5001/api/v0/add"
PINATA_PIN_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"


def upload_to_pinata(file_path):
    file_name = file_path.split("/")[-1]
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }
    with open(file_path, "rb") as f:
        response = requests.post(
            PINATA_PIN_URL, files={"file": (file_name, f.read())}, headers=headers
        )
        return f"ipfs://{response.json()['IpfsHash']}"


def upload_to_ipfs(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(IPFS_ENDPOINT_URL, files={"file": f.read()})
        return f"ipfs://{response.json()['Hash']}"


def save_index(token_id, json_uri):
    uri_list_file_name = f"./metadata/{network.show_active()}/uri_list.json"
    if os.path.exists(uri_list_file_name):
        with open(uri_list_file_name, "r") as f:
            uri_list = json.load(f)
        uri_list[token_id] = json_uri
    else:
        uri_list = {token_id: json_uri}
    with open(uri_list_file_name, "w") as f:
        json.dump(uri_list, f)


def create_metadata(token_id, breed):
    metadata_file_name = f"./metadata/{network.show_active()}/{token_id}.json"
    token_metadata = metadata_template
    token_metadata["name"] = breed
    token_metadata["description"] = f"An adorable {breed.replace('_', ' ')} pup!"
    image_uri = upload_to_ipfs(f"./img/{breed.lower().replace('_', '-')}.png")
    token_metadata["image"] = image_uri
    with open(metadata_file_name, "w") as f:
        json.dump(token_metadata, f)
    json_uri = upload_to_ipfs(metadata_file_name)
    save_index(token_id, json_uri)
    return json_uri


def get_uri(token_id, breed):
    uri_list_file_name = f"./metadata/{network.show_active()}/uri_list.json"
    if not os.path.exists(uri_list_file_name):
        return create_metadata(token_id, breed)
    with open(uri_list_file_name, "r") as f:
        uri_list = json.load(f)
    if str(token_id) in uri_list.keys():
        return uri_list[str(token_id)]
    else:
        return create_metadata(token_id, breed)


def main():
    collectible = Collectible[-1]
    for token_id in range(collectible.tokenCounter()):
        breed = get_breed(collectible.tokenIDToBreed(token_id))
        json_uri = get_uri(token_id, breed)
        print(f"Metadata URI: {json_uri}")
