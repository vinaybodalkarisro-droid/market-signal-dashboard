import feedparser
import pandas as pd
from textblob import TextBlob
from datetime import datetime

MARKET_SOURCES = {
    "Metals": {
        "Gold": [
            "https://www.kitco.com/rss/news",
            "https://www.investing.com/rss/news_301.rss",
            "https://www.fxstreet.com/rss/news"
        ],
        "Silver": [
            "https://www.kitco.com/rss/news",
            "https://www.investing.com/rss/news_302.rss",
            "https://www.fxstreet.com/rss/news"
        ],
        "Crude Oil": [
            "https://www.investing.com/rss/news_301.rss",
            "https://oilprice.com/rss/main",
            "https://www.fxstreet.com/rss/news"
        ]
    },
    "Crypto": {
        "Crypto": [
            "https://cointelegraph.com/rss",
            "https://cryptonews.com/news/feed/"
        ]
    },
    "India": {
        "India Markets": [
            "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
            "https://www.moneycontrol.com/rss/markets.xml"
        ]
    }
}

def sentiment_score(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.15:
        return "Bullish"
    elif polarity < -0.15:
        return "Bearish"
    return "Neutral"

def parse_date(entry):
    if hasattr(entry, "published"):
        try:
            return datetime(*entry.published_parsed[:6]).strftime("%d %b %Y %H:%M")
        except:
            return "N/A"
    return "N/A"

def build_market_table(market, asset):
    sources = MARKET_SOURCES.get(market, {}).get(asset, [])
    rows = []

    for url in sources:
        feed = feedparser.parse(url)

        for entry in feed.entries[:20]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")
            date = parse_date(entry)

            text = f"{title} {summary}"
            direction = sentiment_score(text)

            rows.append({
                "Asset": asset,
                "Date": date,
                "Title": title,
                "Direction": direction,
                "Link": link
            })

    return pd.DataFrame(rows)
