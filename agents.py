import os
from crewai import Agent
from tools.fetch_news_tool import fetch_news
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()


ai_news_fetcher = Agent(
    role='News Fetcher',
    goal='Fetch the latest news articles on Artificial Intelligence',
    tools=[fetch_news],
    verbose=True,
    backstory=(
        "You are a seasoned journalist with a keen eye for news, "
        "and you always ensure that the latest information is brought to light."
    ),
    llm=ChatGoogleGenerativeAI(google_api_key=os.getenv("GOOGLE_API_KEY"), model="gemini-1.5-flash")
)

finance_news_fetcher = Agent(
    role='News Fetcher',
    goal='Fetch the latest news articles on Indian FinancialMarket',
    tools=[fetch_news],
    verbose=True,
    backstory=(
        "You are a seasoned journalist with a keen eye for news, "
        "and you always ensure that the latest information is brought to light."
    ),
    llm=ChatGoogleGenerativeAI(google_api_key=os.getenv("GOOGLE_API_KEY"), model="gemini-1.5-flash")
)

