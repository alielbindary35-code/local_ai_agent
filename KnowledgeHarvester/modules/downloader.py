import os
import time
import requests
import logging
from urllib.parse import urlparse, unquote

class Downloader:
    def __init__(self, config):
        self.config = config
        self.settings = config.get('download_settings', {})
        self.headers = {
            'User-Agent': self.settings.get('user_agent', 'KnowledgeHarvester/1.0')
        }
        self.timeout = self.settings.get('timeout_seconds', 30)
        self.max_retries = self.settings.get('max_retries', 3)
        self.delay = self.settings.get('delay_between_requests', 1.0)
        self.logger = logging.getLogger(__name__)

    def download_file(self, url, output_path):
        """
        Download a file from a URL to the specified output path.
        Returns True if successful, False otherwise.
        """
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"Downloading {url} (Attempt {attempt + 1}/{self.max_retries})")
                response = requests.get(url, headers=self.headers, timeout=self.timeout, verify=self.settings.get('verify_ssl', True))
                response.raise_for_status()

                # Ensure directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                self.logger.info(f"Successfully downloaded to {output_path}")
                time.sleep(self.delay) # Respect rate limiting
                return True

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error downloading {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay * (attempt + 1)) # Exponential backoff
                else:
                    self.logger.error(f"Failed to download {url} after {self.max_retries} attempts")
                    return False
    
    def fetch_content(self, url):
        """
        Fetch content from a URL and return it as text/bytes.
        """
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"Fetching content from {url}")
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.raise_for_status()
                time.sleep(self.delay)
                return response
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error fetching {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay * (attempt + 1))
        return None
