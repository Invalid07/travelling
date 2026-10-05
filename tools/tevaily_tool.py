import os 
import requests
from dotenv import load_dotenv
from tavily import TavilyClient
load_dotenv()

client = TavilyClient(api_key=os.getenv("tavilt_api"))

def tavily_search(query:str):
    responds = client.search(
                         query=query,
                         max_results=7
                            )
    results=[]

    for i, r in enumerate(responds["results"], 1):
        title   = r.get("title", "Unknown")
        url     = r.get("url", "")
        snippet = r.get("content", "").strip()
        if len(snippet) > 300:
            snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

        results.append(f"{i}. **{title}**\n   {url}\n   {snippet}")

    return "\n\n".join(results)