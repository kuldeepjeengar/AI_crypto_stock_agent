from groq import Groq
import os
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import markdown



client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


#---------------------------------------------requirements--------------------
with open('requirements.md', 'r') as f:
    requirement = f.read()

#---------------------------------sample output------------------------------


with open('sample_output.md', 'r') as f:
    smaple_output = f.read()


#---------------------context----------------------------------------------


url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
parameters = {
  'slug': 'bitcoin,ethereum,solana',


}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '5663e98a-8663-4301-b85b-a11beb6cffea',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
#   print(data)

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


json_string = json.dumps(data, indent=4)

# Wrap in Markdown code block
markdown = f"```json\n{json_string}\n```"

user_request = {
    "budget": "$1000",
    "risk_level": "medium",
    "coin_preferences": "prefer BTC, exclude meme coins",
    "requirements": [
        "Fetch current market data: top trending coins, prices, market caps",
        "Determine a list of coins based on the given risk profile",
        "Allocate the budget across 3–5 cryptocurrencies"
    ],
    "output_format": [
        "Coin name and ticker",
        "Amount to invest",
        "Price at time of suggestion",
        "Quantity to acquire",
        "Brief description of the coin (from Wikipedia, CoinMarketCap, LLM, etc.)"
    ]
}



# client = Groq()
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"""below is context 
                            {markdown} 
                            below is user_request
                            {user_request}
                            below is give sample output and dont add any clarification
                            {smaple_output}
                            """,
        }
    ],
    model="llama-3.3-70b-versatile",
)

print("response-----------------",chat_completion.choices[0].message.content)
