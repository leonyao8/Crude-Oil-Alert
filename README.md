# Crude Oil Daily Move Alert

A small Python tool that checks the daily price move in WTI crude oil futures and emails me when it is up or down 3% or more.

## What it does
- Pulls daily prices for WTI crude oil futures (`CL=F`) from Yahoo Finance using the `yfinance` library
- Calculates the percent change from the previous close
- Sends an email through Gmail if the move is at least 3% in either direction
- Runs automatically every weekday using GitHub Actions, so it works without my computer being on

## How it works
1. `crude_oil_alert.py` downloads the last five days of prices and compares the latest price to the previous close.
2. If the absolute move is at or above the threshold, it builds an email with the price details.
3. The email is sent over a secure Gmail connection using an app password.
4. A GitHub Actions workflow (`.github/workflows/crude-oil-alert.yml`) runs the script each weekday afternoon (Eastern time).

## Tech used
Python, yfinance, smtplib, GitHub Actions

## Setup
1. Fork or clone this repo.
2. Turn on two step verification for a Gmail account and create an app password.
3. In your repo, go to Settings > Secrets and variables > Actions and add these secrets:
   - `EMAIL_ADDRESS`: the Gmail address that sends the alert
   - `EMAIL_APP_PASSWORD`: the app password
   - `EMAIL_TO` (optional): where to send alerts, if different from the sender
4. Open the Actions tab, choose "Crude oil alert", click "Run workflow", and enter a threshold of `0` to send a test email.

Credentials are stored as GitHub Secrets and are never written in the code.

## Run it locally
```
pip install -r requirements.txt
export EMAIL_ADDRESS="you@gmail.com"
export EMAIL_APP_PASSWORD="your app password"
export THRESHOLD=0
python crude_oil_alert.py
```
On Windows PowerShell, use `$env:EMAIL_ADDRESS="you@gmail.com"` instead of `export`. A threshold of `0` forces a test email. The default is 3.

## Notes
- Free Yahoo Finance data can be delayed, so this is a monitoring tool and not for trading decisions.
- The alert compares the latest price to the previous close, so it is checked once per day.

## Ideas to extend it
- Track natural gas (`NG=F`) and Brent crude (`BZ=F`)
- Chart the last 30 days of prices
- Add a short note on what moved prices, using public inventory reports
