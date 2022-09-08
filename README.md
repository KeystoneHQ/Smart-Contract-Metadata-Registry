#  Smart Contract Metadata Registry

## Introduction

### Mission
This repo collects **cross-chain** smart contract ABIs to protect the Web3 community against [phishing attacks](https://coinmarketcap.com/alexandria/article/phishing-attack-hits-two-major-defi-protocols-users-told-to-stay-away) targeting average Web3 users and sophisticated [remote attacks](https://medium.com/@hugh_karp/nxm-hack-update-72c5c017b48) on whales.

### Motivation
Ethereum and other blockchain decentralized networks are trying to rebuild trust through trustless computational systems. One of the most important mantras in the blockchain community is “Don’t trust. Verify!”.

To apply this mantra to signing a normal transaction on a software or hardware wallet, the user needs to fully verify at least the amount of crypto, destination address (sometimes change address with UTXO model blockchains) and transaction fees. Otherwise an attacker can perform a [ransom attack](https://thecharlatan.ch/Ransom-Coldcard/) to steal crypto assets without gaining access to the user’s recovery phrase (seed) or private keys.
With the booming of Tokenization in 2017 and DeFi projects in 2020, blockchain transactions have become much more complex than just sending coins on mainnet. Transactions that are interacting with smart contracts require software and hardware wallets to be able to do ABI decoding to avoid [blind signing](https://blog.keyst.one/blind-signing-a-security-black-hole-for-the-ethereum-community-13f909b848b6).

This repo is a community effort to collect ABIs to protect users against [phishing attacks](https://coinmarketcap.com/alexandria/article/phishing-attack-hits-two-major-defi-protocols-users-told-to-stay-away) and sophisticated [remote attacks](https://medium.com/@hugh_karp/nxm-hack-update-72c5c017b48). Any software and hardware wallets can use the data in this repo to decode corresponding smart contracts to enhance signing security for the Web3 community.

## Structure
The repo is a collection of contract data such as names, [contract metadata](https://docs.soliditylang.org/en/v0.8.6/metadata.html) and other data fields.

All of the [contract metadata](https://docs.soliditylang.org/en/v0.8.6/metadata.html) is grouped by chain. For each contract, it has a json file with  the contract address as its name.

For each json file, there are these fields:

```
{
    "name": string, // contract name optional
    "chainId": number, // for evm chain, this is the chainId of the deployed chain.
    "address": string, // contract address required
    "metadata":  json, // contract metadata required
    "version": number // contract version number required
    "checkPoints": [], // reserved field optional
    "isProxy": boolean, // whether this is an proxy contract which follows [EIP-1967](https://eips.ethereum.org/EIPS/eip-1967) optional
    "principalAddress": the principal contract address if this is an proxy contract optinal.
}
```
The “Address” and “metadata” are two required fields. The address follows the [EIP 55 address checksum format](https://github.com/ethereum/EIPs/issues/55).

The “metadata” field follows the [contract metadata](https://docs.soliditylang.org/en/v0.8.6/metadata.html).The output field in the metadata are required which should including the abi, userdoc and devdoc three fields. 

```
{
  ....
  // Required: Generated information about the contract.
  output:
  {
    // Required: ABI definition of the contract
    abi: [ ... ],
    // Required: NatSpec user documentation of the contract
    userdoc: [ ... ],
    // Required: NatSpec developer documentation of the contract
    devdoc: [ ... ],
  }
}

```

### Proxy Contract
For proxy contract which follows the EIP-1967, please fill the abi of your origin contract instead of the proxy contract and set the `isProxy` field to `true` and set the your origin contract address to the `principalAddress` field.

## Contributors
- <img src="https://www.sushi.com/_next/static/media/logo.d019d88b.png" width="20"/> [sushiswap](https://www.sushi.com/) by [LufyCZ](https://github.com/LufyCZ)
- <img src="https://pancakeswap.finance/images/tokens/0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82.png" width="20"/> [pancakeswap](https://pancakeswap.finance/) by [Chef-Cheems](https://github.com/Chef-Cheems) 




## Wallet Supports Transaction ABI Decoding
- [Keystone Hardware Wallet](https://support.keyst.one/advanced-features/decode-defi-transactions)

- [MetaMask](https://metamask.zendesk.com/hc/en-us/articles/4412543412123)

- [Rabby Wallet](https://medium.com/@rabby_io/rabby-release-announcement-564406988e2b)  

## Related Solutions & Resources
- [MetaMask Transaction Insight](https://metamask.zendesk.com/hc/en-us/articles/4412543412123) 

- [Sourcify](https://sourcify.dev/) (Ethereum Only)

## License
MIT
