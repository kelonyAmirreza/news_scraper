import os
from sys import argv
from dotenv import load_dotenv
from typing import List, Dict
from datetime import date, timedelta

from newsapi import NewsApiClient


def main():
    init()

    print(news_api_get_articles(["mode", "fashion"]))
    # for article in all_articles["articles"]:
    #     print(article, end="\n"*3)


def init():
    load_dotenv()

    if len(argv) == 2 and argv[1] == "n":
        """
        Importing the newsapi API key from the .env file and create the api client
        """

        global NEWSAPI_API_CLIENT
        NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")
        if not NEWSAPI_API_KEY:
            raise EnvironmentError("NEWSAPI_API_KEY not set correctly")
        NEWSAPI_API_CLIENT = NewsApiClient(api_key=NEWSAPI_API_KEY)

    elif len(argv) == 2 and argv[1] == "c":
        """
        Importing the newsapi API key from the .env file and create the api client
        """
        print(2)


def news_api_get_articles(keywords: List[str], sources: List[str] = None, domains: List[str] = None, daysBefore: int = 1, lang: str = "en", sort_by='relevancy') -> List[Dict]:
    """
    Returns a list of news articles related to the given search keyword.

    Args:
        keywords: A list of strings containing the keywords to search for.
        sources: A list of sources to search (optional, defaults to None).
        domains: A list of domains to search (optional, defaults to None).
        days_before: An integer representing how many days before the current date to search for articles (optional, defaults to 1 day).
        lang: A string representing the language of the articles to search for (optional, defaults to "en").
        sort_by: A string representing how to sort the results (optional, defaults to "relevancy").

    Returns:
        A list of dictionaries representing news articles.
    """
    if sources is None:
        sources = []
    if domains is None:
        domains = []
    fromDate = date.today() - timedelta(daysBefore)

    articles = NEWSAPI_API_CLIENT.get_everything(q=" ".join(keywords),
                                                 sources=",".join(sources),
                                                 domains=",".join(domains),
                                                 from_param=fromDate,
                                                 language=lang,
                                                 sort_by=sort_by)
    return articles


main()
