from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller_fix

from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from decouple import config
import time

def scrape_fb_group(group):
    chromedriver_autoinstaller_fix.install()

    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    option.add_experimental_option("prefs", { "profile.default_content_setting_values.notifications": 2})

    driver = webdriver.Chrome(options=option)

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

    time.sleep(2)

    # driver.get('https://www.facebook.com/davin.ko.94')
    driver.get('https://www.facebook.com/groups/2377869205777593')
    time.sleep(1)
    fb_page = BeautifulSoup(driver.page_source, 'html.parser')

    posts = set()
    while len(posts) <= 5:
        soup=BeautifulSoup(driver.page_source,"html.parser")
        all_posts=soup.find_all("div",{"class":"x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"})
        for post in all_posts:
            try:
                # name=post.find("a",{"class":"x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f"}).get_text()
                post_text=post.find("div", {"class": "xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a"}).get_text()
                posts.add(post_text)
            except:
                post_text="not found"
            # print(post_text)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    driver.quit()

    f = open("./fb/fb.txt","w+")
    analyzer = SentimentIntensityAnalyzer()
    for post in posts:
        vs = analyzer.polarity_scores(post)
        f.write(post)
        f.write(str(vs))
        f.write('\n\n')
        print("{:-<65} {}".format(post, str(vs)))
    f.close()

scrape_fb_group('')