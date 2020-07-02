import constants
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from typing import List

from collections import namedtuple


ChangeStock = namedtuple('ChangeStock','rank symbol change prev_day cur_day')
change_stocks = []

class RobinScrape():
    #responsible for scraping robintracker        
    def scrape_popularity_changes(self,driver: webdriver) -> List[ChangeStock]:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 
                                                                                     constants.CLASS_USER_CHANGE)))

        stocks = driver.find_elements_by_class_name(constants.CLASS_USER_CHANGE)
        change_stocks = []
        for i in range(0,len(stocks),5):
            rank = stocks[i].text
            symbol = stocks[i+constants.SYMBOL_DIFF].text
            change = stocks[i+constants.CHANGE_DIFF].text
            prev_day = stocks[i+constants.USERS_PREV_DAY_DIFF].text
            cur_day = stocks[i+constants.USERS_CUR_DAY_DIFF].text
            change_stock = ChangeStock(rank,symbol,change,prev_day,cur_day)
            change_stocks.append(change_stock)
        
        return change_stocks
    
    def toggle_relative(self, driver: webdriver) -> None:
        driver.find_element_by_class_name(constants.CLASS_TOGGLE_RELATIVE).click()

    def set_lookback_period(self,driver: webdriver,val: str) -> None:
        select = Select(driver.find_element_by_css_selector(constants.SEL_SELECT))
        select.select_by_value(val)

    def set_min_popularity(self,driver: webdriver, n: int) -> None:
        input_elem = driver.find_element_by_css_selector(constants.SEL_MIN_POP)
        input_elem.clear()
        input_elem.send_keys(str(n))
    
    def set_change_type(self, driver: webdriver, change_type: str) -> None:
        select = Select(driver.find_elements_by_css_selector(constants.SEL_SELECT)[1])
        select.select_by_value(change_type)
    