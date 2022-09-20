# SupResistCalc
"""A script designed to screen Fx pairs from Oanda API and find breakouts, then process trade logic and manage trade profile. You must have an API key from Oanda and place a line in a config.py file like the one displayed:
headers = {'Content-Type': 'application/json','Authorization': 'Bearer {your_API_KEY}','Accept-Charset': 'UTF-8'}
"""

# Install packages from requirements.txt
cat requirements.txt | xargs -n 1 pip install