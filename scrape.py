import requests
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def scrape_site(name, scrape_func):
    print(f'Scraping {name}... ', end='', flush=True)

    has_stock = scrape_func()
    if has_stock:
        print('Stock found :D')
    else:
        print('No stock found :(')

    return has_stock


def scrape_bigw():
    resp = requests.get('https://www.bigw.com.au/ps5')

    if resp.status_code == 404 or 'Please continue to check back online for further updates' in resp.text:
        return False

    return True


def selenium_get_with_wait(driver, lambd, timeout=3):
    elements = []
    try:
        elements = WebDriverWait(driver, timeout=timeout).until(lambd)
    except selenium.common.exceptions.TimeoutException:
        pass
    return elements


def selenium_element_contains_string(driver, string):
    return selenium_get_with_wait(driver, lambda d: d.find_element_by_xpath(f"//*[text()[contains(.,'{string}')]]"))


def scrape_target(driver):
    driver.get('https://www.target.com.au/playstation-5')

    no_stock_str = 'Releasing soon'
    not_available_text = selenium_element_contains_string(driver, no_stock_str)
    if not_available_text or isinstance(not_available_text, list):
        return False

    return True


def scrape_jb(driver):
    driver.get('https://www.jbhifi.com.au/collections/games-consoles/playstation-consoles')

    ps5_strings = ('ps5', 'playstation 5', ' 5 ')
    for title in selenium_get_with_wait(driver, lambda d: d.find_elements_by_class_name('product-tile__title')):
        if any(s in title.get_attribute('innerText').lower() for s in ps5_strings):
            return True

    return False


bigw_found = target_found = jb_found = False


def scrape(headless=False):
    global bigw_found, target_found, jb_found
    chrome_options = webdriver.ChromeOptions()
    # This enables headless Chrome control so the window isn't opened and displayed
    if headless:
        chrome_options.headless = True

    driver = webdriver.Chrome(executable_path='chromedriver_linux64/chromedriver', options=chrome_options)

    stock_str = ''
    if not bigw_found and scrape_site('BIG W', scrape_bigw):
        bigw_found = True
        stock_str += 'BIG W appears to have stock! https://www.bigw.com.au/ps5\n'
    if not target_found and scrape_site('Target', lambda: scrape_target(driver)):
        target_found = True
        stock_str += 'Target appears to have stock! https://www.target.com.au/playstation-5\n'
    if not jb_found and scrape_site('JB HI-FI', lambda: scrape_jb(driver)):
        jb_found = True
        stock_str += 'JB HIFI appears to have stock! https://www.jbhifi.com.au/collections/games-consoles/playstation-consoles\n'

    driver.quit()

    return stock_str


if __name__ == '__main__':
    print(scrape())
