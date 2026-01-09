# Zerodha Algo Trading Framework

This repository demonstrates a modular, production-grade
algorithmic trading framework built using Zerodha Kite APIs.

## Architecture
- Broker abstraction
- Strategy pattern
- Risk management hooks
- Secure runtime strategy injection

## Strategy Logic
Core trading strategies are intentionally excluded to protect
proprietary intellectual property.

## Usage
Strategies are injected at runtime using environment variables.

Example:
export STRATEGY_CLASS=my_strategy.MomentumV1
