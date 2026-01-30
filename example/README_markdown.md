# Markdown Support in Scribus Generator

This directory contains example files demonstrating Markdown formatting support in Scribus Generator.

## Files

- **markdown_test.csv**: Example CSV data with Markdown formatting
- **markdown_test.sla**: Scribus template for testing Markdown conversion

## What is Markdown?

Markdown is a lightweight markup language that lets you add formatting to plain text using simple, readable syntax. With Scribus Generator's Markdown support, you can write formatted text in your CSV files without worrying about complex Scribus styling.

## Quick Start

1. Open `markdown_test.sla` in Scribus
2. Run Scribus Generator (Script → Execute Script → ScribusGenerator.py)
3. Select `markdown_test.csv` as your data file
4. Generate the output

The Markdown syntax in your CSV will automatically be converted to properly formatted Scribus text!

## Supported Markdown Syntax

### Text Emphasis

```markdown
**bold text**          → Bold font variant
*italic text*          → Italic font variant
***bold italic***      → Bold italic font variant
`inline code`          → Courier New monospace font
```

**Example CSV:**
```csv
name,description
John,Working with **Python** and *Scribus*
Jane,Expert in `code` and **design**
```

### Headings

```markdown
# Heading 1           → 2.0x base font size
## Heading 2          → 1.5x base font size
### Heading 3         → 1.17x base font size
#### Heading 4        → 1.0x base font size (same as base)
##### Heading 5       → 0.83x base font size
###### Heading 6      → 0.67x base font size
```

**Example CSV:**
```csv
title,content
# Big Title,Some text here
## Subtitle,More content
```

### Lists

```markdown
Bullet lists (use -, *, or +):
- First item
- Second item
- Third item

Numbered lists:
1. First step
2. Second step
3. Third step
```

**Example CSV:**
```csv
name,tasks
Project A,"Key deliverables:
- Design mockups
- Write documentation
- Deploy to production"
Project B,"Process:
1. Planning phase
2. Development
3. Testing
4. Launch"
```

### Links

```markdown
[Link text](https://example.com)  → Converted to: Link text (https://example.com)
```

Links are converted to a printer-friendly format perfect for business cards, flyers, and printed materials.

**Example CSV:**
```csv
name,website
Company,Visit [our website](https://example.com) for more info
Contact,Email us at [support](mailto:support@example.com)
```

## Practical Examples

### Business Cards

CSV data:
```csv
name,title,email,phone,description
John Doe,**Senior Developer**,john@example.com,555-1234,Specialist in *Python* and **web development**
Jane Smith,***Product Manager***,jane@example.com,555-5678,Expert in **agile methodologies** and team leadership
```

### Event Flyers

CSV data:
```csv
event,date,description
Workshop,2026-02-15,"Join us for:
- **Hands-on training**
- *Live demonstrations*
- Q&A session

Visit [our site](https://example.com) to register!"
Conference,2026-03-20,"# Tech Summit 2026

## Featured Topics
1. AI & Machine Learning
2. Cloud Computing
3. Cybersecurity

Register at [summit.example.com](https://summit.example.com)"
```

### Product Catalogs

CSV data:
```csv
product,features,specs
Widget Pro,"**Premium Features:**
- High performance
- *Energy efficient*
- 2-year warranty","Specs:
- Weight: `2.5kg`
- Power: **100W**
- Size: *30x20x10cm*"
```

### Team Directory

CSV data:
```csv
name,role,skills,contact
Alice Johnson,*Team Lead*,"**Core Skills:**
- Project management
- Strategic planning
- Team development",Contact: [alice@team.com](mailto:alice@team.com)
Bob Wilson,**Developer**,"**Technologies:**
- `Python`
- `JavaScript`
- `SQL`",Connect on [LinkedIn](https://linkedin.com/in/bob)
```

## Tips and Best Practices

### 1. Font Compatibility

Markdown uses font variants based on your template's base font:
- If your template uses "Arial Regular", bold becomes "Arial Bold"
- Inline code always uses "Courier New Regular"
- Make sure these font variants are installed in your system

### 2. Multi-line Text

For longer formatted text, use quoted fields in your CSV:

```csv
name,description
Item,"This is a longer description with:
- **Bold points**
- *Italic emphasis*
- Multiple lines"
```

### 3. Mixing Plain and Markdown Text

You can mix both in the same field:

```csv
description
Plain text with **some bold** and *some italic* parts.
```

### 4. Escaping Special Characters

If you need literal asterisks or other Markdown characters, you have two options:
1. Disable Markdown for that generation (use `--no-markdown` flag)
2. Use HTML entities (though this is less reliable)

### 5. Testing Your Data

Always test with a small subset first:
```bash
python ScribusGeneratorCLI.py --single -c your_data.csv your_template.sla -o output/
```

## Controlling Markdown

### Enable/Disable in GUI

1. Open Scribus Generator dialog
2. Look for "Convert Markdown" checkbox in Misc Settings
3. Check to enable, uncheck to disable

### Command Line Options

Enable (default):
```bash
python ScribusGeneratorCLI.py --markdown -c data.csv template.sla
```

Disable:
```bash
python ScribusGeneratorCLI.py --no-markdown -c data.csv template.sla
```

### Configuration File

Edit `ScribusGeneratorBackend.py`:
```python
# Set to 1 to enable, 0 to disable
MARKDOWN_ENABLED = 1

# Auto-detect Markdown or require explicit marker
MARKDOWN_AUTO_DETECT = 1

# Optional marker when auto-detect is off
MARKDOWN_MARKER = '%MARKDOWN%'
```

## Troubleshooting

### Markdown Not Converting

**Problem:** Markdown syntax appears literally (e.g., `**text**` instead of bold)

**Solutions:**
1. Check "Convert Markdown" is enabled in GUI or use `--markdown` flag
2. Verify your CSV is UTF-8 encoded
3. Make sure you're using the correct Markdown syntax
4. Check logs in `scribusGenerator.log` for any errors

### Font Issues

**Problem:** Bold/italic not showing correctly

**Solutions:**
1. Verify the font variants exist (e.g., "Arial Bold" for bold)
2. Try a different base font in your Scribus template
3. Install missing font variants on your system

### Special Characters

**Problem:** Strange characters or encoding issues

**Solutions:**
1. Save your CSV as UTF-8 encoded
2. Use proper Unicode characters (é, ñ, 中, etc.)
3. Check your CSV editor's encoding settings

### Lists Not Formatting

**Problem:** List items appear on same line

**Solutions:**
1. Make sure list items are on separate lines in your CSV field
2. Use quoted fields for multi-line content
3. Check that line breaks are preserved in your CSV export

## Advanced Usage

### Custom Markdown Processing

For advanced users, you can customize Markdown processing by editing `MarkdownConverter.py`:

```python
# Example: Change bullet character
# In HTMLToScribusConverter.handle_starttag():
if self.in_unordered_list:
    self.text_buffer = '▶ '  # Use arrow instead of bullet
```

### Integration with Other Tools

Markdown data can come from many sources:
- Spreadsheet exports (Excel, Google Sheets, LibreOffice)
- Database queries
- Content management systems
- Static site generators
- Version control commit messages

### Batch Processing

Process multiple templates with Markdown:
```bash
for template in templates/*.sla; do
    python ScribusGeneratorCLI.py --markdown -c data.csv "$template"
done
```

## More Information

- [Scribus Generator Main README](../README.md)
- [Markdown Guide](https://www.markdownguide.org/)
- [CSV Format Specification](https://tools.ietf.org/html/rfc4180)
- [Scribus Documentation](https://wiki.scribus.net/)

## Contributing

Found a bug or have a feature request? Please [open an issue](https://github.com/berteh/ScribusGenerator/issues) on GitHub!

## License

Scribus Generator is released under the MIT License. See the LICENSE file for details.
