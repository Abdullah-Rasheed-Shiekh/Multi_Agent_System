from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str)->str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URL and snippets"""
    results=tavily.search(query=query,max_results=5)

    output=[]
    for r in results['results']:
        output.append(
            f"Title: {r['title']}\nURL:{r['url']}\nSnippet:{r['content'][:300]}\n"
        )
    
    return "\n----\n".join(output)

@tool
def scrape_url(url:str)->str:
    """Scrpae and return clean text content from a given URL for deeper reading."""
    try:
        response=requests.get(url,timeout=10,headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text,"html.parser")
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=" ",strip=True)[:3000]
    except Exception as e:
        return f"Could Not Scrape Url:{str(e)}"

