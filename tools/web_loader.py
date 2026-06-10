from langchain_community.document_loaders import WebBaseLoader
import bs4

def load_web_content(urls: list):
    """
    Load web content from a list of URLs using WebBaseLoader.
    """
    if not urls:
        return []

    try:
        loader = WebBaseLoader(
            web_paths=urls,
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    ["h1", "h2", "h3", "p", "article"]
                )
            ),
            requests_kwargs={
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                }
            }
        )
        docs = loader.load()
        return docs
    except Exception as e:
        print(f"[WebBaseLoader Error] {e}")
        return []

def get_links_from_web(hub_url: str):
    """
    Extract all article-like links from a hub page using WebBaseLoader.
    """
    try:
        loader = WebBaseLoader(
            web_paths=[hub_url],
            requests_kwargs={
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                }
            }
        )
        doc = loader.load()[0]
        from bs4 import BeautifulSoup
        import requests
        
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(hub_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True)
            if len(text) > 20 and (href.startswith('http') or href.startswith('/')):
                if href.startswith('/'):
                    from urllib.parse import urljoin
                    href = urljoin(hub_url, href)
                links.append({"title": text, "url": href, "content": text})
        
        return links[:20] 
    except Exception as e:
        print(f"[Link Extraction Error] {e}")
        return []
