#!/usr/bin/env python3
"""
Production-Grade Telegram Crypto Price & Threshold Alert Bot
Pure Python Standard Library (Zero dependencies required).
Deliverable asset for freelance gigs ($50 - $100 value).
"""

import urllib.request
import json
import time

class TelegramCryptoAlertBot:
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token or "YOUR_TELEGRAM_BOT_TOKEN"
        self.chat_id = chat_id or "YOUR_CHAT_ID"
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, text):
        if self.bot_token == "YOUR_TELEGRAM_BOT_TOKEN":
            print(f"[SIMULATED TELEGRAM SEND] -> {text}")
            return True
        url = f"{self.api_url}/sendMessage"
        payload = json.dumps({"chat_id": self.chat_id, "text": text, "parse_mode": "Markdown"}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8")).get("ok", False)
        except Exception as e:
            print(f"[!] Telegram send error: {e}")
            return False

    def get_binance_price(self, symbol="BTCUSDT"):
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return float(data.get("price", 0.0))
        except Exception as e:
            print(f"[!] Error fetching {symbol} price: {e}")
            return None

    def check_threshold(self, symbol="BTCUSDT", upper_limit=100000.0, lower_limit=80000.0):
        price = self.get_binance_price(symbol)
        if price is None:
            return None
        print(f"[+] Current {symbol} Price: ${price:,.2f}")
        if price >= upper_limit:
            msg = f"🚨 *PRICE ALERT:* {symbol} has breached UPPER limit! Current: `${price:,.2f}`"
            self.send_message(msg)
            return "UPPER_BREACH"
        elif price <= lower_limit:
            msg = f"⚠️ *PRICE ALERT:* {symbol} has breached LOWER limit! Current: `${price:,.2f}`"
            self.send_message(msg)
            return "LOWER_BREACH"
        return "NORMAL"

if __name__ == "__main__":
    print("=" * 65)
    print("  [DUKE] Telegram Crypto Alert Bot Engine (Freelance Ready)")
    print("=" * 65)
    bot = TelegramCryptoAlertBot()
    status = bot.check_threshold("BTCUSDT", upper_limit=150000, lower_limit=20000)
    print(f"[+] Evaluation Status: {status}")
    print("=" * 65)
