#!/usr/bin/env python3
"""
Generate dual-theme PDFs (Light & Dark) for Maaza paper.

Copyright 2025 CycleCore Technologies
Licensed under the Apache License, Version 2.0
"""

import markdown
import re
from pathlib import Path

# Try importing weasyprint for PDF generation
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    print("⚠️  WeasyPrint not available. Install with: pip install weasyprint")

def read_paper():
    """Read the markdown paper."""
    paper_path = Path('/home/rain/SLMBench/papers/MAAZA_PAPER_FULL_CONTENT.md')
    with open(paper_path, 'r') as f:
        content = f.read()
    return content

def replace_figure_references(content, theme='light'):
    """Replace ASCII figures with image references."""
    # Pattern to match ASCII figure blocks
    figure_pattern = r'```\s*\n(.*?Figure \d+:.*?)\n```'
    
    def replace_ascii_with_image(match):
        text = match.group(1)
        # Extract figure number
        fig_num_match = re.search(r'Figure (\d+)', text)
        if fig_num_match:
            fig_num = fig_num_match.group(1)
            # Determine which figure based on number
            figure_files = {
                '1': 'figure1_performance_vs_size',
                '2': 'figure2_performance_by_complexity',
                '3': 'figure3_disk_size_vs_performance',
                '4': 'figure4_fine_tuning_comparison',
            }
            if fig_num in figure_files:
                suffix = '_DARK' if theme == 'dark' else ''
                img_path = f'figures/{figure_files[fig_num]}{suffix}.png'
                caption = text.split('\n')[0]  # First line as caption
                return f'\n\n![{caption}]({img_path})\n\n*{caption}*\n\n'
        return match.group(0)
    
    content = re.sub(figure_pattern, replace_ascii_with_image, content, flags=re.DOTALL)
    return content

def generate_html(content, theme='light'):
    """Convert markdown to HTML with theme-specific CSS."""
    # Convert markdown to HTML
    html_content = markdown.markdown(content, extensions=['tables', 'fenced_code'])
    
    # Theme-specific CSS
    if theme == 'dark':
        css = """
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.6;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 1in;
            background-color: #1a1a1a;
            color: #f0f0f0;
        }
        h1, h2, h3, h4 {
            color: #ffffff;
            border-bottom: 2px solid #4FC3F7;
            padding-bottom: 0.3em;
        }
        h1 { font-size: 24pt; margin-top: 0; }
        h2 { font-size: 18pt; margin-top: 1.5em; }
        h3 { font-size: 14pt; margin-top: 1.2em; }
        code {
            background-color: #2a2a2a;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #4FC3F7;
        }
        pre {
            background-color: #2a2a2a;
            padding: 1em;
            border-left: 4px solid #4FC3F7;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
            background-color: #2a2a2a;
        }
        th, td {
            border: 1px solid #505050;
            padding: 8px 12px;
            text-align: left;
        }
        th {
            background-color: #3a3a3a;
            font-weight: bold;
            color: #4FC3F7;
        }
        tr:nth-child(even) {
            background-color: #252525;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 1em auto;
        }
        a {
            color: #4FC3F7;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        blockquote {
            border-left: 4px solid #CE93D8;
            padding-left: 1em;
            margin-left: 0;
            font-style: italic;
            color: #d0d0d0;
        }
        strong {
            color: #ffffff;
        }
        """
    else:  # light theme
        css = """
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.6;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 1in;
            background-color: #ffffff;
            color: #000000;
        }
        h1, h2, h3, h4 {
            color: #2E86AB;
            border-bottom: 2px solid #2E86AB;
            padding-bottom: 0.3em;
        }
        h1 { font-size: 24pt; margin-top: 0; }
        h2 { font-size: 18pt; margin-top: 1.5em; }
        h3 { font-size: 14pt; margin-top: 1.2em; }
        code {
            background-color: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #2E86AB;
        }
        pre {
            background-color: #f5f5f5;
            padding: 1em;
            border-left: 4px solid #2E86AB;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }
        th {
            background-color: #f8f8f8;
            font-weight: bold;
            color: #2E86AB;
        }
        tr:nth-child(even) {
            background-color: #fafafa;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 1em auto;
        }
        a {
            color: #2E86AB;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        blockquote {
            border-left: 4px solid #A23B72;
            padding-left: 1em;
            margin-left: 0;
            font-style: italic;
            color: #555;
        }
        """
    
    # Complete HTML document
    html_doc = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Maaza Paper - {theme.capitalize()} Mode</title>
        <style>{css}</style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    return html_doc

def generate_pdf(theme='light'):
    """Generate PDF for specified theme."""
    if not WEASYPRINT_AVAILABLE:
        print(f"❌ Cannot generate {theme} PDF without WeasyPrint")
        return False
    
    print(f"\n{'='*70}")
    print(f"📄 Generating {theme.upper()} MODE PDF...")
    print(f"{'='*70}\n")
    
    # Read and process paper
    content = read_paper()
    content_with_figs = replace_figure_references(content, theme)
    html = generate_html(content_with_figs, theme)
    
    # Save HTML (for debugging)
    html_path = f'/home/rain/SLMBench/papers/MAAZA_PAPER_v0.4_{theme.upper()}.html'
    with open(html_path, 'w') as f:
        f.write(html)
    print(f"✅ HTML saved: {html_path}")
    
    # Generate PDF
    pdf_path = f'/home/rain/SLMBench/papers/MAAZA_PAPER_v0.4_{theme.upper()}.pdf'
    try:
        HTML(string=html, base_url='/home/rain/SLMBench/papers/').write_pdf(pdf_path)
        print(f"✅ PDF saved: {pdf_path}")
        return True
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False

def main():
    """Generate both light and dark mode PDFs."""
    print("\n" + "="*70)
    print("📊 DUAL-THEME PDF GENERATOR - Maaza Paper v0.4")
    print("="*70)
    
    if not WEASYPRINT_AVAILABLE:
        print("\n⚠️  WeasyPrint is required to generate PDFs")
        print("\nInstall with:")
        print("  pip install weasyprint")
        print("\nAlternatively, use pandoc:")
        print("  pandoc MAAZA_PAPER_FULL_CONTENT.md -o paper.pdf")
        return
    
    # Generate both themes
    light_success = generate_pdf('light')
    dark_success = generate_pdf('dark')
    
    print("\n" + "="*70)
    if light_success and dark_success:
        print("✅ BOTH PDFs GENERATED SUCCESSFULLY!")
    elif light_success or dark_success:
        print("⚠️  PARTIAL SUCCESS - Check errors above")
    else:
        print("❌ PDF GENERATION FAILED - See errors above")
    print("="*70)
    
    if light_success or dark_success:
        print("\n📁 Output files:")
        if light_success:
            print("  • MAAZA_PAPER_v0.4_LIGHT.pdf (traditional)")
        if dark_success:
            print("  • MAAZA_PAPER_v0.4_DARK.pdf (modern) 🌙")
        print("\n💡 Both versions use the same content, just different aesthetics!")
        print("="*70 + "\n")

if __name__ == '__main__':
    main()

