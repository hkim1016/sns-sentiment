from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from decouple import config
import time

def scrape_fb_group(group_id, amount):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument("--headless")
    options.add_experimental_option("prefs", { "profile.default_content_setting_values.notifications": 2})

    # service = Service("./chromedriver")

    driver = webdriver.Remote(command_executor="http://chrome:4444/wd/hub", options=options)

    url = "https://www.facebook.com"
    driver.get(url)
    driver.maximize_window()

    wait = WebDriverWait(driver, 30)

    email_field = wait.until(EC.visibility_of_element_located((By.ID, 'email')))
    pass_field = wait.until(EC.visibility_of_element_located((By.ID, 'pass')))
    loginbtn = wait.until(EC.visibility_of_element_located((By.NAME, 'login')))
    email_field.send_keys(config('FB_EMAIL'))
    pass_field.send_keys(config('FB_PASS'))
    loginbtn.click()

    time.sleep(1)

    driver.get(f'https://www.facebook.com/groups/{group_id}')
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    posts = set()
    print(int(amount))
    while len(posts) < int(amount):
        print(len(posts))
        all_posts=soup.find_all("div",{"class":"x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"})
        for post in all_posts:
            try:
                post_text=post.find("div", {"class": "xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a"}).get_text()
                print(post_text)
                posts.add(post_text)
                if len(posts) > int(amount):
                    break
            except:
                post_text="not found"
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(2)

    driver.quit()
    print(posts)

    all_compounds = []
    analyzer = SentimentIntensityAnalyzer()
    for post in posts:
        vs = analyzer.polarity_scores(post)
        all_compounds.append(vs['compound'])

    return all_compounds

def get_fb_group_compound(group, amount):
    compounds = scrape_fb_group(group, amount)
    sum = 0
    for compound in compounds:
        sum += compound
    return round(sum / len(compounds), 4)

if __name__ == '__main__':
    print(get_fb_group_compound(''))