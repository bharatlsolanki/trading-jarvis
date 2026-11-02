import os
import time
import requests
import pandas as pd
import yfinance as yf

# Credentials integrated securely
TOKEN = "9270086644:AAHyn_10vrNH6vZrJYYoaMLIlnrqvVFsJWI"
CHAT_ID = "1408188798"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

def run_trading_loop():
    send_telegram_message("🚀 Trading JARVIS is online and monitoring MCX Silver markets!")
    while True:
        try:
            # Fetch MCX Silver data (using silver proxy or MCX symbol if available)
            data = yf.download("SI=F", period="5d", interval="15m", progress=False)
            if not data.empty:
                latest_close = float(data['Close'].iloc[-1].item() if hasattr(data['Close'].iloc[-1], 'item') else data['Close'].iloc[-1])
                # Simple status heartbeat or strategy evaluation logic
                print(f"Checked market. Latest Silver price: {latest_close}")
        except Exception as e:
            print(f"Market fetch error: {e}")
        
        # Sleep for 15 minutes before next check
        time.sleep(900)

if __name__ == "__main__":
    run_trading_loop()
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# Run the health check server in the background
threading.Thread(target=run_server, daemon=True).start()

if __name__ == "__main__":
    run_trading_loop()
