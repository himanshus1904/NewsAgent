from crewai import Task
from config.agents import ai_news_fetcher, finance_news_fetcher



# Fetch News Task
ai_fetch_news_task = Task(
    description=(
        "Fetch the latest news articles on Artificial Intelligence. Ensure the articles are relevant to the topic"
    ),
    expected_output='News articles',
    agent=ai_news_fetcher
)

finance_fetch_news_task = Task(
    description=(
        "Fetch the latest news articles on Indian Financial Market. Ensure the articles are relevant to the topic"
    ),
    expected_output='News articles',
    agent=finance_news_fetcher
)



