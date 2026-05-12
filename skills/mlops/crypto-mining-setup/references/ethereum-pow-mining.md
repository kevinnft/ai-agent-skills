# Ethereum PoW Mining (Browser & CLI)

Reference for traditional proof-of-work mining on Ethereum mainnet, covering browser-based mining (WebGPU/WASM) and CLI automation.

## Example: HASH256 Token Mining

**Contract:** 0xAC7b5d06fa1e77D08aea40d46cB7C5923A87A0cc (Ethereum mainnet)
**Website:** https://hash256.org
**Type:** Browser-based keccak256 PoW mining

### Mining Algorithm

```python
# Challenge generation (bound to miner address)
challenge = keccak256(chainId ‖ contract ‖ miner ‖ epoch)

# Solution mining
for nonce in range(max_iterations):
    solution = keccak256(challenge ‖ nonce)
    if solution < difficulty:
        submit_mint(nonce)
        break
```

### Key Properties

1. **Address-bound challenges** — Solutions cannot be stolen from mempool
2. **Epoch rotation** — Every 100 blocks (~20 min), pre-computed solutions expire
3. **Replay protection** — Each (miner, nonce, epoch) tuple mints once
4. **Rate limiting** — Max 10 mints per block
5. **Difficulty adjustment** — Retargets every 2,016 mints (Bitcoin-style)

### CLI Mining Implementation

**Prerequisites:**
```bash
pip install web3 eth-hash[pycryptodome] python-dotenv
```

**Configuration:**
```bash
# .env file
PRIVATE_KEY=your_private_key_here
RPC_URL=https://eth.llamarpc.com
```

**Mining Script Template:**
```python
from web3 import Web3
from eth_hash.auto import keccak

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Get mining parameters
challenge = contract.functions.getCurrentChallenge().call()
difficulty = contract.functions.getCurrentDifficulty().call()
epoch = contract.functions.getCurrentEpoch().call()

# Mine solution
for nonce in range(1000000):
    solution = keccak(challenge + nonce.to_bytes(32, 'big'))
    if int.from_bytes(solution, 'big') < difficulty:
        # Submit to contract
        tx = contract.functions.mint(nonce).build_transaction({...})
        signed = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        break
```

### Contract ABI Extraction

**Method 1: Etherscan API (if verified)**
```python
import requests
url = "https://api.etherscan.io/v2/api"
params = {
    "chainid": 1,
    "module": "contract",
    "action": "getabi",
    "address": contract_address
}
response = requests.get(url, params=params)
abi = response.json()["result"]
```

**Method 2: Reverse Engineer from Frontend**
```bash
# Download mining page
curl -sL https://hash256.org/mine > mine.html

# Extract JavaScript bundles
grep -oP '/_next/static/chunks/[^"]+\.js' mine.html | while read bundle; do
    curl -sL "https://hash256.org${bundle}" > "$(basename $bundle)"
done

# Search for mining logic
grep -r "keccak\|mine\|nonce\|difficulty" *.js
```

**Method 3: Direct Contract Interaction (no ABI)**
```python
# Call contract by function signature
# getCurrentChallenge() -> bytes32
result = w3.eth.call({
    'to': contract_address,
    'data': '0x...'  # keccak256("getCurrentChallenge()")[:4]
})
```

### Profitability Analysis

**Break-even calculation:**
```python
# Costs
gas_units = 100000  # Estimate for mint() call
gas_price_gwei = 30  # Current gas price
eth_price_usd = 3000

gas_cost_eth = (gas_units * gas_price_gwei) / 1e9
gas_cost_usd = gas_cost_eth * eth_price_usd

# Revenue
reward_tokens = 100  # Era 1 reward
token_price_usd = 0.10  # Check Uniswap

revenue_usd = reward_tokens * token_price_usd

# Profit
profit_usd = revenue_usd - gas_cost_usd
roi_percent = (profit_usd / gas_cost_usd) * 100

# Break-even token price
breakeven_price = gas_cost_usd / reward_tokens
```

**Example:**
- Gas: 100k units @ 30 gwei = 0.003 ETH = $9
- Reward: 100 tokens
- **Break-even price: $0.09 per token**

### Optimization Strategies

**1. Multi-threading (CPU)**
```python
from concurrent.futures import ThreadPoolExecutor

def mine_range(start, end, challenge, difficulty):
    for nonce in range(start, end):
        solution = keccak(challenge + nonce.to_bytes(32, 'big'))
        if int.from_bytes(solution, 'big') < difficulty:
            return nonce
    return None

# Use all CPU cores
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = []
    chunk_size = 1000000
    for i in range(8):
        futures.append(executor.submit(
            mine_range, i*chunk_size, (i+1)*chunk_size, challenge, difficulty
        ))
```

**2. GPU Mining (ROCm for AMD)**
```python
import pyopencl as cl

# OpenCL kernel for keccak256
kernel_code = """
__kernel void mine_keccak(
    __global const uchar *challenge,
    __global const ulong *difficulty,
    __global ulong *result_nonce,
    const uint start_nonce
) {
    uint gid = get_global_id(0);
    uint nonce = start_nonce + gid;
    
    // Implement keccak256 here
    // If solution < difficulty: atomic_cmpxchg(result_nonce, 0, nonce);
}
"""

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
prg = cl.Program(ctx, kernel_code).build()
```

**3. Gas Optimization**
- Monitor gas prices: https://etherscan.io/gastracker
- Submit during low-traffic periods (nights/weekends)
- Use EIP-1559 dynamic fees
- Consider Flashbots for MEV protection

### Common Pitfalls

**1. Contract Not Verified**
- Cannot fetch ABI from Etherscan
- Must reverse engineer from frontend or wait for verification
- Workaround: Use function signatures directly

**2. High Gas Costs**
- Ethereum mainnet gas can be $5-50 per transaction
- Calculate profitability BEFORE mining
- Consider L2 alternatives if available

**3. Epoch Expiry**
- Solutions expire every ~20 minutes
- Must check epoch changes during mining
- Restart mining loop when epoch changes

**4. Race Conditions**
- Multiple miners competing for same solution
- Transaction may fail if someone else submits first
- Use higher gas price for priority

**5. Difficulty Adjustment**
- Difficulty increases as more miners join
- Profitability decreases over time
- Monitor difficulty trends before scaling

### Monitoring

**Gas prices:**
```bash
curl -s "https://api.etherscan.io/api?module=gastracker&action=gasoracle" | jq
```

**Token price (Uniswap):**
```bash
# Check pool reserves and calculate price
# Or use Uniswap API/subgraph
```

**Mining progress:**
```bash
tail -f miner.log
```

### Security Considerations

1. **Private key safety** — Never commit to git, use .env files
2. **Gas estimation** — Always estimate before submitting
3. **Transaction monitoring** — Wait for confirmation before claiming success
4. **Mempool protection** — Consider Flashbots for high-value mints
5. **Contract verification** — Verify contract code before interacting

### Resources

- Etherscan API: https://docs.etherscan.io/
- Web3.py docs: https://web3py.readthedocs.io/
- Keccak256 reference: https://en.wikipedia.org/wiki/SHA-3
- Gas tracker: https://etherscan.io/gastracker
- Uniswap pools: https://app.uniswap.org/

## Session-Specific Implementation

**Project:** hash256-miner (~/hash256-miner/)
**Created:** 2026-05-11
**Status:** Proof of concept (contract not verified)

**Files created:**
- `miner.py` — Main mining script with web3.py
- `extract_abi.py` — Etherscan ABI extractor
- `download_js.sh` — Frontend reverse engineering
- `requirements.txt` — Python dependencies
- Documentation: README.md, QUICKSTART.md, IMPLEMENTATION_GUIDE.md

**Key findings:**
- Contract 0xAC7b5d06fa1e77D08aea40d46cB7C5923A87A0cc not verified on Etherscan
- Genesis sold out @ $0.03, mining live
- Break-even HASH price: $0.09 (with 30 gwei gas)
- Requires reverse engineering ABI from frontend JavaScript

**User hardware:**
- CPU: AMD Ryzen 7 7700 (8 cores) — estimated 1-10 MH/s keccak256
- GPU: AMD RX 7700 XT (12GB) — estimated 100-500 MH/s with ROCm
