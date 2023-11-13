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
