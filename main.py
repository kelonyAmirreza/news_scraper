import os
from sys import argv
from dotenv import load_dotenv
from typing import List, Dict
from datetime import date, timedelta

from newsapi import NewsApiClient
import openai


def main():
    api_client_chosen = init()

    if api_client_chosen == "newsapi":

        articles = news_api_get_articles(["mode", "fashion"])
        for article in articles["articles"]:
            print(article, end="\n"*3)

    else:
        response = openao_get_articles(["mode", "fashion"], "trend")

        for result in response.choices[0].text.split("\n"):
            print(result)


def init() -> str:
    """
        Importing the newsapi API key from the .env file and create the api client
    """

    load_dotenv()

    if len(argv) == 2 and argv[1] == "n":

        global NEWSAPI_API_CLIENT
        NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")
        if not NEWSAPI_API_KEY:
            raise EnvironmentError("NEWSAPI_API_KEY not set correctly")
        NEWSAPI_API_CLIENT = NewsApiClient(api_key=NEWSAPI_API_KEY)

        return "newsapi"

    else:
        OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        if not OPENAI_ORGANIZATION or not OPENAI_API_KEY:
            raise EnvironmentError("OPEN AI API_KEYS not set correctly")

        openai.organization = OPENAI_ORGANIZATION
        openai.api_key = OPENAI_API_KEY

        return "chatgpt"


def news_api_get_articles(keywords: List[str], sources: List[str] = None, domains: List[str] = None,
                          daysBefore: int = 1, lang: str = "en", sort_by='relevancy') -> List[Dict]:
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


def openao_get_articles(keywords: List[str], category: str = "people",
                        model_engine: str = "text-davinci-003", max_tokens: int = 4000, max_results: int = 5):
    """
    Uses OpenAI's GPT-3 API to generate articles related to the given keywords.

    Args:
    keywords: A list of strings representing the keywords related to the article you want to generate.
    category:  A string representing the type of article you want to generate. (optional, Defaults to "people").
                     Only accepts values of "people", "trend", or "history".
    model_engine: A string representing the OpenAI engine used to generate the article. (optional, Defaults to "text-davinci-003").
    max_tokens:  An integer representing the maximum number of tokens used in the generated article. (optional, Defaults to 1024).
    max_results: An integer representing the maximum number of results to return. (optional, Defaults to 5).

    Errors:
    raises ValueError: If an invalid category parameter is provided.

    Returns:
    A dictionary containing the generated article and any other relevant information returned by the OpenAI API.
    """

    if category != "people" and category != "trend" and category != "history":
        raise ValueError(
            "Wrong category selecte. Only (people, trend and history supported)")

    # prompt_people = f"List the what most famous celebrities or influencers related to {keywords} did or wear in the last few days and news around them."
    prompt_people = f"Can you retrieve the latest news and updates related to {keywords} for top celebrities and influencers? Please include any recent fashion choices or noteworthy actions taken by them in the past few days."

    prompt_trend = f"Find the latest trends on {keywords} and see what the trends are saying. and say it in informative tone"

    history_prompt = f"GPT, please find the most significant historical events associated with {keywords} for the leading companies in the sector."

    if category == "people":
        prompt = prompt_people
    elif category == "trend":
        prompt = prompt_trend
    else:
        prompt = history_prompt

    response = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=max_tokens,
                                        n=1, stop=None, temperature=0.5, frequency_penalty=0, presence_penalty=0)

    return response


main()
