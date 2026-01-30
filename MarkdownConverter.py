#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Markdown to Scribus Converter Module

This module handles conversion of Markdown syntax in CSV data to Scribus-compatible
formatting using ITEXT elements with appropriate styling.

Part of ScribusGenerator - https://github.com/berteh/ScribusGenerator/
"""

import re
import logging
import mistune
from html.parser import HTMLParser
import xml.etree.ElementTree as ET


class MarkdownConverter:
    """
    Converts Markdown text to Scribus ITEXT XML elements.
    
    Supports:
    - Bold (**text** or __text__)
    - Italic (*text* or _text_)
    - Headings (# H1 through ###### H6)
    - Inline code (`code`)
    - Links ([text](url)) - converted to "text (url)"
    - Lists (bullet and numbered)
    - Blockquotes (> text)
    """
    
    # Common Markdown indicators for quick detection
    MARKDOWN_INDICATORS = [
        '#',      # Headings
        '**',     # Bold
        '__',     # Bold (alternative)
        '*',      # Italic or list
        '_',      # Italic (alternative)
        '`',      # Code
        '[',      # Links
        ']',      # Links
        '>',      # Blockquotes
        '-',      # Lists
        '+',      # Lists
    ]
    
    def __init__(self):
        """Initialize the Markdown converter with mistune parser."""
        self.markdown_parser = mistune.create_markdown()
        logging.debug('MarkdownConverter initialized')
    
    def detect_markdown(self, text):
        """
        Detect if text contains Markdown syntax.
        
        Performs a quick check for common Markdown indicators to avoid
        unnecessary parsing of plain text.
        
        Args:
            text (str): Text to check for Markdown syntax
            
        Returns:
            bool: True if text appears to contain Markdown, False otherwise
        """
        if not text or not isinstance(text, str):
            return False
        
        # Quick check for common Markdown patterns
        for indicator in self.MARKDOWN_INDICATORS:
            if indicator in text:
                # Additional validation for some patterns to reduce false positives
                if indicator in ['*', '_', '-', '+']:
                    # Check for actual formatting patterns, not just single characters
                    if indicator == '*':
                        if '**' in text or re.search(r'\*\w+\*', text):
                            return True
                    elif indicator == '_':
                        if '__' in text or re.search(r'_\w+_', text):
                            return True
                    elif indicator in ['-', '+']:
                        # List pattern: starts with dash/plus and space
                        if re.search(r'^\s*[-+]\s+\w', text, re.MULTILINE):
                            return True
                else:
                    return True
        
        # Check for numbered lists (1. 2. etc)
        if re.search(r'^\s*\d+\.\s+\w', text, re.MULTILINE):
            return True
        
        return False
    
    def convert_markdown_to_scribus_xml(self, markdown_text, base_font='Arial Regular', 
                                       base_fontsize='12', base_color='Black'):
        """
        Convert Markdown text to Scribus ITEXT XML elements.
        
        This is the main conversion method that parses Markdown and generates
        Scribus-compatible XML string that can be inserted into an SLA file.
        
        Args:
            markdown_text (str): Markdown formatted text
            base_font (str): Base font to use (e.g., 'Arial Regular')
            base_fontsize (str): Base font size (e.g., '12')
            base_color (str): Base color name (e.g., 'Black')
            
        Returns:
            str: XML string containing ITEXT elements ready for Scribus
        """
        if not markdown_text:
            return ''
        
        # Parse Markdown to HTML first
        html = self.markdown_parser(markdown_text)
        
        logging.debug(f'Parsed Markdown to HTML: {html[:100]}...')
        
        # Convert HTML to Scribus ITEXT elements
        converter = HTMLToScribusConverter(base_font, base_fontsize, base_color)
        scribus_xml = converter.convert(html)
        
        logging.debug(f'Converted to Scribus XML: {scribus_xml[:100]}...')
        
        return scribus_xml


class HTMLToScribusConverter(HTMLParser):
    """
    Converts HTML (from Markdown parser) to Scribus ITEXT elements.
    
    This parser walks through the HTML output from mistune and generates
    appropriate Scribus ITEXT elements with correct font attributes.
    """
    
    def __init__(self, base_font, base_fontsize, base_color):
        super().__init__()
        self.base_font = base_font
        self.base_fontsize = base_fontsize
        self.base_color = base_color
        
        # Font family without style
        self.font_family = base_font.rsplit(' ', 1)[0] if ' ' in base_font else base_font
        
        # Stack to track current formatting state
        self.format_stack = []
        
        # Output list of ITEXT elements
        self.itext_elements = []
        
        # Current text buffer
        self.text_buffer = ''
    
    def get_current_font(self):
        """Get current font based on format stack."""
        if 'strong' in self.format_stack or 'b' in self.format_stack:
            if 'em' in self.format_stack or 'i' in self.format_stack:
                return f'{self.font_family} Bold Italic'
            return f'{self.font_family} Bold'
        elif 'em' in self.format_stack or 'i' in self.format_stack:
            return f'{self.font_family} Italic'
        elif 'code' in self.format_stack:
            return 'Courier New Regular'
        return self.base_font
    
    def get_current_fontsize(self):
        """Get current font size based on format stack."""
        # Check for heading tags
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            if tag in self.format_stack:
                base_size = float(self.base_fontsize)
                sizes = {
                    'h1': base_size * 2.0,
                    'h2': base_size * 1.5,
                    'h3': base_size * 1.17,
                    'h4': base_size * 1.0,
                    'h5': base_size * 0.83,
                    'h6': base_size * 0.67,
                }
                return str(sizes[tag])
        return self.base_fontsize
    
    def flush_text_buffer(self):
        """Flush current text buffer to ITEXT element."""
        if self.text_buffer:
            font = self.get_current_font()
            fontsize = self.get_current_fontsize()
            
            # XML escape the text
            text = self.escape_xml(self.text_buffer)
            
            # Create ITEXT element
            itext = f'<ITEXT CH="{text}" FONT="{font}" FONTSIZE="{fontsize}" />'
            self.itext_elements.append(itext)
            
            self.text_buffer = ''
    
    def escape_xml(self, text):
        """Escape special XML characters."""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&apos;')
        return text
    
    def handle_starttag(self, tag, attrs):
        """Handle opening HTML tags."""
        # Flush buffer before changing format for inline elements too
        if tag in ['strong', 'em', 'b', 'i', 'code']:
            self.flush_text_buffer()
        
        # Flush buffer before changing format for block elements
        if tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']:
            self.flush_text_buffer()
        
        self.format_stack.append(tag)
        
        # Handle special tags
        if tag == 'br':
            self.flush_text_buffer()
            self.itext_elements.append('<breakline />')
        elif tag == 'a':
            # Extract URL for later
            for attr_name, attr_value in attrs:
                if attr_name == 'href':
                    self.current_link_url = attr_value
    
    def handle_endtag(self, tag):
        """Handle closing HTML tags."""
        # Flush buffer before removing format (so current format is still active)
        if tag in ['strong', 'em', 'b', 'i', 'code', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.flush_text_buffer()
        
        # Remove from stack
        if tag in self.format_stack:
            self.format_stack.remove(tag)
        
        # Handle links - append URL in parentheses
        if tag == 'a' and hasattr(self, 'current_link_url'):
            self.text_buffer += f' ({self.current_link_url})'
            self.flush_text_buffer()
            delattr(self, 'current_link_url')
        
        # Handle block elements - add line break
        if tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']:
            self.flush_text_buffer()
            self.itext_elements.append('<breakline />')
        
        # Handle list items - add bullet or number
        if tag == 'ul':
            self.flush_text_buffer()
        elif tag == 'ol':
            self.flush_text_buffer()
    
    def handle_data(self, data):
        """Handle text data."""
        # Strip only leading/trailing whitespace from complete blocks
        # but preserve internal whitespace
        if data.strip():  # Only process non-empty data
            self.text_buffer += data
    
    def convert(self, html):
        """
        Convert HTML to Scribus ITEXT elements.
        
        Args:
            html (str): HTML string from Markdown parser
            
        Returns:
            str: XML string with ITEXT elements
        """
        self.feed(html)
        self.flush_text_buffer()
        
        # Join all ITEXT elements
        result = ''.join(self.itext_elements)
        
        # Clean up: remove trailing breakline if present
        result = result.rstrip()
        if result.endswith('<breakline />'):
            result = result[:-len('<breakline />')]
        
        return result


# Module-level functions for easy import
def detect_markdown(text):
    """Quick check if text contains Markdown syntax."""
    converter = MarkdownConverter()
    return converter.detect_markdown(text)


def convert_markdown(text, base_font='Arial Regular', base_fontsize='12', base_color='Black'):
    """Convert Markdown text to Scribus ITEXT XML."""
    converter = MarkdownConverter()
    return converter.convert_markdown_to_scribus_xml(text, base_font, base_fontsize, base_color)
