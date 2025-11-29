import os
import logging
import markdownify
from bs4 import BeautifulSoup
import pypdf

class ContentProcessor:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def html_to_markdown(self, html_content, base_url=None):
        """
        Convert HTML content to Markdown.
        """
        try:
            # Pre-process with BeautifulSoup to remove unwanted elements
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove scripts, styles, navs, footers if possible to get clean content
            for tag in soup(['script', 'style', 'nav', 'footer', 'iframe', 'noscript']):
                tag.decompose()

            # Convert to markdown
            md = markdownify.markdownify(str(soup), heading_style="ATX")
            return md.strip()
        except Exception as e:
            self.logger.error(f"Error converting HTML to Markdown: {e}")
            return None

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a PDF file.
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n\n"
            return text.strip()
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
            return None

    def save_content(self, content, output_path):
        """
        Save text content to a file.
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            self.logger.error(f"Error saving content to {output_path}: {e}")
            return False
