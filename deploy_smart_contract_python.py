import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()


with open(
    "/Users/umar/Downloads/Blockchain_Dev/Python_web_3.0/web3_py_simple_storage/SimpleStorageContract.sol",
    "r",
) as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorageContract.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorageContract.sol"]["SimpleStorage"][
    "evm"
]["bytecode"]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorageContract.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# set up connection
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x9a21D4EaD05B302916D8B2Cd16D2d8CD5bdB0d99"
# private_key = os.getenv("PRIVATE_KEY")
private_key = "0xafb98d224dcc7768934bee92d8b6c330b06ff88a5e12b9cfb629bc30323b6547"
# initialize contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(my_address)
# set up transaction from constructor which executes when firstly
tx = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_tx = w3.eth.account.signTransaction(tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Contract deployed to {tx_receipt.contractAddress}")


# Working with deployed Contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(f"Initial stored value at Retrieve {simple_storage.functions.retrieve().call()}")
new_transaction = simple_storage.functions.store(25).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_new_txn = w3.eth.account.sign_transaction(
    new_transaction, private_key=private_key
)
tx_new_hash = w3.eth.send_raw_transaction(signed_new_txn.rawTransaction)
print("Sending new transaction...")
tx_new_receipt = w3.eth.wait_for_transaction_receipt(tx_new_hash)

print(f"New stored value at Retrieve {simple_storage.functions.retrieve().call()}")
