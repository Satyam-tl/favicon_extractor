from pymongo import MongoClient
from settings import settings
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class FaviconStorage:
    def __init__(self):
        self.mongo_client = MongoClient(settings.MONGODB_URL)
        self.database = self.mongo_client[settings.DATABASE_NAME]
        self.collection = self.database[settings.COLLECTION_NAME]

        self.collection.create_index("domain", unique=True)

    def extract_domain(self, url):
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc

            if domain.startswith("www."):
                domain = domain[4:]
            return domain
        except Exception as e:
            print(f"Error extracting domain from {url}: {e}")
            return None
        
    def store_favicon(self, url, favicon_url):
        domain = self.extract_domain(url)
        if not domain:
            return

        document = {
            "domain": domain,
            "favicon_url": favicon_url
        }

        try:
            result = self.collection.update_one(
                {"domain": domain},
                {"$set": document},
                upsert=True
            )

            if result.upserted_id:
                logger.info(f"New source registered: {domain}")
            elif result.modified_count > 0:
                logger.info(f"Updated existing source: {domain}")
            else:
                logger.info(f"Source already up to date: {domain}")

        except Exception as e:
            print(f"Error storing favicon for {domain}: {e}")

    def get_favicon(self, url):
        domain = self.extract_domain(url)
        if not domain:
            return None

        try:
            document = self.collection.find_one({"domain": domain})
            if document:
                return document.get("favicon_url")
            else:
                return None
        except Exception as e:
            logger.info(f"Error retrieving favicon for {domain}: {e}")
            return None
        
    

