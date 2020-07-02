import datetime
import re
from twitterscraper import query_tweets

class StockTweetScraper():
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol.lower()
        
    def get_tweets(self, begindate: datetime) -> list:
        tweets = []
        for tweet in query_tweets("$"+self.symbol, begindate=begindate):
            tweets.append(tweet)
        return tweets
    
    def get_related(self, tweet_texts: list) -> dict:
        symbol_freq = {}
        
        for tweet in tweet_texts:
            extracted_symbols = re.findall(r"\$[a-zA-Z]+",tweet)
            
            for symbol in extracted_symbols:
                symbol = symbol.lower()
                if symbol in symbol_freq and symbol[1:] != self.symbol:
                    symbol_freq[symbol] += 1
                else:
                    symbol_freq[symbol] = 1
            
        return sorted(symbol_freq.items(), key=lambda item: item[1],reverse=True)
        