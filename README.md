# Advanced Crypto Trading Bot

This project implements a basic structure for an AI driven crypto trading bot as described in the design document. It focuses on paper trading on Phemex Futures using Python 3.12. The codebase is modular and ready to be extended with reinforcement learning and agentic GPT control.

## Features
- Market data ingestion via `ccxt`.
- Simple technical indicator calculations using the `ta` package.
- Basic rule based strategy with risk management.
- Execution module for Phemex testnet/mainnet.
- Placeholder reinforcement learning policy.
- Sentiment agent example using LangChain and OpenAI.

## Setup
1. Copy `.env.example` to `.env` and fill in API keys.
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the bot:
   ```bash
   python run_bot.py
   ```

The bot is minimal and intended for educational use. Extend modules under `src/` to implement full functionality according to the design specification.
