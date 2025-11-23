#!/usr/bin/env python3
"""
Generate PDF from Maaza paper using reportlab (no LaTeX needed).

Copyright 2025 CycleCore Technologies
Licensed under the Apache License, Version 2.0
"""

import os
from pathlib import Path
import markdown
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import re

def read_paper():
    """Read the markdown paper."""
    paper_path = Path('/home/rain/SLMBench/papers/MAAZA_PAPER_FULL_CONTENT.md')
    with open(paper_path, 'r') as f:
        content = f.read()
    return content

def simple_markdown_to_flowables(content, styles, theme='light'):
    """Convert markdown to reportlab flowables (simplified)."""
    flowables = []
    lines = content.split('\n')
    
    i = 0
    current_para = []
    in_code_block = False
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip YAML frontmatter
        if i < 10 and line.startswith('**') and ':' in line:
            i += 1
            continue
        
        # Headers
        if line.startswith('# ') and not in_code_block:
            if current_para:
                flowables.append(Paragraph(' '.join(current_para), styles['Normal']))
                current_para = []
            title = line[2:].strip()
            flowables.append(Spacer(1, 0.3*inch))
            flowables.append(Paragraph(title, styles['MainTitle']))
            flowables.append(Spacer(1, 0.2*inch))
        
        elif line.startswith('## ') and not in_code_block:
            if current_para:
                flowables.append(Paragraph(' '.join(current_para), styles['Normal']))
                current_para = []
            heading = line[3:].strip()
            flowables.append(Spacer(1, 0.2*inch))
            flowables.append(Paragraph(heading, styles['Heading1']))
            flowables.append(Spacer(1, 0.1*inch))
        
        elif line.startswith('### ') and not in_code_block:
            if current_para:
                flowables.append(Paragraph(' '.join(current_para), styles['Normal']))
                current_para = []
            heading = line[4:].strip()
            flowables.append(Spacer(1, 0.15*inch))
            flowables.append(Paragraph(heading, styles['Heading2']))
            flowables.append(Spacer(1, 0.05*inch))
        
        # Code blocks
        elif line.startswith('```'):
            in_code_block = not in_code_block
            if current_para and not in_code_block:
                flowables.append(Paragraph(' '.join(current_para), styles['Code']))
                current_para = []
        
        # Horizontal rules
        elif line.startswith('---') and not in_code_block:
            if current_para:
                flowables.append(Paragraph(' '.join(current_para), styles['Normal']))
                current_para = []
            flowables.append(Spacer(1, 0.1*inch))
        
        # Empty lines
        elif not line and not in_code_block:
            if current_para:
                text = ' '.join(current_para)
                # Clean up markdown formatting
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
                text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
                text = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text)
                flowables.append(Paragraph(text, styles['Normal']))
                flowables.append(Spacer(1, 0.1*inch))
                current_para = []
        
        # Regular content
        else:
            if not in_code_block:
                current_para.append(line)
        
        i += 1
    
    # Flush remaining
    if current_para:
        text = ' '.join(current_para)
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text)
        flowables.append(Paragraph(text, styles['Normal']))
    
    return flowables

def generate_pdf_simple(theme='light'):
    """Generate a simple PDF (text-focused, figures referenced but not embedded)."""
    print(f"\n{'='*70}")
    print(f"📄 Generating {theme.upper()} MODE PDF (Simplified)")
    print(f"{'='*70}\n")
    
    output_path = f'/home/rain/SLMBench/papers/MAAZA_PAPER_v0.4_{theme.upper()}_SIMPLE.pdf'
    
    # Create document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Customize for theme
    if theme == 'dark':
        # Note: ReportLab doesn't support dark backgrounds easily
        # This will be light with notes about dark figures
        pass
    
    # Custom styles
    styles.add(ParagraphStyle(
        name='MainTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2E86AB'),
        spaceAfter=12,
        alignment=TA_CENTER,
    ))
    
    # Read and convert
    print("📝 Reading paper content...")
    content = read_paper()
    
    print("🔄 Converting markdown to PDF flowables...")
    flowables = simple_markdown_to_flowables(content, styles, theme)
    
    # Add note about figures
    note_style = ParagraphStyle(
        name='Note',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        leftIndent=20,
        rightIndent=20,
        spaceBefore=6,
        spaceAfter=6,
    )
    
    figure_note = Paragraph(
        f"<i>Note: This is a simplified text-only PDF. "
        f"High-resolution figures are available separately in "
        f"/home/rain/SLMBench/papers/figures/ "
        f"({'Dark mode' if theme == 'dark' else 'Light mode'} versions with _DARK suffix). "
        f"For a full-featured PDF with embedded figures, use LaTeX or Overleaf.</i>",
        note_style
    )
    
    flowables.insert(0, Spacer(1, 0.5*inch))
    flowables.insert(1, figure_note)
    flowables.insert(2, Spacer(1, 0.3*inch))
    
    # Build PDF
    print("🏗️  Building PDF document...")
    try:
        doc.build(flowables)
        size = os.path.getsize(output_path) / 1024  # KB
        print(f"✅ PDF generated: {output_path}")
        print(f"   Size: {size:.1f} KB")
        return True
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False

def main():
    """Generate simple text PDFs."""
    print("\n" + "="*70)
    print("📊 SIMPLE PDF GENERATOR - Maaza Paper v0.4")
    print("="*70)
    print("\n⚠️  Note: This creates text-focused PDFs without embedded figures.")
    print("   Figures are available separately in the figures/ directory.")
    print("   For full-featured PDFs with embedded figures, install LaTeX.\n")
    
    # Generate light mode
    light_success = generate_pdf_simple('light')
    
    # Generate dark mode note
    print("\n" + "="*70)
    print("🌙 Dark Mode Note")
    print("="*70)
    print("\n⚠️  ReportLab doesn't support dark backgrounds easily.")
    print("   Created light PDF with reference to dark figures.")
    print("   For true dark mode PDF, use LaTeX/Overleaf approach.\n")
    
    print("="*70)
    if light_success:
        print("✅ SIMPLIFIED PDF GENERATED!")
        print("\n📁 Output:")
        print("  • MAAZA_PAPER_v0.4_LIGHT_SIMPLE.pdf")
        print("\n📊 Figures available separately:")
        print("  • figures/figure[1-4]_*.png (light mode)")
        print("  • figures/figure[1-4]_*_DARK.png (dark mode)")
        print("\n💡 For LaTeX-based PDFs with embedded figures:")
        print("  1. Install: sudo apt-get install texlive-xetex")
        print("  2. Run: ./generate_pdfs.sh")
    else:
        print("❌ PDF generation failed")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()

