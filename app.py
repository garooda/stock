import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "YOUR_API_KEY"
NEWS_API_KEY = "YOUR_API_KEY"
TWILIO_SID = "YOUR_API_KEY"
TWILIO_TOKEN = "YOUR_API_KEY"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "interval": "5min",
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
day_before_yesterday = data_list[1]
day_before_yesterday_closing = float(day_before_yesterday["4. close"])
difference = abs(yesterday_closing_price - day_before_yesterday_closing)

up_down = None
if difference > 1:
    up_down = "🔺"
else:
    up_down = "🔻"
diff_percentage =  (difference / yesterday_closing_price)*100


if abs(diff_percentage) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)


formatted_article = [f"{STOCK_NAME}: {up_down}{diff_percentage:.2f}%\nHeadline: {article['title']} .\nBrief: {article['description']}" for article in three_articles]

client = Client(TWILIO_SID, TWILIO_TOKEN)

for article in formatted_article:
    message = client.messages.create(
                     body=article,
                     from_='YOUR_TWILIO_NUMBER',
                     to='YOUR_NUMBER'
                 )