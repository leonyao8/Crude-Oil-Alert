"""Crude oil daily move alert.

Checks the daily percent change in WTI crude oil futures and sends an email
if the move is at least THRESHOLD percent up or down.
"""

import os
import smtplib
import ssl
from email.message import EmailMessage

import yfinance as yf

TICKER = "CL=F"  # WTI crude oil futures on Yahoo Finance
THRESHOLD = float(os.environ.get("THRESHOLD", "3"))  # percent


def get_daily_change():
    """Return (previous close, latest price, percent change)."""
    history = yf.Ticker(TICKER).history(period="5d", interval="1d")
    closes = history["Close"].dropna()
    if len(closes) < 2:
        raise RuntimeError("Not enough price data returned.")
    previous_close = float(closes.iloc[-2])
    latest = float(closes.iloc[-1])
    percent_change = (latest - previous_close) / previous_close * 100
    return previous_close, latest, percent_change


def send_email(subject, body):
    sender = os.environ["EMAIL_ADDRESS"]
    password = os.environ["EMAIL_APP_PASSWORD"]
    recipient = os.environ.get("EMAIL_TO") or sender

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, password)
        server.send_message(message)


def main():
    previous_close, latest, percent_change = get_daily_change()
    print(f"Previous close: {previous_close:.2f}")
    print(f"Latest price:   {latest:.2f}")
    print(f"Daily change:   {percent_change:+.2f}%")

    if abs(percent_change) >= THRESHOLD:
        direction = "up" if percent_change > 0 else "down"
        subject = f"Crude oil is {direction} {abs(percent_change):.2f}% today"
        body = (
            f"WTI crude oil ({TICKER}) moved {percent_change:+.2f}% today.\n\n"
            f"Previous close: {previous_close:.2f}\n"
            f"Latest price:   {latest:.2f}\n"
            f"Alert threshold: {THRESHOLD}%\n"
        )
        send_email(subject, body)
        print("Alert email sent.")
    else:
        print("Move is below the threshold. No alert.")


if __name__ == "__main__":
    main()