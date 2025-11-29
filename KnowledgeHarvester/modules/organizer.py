import os
import re
import logging
from datetime import datetime

class Organizer:
    def __init__(self, config):
        self.config = config
        self.paths = config.get('paths', {})
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Project root
        self.logger = logging.getLogger(__name__)

    def get_output_path(self, category, title, extension):
        """
        Generate a standardized output path for a file.
        """
        # Sanitize title for filename
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        
        filename = f"{safe_title}.{extension}"
        
        # Determine category folder
        category_path = os.path.join(self.base_dir, self.paths.get('materials', 'data/materials'), category)
        
        return os.path.join(category_path, filename)

    def get_processed_path(self, category, title, extension='md'):
        """
        Generate path for processed/extracted content.
        """
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        
        filename = f"{safe_title}.{extension}"
        
        # Determine extracted folder
        extracted_path = os.path.join(self.base_dir, self.paths.get('extracted', 'data/extracted'), category)
        
        return os.path.join(extracted_path, filename)

    def save_metadata(self, metadata, category, title):
        """
        Save metadata about the download.
        """
        import json
        
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        
        metadata_dir = os.path.join(self.base_dir, self.paths.get('metadata', 'data/metadata'), category)
        os.makedirs(metadata_dir, exist_ok=True)
        
        metadata_path = os.path.join(metadata_dir, f"{safe_title}.json")
        
        metadata['downloaded_at'] = datetime.now().isoformat()
        
        try:
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            return True
        except Exception as e:
            self.logger.error(f"Error saving metadata: {e}")
            return False
