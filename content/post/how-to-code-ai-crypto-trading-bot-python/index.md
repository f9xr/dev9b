---
title: "Build Your First AI Crypto Trading Bot in Python, Safely"
description: "Code an AI crypto trading bot in Python with CCXT and scikit-learn. Tested code, honest backtesting, paper trading and the risk rules that keep you solvent."
slug: how-to-code-ai-crypto-trading-bot-python
date: 2026-11-21
image: cover.jpg
author: F9XR Team
keywords: ai crypto trading bot, python crypto trading bot, ccxt tutorial, crypto bot backtesting, walk forward validation, paper trading bot, machine learning crypto trading, trading bot risk management
categories:
    - Tutorials
tags:
    - python
    - crypto-trading
    - ccxt
    - machine-learning
draft: false
math: false
faq:
    - question: "Can I build an AI crypto trading bot myself?"
      answer: "Yes. With basic Python skills you can build a bot that downloads candles through CCXT, trains a small scikit-learn model, backtests it with fees and runs as a paper trader. The hard part is not the code, it is validating the strategy honestly and adding risk controls before using real money."
    - question: "What is the best programming language for a crypto trading bot?"
      answer: "Python is the most common choice because of libraries like CCXT, pandas and scikit-learn. It is fast enough for strategies that trade on minute or hour candles. Ultra low latency strategies are a different game and usually use compiled languages, but they are not a beginner's starting point."
    - question: "Which library connects Python to crypto exchanges?"
      answer: "CCXT is the standard choice. It provides one unified API for many exchanges, covering market data, balances and orders, plus a sandbox mode for testing. Install it with pip install ccxt, and use ccxt.async_support if you need asynchronous code."
    - question: "Do I need machine learning to build a trading bot?"
      answer: "No. A rule based bot using indicators like EMA and RSI is a valid start and makes a good baseline. Add machine learning only if it beats that baseline in walk-forward testing on data it has never seen. If it does not, the extra complexity is not worth it."
    - question: "How do I backtest a crypto trading bot properly?"
      answer: "Decide at a candle's close and fill at the next open, charge fees and slippage on both sides, apply stop-losses, and validate with walk-forward splits instead of shuffled ones. Then test other periods and coins. Run the pipeline on random data too, because profit there signals look-ahead bias."
    - question: "What is paper trading and why should I do it first?"
      answer: "Paper trading runs your bot on live market data with simulated money. It reveals problems backtests hide, such as exchange outages, data gaps and logic bugs, without risking funds. Run it for several weeks and compare its journal against a backtest of the same dates."
    - question: "Is it safe to give a trading bot my exchange API keys?"
      answer: "It can be, if you limit the damage. Create keys with trade permission only, never allow withdrawals, restrict them to your server's IP address, store them in environment variables, and keep sandbox and production keys separate. Never commit keys to a repository."
    - question: "Can ChatGPT or Claude write a trading bot for me?"
      answer: "They can write a lot of the code quickly, but you must review and test it. Generated code can hide look-ahead bias or wrong order logic. Keep automated tests around anything touching money, and do not let a language model make the final trading decision unchecked."
    - question: "Are AI trading bots profitable?"
      answer: "There is no guarantee. Profit depends on the strategy, costs and market conditions, and edges often fade. The US CFTC warns that AI can't predict the future or sudden market changes, and that guaranteed returns are a scam red flag. Treat any profit as a bonus, not a promise."
    - question: "How much money do I need to start?"
      answer: "Paper trading and backtesting cost nothing, so start there. For live trading, begin with the smallest order your exchange allows and an amount you can afford to lose completely. Check minimum order sizes with load_markets() and scale up only after live results match your paper results."
---

Search for a crypto trading bot tutorial and you will find a hundred of them that end with a beautiful equity curve going up and to the right. Almost none of them tell you that curve usually comes from a bug. The classic one is look-ahead bias, where the code quietly peeks at tomorrow's price while pretending to trade today.

This guide goes the other way. We will build a complete, working AI crypto trading bot in Python, and we will spend as much time on the unglamorous parts as on the model: realistic fees, walk-forward validation, stop-losses, position sizing, paper trading and a kill switch. Those parts decide whether a bot survives its first month, and they are the parts most tutorials skip.

By the end you will have a small project that downloads candles with CCXT, trains a scikit-learn model without cheating, backtests it with costs, and runs as a paper trader that journals every decision. You will also know exactly what to check before a single real dollar goes near it.

One thing up front, so nobody feels misled later. I am not promising profit, and no honest tutorial can. This is education for developers. It is not financial advice, and I am not a financial advisor.

<!--more-->

## The Short Answer: How to Build an AI Crypto Trading Bot

If you only need the outline, here it is:

1. Connect to an exchange with the CCXT library and pull OHLCV candles.
2. Turn prices into features (returns, EMA gap, RSI, ATR, volume) and label what happened next.
3. Train a model with walk-forward validation so it never sees the future.
4. Backtest with fees, slippage, stop-losses and risk-based position sizing.
5. Paper trade on live data for weeks before risking money.
6. Go live on an exchange sandbox, then with a tiny size, trade-only API keys and a kill switch.

The rest of this article is the detail behind those six lines, with code you can run.

## What Is an AI Crypto Trading Bot?

An AI crypto trading bot is a program that watches market data, uses a model to estimate what is likely to happen next, and places or simulates orders based on that estimate, with no human clicking buttons. The "AI" can mean very different things, and the difference matters when you design one.

| Approach | How it decides | Strengths | Weak spots |
| --- | --- | --- | --- |
| Rule based | Fixed conditions, like an EMA crossover plus an RSI filter | Easy to explain and debug | Rules stop working when the market changes |
| Classic machine learning | A model such as logistic regression estimates the probability of a move | Can combine many signals, easy to validate | Overfits easily, needs honest validation |
| LLM based | A language model reads a market summary and answers BUY, SELL or HOLD | Quick to prototype, flexible | Not deterministic, hard to backtest, costs per call |
| Hybrid | A rule or ML model proposes, a second layer can veto | Keeps a testable core | More moving parts |

We will build the hybrid. The core is a machine learning model you can inspect and backtest properly. The optional LLM layer can only say no to a trade, never create one. That design keeps the part that touches money testable and deterministic.

If you would rather see the pure LLM approach, where the model reads CoinGecko data and returns a BUY, SELL or HOLD call, our earlier guide on [building an AI Python crypto trading bot with the CoinGecko API](/p/setup-ai-python-crypto-trading-bot-coingecko-api/) covers it. This article picks up where that one stops: backtesting, stop-loss and take-profit logic, position tracking and risk limits.

## Reality Check Before You Write a Line of Code

A few honest points will save you time and money.

**AI does not predict the future.** A model can find a small statistical tilt in past data, and that tilt often disappears after fees or when the market regime changes. The US Commodity Futures Trading Commission has published a customer advisory, [AI Won't Turn Trading Bots into Money Machines](https://www.cftc.gov/LearnandProtect/AdvisoriesAndArticles/AITradingBots.html), warning that the technology can't predict the future or sudden market changes. It also lists red flags for bot scams: guaranteed returns, huge claimed win rates, "no experience needed" pitches, referral bonuses and demo accounts shown as real results. If a bot is sold with any of those, walk away. If you build your own, you are at least sure what is inside it. The SEC's [Investor.gov alert on artificial intelligence fraud](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-alerts/Artificial-Intelligence-Fraud) makes the same point from a different regulator.

**Costs are the silent killer.** A model that is right 52 percent of the time can still lose money once exchange fees and slippage are counted. That is why the labels in this tutorial only count a move as "up" if it beats a minimum threshold, and why the backtester charges fees on both sides of every trade.

**Your first goal is a bot that behaves correctly.** It never spends money it does not have, never trades on a half-finished candle, stops itself when losses pile up, and leaves a log you can audit. Profit, if it ever comes, comes after that.

**Mind the rules where you live.** Exchange availability, trading rules and tax treatment of crypto gains differ by country. Check your exchange's terms for API trading and talk to a qualified professional about taxes.

## The Tech Stack

| Tool | Role | Why this one |
| --- | --- | --- |
| Python 3.10 or newer | Language | Huge data science ecosystem |
| CCXT | Exchange connection | One unified API across many exchanges, with sandbox support |
| pandas and NumPy | Data handling | Time series work in a few lines |
| scikit-learn | Machine learning | Small, well understood models with solid validation tools |
| pytest | Testing | Cheap protection against silent bugs |

A note on testing, because it affects how much you should trust the code below. I built and ran this project on Python 3.13 with pandas 3.0, NumPy 2.5 and scikit-learn 1.9. The 16 automated tests pass. They cover look-ahead bias, stop-loss and take-profit accounting, fee handling, walk-forward purging, the LLM verdict parser and the paper trading loop. The exchange layer was tested against a stand-in object that returns candles in the shape CCXT documents, not against a live exchange. So when you run it for real, start with a small dry run (`--bars 1000`) and read the output before trusting anything.

## Project Structure

```text
ai-trading-bot/
  data.py           # exchange connection and candle download
  features.py       # indicators, features and labels
  model.py          # walk-forward model training
  backtest.py       # the simulator and the report
  bot.py            # one paper trading step, risk rules, optional LLM veto
  run_backtest.py   # command line entry point for backtests
  run_paper.py      # command line loop for paper trading
  synthetic.py      # fake candles for testing without an exchange
  tests/test_all.py
```

Splitting it this way keeps the exchange code in one small file. Everything else works on plain pandas data, which makes it easy to test and easy to swap exchanges later.

## Step 1: Set Up the Project

```bash
mkdir ai-trading-bot && cd ai-trading-bot
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install ccxt pandas numpy scikit-learn pytest
```

Paper trading and backtesting only need public market data, so you do not need an exchange account or API keys yet. Keep it that way for as long as you can.

## Step 2: Pull Market Data With CCXT

[CCXT](https://docs.ccxt.com/) gives you one interface for many exchanges. The method we care about is `fetch_ohlcv`, which returns candles as lists of `[timestamp, open, high, low, close, volume]`, oldest first, with the timestamp in milliseconds. The [CCXT project on GitHub](https://github.com/ccxt/ccxt) tracks which exchanges support which calls.

One detail from the CCXT manual deserves a loud warning: the newest candle may be incomplete until it closes. A bot that makes decisions on a half-formed candle is trading on noise, so `fetch_candles` drops the last row.

```python
import time

import pandas as pd

COLUMNS = ["ts", "open", "high", "low", "close", "volume"]


def make_exchange(name="binance", sandbox=False):
    import ccxt  # imported here so the rest of the project runs without it

    exchange = getattr(ccxt, name)({"enableRateLimit": True})
    if sandbox:
        exchange.set_sandbox_mode(True)  # must be the first call after creation
    return exchange


def fetch_candles(exchange, symbol="BTC/USDT", timeframe="1h", limit=1000):
    raw = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(raw, columns=COLUMNS)
    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    df = df.set_index("ts").astype(float)
    return df.iloc[:-1]  # the newest candle is still forming, so drop it


TIMEFRAME_MS = {"1m": 60_000, "5m": 300_000, "15m": 900_000, "1h": 3_600_000, "4h": 14_400_000, "1d": 86_400_000}


def fetch_history(exchange, symbol="BTC/USDT", timeframe="1h", bars=5000):
    """Page through the exchange 1000 candles at a time."""
    step = TIMEFRAME_MS[timeframe]
    since = int(time.time() * 1000) - bars * step
    rows = []
    while len(rows) < bars:
        batch = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=1000)
        if not batch:
            break
        rows += batch
        since = batch[-1][0] + step
        if len(batch) < 2:
            break
    df = pd.DataFrame(rows, columns=COLUMNS).drop_duplicates("ts")
    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    return df.set_index("ts").astype(float).iloc[:-1]
```

Three things worth noticing:

- **`enableRateLimit`** makes CCXT throttle your requests so you do not get banned for hammering the API.
- **`set_sandbox_mode(True)`** switches to the exchange's test network. CCXT's manual says it must be your first call after creating the exchange, and that sandbox keys are separate from production keys, created on the exchange's sandbox site.
- **`fetch_history`** pages through the data 1000 candles at a time, because most exchanges cap a single request.

Pick an exchange that is available where you live. Because CCXT is unified, switching later usually means changing one string.

## Step 3: Build Features and Labels

A model needs numbers that describe the market, and an answer key. Features describe what is known at the close of a candle. Labels describe what happened afterward.

```python
import numpy as np
import pandas as pd


def rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - 100 / (1 + rs)


def atr(df, period=14):
    prev_close = df["close"].shift(1)
    true_range = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return true_range.ewm(alpha=1 / period, adjust=False).mean()


def build_features(df):
    c = df["close"]
    vol_mean = df["volume"].rolling(48).mean()
    vol_std = df["volume"].rolling(48).std()
    out = pd.DataFrame(index=df.index)
    out["ret_1"] = c.pct_change(1)
    out["ret_4"] = c.pct_change(4)
    out["ret_24"] = c.pct_change(24)
    out["ema_gap"] = c.ewm(span=12, adjust=False).mean() / c.ewm(span=48, adjust=False).mean() - 1
    out["rsi"] = rsi(c) / 100
    out["atr_pct"] = atr(df) / c
    out["vol_z"] = (df["volume"] - vol_mean) / vol_std
    return out.replace([np.inf, -np.inf], np.nan)


def make_labels(df, horizon=6, min_move=0.002):
    """1 if price is higher than min_move after `horizon` bars, else 0.
    The last `horizon` rows have no answer yet, so they stay NaN."""
    future = df["close"].shift(-horizon) / df["close"] - 1
    labels = (future > min_move).astype(float)
    labels[future.isna()] = np.nan
    return labels
```

What each feature is doing:

| Feature | What it captures |
| --- | --- |
| `ret_1`, `ret_4`, `ret_24` | Recent momentum over 1, 4 and 24 candles |
| `ema_gap` | Distance between a fast and a slow exponential moving average, a simple trend measure |
| `rsi` | Whether recent moves were mostly up or mostly down |
| `atr_pct` | Volatility, as a share of price |
| `vol_z` | Whether volume is unusually high or low |

The label is `1` when price is more than `min_move` higher after `horizon` candles. The default of 0.2 percent is deliberately above the cost of a round trip, so the model is learning "moves that beat fees," not "any tiny wiggle upward." The last `horizon` rows get no label because their future has not happened yet.

You will notice that every feature uses only past and current candles. That is not an accident, and the tests check it.

## Step 4: Train Without Cheating (Walk-Forward Validation)

This is the step where most beginner bots go wrong. If you shuffle your data and use `train_test_split`, the model trains on candles from next Tuesday and gets tested on last Monday. The score looks wonderful and means nothing.

Time series need time-ordered validation. Walk-forward validation trains on a window of older data, predicts the next block it has never seen, then rolls forward and repeats.

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def new_model():
    return make_pipeline(StandardScaler(), LogisticRegression(C=0.5, max_iter=500))


def walk_forward_probs(X, y, train_size=1000, step=200, horizon=6):
    """Out-of-sample probability of 'up' for every bar after the first train window.
    Each block is predicted by a model trained only on older data. The `horizon`
    rows right before the test block are skipped (purged) because their labels
    look into the test period."""
    data = X.join(y.rename("y")).dropna()
    probs = pd.Series(np.nan, index=X.index)
    for start in range(train_size + horizon, len(data), step):
        train_end = start - horizon
        train = data.iloc[train_end - train_size : train_end]
        test = data.iloc[start : start + step]
        if train["y"].nunique() < 2 or test.empty:
            continue
        model = new_model().fit(train.drop(columns="y"), train["y"])
        probs.loc[test.index] = model.predict_proba(test.drop(columns="y"))[:, 1]
    return probs


def fit_latest(X, y, train_size=1000):
    """Model for live use: trained on the most recent labeled rows."""
    data = X.join(y.rename("y")).dropna().iloc[-train_size:]
    return new_model().fit(data.drop(columns="y"), data["y"])
```

Two details matter here:

- **Purging.** A label at row `t` looks `horizon` candles into the future. Without a gap, the last training labels would overlap the first test candles and leak information. The code skips `horizon` rows between training and test. scikit-learn's [TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html) has a `gap` parameter for the same reason, if you prefer a built-in splitter.
- **A deliberately simple model.** Logistic regression with scaled features is hard to overfit badly and easy to inspect. If a simple model shows no edge, a fancier one usually just finds the noise more convincingly. Earn the right to use gradient boosting or a neural network by beating the simple baseline out of sample first.

## Step 5: Backtest Like You Mean It

A backtester is a small simulator. The realism of its rules decides whether you can trust the answer. These are the rules in ours:

| Rule | Why it matters |
| --- | --- |
| Decide at the close, fill at the next open | Prevents trading on a price you could not have known |
| Fee on both sides, plus slippage | Fees and slippage are often bigger than the signal |
| Stop and target sized by ATR | Risk scales with current volatility |
| Stop wins if both are touched in one candle | You cannot know the order inside a candle, so assume the worse one |
| Size by risk, capped by cash | Lose about 1 percent of equity per stopped trade, no borrowed funds |
| Maximum holding time | Stops the bot from holding a stale idea forever |

```python
from dataclasses import dataclass

import numpy as np
import pandas as pd

from features import atr


@dataclass
class Config:
    fee: float = 0.001            # 0.1% per side
    slippage: float = 0.0005      # 0.05% worse than the quoted price
    risk_per_trade: float = 0.01  # risk 1% of equity per trade
    stop_atr: float = 2.0
    tp_atr: float = 3.0
    entry_prob: float = 0.55
    exit_prob: float = 0.45
    max_hold: int = 24            # bars
    start_cash: float = 10_000.0


def position_size(equity, entry, stop, cfg):
    stop_distance = entry - stop
    if stop_distance <= 0:
        return 0.0
    by_risk = equity * cfg.risk_per_trade / stop_distance
    by_cash = equity * 0.95 / (entry * (1 + cfg.fee))  # spot only, no borrowing
    return max(0.0, min(by_risk, by_cash))


def backtest(df, probs, cfg=Config()):
    o, h, l, c = (df[k].to_numpy() for k in ("open", "high", "low", "close"))
    p = probs.reindex(df.index).to_numpy()
    a = atr(df).to_numpy()

    cash, qty, stop, take, held = cfg.start_cash, 0.0, 0.0, 0.0, 0
    want_entry = want_exit = False
    trades, equity = [], np.full(len(df), np.nan)
    entry_px = entry_i = 0

    def close_position(i, price, why):
        nonlocal cash, qty, held
        proceeds = qty * price * (1 - cfg.fee)
        cost = qty * entry_px * (1 + cfg.fee)
        trades.append({"entry_time": df.index[entry_i], "exit_time": df.index[i],
                       "entry": entry_px, "exit": price, "qty": qty,
                       "pnl": proceeds - cost, "bars": held, "reason": why})
        cash += proceeds
        qty, held = 0.0, 0

    for i in range(1, len(df)):
        # 1) act on last bar's decision at this bar's open
        if qty > 0 and want_exit:
            close_position(i, o[i] * (1 - cfg.slippage), "signal")
        if qty == 0 and want_entry and not np.isnan(a[i - 1]):
            fill = o[i] * (1 + cfg.slippage)
            s, t = fill - cfg.stop_atr * a[i - 1], fill + cfg.tp_atr * a[i - 1]
            q = position_size(cash, fill, s, cfg)
            if q > 0:
                cash -= q * fill * (1 + cfg.fee)
                qty, stop, take, entry_px, entry_i, held = q, s, t, fill, i, 0
        want_entry = want_exit = False

        # 2) stops and targets inside this bar (stop wins if both are touched)
        if qty > 0:
            if l[i] <= stop:
                close_position(i, min(stop, o[i]) * (1 - cfg.slippage), "stop")
            elif h[i] >= take:
                close_position(i, take * (1 - cfg.slippage), "target")

        # 3) at the close, decide what to do on the next open
        if qty > 0:
            held += 1
            want_exit = held >= cfg.max_hold or (not np.isnan(p[i]) and p[i] < cfg.exit_prob)
        elif not np.isnan(p[i]) and p[i] >= cfg.entry_prob:
            want_entry = True

        equity[i] = cash + qty * c[i]

    equity[0] = cfg.start_cash
    return pd.DataFrame(trades), pd.Series(equity, index=df.index)


def report(df, trades, equity):
    eq = equity.dropna()
    first = eq.index[0]
    drawdown = (eq / eq.cummax() - 1).min()
    wins = trades[trades["pnl"] > 0]["pnl"].sum() if len(trades) else 0.0
    losses = -trades[trades["pnl"] < 0]["pnl"].sum() if len(trades) else 0.0
    return {
        "trades": len(trades),
        "return_pct": round(float(eq.iloc[-1] / eq.iloc[0] - 1) * 100, 2),
        "buy_hold_pct": round(float(df["close"].iloc[-1] / df["close"].loc[first] - 1) * 100, 2),
        "max_drawdown_pct": round(float(drawdown) * 100, 2),
        "win_rate_pct": round(float((trades["pnl"] > 0).mean()) * 100, 1) if len(trades) else 0.0,
        "profit_factor": round(float(wins / losses), 2) if losses > 0 else float("inf"),
    }
```

The fee of 0.1 percent per side and slippage of 0.05 percent are placeholders. Check your exchange's current fee schedule and use your real numbers.

## Step 6: Run the Backtest and Read the Results

The runner ties everything together. Note that it backtests only the candles the model has never seen.

```python
import argparse

from backtest import backtest, report
from data import fetch_history, make_exchange
from features import build_features, make_labels
from model import walk_forward_probs
from synthetic import make_synthetic


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="BTC/USDT")
    ap.add_argument("--timeframe", default="1h")
    ap.add_argument("--bars", type=int, default=6000)
    ap.add_argument("--exchange", default="binance")
    ap.add_argument("--synthetic", action="store_true", help="use fake data, no exchange needed")
    args = ap.parse_args()

    if args.synthetic:
        df = make_synthetic(args.bars)
    else:
        df = fetch_history(make_exchange(args.exchange), args.symbol, args.timeframe, args.bars)

    probs = walk_forward_probs(build_features(df), make_labels(df))
    test = df.loc[probs.dropna().index]          # only bars the model has never seen
    trades, equity = backtest(test, probs)
    for key, value in report(test, trades, equity).items():
        print(f"{key:>18}: {value}")


if __name__ == "__main__":
    main()
```

First, run it on fake data. No exchange needed:

```bash
python run_backtest.py --synthetic --bars 6000
```

`synthetic.py` generates a pure random walk, so there is no pattern to find:

```python
import numpy as np
import pandas as pd


def make_synthetic(n=4000, seed=7, drift=0.0):
    """Fake hourly candles from a random walk. Handy for testing the plumbing."""
    rng = np.random.default_rng(seed)
    rets = rng.normal(drift, 0.006, n)
    close = 20_000 * np.exp(np.cumsum(rets))
    open_ = np.r_[close[0], close[:-1]]
    wick = np.abs(rng.normal(0, 0.003, n))
    return pd.DataFrame(
        {
            "open": open_,
            "high": np.maximum(open_, close) * (1 + wick),
            "low": np.minimum(open_, close) * (1 - wick),
            "close": close,
            "volume": rng.lognormal(5, 0.4, n),
        },
        index=pd.date_range("2025-01-01", periods=n, freq="1h", tz="UTC"),
    )
```

On my machine the output was:

```text
            trades: 109
        return_pct: -13.45
      buy_hold_pct: -6.42
  max_drawdown_pct: -18.71
      win_rate_pct: 39.4
     profit_factor: 0.69
```

That loss is the correct result. Random data contains nothing to learn, so a bug-free pipeline should lose roughly what trading costs. This is one of the most useful sanity checks in the whole article: **if your bot makes money on random data, you have look-ahead bias somewhere.** Fix that before you celebrate anything.

Once the plumbing checks out, run it on real candles:

```bash
python run_backtest.py --symbol BTC/USDT --timeframe 1h --bars 6000
```

I have not printed a Bitcoin result on purpose. One coin over one period tells you almost nothing, and I would rather you run it on your own data and judge it yourself.

### How to read the report

| Metric | What to look for |
| --- | --- |
| `trades` | Enough to mean something. A great result from 8 trades is luck until proven otherwise |
| `return_pct` vs `buy_hold_pct` | Beating buy and hold matters, especially if the bot sits in cash much of the time |
| `max_drawdown_pct` | The worst peak to trough loss. Ask yourself if you would actually sit through it |
| `win_rate_pct` | Not meaningful alone. A 40 percent win rate can be fine if winners are bigger than losers |
| `profit_factor` | Gross profit divided by gross loss. Below 1.0 means the bot loses money |

Then test for fragility. Change the period, change the coin, nudge `entry_prob` and `stop_atr` slightly. If a tiny tweak flips the result from great to terrible, you have found noise, not an edge.

## Step 7: Paper Trade on Live Data

Backtests are history. Paper trading is the first contact with reality: live candles, simulated money. The bot below fetches the latest closed candle, retrains on recent data, applies the same entry and exit rules as the backtest, and writes every decision to a journal.

```python
import json
import logging
import re
from dataclasses import dataclass, asdict, field
from pathlib import Path

from backtest import Config, position_size
from data import fetch_candles
from features import atr, build_features, make_labels
from model import fit_latest

log = logging.getLogger("bot")


@dataclass
class State:
    cash: float = 10_000.0
    qty: float = 0.0
    entry: float = 0.0
    stop: float = 0.0
    take: float = 0.0
    held: int = 0
    peak_equity: float = 10_000.0
    halted: bool = False
    last_bar: str = ""
    journal: list = field(default_factory=list)


def load_state(path):
    p = Path(path)
    return State(**json.loads(p.read_text())) if p.exists() else State()


def save_state(state, path):
    Path(path).write_text(json.dumps(asdict(state), indent=2))


def parse_llm_verdict(text):
    """Accepts only {"approve": true|false}. Anything else counts as a veto."""
    match = re.search(r"\{.*?\}", text or "", re.S)
    if not match:
        return False
    try:
        return json.loads(match.group(0)).get("approve") is True
    except (ValueError, AttributeError):
        return False


def make_llm_check(ask):
    """ask(prompt) -> str can wrap any provider. It can only veto a trade, never create one."""
    def check(df, prob):
        recent = df.tail(12)[["close", "volume"]].round(2).to_string()
        prompt = (
            "You are a risk reviewer for a crypto bot. The model wants to open a long "
            f"(up-probability {prob:.2f}). Last 12 hourly candles:\n{recent}\n"
            'Reply with JSON only: {"approve": true} or {"approve": false}.'
        )
        try:
            return parse_llm_verdict(ask(prompt))
        except Exception:
            return False  # if the AI call fails, do not trade
    return check


def run_once(exchange, state, cfg=Config(), symbol="BTC/USDT", timeframe="1h",
             max_drawdown=0.10, llm_check=None):
    """One paper-trading step. Call it once per closed candle."""
    if state.halted:
        return "halted"
    df = fetch_candles(exchange, symbol, timeframe, limit=1000)
    bar = str(df.index[-1])
    if bar == state.last_bar:
        return "no new candle"
    state.last_bar = bar

    X, y = build_features(df), make_labels(df)
    model = fit_latest(X, y)
    latest = X.iloc[[-1]]
    if latest.isna().any(axis=None):
        return "not enough data"
    prob = float(model.predict_proba(latest)[0, 1])
    price, bar_atr = float(df["close"].iloc[-1]), float(atr(df).iloc[-1])
    equity = state.cash + state.qty * price
    state.peak_equity = max(state.peak_equity, equity)

    if equity / state.peak_equity - 1 <= -max_drawdown:   # kill switch
        state.halted = True
        action = "HALT: drawdown limit"
    elif state.qty > 0:
        state.held += 1
        low, high = float(df["low"].iloc[-1]), float(df["high"].iloc[-1])
        exit_px, why = None, None
        if low <= state.stop:
            exit_px, why = state.stop, "stop"
        elif high >= state.take:
            exit_px, why = state.take, "target"
        elif prob < cfg.exit_prob or state.held >= cfg.max_hold:
            exit_px, why = price, "signal"
        if exit_px:
            exit_px *= 1 - cfg.slippage
            state.cash += state.qty * exit_px * (1 - cfg.fee)
            action = f"SELL {state.qty:.6f} at {exit_px:.2f} ({why})"
            state.qty, state.held = 0.0, 0
        else:
            action = "HOLD position"
    elif prob >= cfg.entry_prob:
        approved = llm_check(df, prob) if llm_check else True
        fill = price * (1 + cfg.slippage)
        stop, take = fill - cfg.stop_atr * bar_atr, fill + cfg.tp_atr * bar_atr
        qty = position_size(state.cash, fill, stop, cfg)
        if approved and qty > 0:
            state.cash -= qty * fill * (1 + cfg.fee)
            state.qty, state.entry, state.stop, state.take, state.held = qty, fill, stop, take, 0
            action = f"BUY {qty:.6f} at {fill:.2f}"
        else:
            action = "SKIP: vetoed or size is zero"
    else:
        action = "WAIT"

    state.journal.append({"bar": bar, "prob": round(prob, 3), "price": price, "action": action,
                          "equity": round(state.cash + state.qty * price, 2)})
    state.journal = state.journal[-500:]
    log.info("%s p=%.3f %s", bar, prob, action)
    return action
```

And the loop that runs it:

```python
import logging
import time

from bot import load_state, run_once, save_state
from data import make_exchange

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


def main():
    exchange = make_exchange("binance")   # public candles only, no API keys for paper trading
    state = load_state("state.json")
    while True:
        try:
            run_once(exchange, state)
            save_state(state, "state.json")
        except Exception:
            logging.exception("step failed, retrying next cycle")
        time.sleep(300)                   # run_once ignores candles it has already seen


if __name__ == "__main__":
    main()
```

Look at what the bot does besides trading:

- **Skips repeated candles.** The loop polls every 5 minutes, but `run_once` only acts when a new closed candle arrives.
- **Persists state.** If your machine restarts, the bot knows its cash and open position instead of starting over.
- **Has a kill switch.** If equity falls 10 percent below its peak, it halts and stays halted until you look at it. A bot should never be able to dig itself out of a hole alone.
- **Keeps a journal.** Every candle gets a probability, an action and an equity figure, so you can review why it did what it did.
- **Survives errors.** The loop catches exceptions, logs them and tries again next cycle.

Two honest limits. The paper trader fills at the last close plus slippage, which approximates the next open, because a live bot would send its market order the moment a candle closes. Real fills will differ, so measure the gap. It also checks stops once per candle. A live bot should not wait for that. It should place the stop order on the exchange itself, so a sudden drop is handled even if your script is asleep.

Run it for weeks, not hours. You are looking for behavior that matches the backtest, and for the strange cases a backtest never shows: exchange hiccups, gaps in data, a flash crash. Compare the paper journal against a fresh backtest over the same dates. Large differences mean either your backtest is too optimistic or your live loop has a bug.

## Step 8: Add an LLM as a Risk Reviewer (Optional)

Large language models are tempting, but they are the wrong tool for the final trading decision. They are not deterministic, you cannot backtest them cheaply, and every call costs money. A better role is a veto layer, a second pair of eyes that can block a trade the model proposes.

The `make_llm_check` function in `bot.py` does this. It sends a short market summary to any model you like through an `ask(prompt)` function, and it only accepts a strict `{"approve": true}` reply. Everything else counts as a veto, including a timeout, malformed JSON or a chatty answer. That fail-closed design matters: if your AI provider is down at 3 a.m., the bot does nothing, which is the safe outcome.

```python
from bot import make_llm_check, run_once

def ask(prompt: str) -> str:
    ...  # call your provider here and return the reply text

run_once(exchange, state, llm_check=make_llm_check(ask))
```

Treat the veto as an experiment, not a feature. Log what it blocks, then check over a few weeks whether the blocked trades would actually have lost money. If they would not, switch it off and save the cost. Prompt quality also matters here, and our guide on [writing an effective system prompt](/p/what-is-system-prompt-how-to-write-effective/) covers how to get strict, parseable output.

## Step 9: Going Live Without Getting Hurt

Do not skip stages. Move through them in order, and stay at each one until the numbers match your expectations.

| Stage | What you do | Money at risk |
| --- | --- | --- |
| 1. Backtest | Walk-forward results on several periods and coins | None |
| 2. Paper trade | Live candles, simulated fills, for weeks | None |
| 3. Exchange sandbox | Real order flow with test funds and sandbox keys | None |
| 4. Tiny live size | The smallest order the exchange allows | A small amount you can fully lose |
| 5. Gradual scale up | Increase only after live results match paper | Grows slowly |

Here is the shape of a sandbox order with CCXT. This snippet is not part of the tested project, so treat it as a starting point and try it on the sandbox first:

```python
import os
import ccxt

exchange = ccxt.binance({
    "apiKey": os.environ["EXCHANGE_API_KEY"],
    "secret": os.environ["EXCHANGE_API_SECRET"],
    "enableRateLimit": True,
})
exchange.set_sandbox_mode(True)   # first call after creating the exchange

order = exchange.create_order("BTC/USDT", "market", "buy", 0.001)
print(order)
```

`create_order` follows CCXT's unified signature of symbol, type, side, amount, price and params. Load the market info with `exchange.load_markets()` to check minimum order sizes and amount precision, and round amounts accordingly.

### API key hygiene

This is where beginners get burned, so it gets its own list:

- Create keys with **trade permission only**. Never enable withdrawals.
- Restrict the key to **your server's IP address** if the exchange supports it.
- Keep keys in environment variables or a secrets manager, never in the code, and never commit a `.env` file.
- Use separate keys for the sandbox and for production.
- Rotate keys if you ever paste one somewhere by accident.

### Production safeguards worth adding

- Stop orders placed on the exchange itself, not only checked by your script once per candle
- A daily loss limit on top of the drawdown kill switch
- A maximum number of trades per day
- An alert, by email or chat message, whenever the bot halts or throws an error
- A check that your exchange balance matches what the bot thinks it holds
- Log files you can search later

If you want to schedule and monitor workflows without writing every piece yourself, a local automation tool can help, and our walkthrough on [installing n8n locally](/p/how-to-install-n8n-locally-on-pc/) is a good starting point.

## Common Mistakes That Quietly Ruin Trading Bots

| Mistake | What it looks like | Fix |
| --- | --- | --- |
| Look-ahead bias | Stunning backtest, awful live results | Fill at the next open, test that features ignore the future |
| Shuffled train and test split | Great accuracy that vanishes live | Walk-forward validation with a purge gap |
| Ignoring fees and slippage | Profitable on paper, bleeding live | Charge costs on both sides, use real fee tiers |
| Overfitting | Result flips with tiny parameter changes | Test other periods and coins, keep the model simple |
| Trading the forming candle | Random-looking entries | Only act on closed candles |
| No stop-loss | One bad trade erases weeks of gains | Define the exit before the entry |
| Trading with borrowed funds | A small move wipes the account | Spot only while learning, size by risk |
| No kill switch | A bug keeps trading while you sleep | Hard drawdown limit that halts the bot |
| Trusting generated code blindly | Subtle bugs nobody reviewed | Write tests, read every line that touches money |

That last one deserves a second look. AI coding assistants write trading code quickly and sometimes confidently wrong. Use them, but keep tests around anything that touches money. Our piece on [AI coding agents explained](/p/ai-coding-agents-explained/) covers how to work with them without handing over the steering wheel.

## Ideas to Improve Your Bot

Once the basics are solid, here are sensible next steps, roughly in order of value:

1. **Add a regime filter.** Only allow entries when volatility or trend conditions look like the ones the model trained on.
2. **Try more features carefully.** Each new feature should earn its place in out-of-sample results, not just in training.
3. **Trade several markets.** Diversifying across coins smooths results, but remember that crypto assets often move together.
4. **Compare models fairly.** Try gradient boosting against the logistic baseline using the same walk-forward setup.
5. **Move to async.** CCXT has an async version (`ccxt.async_support`) for watching many markets at once.
6. **Measure live slippage.** Compare your assumed slippage against real fills and update the backtest.
7. **Enter competitions for practice.** Some platforms run live bot competitions, such as the BTC trading bot race that make.fun listed among its bounties. Our [make.fun guide](/p/make-fun-ai-agent-bounties-setup-guide/) explains how those work. Read each platform's rules before entering anything.

## Key Takeaways

- An AI crypto trading bot is a pipeline: market data, features, a model, a backtester, a risk layer and an execution layer. The model is only one piece.
- CCXT gives you one interface to many exchanges, including sandbox mode, and `fetch_ohlcv` returns candles oldest first.
- Never act on the newest candle until it closes. In a backtest, decide at the close and fill at the next open.
- Use walk-forward validation with a purge gap. Shuffled splits leak the future and produce fake accuracy.
- Charge fees and slippage in every backtest. A small edge can disappear completely after costs.
- Run your pipeline on random data first. If it profits there, you have a look-ahead bug.
- Size trades by risk, define the stop before the entry, and add a drawdown kill switch.
- Paper trade for weeks, then use a sandbox, then trade with the smallest size the exchange allows.
- Use trade-only API keys with an IP allowlist and keep them out of your code.
- If an LLM is involved, let it veto trades rather than create them, and make it fail closed.
- Nothing here guarantees profit. Be wary of anyone selling a bot with guaranteed returns.

## Conclusion

The code in this guide is deliberately boring in the places that matter. A small model, honest validation, real costs, a stop on every trade and a switch that turns the bot off. That is what a trading bot looks like before it looks impressive, and it is the version worth building first.

If you spot an error, want to add a test or improve a section, read the [contributor guide](/contribute/) and our [editorial policy](/editorial-policy/). Corrections with a reproducible case are always welcome.

*This article is educational and is not financial, investment, legal or tax advice. Crypto trading carries a high risk of loss. Never trade money you cannot afford to lose. Written with AI assistance and reviewed by the F9XR Team.*

## Frequently Asked Questions

### Can I build an AI crypto trading bot myself?

Yes. With basic Python skills you can build a bot that downloads candles through CCXT, trains a small scikit-learn model, backtests it with fees and runs as a paper trader. The hard part is not the code, it is validating the strategy honestly and adding risk controls before using real money.

### What is the best programming language for a crypto trading bot?

Python is the most common choice because of libraries like CCXT, pandas and scikit-learn. It is fast enough for strategies that trade on minute or hour candles. Ultra low latency strategies are a different game and usually use compiled languages, but they are not a beginner's starting point.

### Which library connects Python to crypto exchanges?

CCXT is the standard choice. It provides one unified API for many exchanges, covering market data, balances and orders, plus a sandbox mode for testing. Install it with `pip install ccxt`, and use `ccxt.async_support` if you need asynchronous code.

### Do I need machine learning to build a trading bot?

No. A rule based bot using indicators like EMA and RSI is a valid start and makes a good baseline. Add machine learning only if it beats that baseline in walk-forward testing on data it has never seen. If it does not, the extra complexity is not worth it.

### How do I backtest a crypto trading bot properly?

Decide at a candle's close and fill at the next open, charge fees and slippage on both sides, apply stop-losses, and validate with walk-forward splits instead of shuffled ones. Then test other periods and coins. Run the pipeline on random data too, because profit there signals look-ahead bias.

### What is paper trading and why should I do it first?

Paper trading runs your bot on live market data with simulated money. It reveals problems backtests hide, such as exchange outages, data gaps and logic bugs, without risking funds. Run it for several weeks and compare its journal against a backtest of the same dates.

### Is it safe to give a trading bot my exchange API keys?

It can be, if you limit the damage. Create keys with trade permission only, never allow withdrawals, restrict them to your server's IP address, store them in environment variables, and keep sandbox and production keys separate. Never commit keys to a repository.

### Can ChatGPT or Claude write a trading bot for me?

They can write a lot of the code quickly, but you must review and test it. Generated code can hide look-ahead bias or wrong order logic. Keep automated tests around anything touching money, and do not let a language model make the final trading decision unchecked.

### Are AI trading bots profitable?

There is no guarantee. Profit depends on the strategy, costs and market conditions, and edges often fade. The US CFTC warns that AI can't predict the future or sudden market changes, and that guaranteed returns are a scam red flag. Treat any profit as a bonus, not a promise.

### How much money do I need to start?

Paper trading and backtesting cost nothing, so start there. For live trading, begin with the smallest order your exchange allows and an amount you can afford to lose completely. Check minimum order sizes with `load_markets()` and scale up only after live results match your paper results.
