
from RobinScrape import RobinScrape, ChangeStock
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import constants

def get_related_sym_tweets(symbol: str)->None:
        
    inner_tweets_df = pd.DataFrame(columns=[constants.PRIMARY_SYMBOL,constants.TWEET_TEXT,constants.TIMESTAMP])
    symbol_processor = StockTweetScraper(symbol.lower())
    yesterday = datetime.date.today() - datetime.timedelta(days = 1)
    tweets = symbol_processor.get_tweets(yesterday)
    for tweet in tweets:
        row = {constants.PRIMARY_SYMBOL:symbol.lower(),constants.TWEET_TEXT:tweet.text,constants.TIMESTAMP:tweet.timestamp}
        inner_tweets_df = inner_tweets_df.append(row,ignore_index=True)
    return inner_tweets_df

if __name__ == "__main__":

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(executable_path="driver/chromedriver.exe",options=options) #webdriver.Firefox()
    driver.get(constants.BASE_URL + constants.POPULARITY_CHANGES)

    scraper = RobinScrape()
    scraper.toggle_relative(driver)
    scraper.set_lookback_period(driver,constants.ONE_DAY)
    changes = scraper.scrape_popularity_changes(driver)
    driver.close()

    perc_change_df = pd.DataFrame(columns=[constants.SYMBOL,constants.PREV_DAY,constants.CUR_DAY,constants.DATE])
    perc_change_df.set_index(constants.SYMBOL)
    for stock in changes:
        row_to_add = {constants.SYMBOL: stock.symbol,
                    constants.PREV_DAY: stock.prev_day,
                    constants.CUR_DAY: stock.cur_day,
                    constants.DATE:datetime.date.today()}
        perc_change_df = perc_change_df.append(row_to_add,ignore_index=True)

    perc_change_df.to_csv('percChange'+str(datetime.date.today())+'.csv')

    top_symbol_tweets_df = pd.DataFrame(columns=[constants.PRIMARY_SYMBOL,constants.TWEET_TEXT,constants.TIMESTAMP])

    with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_rows = {executor.submit(get_related_sym_tweets, symbol): symbol for symbol in perc_change_df.symbol}
    for future in concurrent.futures.as_completed(future_to_rows):
        try:
            rows = future.result()
        except Exception as e:
            print(e)
            continue
        else:
            if rows.shape[0] > 0:
                top_symbol_tweets_df = top_symbol_tweets_df.append(rows)