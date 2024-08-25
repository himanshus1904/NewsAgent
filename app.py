import streamlit as st
from crewai import Crew, Process
from config.agents import ai_news_fetcher, finance_news_fetcher
from config.tasks import ai_fetch_news_task, finance_fetch_news_task
import json
import config.topic
import requests, json
from bs4 import BeautifulSoup


def image_extractor():
    with open('news.json', 'r') as file:
        data = json.load(file)
    for entry in data:
        url = entry['news_source_url']
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        og_images = soup.find_all('meta', property='og:image')
        og_image_urls = [img['content'] for img in og_images]
        entry['img_url'] = og_image_urls
    with open('news.json', 'w') as file:
        json.dump(data, file, indent=4)


def generate_news(topic):
    config.topic.var = topic
    if config.topic.var == "Artificial Intelligence":
        news_crew = Crew(
            agents=[ai_news_fetcher],  # , news_formatter],
            tasks=[ai_fetch_news_task],  # , format_news_task],
            process=Process.sequential
        )
    else:
        news_crew = Crew(
            agents=[finance_news_fetcher],  # , news_formatter],
            tasks=[finance_fetch_news_task],  # , format_news_task],
            process=Process.sequential
        )
    news_crew.kickoff()

    image_extractor()
    with open('news.json', 'r') as f:
        updated_data = json.load(f)

    return updated_data


def display_news(news_data):
    for entry in news_data:
        st.markdown(f"### {entry['headline']}")
        st.markdown(entry['news_content'])
        st.markdown(entry['news_source_url'])
        st.markdown(entry['article_date'])
        if 'img_url' in entry:
            for img_url in entry['img_url']:
                st.image(img_url, use_column_width=True)
        st.markdown("---")  # Separator between news entries


if __name__ == '__main__':
    st.title("News Generator")
    st.header("Generate News")
    st.write("Choose a category below to generate the latest news.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("AI"):
            news_data = generate_news("Artificial Intelligence")
            if news_data:
                st.subheader("AI News")
                display_news(news_data)

    with col2:
        if st.button("Finance"):
            news_data = generate_news("Indian Finance and Stock Market")
            if news_data:
                st.subheader("Finance News")
                display_news(news_data)






