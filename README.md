# LangChain x402 Payment Agent 🤖

A Python-based AI agent that implements the x402 payment protocol using macaroon authentication tokens to access protected API endpoints on the Ethereum Sepolia testnet.

## What This Does

This agent demonstrates a complete machine-to-machine payment flow:

1. **Checks wallet balance** on Sepolia testnet
2. **Fetches live blockchain data** via Alchemy RPC
3. **Attempts API access** → receives HTTP 402 Payment Required
4. **Makes stablecoin payment** (0.001 USDC simulation)
5. **Receives macaroon token** with caveats (time, method, endpoint)
6. **Accesses protected API** using the macaroon

## Concepts Implemented

- **x402 Protocol** — HTTP 402-based machine-to-machine payment flow
- **Macaroons** — Cryptographic authentication tokens with caveats
- **ERC-8004** — Agent identity via Ethereum wallet address
- **LangChain + Web3** — AI agent equipped with blockchain wallet

## Setup

```bash
pip install langchain langchain-community web3 requests
```

## Run

```bash
python3 agent.py
```

## Example Output
🤖 LangChain x402 Payment Agent
Agent Address: 0x68980cec476eCCb1cf8Cd23D8Fa4cB93Bb9f5311
📊 Step 1: Checking wallet balance...
Agent wallet balance: 0.0958 ETH
⛓️  Step 2: Fetching blockchain state...
Latest block: #11228210
🌐 Step 3: Attempting API access without payment...
Status: 402 - Payment Required
Payment required: 0.001 USDC
💳 Step 4: Agent making x402 payment...
Payment ID: PAY_1783499418
🍪 Step 5: Receiving macaroon authentication token...
Caveats: ['time < 1783503018', 'method = GET', 'endpoint = /api/data']
✅ Step 6: Accessing API with macaroon...
Status: 200
Content: 🔐 Secret API data: ETH price = $1,579.56
🎉 x402 Payment Flow Complete!

## Tech Stack

- **Python 3** — Core language
- **Web3.py** — Ethereum blockchain interaction
- **LangChain** — Agent framework
- **Alchemy** — Sepolia RPC provider
- **Sepolia Testnet** — Ethereum test network

## Agent Wallet
