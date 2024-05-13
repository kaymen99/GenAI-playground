import os, json, re, requests
from langchain_core.agents import tool
from bs4 import BeautifulSoup

class SearchTools():

  @tool("Search internet")
  def search_internet(query):
    """Useful to search the internet about a given topic and return relevant
    results."""
    return SearchTools.search(query)

  @tool("Search medium blog")
  def search_medium(query):
    """Useful to search for medium posts about a given topic and return relevant
    results."""
    query = f"site:medium.com {query}"
    return SearchTools.search(query)

  def search(query, n_results=10):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()['organic']
    strings = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    for result in results[:n_results]:
        url = result['link']

        # scrape the page content
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.get_text()

        # normalize whitespaces and cleanup text
        content = re.sub("\s+", " ", content).strip()

        try:
            strings.append('\n'.join([
                f"Title: {result['title']}",
                            f"Link: {result['link']}",
                f"Content: {content}",
                            "\n"
            ]))
        except KeyError:
            next

    content = '\n'.join(strings)
    return f"\nSearch result: {content}\n"