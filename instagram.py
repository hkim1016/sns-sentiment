import pandas as pd
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from snscrape.modules.instagram import InstagramHashtagScraper
from snscrape.modules.instagram import InstagramUserScraper

translator = Translator()

def scrape_insta_hashtag(hashtag, amount):
    scraper = InstagramHashtagScraper(hashtag)

    posts = []

    for i, item in enumerate(scraper.get_items()):
        if translator.detect(item.content).lang == 'en':
            posts.append(item)
        if len(posts) > int(amount):
            break

    df = pd.DataFrame(posts)

    captions = df['content'].tolist()

    all_compounds = []
    analyzer = SentimentIntensityAnalyzer()
    for caption in captions:
        vs = analyzer.polarity_scores(caption)
        all_compounds.append(vs['compound'])
    return all_compounds

def scrape_insta_user(user, amount):
    scraper = InstagramUserScraper(user)

    posts = []

    for i, item in enumerate(scraper.get_items()):
        if translator.detect(item.content).lang == 'en':
            posts.append(item)
        if len(posts) > int(amount):
            break

    df = pd.DataFrame(posts)

    captions = df['content'].tolist()

    all_compounds = []
    analyzer = SentimentIntensityAnalyzer()
    for caption in captions:
        vs = analyzer.polarity_scores(caption)
        all_compounds.append(vs['compound'])
    return all_compounds

def get_insta_compound(name, category, amount):
    if category == 'hashtag':
        compounds = scrape_insta_hashtag(name, amount)
    if category == 'profile':
        compounds = scrape_insta_user(name, amount)
    sum = 0
    for compound in compounds:
        sum += compound
    return round(sum / len(compounds), 4)

if __name__ == '__main__':
    get_insta_compound('camera', 'hashtag', 3)
















# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# import chromedriver_autoinstaller_fix

# from bs4 import BeautifulSoup
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# from decouple import config
# import time

# chromedriver_autoinstaller_fix.install()

# option = Options()
# option.add_argument("--disable-infobars")
# option.add_argument("start-maximized")
# option.add_argument("--disable-extensions")
# option.add_experimental_option("prefs", { "profile.default_content_setting_values.notifications": 2})

# driver = webdriver.Chrome(options=option)

# url = "https://www.instagram.com"
# driver.get(url)
# driver.maximize_window()

# wait = WebDriverWait(driver, 30)

# username_field = wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
# pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'password')))
# username_field.send_keys(config('INSTA_USERNAME'))
# pass_field.send_keys(config('INSTA_PASS'))
# login_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='_acan _acap _acas _aj1-']")))
# login_btn.click()

# time.sleep(3)

# saveinfo_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='_acan _acap _acas _aj1-']")))
# saveinfo_btn.click()

# time.sleep(2)

# driver.get('https://www.instagram.com/explore/tags/camera/')
# time.sleep(1)
# insta_page = BeautifulSoup(driver.page_source, 'html.parser')

# post_links = set()
# while len(post_links) <= 2:
#     soup=BeautifulSoup(driver.page_source,"html.parser")
#     all_posts=soup.find_all("div",{"class":"_aabd _aa8k  _al3l"})
#     for post in all_posts:
#         try:
#             # name=post.find("a",{"class":"x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f"}).get_text()
#             link=post.find("a", {"class": "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd"}, href=True)
#             post_links.add(link['href'])
#         except:
#             post_text="not found"
#         # print(post_text)
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(3)

# f = open("insta.txt","w+")
# for link in post_links:
#     f.write(link)
#     f.write('\n\n')
#     print(link)

# time.sleep(300)