import os
import yaml
import logging
import argparse
from tqdm import tqdm
from modules.downloader import Downloader
from modules.processor import ContentProcessor
from modules.organizer import Organizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("knowledge_harvester.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description='Knowledge Harvester - Documentation Downloader')
    parser.add_argument('--config', default='config.yaml', help='Path to configuration file')
    parser.add_argument('--category', help='Specific category to download (e.g., docker, postgresql)')
    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return

    downloader = Downloader(config)
    processor = ContentProcessor(config)
    organizer = Organizer(config)

    sources = config.get('sources', {})
    
    # Filter sources if category provided
    if args.category:
        if args.category in sources:
            sources = {args.category: sources[args.category]}
        else:
            logger.error(f"Category '{args.category}' not found in sources.")
            return

    total_urls = sum(len(source.get('urls', [])) for source in sources.values())
    logger.info(f"Starting harvest of {total_urls} URLs...")

    with tqdm(total=total_urls, desc="Harvesting Knowledge") as pbar:
        for category, source_data in sources.items():
            logger.info(f"Processing category: {category}")
            urls = source_data.get('urls', [])
            
            for item in urls:
                url = item.get('url')
                title = item.get('title', 'Untitled')
                doc_type = item.get('type', 'html')
                
                pbar.set_description(f"Processing {title}")
                
                # Determine paths
                ext = 'pdf' if doc_type == 'pdf' else 'html'
                if item.get('is_github'):
                    ext = 'md'
                
                output_path = organizer.get_output_path(category, title, ext)

                # URL Transformation
                if item.get('is_github', False):
                    if 'github.com' in url and '/blob/' in url:
                        url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
                        logger.info(f"Converted GitHub URL to raw: {url}")
                
                # Download
                success = downloader.download_file(url, output_path)
                
                if success:
                    # Process content
                    processed_content = None
                    if doc_type == 'html':
                        # Read the downloaded HTML
                        try:
                            with open(output_path, 'r', encoding='utf-8', errors='ignore') as f:
                                html_content = f.read()
                            processed_content = processor.html_to_markdown(html_content, url)
                        except Exception as e:
                            logger.error(f"Error reading HTML file {output_path}: {e}")
                            
                    elif doc_type == 'pdf':
                        processed_content = processor.extract_text_from_pdf(output_path)
                    
                    elif doc_type == 'markdown' or item.get('is_github'):
                        # Already markdown, just read it (maybe clean it?)
                        try:
                            with open(output_path, 'r', encoding='utf-8', errors='ignore') as f:
                                processed_content = f.read()
                        except Exception as e:
                            logger.error(f"Error reading Markdown file {output_path}: {e}")

                    # Save processed content
                    if processed_content:
                        processed_path = organizer.get_processed_path(category, title, 'md')
                        processor.save_content(processed_content, processed_path)
                        
                        # Save metadata
                        metadata = {
                            'url': url,
                            'title': title,
                            'category': category,
                            'original_path': output_path,
                            'processed_path': processed_path,
                            'type': doc_type
                        }
                        organizer.save_metadata(metadata, category, title)
                
                pbar.update(1)

    logger.info("Harvest complete!")

if __name__ == "__main__":
    main()
