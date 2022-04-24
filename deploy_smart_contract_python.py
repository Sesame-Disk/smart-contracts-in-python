from web3 import Web3
import os
from solc import compile_standard, install_solc
from dotenv import load_dotenv
import json

load_dotenv()

with open("SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("v0.4.11")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
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
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]
# set up connection
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x22d9529aa7b67b2738d4B082Bf4074758D04b0ff"
private_key = os.getenv("PRIVATE_KEY")
# initialize contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(my_address)
# set up transaction from constructor which executes when firstly
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
signed_tx = w3.eth.account.signTransaction(transaction, private_key=private_key)
tx_hash = w3.eth.account.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# calling functinos in contract block
# to work with a contract, you need abi and address

storage_sol = w3.eth.contract(abi=abi, address=tx_receipt.contractAddress)
call_fun = storage_sol.functions.store(5).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
sign_call_fun = w3.eth.account.signTransaction(call_fun, private_key=private_key)
tx_call_fun_hash = w3.eth.send_raw_transaction(sign_call_fun.rawTransaction)
tx_call_fun_receipt = w3.eth.wait_for_transaction_receipt(tx_call_fun_hash)

print(storage_sol.functions.retrieve().call())
