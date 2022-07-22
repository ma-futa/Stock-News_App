import datetime
import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
DAILY_STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "Q566FJQTYDWWIVDM"
def get_percentage_change():
    daily_stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": STOCK_API_KEY
    }
    daily_stock_response = requests.get(url=DAILY_STOCK_ENDPOINT, params=daily_stock_params)
    daily_stock_response.raise_for_status()
    days_stock_closings = [float(value['4. close']) for (key, value) in daily_stock_response.json()['Time Series (Daily)'].items()]
    print(days_stock_closings)
    difference = abs(days_stock_closings[0] - days_stock_closings[1])
    difference_percentage = difference / days_stock_closings[1] * 100
    return difference_percentage


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "ef7f57ea894248028397fe691637b8ae"
def get_news():
    date = datetime.datetime.now()
    news_params = {
        "q": COMPANY_NAME,
        "from": f"{date.year}-{date.month}-{date.day}",
        "sortBy": "popularity",
        "pageSize": 3,
        "language": "en",
        "apiKey": NEWS_API_KEY
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    print(news_response.json()['articles'][0])
    return [{'author': news_item['author'], 'title': news_item.get('title'), 'description': news_item.get('description'),
             'date': news_item['publishedAt'], 'content': news_item.get('content')} for news_item in
            news_response.json()['articles']]


## STEP 3: Use https://www.twilio.com

# Send a seperate message with the percentage change and each article's title and description to your phone number.
account_sid = "ACed5dcf790f17cf39c1918ffdf5e4ef2d"
auth_token = "268e87dd352a577dc45bef6b9c7d167b"
my_number = "+13193673549"

percentage_change = get_percentage_change()
if percentage_change > 0.05:
    news = get_news()
    body = f"{STOCK:} {percentage_change}\n"
    for news_item in news:
        body += f"Headline: {news_item['title']}\nBrief: {news_item['description']}\n"
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=body,
        from_=my_number,
        to='+233271250546'
    )
    print(message.status)

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
