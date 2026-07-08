import os
import json
import time
from web3 import Web3

# ============================================
# MOCK x402 PAYMENT FLOW WITH LANGCHAIN AGENT
# ============================================

# Connect to Sepolia
w3 = Web3(Web3.HTTPProvider("https://eth-sepolia.g.alchemy.com/v2/IZYEU2cWBgnFmgiTAgpWD"))

AGENT_ADDRESS = "0x68980cec476eCCb1cf8Cd23D8Fa4cB93Bb9f5311"

# ============================================
# MOCK MACAROON SYSTEM
# ============================================

def generate_macaroon(payment_id, amount, expiry_seconds=3600):
    """Generate a mock macaroon token after payment"""
    import hashlib
    import time
    
    expiry = int(time.time()) + expiry_seconds
    data = f"{payment_id}:{amount}:{expiry}"
    token = hashlib.sha256(data.encode()).hexdigest()
    
    return {
        "token": token,
        "payment_id": payment_id,
        "amount": amount,
        "expiry": expiry,
        "caveats": [
            f"time < {expiry}",
            "method = GET",
            "endpoint = /api/data"
        ]
    }

def verify_macaroon(macaroon):
    """Verify macaroon is valid and not expired"""
    current_time = int(time.time())
    return current_time < macaroon["expiry"]

# ============================================
# MOCK API SERVER
# ============================================

def mock_api_call(endpoint, macaroon=None):
    """Simulate an API that requires x402 payment"""
    if macaroon is None:
        return {
            "status": 402,
            "error": "Payment Required",
            "payment_details": {
                "amount": "0.001 USDC",
                "address": "0xMockAPIWallet",
                "chain": "sepolia"
            }
        }
    
    if not verify_macaroon(macaroon):
        return {"status": 401, "error": "Macaroon expired"}
    
    return {
        "status": 200,
        "data": {
            "message": "Access granted!",
            "content": "🔐 Secret API data: ETH price = $1,579.56",
            "timestamp": int(time.time())
        }
    }

# ============================================
# LANGCHAIN AGENT TOOLS
# ============================================

def check_balance():
    """Tool: Check agent wallet balance"""
    balance_wei = w3.eth.get_balance(AGENT_ADDRESS)
    balance_eth = w3.from_wei(balance_wei, 'ether')
    return f"Agent wallet balance: {balance_eth:.4f} ETH"

def get_block_info():
    """Tool: Get latest block info"""
    block = w3.eth.get_block('latest')
    return f"Latest block: #{block['number']}, timestamp: {block['timestamp']}"

def make_payment(amount_usdc):
    """Tool: Simulate making a stablecoin payment"""
    print(f"   💸 Simulating payment of {amount_usdc} USDC...")
    time.sleep(1)
    payment_id = f"PAY_{int(time.time())}"
    return {
        "success": True,
        "payment_id": payment_id,
        "amount": amount_usdc,
        "tx_hash": f"0x{'mock' * 8}"
    }

# ============================================
# MAIN AGENT FLOW
# ============================================

def run_agent():
    print("🤖 LangChain x402 Payment Agent")
    print("=" * 50)
    print(f"Agent Address: {AGENT_ADDRESS}")
    print()
    
    # Step 1: Check balance
    print("📊 Step 1: Checking wallet balance...")
    balance = check_balance()
    print(f"   {balance}")
    print()
    
    # Step 2: Get blockchain info
    print("⛓️  Step 2: Fetching blockchain state...")
    block_info = get_block_info()
    print(f"   {block_info}")
    print()
    
    # Step 3: Try to access API without payment
    print("🌐 Step 3: Attempting API access without payment...")
    response = mock_api_call("/api/data")
    print(f"   Status: {response['status']} - {response['error']}")
    print(f"   Payment required: {response['payment_details']['amount']}")
    print()
    
    # Step 4: Make payment
    print("💳 Step 4: Agent making x402 payment...")
    payment = make_payment("0.001")
    print(f"   Payment ID: {payment['payment_id']}")
    print(f"   TX Hash: {payment['tx_hash']}")
    print()
    
    # Step 5: Get macaroon
    print("🍪 Step 5: Receiving macaroon authentication token...")
    macaroon = generate_macaroon(payment['payment_id'], payment['amount'])
    print(f"   Token: {macaroon['token'][:32]}...")
    print(f"   Caveats: {macaroon['caveats']}")
    print()
    
    # Step 6: Access API with macaroon
    print("✅ Step 6: Accessing API with macaroon...")
    response = mock_api_call("/api/data", macaroon)
    print(f"   Status: {response['status']}")
    print(f"   Response: {response['data']['message']}")
    print(f"   Content: {response['data']['content']}")
    print()
    
    print("=" * 50)
    print("🎉 x402 Payment Flow Complete!")
    print("Agent successfully paid for and accessed protected API endpoint.")

if __name__ == "__main__":
    run_agent()
