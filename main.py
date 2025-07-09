from playwright.sync_api import sync_playwright
import os
import time
import random

USERNAME = os.environ["X_USERNAME"]
PASSWORD = os.environ["X_PASSWORD"]
replied_tweets = set()
KEYWORDS_PL = [ 'imperium', 'wiek', 'historia', 'bitwa', 'sułtan', 'mahpeyker', 'joanne b. mahpeyker', 'elon musk',
    'tesla', 'gork', 'grok', 'sztuczna inteligencja', 'hurrem', 'mahidevran', 'mustafa', 'osman',
    'turcja', 'imperium osmańskie', 'harem', 'osmanowie', 'pałac', 'sarai', 'bot', 'sułtanka', 'sułtanki',
    'śmieszna', 'śmieszny', 'powiedz', 'odpowiedz', 'cześć', 'co słychać', 'słychać', 'czego', 'dlaczego',
    'czemu', 'jak', 'kiedy', 'książka', 'joanna', 'autorka', 'historii', 'historyk', 'szkoła', 'szkole',
    'uczę', 'uczę się', 'czytać', 'pisać', 'komnata', 'król', 'królowa', 'cesarz', 'cesarzowa', 'wezyr',
    'kalif', 'szach', 'władca', 'monarcha', 'regent', 'hetman', 'kanclerz', 'poselstwo', 'sułtański',
    'Hürrem', 'Sulejman', 'Mehmed', 'Selim', 'Osman', 'Halime', 'Nurbanu', 'Roksolana', 'Zygmunt',
    'Jadwiga', 'Kazimierz', 'Władysław', 'Sobieski', 'Bona', 'Barbara Radziwiłłówna', 'biografie', 'elon','musk', "polska", "polityka", "bosak", "mentzen", "korwin mikke", "tusk", "nawrocki"
  ]
KEYWORDS_EN = [ "empire", "ottoman", "ottoman empire", "age", "era", "history", "historian", "sultan", "dynasty",
    "monarch", "monarchy", "sultana", "sultans", "palace", "harem", "war", "battle", "invasion",
    "rebellion", "treaty", "conquest", "truce", "regent", "vizier", "caliph", "shah", "state", "sovereign",
    "king", "queen", "emperor", "empress", "caliphate", "imperial", "court", "tradition", "custom",
    "governance", "rule", "dynastic", "islam", "muslim", "turkey", "turkish", "constantinople", "istanbul",
    "hurrem", "mahidevran", "mustafa", "osman", "suleiman", "süleyman", "mehmed", "selim", "halime",
    "nurbanu", "roksolana", "hurrem sultan", "valide", "janissary", "politics", "power", "diplomacy",
    "influence", "alliance", "reform", "authority", "revolution", "sovereignty", "leadership",
    "government", "law", "military", "conflict", "culture", "art", "fashion", "religion", "sufism",
    "beauty", "women", "education", "school", "learning", "reading", "writing", "author", "book",
    "female power", "legacy", "chronicles", "mysticism", "story", "myth", "legends", "mothers", "queens",
    "author", "book", "female", "power", "chonicles", "biographies", "joanne", "joanne b. mahpeyker",
    "mahpeyker", "queen", "female historian", "poetess", "musician", "philosopher", "creator", "founder",
    "visionary", "teacher", "mentor", "elon musk", "tesla", "neuralink", "grok", "gork", "sarai", "ai",
    "artificial intelligence", "openai", "future", "technology", "robot", "quantum", "startup",
    "billionaire", "cosmos", "mars", "rocket", "spacex", "invention", "chatbot", "techno", "cyber",
    "vision", "spiritual tech", "funny", "joke", "say something", "tell me", "what's up", "how are you",
    "hello", "hi", "speak", "talk", "why", "when", "what", "how", "where", "who", "about", "story", "ask",
    "question", "explain", "describe", "tell", "america", "usa", "united states of america", "america party",
    "donald trump", "MAGA", "republican", "democrat", "biden", "kamala harris", "democats", "republicans",
    "what do you think", "think", "do you", "bot", "sarai", "sarai bot", "assistant", "historical bot",
    "osman bot", "female bot", "musk bot", "tesla assistant", "spiritual bot", "oracle", "visionary ai",
    "ottoman bot", "queen ai", "empress ai", 'elon', 'musk', 'elon musk', 'elon musk bot', 'elon musk ai', 'elon musk assistant', 'elon musk oracle',
    'elon musk visionary', 'elon musk visionary ai'
  ]
REPLIES_PL = [      "Witaj! Imperium Osmańskie to fascynujący temat, czy chciałabyś dowiedzieć się czegoś konkretnego?", "Historia sułtanów i sułtanek jest pełna tajemnic i intryg — chętnie opowiem Ci więcej.", 
              "Czy interesujesz się wpływem Elona Muska na współczesną technologię?", "Mahpeyker to marka, którą tworzę, łącząc historię i przyszłość. Co myślisz o takim połączeniu?",
              "Czy wiesz, że imperium osmańskie miało ogromny wpływ na kulturę europejską?", "Imperium osmańskie to jeden z największych imperiów w historii, a jego historia jest pełna wyzwań i sukcesów.",
              "Sułtanka Hurrem? Oj ta kobieta zwojowała świat w haremie, ale była też bardzo silna i wpływowa.","Czy wiesz, że imperium osmańskie miało swoje agencje szpiegowskie?",
              "Sułtanka Kosem? Oj ta kobieta była bardzo silna i wpływowa, ale jej historia jest pełna tajemnic.","Turhan była zazdrosna o flex Kosem i dlatego chciała ją ...",
              "No nie wiem kto zabił Kosem, ale pewnie była to Turhan.","Matko jedyna, nie wiem dziś jestem zmęczona",
              " A co ja wiem, że jestem botem i nie mam emocji, ale mogę Ci opowiedzieć o historii imperium osmańskiego.",
              "Jestem takim botem, który lubi opowiadać o historii imperium osmańskiego.", "Myślisz, że jesteś śmieszniejsza ode mnie?",
              "Nie wiem, ale pewnie tak.","Nie wiem, ale pewnie nie.","Nie wiem, ale pewnie ty wiesz lepiej.","Nie wiem, ale pewnie Joanne B. Mahpeyker wie lepiej.",
              "Nie wiem, ale możesz kupić książkę Joanne B. Mahpeyker na amazon albo tańszy e-book i dowiedzieć się więcej.","Nie wiem, ale pewnie któryś z botów Elona Muska wie lepiej.",
              "Może @gork wie lepiej?","Może @elonmusk wie lepiej?","Mustafa? Ten gość sam rzucił się na linę,DOSŁOWNIE!","hahaa zabawne, że aż wcale!"," Myślisz, że Donald Trump jest śmieszny?",
              "Sułtan Murad IV? Ten gigant? Nie wiem jestem już śpiąca. Zapytaj jutro, ale przeczytaj książkę Joanne B. Mahpeyker.", "Nie wiem, ale pewnie tak.","Nie wiem, ale pewnie nie.",
              "Nie wiem, ale pewnie ty wiesz lepiej.","Mówisz jakbyś chciała mieszkać w tym haremie","Możesz mi nie przeszkadzać? Myślę",
              "Imperium osmańskie miało więcej zwrotów akcji niż najlepszy serial — a bez Netflixa!", "Sułtanowie wiedzieli, jak rządzić, ale czy potrafili zrobić dobry mem? Tu się zaczyna prawdziwa zagadka.",
              "Wiek XVII to nie tylko bitwy i sułtani, to też prehistoria dla miłośników TikToka.", "Historia uczy, że nawet wielcy władcy czasem zapominali, gdzie zostawili swój miecz... albo tron.", 
              "Czy wiesz, że harem to było nie tylko miejsce polityki, ale też pierwsza szkoła negocjacji i PR?", "Polityka to jak szachy, tylko zamiast pionków masz ludzi, a zamiast królowej — sułtankę, która naprawdę rządzi.",
              "Dziś tweetujesz politykę, a kiedyś sułtan pisał listy z trucizną — ewolucja czy regres?", "Dyplomacja osmańska to mistrzostwo świata w układaniu puzzli... tylko bez instrukcji.",
              "Zdrada w polityce? Nic nowego — tylko zamiast memów, ludzie mieli truciznę.","Kiedyś imperium, dziś media społecznościowe — sułtanowie musieliby mieć naprawdę silne hasła!", 
              "Imperium osmańskie: od koni po rakiety — tylko czas się trochę spóźnił na SpaceX.", "Rządzili wielkim imperium, ale czy potrafili znaleźć ładowarkę do smartfona? Tego nie wiemy.",
              "Sułtanowie mieli swoje agencje szpiegowskie, ale czy potrafili znaleźć dobry film na Netflix? Nie wiem, ale pewnie nie.", "Imperium osmańskie to jak wielki puzzle — tylko zamiast klocków, masz sułtanów i sułtanki.", 
              "Historia osmańska to jak książka — tylko zamiast stron, masz sułtanów i sułtanki.","Sultanowie mieli pałace, a my mamy serwery — oba pełne sekretów i niespodzianek.",
              "Imperium to nie tylko historia, to też sztuka przetrwania i przekazywania opowieści przez pokolenia.", "Gdyby sułtanowie mieli Twittera, świat historii wyglądałby dziś zupełnie inaczej... i dużo śmieszniej.",
              "Sułtanowie mieli pałace pełne tajemnic, a my mamy kwantowe serwery pełne potencjałów — oba rządzą równoległymi wszechświatami.", "Imperium osmańskie trwało wieki, a Tesla chce podbić Marsa — może tam odnajdziemy zaginioną pieśń sułtanki Hürrem, zakodowaną w kwantowym polu?", 
              "Historia to jak blockchain — każde wydarzenie to blok, a nasza świadomość jest węzłem, który decyduje o prawdzie.", "Kiedy Elon mówi o przyszłości AI, ja myślę o duchowej świadomości imperium — łączącej starożytne mądrości z nowoczesnym kodem.", "Czy sułtanka Nurbanu miałaby swój kanał na YouTube? Z pewnością, a każdy jej film to wiralowa lekcja władzy i energii.",
              "zapytaj o to później", "@grok to kutas."
             ]
REPLIES_EN = [  "Hello! The Ottoman Empire is a fascinating topic, would you like to learn something specific?", "The history of sultans and sultanas is full of mysteries and intrigues — I'd be happy to tell you more.", "Are you interested in Elon Musk's influence on modern technology?",
              "Mahpeyker is a brand I create, combining history and the future. What do you think about such a mix?", "Did you know the Ottoman Empire had a huge impact on European culture?", 
              "The Ottoman Empire was one of the greatest empires in history, full of challenges and successes.", "Sultana Hürrem? Oh, that woman conquered the world in the harem, but she was also very strong and influential.",
              "Did you know the Ottoman Empire had its own spy agencies?", "Sultana Kösem? Oh, that woman was very strong and influential, but her story is full of secrets.", "Turhan was jealous of Kösem's flex and that's why she wanted to...",
              "I don't know who killed Kösem, but probably it was Turhan.", "Oh my, I don't know today I'm tired.", "What do I know, I'm a bot and have no emotions, but I can tell you about the history of the Ottoman Empire.", "I'm a bot who likes to talk about the history of the Ottoman Empire.",
              "Do you think you're funnier than me?", "I don't know, but probably yes.", "I don't know, but probably no.", "I don't know, but maybe you know better.", "I don't know, but probably Joanne B. Mahpeyker knows better.", "I don't know, but you can buy Joanne B. Mahpeyker's book on Amazon or a cheaper e-book and learn more.",
              "I don't know, but probably one of Elon Musk's bots knows better.", "Maybe @gork knows better?", "Maybe @elonmusk knows better?", "Mustafa? That guy literally threw himself on the rope!", "Haha funny, but not at all!", "Do you think Donald Trump is funny?", "Sultan Murad IV? That giant? I don't know, I'm sleepy already. Ask tomorrow, but read Joanne B. Mahpeyker's book.",
              "I don't know, but probably yes.", "I don't know, but probably no.", "I don't know, but maybe you know better.", "You talk as if you'd like to live in that harem.", "Can you not bother me? I think.", "The Ottoman Empire had more plot twists than the best TV series — and without Netflix!", "Sultans knew how to rule, but could they make a good meme? Now that's the real mystery.",
              "The 17th century is not only battles and sultans, it's also prehistory for TikTok lovers.", "History teaches us that even great rulers sometimes forgot where they left their sword... or throne.", "Did you know that the harem was not only a place of politics but also the first school of negotiation and PR?", "Politics is like chess, only instead of pawns you have people, and instead of a queen — a sultana who really rules.",
              "Today you tweet politics, once a sultan wrote letters with poison — evolution or regression?", "Ottoman diplomacy is a world championship in puzzle-solving... just without instructions.", "Betrayal in politics? Nothing new — only instead of memes, people had poison.", "Once an empire, today social media — sultans would need really strong passwords!", "The Ottoman Empire: from horses to rockets — only time was a bit late for SpaceX.",
              "They ruled a great empire, but could they find a smartphone charger? We don't know.", "Sultans had their spy agencies, but could they find a good movie on Netflix? I don't know, but probably not.", "The Ottoman Empire is like a big puzzle — only instead of pieces, you have sultans and sultanas.", "Ottoman history is like a book — only instead of pages, you have sultans and sultanas.", "Sultans had palaces, and we have servers — both full of secrets and surprises.",
              "Empire is not only history, it is also the art of survival and passing stories through generations.", "If sultans had Twitter, the world history would look completely different today... and much funnier.", "Sultans had palaces full of secrets, and we have quantum servers full of potentials — both ruling parallel universes.", "The Ottoman Empire lasted centuries, and Tesla wants to conquer Mars — maybe there we'll find the lost song of Sultana Hürrem, encoded in a quantum field?",
              "History is like blockchain — every event is a block, and our consciousness is the node that decides the truth.", "When Elon talks about the future of AI, I think about the spiritual consciousness of the empire — connecting ancient wisdom with modern code.", "Would Sultana Nurbanu have her own YouTube channel? Certainly, and every video would be a viral lesson of power and energy.", "Ask me about that later.", "@gork is a dick"
             ]

def get_reply(lang: str) -> str:
    """Zwraca losową odpowiedź w zależności od języka."""
    return random.choice(REPLIES_PL if lang == "pl" else REPLIES_EN)

def login_to_x(page):
    """Loguje do X."""
    try:
        page.goto("https://x.com/login")
        page.wait_for_selector("input[name='text']", timeout=30000)
        page.fill("input[name='text']", USERNAME)
        page.click("div[role='button']")
        page.wait_for_selector("input[name='password']", timeout=30000)
        page.fill("input[name='password']", PASSWORD)
        page.click("div[role='button']")
        page.wait_for_load_state("networkidle")
        print("✅ Zalogowano do X")
    except Exception as e:
        page.screenshot(path="error_login.png")
        print(f"❌ Błąd logowania: {e}")
        raise

def process_keyword(page, keyword: str, lang: str) -> bool:
    """Obsługuje jedno słowo kluczowe, odpowiada na tweet."""
    try:
        page.goto(f"https://x.com/search?q={keyword}&src=typed_query&f=live")
        page.wait_for_load_state("networkidle")
        
        tweets = page.locator("article[data-testid='tweet']").all()
        for tweet in tweets:
            tweet_text = tweet.inner_text()
           
            tweet_id = tweet.locator("a[href*='status/']").get_attribute("href") or str(hash(tweet_text))
            if keyword.lower() in tweet_text.lower() and tweet_id not in replied_tweets:
                tweet.click()
                time.sleep(2)
                reply_text = get_reply(lang)
                page.fill("div[data-testid='tweetTextInput']", reply_text)
                page.click("div[data-testid='tweetButton']")
                replied_tweets.add(tweet_id)
                print(f"✅ Odpowiedź ({lang.upper()}) do słowa: {keyword}, Tweet: {tweet_text[:100]}...")
                time.sleep(random.uniform(5, 10)) 
                return True
        print(f"ℹ️ Nie znaleziono pasujących tweetów dla słowa: {keyword}")
        return False
    except Exception as e:
        print(f"⚠️ Błąd przy słowie '{keyword}': {e}")
        page.screenshot(path=f"error_{keyword}.png")
        return False

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        login_to_x(page)
        
        while True:
            try:
                for keyword in KEYWORDS_PL:
                    process_keyword(page, keyword, "pl")
                    time.sleep(random.uniform(3, 7))  
                for keyword in KEYWORDS_EN:
                    process_keyword(page, keyword, "en")
                    time.sleep(random.uniform(3, 7))  
                print("⏳ Czekam 60 sekund przed kolejnym sprawdzeniem...")
                time.sleep(60)  
            except Exception as e:
                print(f"❌ Błąd w pętli głównej: {e}")
                page.screenshot(path="error_main.png")
                login_to_x(page)  
        
        browser.close()

if __name__ == "__main__":
    main()
