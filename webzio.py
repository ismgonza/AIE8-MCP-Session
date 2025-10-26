import requests
from dotenv import load_dotenv
import os

load_dotenv()

class Webzio:
    def __init__(self, query: str, sentiment: str, language: str = "english"):
        self.url = "https://api.webz.io/newsApiLite"
        self.query = query
        self.sentiment = sentiment
        self.language = language
        self.params = {
            "token": os.getenv('WEBZIO'),
            "q": query,
            "sentiment": sentiment,
            "language": language
        }

    def get_news(self):
        response = requests.get(self.url, params=self.params)
        return response.json()

    def __str__(self):
        try:
            news_data = self.get_news()
            total_results = news_data.get('totalResults', 0)
            posts = news_data.get('posts', [])
            requests_left = news_data.get('requestsLeft', 'N/A')
            
            result = f"Query: '{self.query}' | Sentiment: {self.sentiment} | Language: {self.language}\n"
            result += f"Total Results: {total_results}\n"
            result += f"Posts Retrieved: {len(posts)}\n"
            result += f"API Requests Left: {requests_left}\n"
            
            if posts:
                result += "\nTop Articles:\n"
                for i, post in enumerate(posts[:5], 1):
                    title = post.get('title', 'No title')
                    url = post.get('url', 'No URL')
                    result += f"{i}. {title}\n   URL: {url}\n"
            
            return result
        except Exception as e:
            return f"Error fetching news: {str(e)}"

if __name__ == "__main__":
    query = input("Enter search query: ")
    sentiment = input("Enter sentiment (positive/negative/neutral): ") or "neutral"
    language = input("Enter language (default: english): ") or "english"
    webzio = Webzio(query, sentiment, language)
    print(webzio)