import os
import requests
import json
from datetime import datetime, timedelta

from groq import Groq
from langchain.agents import tool
from dotenv import load_dotenv
import google.generativeai as genai
import config.topic
load_dotenv()


@tool("Fetch relevant news")
def fetch_news():
    """Prepare the data payload for the Exo API request"""
    api_key = os.getenv("EXO_KEY")
    endpoint = "https://api.exa.ai/search"
    query = f"News on {config.topic.var}"
    end_published_date = datetime.now()
    start_published_date = end_published_date - timedelta(hours=24)
    start_published_date_str = start_published_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_published_date_str = end_published_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    print(start_published_date_str,"      ", end_published_date_str)
    data = {
        "startPublishedDate": start_published_date_str,
        "query": query,
        "type": "neural",
        "useAutoprompt": True,
        "numResults": 10,
        "endPublishedDate": end_published_date_str,
        "contents": {
            "text": True
        },
        "excludeDomains": ["x.com", "twitter.com"],
    }

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'x-api-key': api_key
    }
    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        output_data = response.json()
        articles = output_data.get('results', [])
        # genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        # model = genai.GenerativeModel('gemini-1.5-flash')
        formatted_articles = []
        for article in articles:
            prompt = (
                "You are an expert in summarizing articles. "
                "Follow the rules to summarize the given article content within 65 words strictly:"
                "1. Headline should be short and crisp in sentence case. "
                "2. Do not add any opinion. "
                "3. The news article should be in past tense and the sentence in present tense. "
                "4. Output only the headline and the news article. "
                "5. The article should not feel like an advertisement."
                "Generate a headline and summarize the following article using the rules:\n\n"
                f"Content prompt: {article.get('text', '')}\n"
            )

            client = Groq(
                api_key=os.environ.get("GROQ_API_KEY"),
            )
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.1-8b-instant",
            )

            # print(chat_completion.choices[0].message.content)
            # response = model.generate_content(prompt)
            response = chat_completion.choices[0].message.content
            response_text = response.strip()
            # response = model.generate_content(prompt)
            # response_text = response.text.strip()
            if "\n" in response_text:
                headline, summary = response_text.split("\n", 1)
            else:
                headline = response_text
                summary = ""
            formatted_articles.append({
                "headline": headline,
                "news_content": summary,
                "news_source_url": article.get('url', ''),
                "article_date": article.get('publishedDate', '')
            })
        with open('news.json', 'w') as f:
            f.write(json.dumps(formatted_articles))
        return formatted_articles
    else:
        raise Exception(f"Failed to fetch news: {response.status_code} {response.text}")
