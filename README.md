# Contracts Meta Repo
A collection of contract data like names, [contract metadata](https://docs.soliditylang.org/en/v0.8.6/metadata.html) and other data fields.

This repo is hoping to collect data as much as possible, so offline signer like hardware wallets can use this information to decode the transaction to provide user-friendly information as much as possible.

## Structure
all the contract meta data are grouped by chain. and for each contract, it has a json file which is named by contract address.

for each json file there are these fields.

```
{
    "name": string, // contract name optional
    "address": string, // contract address required
    "metadata":  json, // contract metadata required
    "checkPoints": [] // reserved field optional
}
```
The Address and metadata are two required field. the address follow [EIP 55 address checksum format](https://github.com/ethereum/EIPs/issues/55).

the metadata field follow the [contract metadata](https://docs.soliditylang.org/en/v0.8.6/metadata.html)



## Help us improve and Submission Process
We would like to maintain this repo with the whole community. The pull request will be really helpful either adding the new contract metadata or modify the existings like name or other field.

1. Fork this repository.
2. do modification.
3. send the pull request.


Many thanks the awesome tool https://sourcify.dev/ for providing current data