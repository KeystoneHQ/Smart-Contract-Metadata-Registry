# Contracts Meta Repo
This is a collection of contract data such as names, [contract metadata](https://docs.soliditylang.org/en/v0.8.6/metadata.html) and other data fields.

This repo hopes to collect as much data as possible so offline signers like hardware wallets can use it to decode transactions for a better user-friendly experience.

## Structure
all of the contract metadata is grouped by chain. For each contract, it has a json file with  the contract address as its name.

For each json file, there are these fields:

```
{
    "name": string, // contract name optional
    "address": string, // contract address required
    "metadata":  json, // contract metadata required
    "checkPoints": [] // reserved field optional
}
```
The “Address” and “metadata” are two required fields. The address follows the[EIP 55 address checksum format](https://github.com/ethereum/EIPs/issues/55).

The “metadata” field follows the [contract metadata](https://docs.soliditylang.org/en/v0.8.6/metadata.html)



## Help us improve and Submit Processes
We would like to maintain this repo with the whole community. The pull request will be really helpful either by adding the new contract metadata or modify the existing names or other fields

1. Fork this repository.
2. Do modification.
3. Send the pull request.

Many thanks for the awesome tool https://sourcify.dev/ for providing the current data