import feedparser
import logging
from urllib.parse import urlparse
from favicon_storage import FaviconStorage
from settings import RSS_FEEDS

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def extract_domain(url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        if domain.startswith("www."):
            domain = domain[4:]
        return domain

def get_high_res_favicon(url):
    # Fake a Browser User-Agent 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        candidates = []

        # common rels: icon, shortcut icon, apple-touch-icon, apple-touch-icon-precomposed
        tags = soup.find_all('link', rel=lambda x: x and ('icon' in x.lower() or 'apple-touch' in x.lower()))

        for tag in tags:
            href = tag.get('href')
            if not href:
                continue

            # Full absolute URL
            full_url = urljoin(url, href)
            
            # Get size info
            sizes = tag.get('sizes') # e.g., "192x192" or "any"
            rel = str(tag.get('rel')).lower()

            # score for sorting
            score = 0
            
            if sizes == "any":
                score = 999999 # SVG/Vector is best
            elif sizes:
                # Parse "192x192" -> 192 * 192 = 36864
                # Sometimes sizes has multiple (e.g. "32x32 64x64"), taking the last/largest
                try:
                    dimensions = sizes.split(' ')[-1] 
                    w, h = map(int, dimensions.split('x'))
                    score = w * h
                except:
                    score = 0
            
            # Boost score for apple-touch-icon if no size is present (usually 180x180)
            if score == 0 and 'apple-touch' in rel:
                score = 180 * 180 

            candidates.append({'url': full_url, 'score': score, 'sizes': sizes or "unknown"})

        # fallback to google favicon service
        if not candidates:
            domain = extract_domain(url)
            logger.info(f"  -> Falling back to Google API for {domain}")
            return f"https://www.google.com/s2/favicons?domain={domain}&sz=512"

        # Sort: Highest score first
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        # 4. Return the winner
        best_icon = candidates[0]
        logger.info(f"Winner for {url}:")
        logger.info(f"  -> URL: {best_icon['url']}")
        logger.info(f"  -> Size: {best_icon['sizes']} (Score: {best_icon['score']})")

        return best_icon['url']

    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None

        

def discover_and_populate_favicons_from_feed():
    storage = FaviconStorage()
    unique_domains = set()

    for feed_config in RSS_FEEDS:
        url = feed_config["url"]
        feed = feedparser.parse(url)

        # Checks the Feed's own link (Good for Mint/ET)
        if 'link' in feed.feed:
            root = extract_domain(feed.feed.link)
            if root: unique_domains.add(root)

        for entry in feed.entries:
             if 'source' in entry and 'href' in entry.source:
                source_url = entry.source.href
                domain = extract_domain(source_url)
                if domain:
                    unique_domains.add(domain)


    for domain in unique_domains:
        if storage.get_favicon(domain):
            continue
        
        full_url = "https://" + domain
        try:
            favicon_url = get_high_res_favicon(full_url)
            if favicon_url:
                storage.store_favicon(domain, favicon_url)
            else:
                logger.warning(f"⚠️  No icon found for {domain}")
        except Exception as e:
            logger.error(f"Error processing domain {domain}: {e}")

        

if __name__ == "__main__":
    discover_and_populate_favicons_from_feed()