from playwright.sync_api import sync_playwright
import os
import time
import random

replied_tweets = set()

KEYWORDS_PL = [ 
    'imperium', 'wiek', 'historia', 'bitwa', 'sułtan', 'mahpeyker', 'joanne b. mahpeyker', 'elon musk',
    'tesla', 'gork', 'grok', 'sztuczna inteligencja', 'hurrem', 'mahidevran', 'mustafa', 'osman',
    'turcja', 'imperium osmańskie', 'harem', 'osmanowie', 'pałac', 'sarai', 'bot', 'sułtanka', 'sułtanki',
    'śmieszna', 'śmieszny', 'powiedz', 'odpowiedz', 'cześć', 'co słychać', 'słychać', 'czego', 'dlaczego',
    'czemu', 'jak', 'kiedy', 'książka', 'joanna', 'autorka', 'historii', 'historyk', 'szkoła', 'szkole',
    'uczę', 'uczę się', 'czytać', 'pisać', 'komnata', 'król', 'królowa', 'cesarz', 'cesarzowa', 'wezyr',
    'kalif', 'szach', 'władca', 'monarcha', 'regent', 'hetman', 'kanclerz', 'poselstwo', 'sułtański',
    'Hürrem', 'Sulejman', 'Mehmed', 'Selim', 'Osman', 'Halime', 'Nurbanu', 'Roksolana', 'Zygmunt',
    'Jadwiga', 'Kazimierz', 'Władysław', 'Sobieski', 'Bona', 'Barbara Radziwiłłówna', 'biografie', 'elon','musk', 
    "polska", "polityka", "bosak", "mentzen", "korwin mikke", "tusk", "nawrocki"
]

KEYWORDS_EN = [ 
    "empire", "ottoman", "ottoman empire", "age", "era", "history", "historian", "sultan", "dynasty",
    "biography", "biographies", "poland", "turkey", "turkish", "mustafa", "hurrem", "mahidevran", "suleiman",
    "süleyman", "ai", "artificial intelligence", "robot", "book", "joanne", "writer", "author", "elon musk",
    "tesla", "x ai", "xai", "grok", "gork", "chatbot", "tech", "spacex", "mars", "venus", "cosmos", "queen",
    "king", "vizier", "caliph", "emperor", "empress", "palace", "harem", "sultana", "history lover", "timeline",
    "timeline cleanse", "historical", "ottomans", "mehmed", "selim", "osman", "halime", "nurbanu", "roxelana"
]

def contains_keywords(tweet_text):
    text = tweet_text.lower()
    return any(keyword.lower() in text for keyword in KEYWORDS_PL + KEYWORDS_EN)

def generate_reply(tweet_text):
    responses = [
        "Ciekawa myśl. A gdyby tak spojrzeć na to przez pryzmat Imperium Osmańskiego?",
        "Zaintrygowałaś mnie tym. Kiedyś podobnie sądzono na dworze sułtana...",
        "To przypomina mi jedną z historii, które opowiadam w mojej książce.",
        "Czy wiesz, że w Imperium Osmańskim sytuacja wyglądała zupełnie inaczej?",
        "Twoje słowa brzmią jak echo z czasów haremu Topkapi.",
        "Brzmisz jak prawdziwa sułtanka. 👑",
        "Jeśli interesuje Cię historia – zapraszam do mojego świata.",
        "Zainspiruj się przeszłością, by stworzyć przyszłość. MAHPEYKER 🌙"
    ]
    return random.choice(responses)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="storage_state.json")
        page = context.new_page()

        page.goto("https://twitter.com/home")
        time.sleep(10)

        for _ in range(20):
            tweets = page.query_selector_all("article")
            for tweet in tweets:
                try:
                    tweet_text_element = tweet.query_selector("div[lang]")
                    if not tweet_text_element:
                        continue

                    tweet_text = tweet_text_element.inner_text()
                    tweet_id = tweet.get_attribute("data-testid")

                    if tweet_text not in replied_tweets and contains_keywords(tweet_text):
                        tweet.hover()
                        time.sleep(1)

                        reply_button = tweet.query_selector("div[data-testid='reply']")
                        if reply_button:
                            reply_button.click()
                            time.sleep(2)

                            textarea = page.query_selector("div[aria-label='Tweet your reply']")
                            if textarea:
                                reply_text = generate_reply(tweet_text)
                                textarea.fill(reply_text)
                                time.sleep(1)

                                send_button = page.query_selector("div[data-testid='tweetButton']")
                                if send_button:
                                    send_button.click()
                                    print(f"Bot odpowiedział na: {tweet_text}")
                                    replied_tweets.add(tweet_text)
                                    time.sleep(3)
                except Exception as e:
                    print(f"Error: {e}")
            page.keyboard.press("PageDown")
            time.sleep(5)

        browser.close()

if __name__ == "__main__":
    main()
