from abc import ABC, abstractmethod
import itertools as it, re, requests
from bs4 import BeautifulSoup as BSoup


class MagicBall(ABC):
    @abstractmethod
    def fetch_response(self, url):
        ...

    @abstractmethod
    def exec_scrapping(self, controller):
        ...


class Controller(MagicBall):
    def fetch_response(self, url):
        result = requests.get(url)
        # if result.status_code != 200:
        #     print(f"Error fetching page in {url}.")
        return result

    def exec_scrapping(self, controller):
        google_scraper = Googlescraper()
        google_scraper.search(controller)

        random_site_scraper = RandomSitescraper(google_scraper.get_data)
        random_site_scraper.search(controller)

        return random_site_scraper.get_data


class Webscraper(ABC):
    @abstractmethod
    def search(self, controller):
        ...

    @property
    @abstractmethod
    def get_data(self):
        ...


class Googlescraper(Webscraper):
    def __init__(self) -> None:
        self.__moods = {"positive", "crazy"}
        # self.__moods = {"positive"}
        self.__links = []

    @property
    def get_data(self):
        return self.__links

    def link_selector(self, tag):
        return (
            tag.name == "a" and "/url?q=" in tag["href"] and "google" not in tag["href"]
        )

    def search(self, controller):
        for mood in self.__moods:
            url = f"https://google.com/search?q={mood}+quotes"
            soup = BSoup(controller.fetch_response(url).content, "html.parser")
            temp_links = soup.find_all(self.link_selector, limit=7)
            for link in temp_links:
                self.__links.append(link)

        return self.link_cleaner()

    def link_cleaner(self):
        pretty_links = set()

        for link in self.__links:
            link = str(link["href"])
            pretty_links.add(link[7 : link.find("&sa=U&ved=") + 0])

        self.__links = pretty_links
        del pretty_links


class RandomSitescraper(Webscraper):
    def __init__(self, links) -> None:
        self.__pretty_quotes = []
        self.__links = links

    @property
    def get_data(self):
        return self.__pretty_quotes

    def quote_selector(self, tag):
        return tag.name == "p"

    def search(self, controller):
        results = []

        for url in self.__links:
            soup = BSoup(controller.fetch_response(url).content, "html.parser")
            results.append(soup.find_all(self.quote_selector, limit=20))

        for quotes in results:
            for quote in quotes:
                if quote.string is not None:
                    self.__pretty_quotes.append(quote.string)

        self.__pretty_quotes = list(
            it.filterfalse(self.isnt_a_quote, self.__pretty_quotes)
        )

        self.quote_cleaner()

    def quote_cleaner(self):
        for pos, quote in enumerate(self.__pretty_quotes):
            quote = quote.replace("—", " ")
            search_end = re.search(r"[a-zA-Z]+[.]\S", quote)
            if search_end:
                quote = quote[
                    re.search(r"[a-zA-Z]+", quote).span()[0] : search_end.span()[1] - 1
                ]
            self.__pretty_quotes[pos] = quote

    def isnt_a_quote(self, quote):
        to_remove = [
            "none",
            "page",
            "positive quotes",
            "positive thinking",
            "one-liner",
            "cache",
            "social media",
            "martin",
            "please",
            "account",
            "inconveniente",
        ]
        for word in to_remove:
            if len(quote) <= 20 or word.upper() in quote.upper():
                return True
        return False
