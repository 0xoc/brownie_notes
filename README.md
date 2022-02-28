# brownie_notes

mainnet fork to local ganache-cli
```
brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='https://eth-mainnet.alchemyapi.io/v2/{ID}' accounts=10 mnemonic=brownie port=8585
```