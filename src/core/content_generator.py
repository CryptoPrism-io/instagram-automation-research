#!/usr/bin/env python3
"""
Content Generator - HTML/CSS to Instagram Image Conversion
Generates Instagram-ready images from HTML templates using Playwright
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import logging
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

class ContentGenerator:
    """
    Generate Instagram content from HTML/CSS templates using Playwright
    """

    def __init__(self, templates_dir: str = "src/templates", output_dir: str = "data/generated_content"):
        """
        Initialize content generator

        Args:
            templates_dir: Directory containing HTML/CSS templates
            output_dir: Directory to save generated images
        """
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Instagram optimal dimensions
        self.instagram_dimensions = {
            'square': {'width': 1080, 'height': 1080},
            'portrait': {'width': 1080, 'height': 1350},
            'landscape': {'width': 1080, 'height': 566},
            'story': {'width': 1080, 'height': 1920}
        }

    def create_post_image(self, template: str, data: Dict[str, Any],
                         format_type: str = 'square', filename: Optional[str] = None) -> str:
        """
        Generate Instagram post image from template

        Args:
            template: Template name (without .html extension)
            data: Data to inject into template
            format_type: Instagram format (square, portrait, landscape, story)
            filename: Optional custom filename

        Returns:
            Path to generated image file
        """
        try:
            # Load and process template
            template_path = self.templates_dir / "html" / f"{template}.html"

            if not template_path.exists():
                raise FileNotFoundError(f"Template not found: {template_path}")

            # Read template
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Replace placeholders with data
            processed_html = self._process_template(html_content, data)

            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{template}_{format_type}_{timestamp}.jpg"

            # Generate image using Playwright
            output_path = self.output_dir / filename
            self._html_to_image(processed_html, output_path, format_type)

            logger.info(f"✅ Generated image: {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"❌ Error generating image: {e}")
            raise

    def _process_template(self, html_content: str, data: Dict[str, Any]) -> str:
        """
        Process template by replacing placeholders with data

        Args:
            html_content: Raw HTML template content
            data: Data dictionary for placeholder replacement

        Returns:
            Processed HTML with data injected
        """
        try:
            # Simple placeholder replacement ({{key}} format)
            processed = html_content

            for key, value in data.items():
                placeholder = f"{{{{{key}}}}}"
                processed = processed.replace(placeholder, str(value))

            # Add CSS file references (relative to template)
            css_link = '<link rel="stylesheet" href="../css/style.css">'
            if '<head>' in processed and css_link not in processed:
                processed = processed.replace('<head>', f'<head>\n    {css_link}')

            return processed

        except Exception as e:
            logger.error(f"❌ Error processing template: {e}")
            raise

    def _html_to_image(self, html_content: str, output_path: Path, format_type: str):
        """
        Convert HTML to image using Playwright

        Args:
            html_content: Processed HTML content
            output_path: Path to save generated image
            format_type: Instagram format type
        """
        try:
            dimensions = self.instagram_dimensions.get(format_type, self.instagram_dimensions['square'])

            with sync_playwright() as p:
                # Launch browser
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # Set viewport size
                page.set_viewport_size(dimensions)

                # Load HTML content
                page.set_content(html_content)

                # Wait for content to load
                page.wait_for_load_state('networkidle')

                # Take screenshot
                page.screenshot(
                    path=str(output_path),
                    full_page=True,
                    type='jpeg',
                    quality=95
                )

                browser.close()

                logger.info(f"✅ Screenshot saved: {output_path}")

        except Exception as e:
            logger.error(f"❌ Error converting HTML to image: {e}")
            raise

    def create_story_content(self, template: str, data: Dict[str, Any],
                           filename: Optional[str] = None) -> str:
        """
        Generate Instagram Story content

        Args:
            template: Story template name
            data: Data for template
            filename: Optional custom filename

        Returns:
            Path to generated story image
        """
        return self.create_post_image(template, data, 'story', filename)

    def batch_generate(self, batch_config: Dict[str, Any]) -> list:
        """
        Generate multiple images from batch configuration

        Args:
            batch_config: Configuration for batch generation

        Returns:
            List of generated image paths
        """
        generated_files = []

        try:
            for item in batch_config.get('items', []):
                template = item.get('template')
                data = item.get('data', {})
                format_type = item.get('format', 'square')
                filename = item.get('filename')

                image_path = self.create_post_image(template, data, format_type, filename)
                generated_files.append(image_path)

            logger.info(f"✅ Batch generation completed: {len(generated_files)} images")
            return generated_files

        except Exception as e:
            logger.error(f"❌ Error in batch generation: {e}")
            raise

    def get_available_templates(self) -> list:
        """
        Get list of available HTML templates

        Returns:
            List of available template names
        """
        templates_path = self.templates_dir / "html"

        if not templates_path.exists():
            return []

        templates = []
        for template_file in templates_path.glob("*.html"):
            templates.append(template_file.stem)

        return sorted(templates)

    def validate_template(self, template: str) -> bool:
        """
        Validate if template exists and is accessible

        Args:
            template: Template name to validate

        Returns:
            True if template is valid, False otherwise
        """
        template_path = self.templates_dir / "html" / f"{template}.html"
        return template_path.exists() and template_path.is_file()

    def get_template_info(self, template: str) -> Dict[str, Any]:
        """
        Get information about a template

        Args:
            template: Template name

        Returns:
            Dictionary with template information
        """
        template_path = self.templates_dir / "html" / f"{template}.html"

        if not template_path.exists():
            return {"error": "Template not found"}

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract placeholders
            import re
            placeholders = re.findall(r'\{\{(\w+)\}\}', content)

            return {
                "name": template,
                "path": str(template_path),
                "size": template_path.stat().st_size,
                "modified": datetime.fromtimestamp(template_path.stat().st_mtime).isoformat(),
                "placeholders": list(set(placeholders))
            }

        except Exception as e:
            return {"error": str(e)}

# Example usage and testing
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Initialize generator
    generator = ContentGenerator()

    # Example: Create a basic post
    test_data = {
        "title": "Instagram Automation Research",
        "subtitle": "Testing Content Generation",
        "description": "Generated with Playwright and HTML templates",
        "hashtags": "#automation #research #instagram"
    }

    try:
        # Check available templates
        templates = generator.get_available_templates()
        print(f"📋 Available templates: {templates}")

        # Create test image (if basic template exists)
        if templates:
            template_name = templates[0]
            image_path = generator.create_post_image(template_name, test_data)
            print(f"✅ Test image generated: {image_path}")
        else:
            print("⚠️ No templates available - create HTML templates in src/templates/html/")

    except Exception as e:
        print(f"❌ Error during testing: {e}")