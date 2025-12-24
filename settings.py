import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URL=os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
    DATABASE_NAME = "favicon_database"
    COLLECTION_NAME = "favicons"


settings = Settings()



RSS_FEEDS = [
    {
        "name": "Mint - Companies",
        "url": "https://www.livemint.com/rss/companies",
        # "parser": parse_standard_date
    },
    {
        "name": "Economic Times - Stocks",
        "url": "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
        # "parser": parse_standard_date
    },
    {
        "name": "Google News - Reliance",
        "url": "https://news.google.com/rss/search?q=RELIANCE&hl=en-IN&gl=IN&ceid=IN:en",
        # "parser": parse_standard_date
    },
    # {
    #     "name": "Google News - HDFC Bank",
    #     "url": "https://news.google.com/rss/search?q=HDFCBANK&hl=en-IN&gl=IN&ceid=IN:en",
    #     "parser": parse_standard_date
    # },
    # {
    #     "name": "Google News - Infosys",
    #     "url": "https://news.google.com/rss/search?q=INFY&hl=en-IN&gl=IN&ceid=IN:en",
    #     "parser": parse_standard_date
    # },
    # {
    #     "name": "Google News - ICICI Bank",
    #     "url": "https://news.google.com/rss/search?q=ICICIBANK&hl=en-IN&gl=IN&ceid=IN:en",
    #     "parser": parse_standard_date
    # },
    # {
    #     "name": "Google News - TCS",
    #     "url": "https://news.google.com/rss/search?q=TCS&hl=en-IN&gl=IN&ceid=IN:en",
    #     "parser": parse_standard_date
    # },
    # {
    #     "name": "Google News - ITC",
    #     "url": "https://news.google.com/rss/search?q=ITC&hl=en-IN&gl=IN&ceid=IN:en",
    #     "parser": parse_standard_date
    # },
    # {
    #     "name": "Google News - L&T",
    #     "url": "https://news.google.com/rss/search?q=LT&hl=en-IN&gl=IN&ceid=IN:en",
    #     "parser": parse_standard_date
    # },
    # {
    #     "name": "Google News - Bharti Airtel",
    #     "url": "https://news.google.com/rss/search?q=BHARTIARTL&hl=en-IN&gl=IN&ceid=IN:en",
    #     "parser": parse_standard_date
    # },
    # {
    #     "name": "Google News - SBI",
    #     "url": "https://news.google.com/rss/search?q=SBIN&hl=en-IN&gl=IN&ceid=IN:en",
    #     "parser": parse_standard_date
    # },
    # {
    #     "name": "Google News - HUL",
    #     "url": "https://news.google.com/rss/search?q=HINDUNILVR&hl=en-IN&gl=IN&ceid=IN:en",
    #     "parser": parse_standard_date
    # },
    # {
    #     "name": "Google News - Axis Bank",
    #     "url": "https://news.google.com/rss/search?q=AXISBANK&hl=en-IN&gl=IN&ceid=IN:en",
    #     "parser": parse_standard_date
    # },
    # {
    #     "name": "Google News - Kotak Bank",
    #     "url": "https://news.google.com/rss/search?q=KOTAKBANK&hl=en-IN&gl=IN&ceid=IN:en",
    #     "parser": parse_standard_date
    # },
]