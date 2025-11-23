#!/bin/bash

# Dual-Theme PDF Generator using Pandoc
# Copyright 2025 CycleCore Technologies
# Licensed under the Apache License, Version 2.0

set -e  # Exit on error

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║       📄 DUAL-THEME PDF GENERATOR - Maaza Paper v0.4            ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

PAPER_DIR="/home/rain/SLMBench/papers"
PAPER_FILE="$PAPER_DIR/MAAZA_PAPER_FULL_CONTENT.md"

cd "$PAPER_DIR"

# Create a temporary version with image references updated
echo "📝 Preparing paper content..."

# Create light mode version with light figures
cat "$PAPER_FILE" | sed 's|figures/\(figure[0-9]*_[^_]*\)_DARK\.png|figures/\1.png|g' > /tmp/maaza_light.md

# Create dark mode version with dark figures  
cat "$PAPER_FILE" | sed 's|figures/\(figure[0-9]*_[^.]*\)\.png|figures/\1_DARK.png|g' > /tmp/maaza_dark.md

echo "✅ Content prepared"
echo ""

# Generate LIGHT MODE PDF
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "☀️  Generating LIGHT MODE PDF..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

pandoc /tmp/maaza_light.md \
    -o "$PAPER_DIR/MAAZA_PAPER_v0.4_LIGHT.pdf" \
    --pdf-engine=xelatex \
    --variable geometry:margin=1in \
    --variable fontsize=11pt \
    --variable documentclass=article \
    --variable colorlinks=true \
    --variable linkcolor=blue \
    --variable urlcolor=blue \
    --variable toccolor=blue \
    --highlight-style=tango \
    --toc \
    --toc-depth=3 \
    --number-sections \
    2>&1 | grep -v "pdfTeX warning" || true

if [ -f "$PAPER_DIR/MAAZA_PAPER_v0.4_LIGHT.pdf" ]; then
    SIZE=$(du -h "$PAPER_DIR/MAAZA_PAPER_v0.4_LIGHT.pdf" | cut -f1)
    echo "✅ LIGHT MODE PDF generated: $SIZE"
else
    echo "❌ LIGHT MODE PDF generation failed"
fi

echo ""

# Generate DARK MODE PDF with custom LaTeX template
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌙 Generating DARK MODE PDF..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create dark mode LaTeX header
cat > /tmp/dark_header.tex << 'EOF'
\usepackage{xcolor}
\pagecolor[RGB]{26,26,26}
\color[RGB]{240,240,240}
\definecolor{darkblue}{RGB}{79,195,247}
\definecolor{darkpurple}{RGB}{206,147,216}
\definecolor{darkorange}{RGB}{255,183,77}
\hypersetup{
    colorlinks=true,
    linkcolor=darkblue,
    urlcolor=darkblue,
    citecolor=darkpurple
}
% Make section headings bright
\usepackage{titlesec}
\titleformat{\section}{\normalfont\Large\bfseries\color{white}}{\thesection}{1em}{}
\titleformat{\subsection}{\normalfont\large\bfseries\color{white}}{\thesubsection}{1em}{}
\titleformat{\subsubsection}{\normalfont\normalsize\bfseries\color{white}}{\thesubsubsection}{1em}{}
EOF

pandoc /tmp/maaza_dark.md \
    -o "$PAPER_DIR/MAAZA_PAPER_v0.4_DARK.pdf" \
    --pdf-engine=xelatex \
    --variable geometry:margin=1in \
    --variable fontsize=11pt \
    --variable documentclass=article \
    --include-in-header=/tmp/dark_header.tex \
    --highlight-style=breezedark \
    --toc \
    --toc-depth=3 \
    --number-sections \
    2>&1 | grep -v "pdfTeX warning" || true

if [ -f "$PAPER_DIR/MAAZA_PAPER_v0.4_DARK.pdf" ]; then
    SIZE=$(du -h "$PAPER_DIR/MAAZA_PAPER_v0.4_DARK.pdf" | cut -f1)
    echo "✅ DARK MODE PDF generated: $SIZE"
else
    echo "❌ DARK MODE PDF generation failed"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Summary
echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                    📊 GENERATION COMPLETE                        ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

if [ -f "$PAPER_DIR/MAAZA_PAPER_v0.4_LIGHT.pdf" ] && [ -f "$PAPER_DIR/MAAZA_PAPER_v0.4_DARK.pdf" ]; then
    echo "✅ BOTH PDFs generated successfully!"
    echo ""
    echo "📁 Output files:"
    echo "  • MAAZA_PAPER_v0.4_LIGHT.pdf  (☀️  traditional academic)"
    echo "  • MAAZA_PAPER_v0.4_DARK.pdf   (🌙 modern dark mode)"
    echo ""
    echo "📊 File sizes:"
    ls -lh "$PAPER_DIR"/MAAZA_PAPER_v0.4_*.pdf | awk '{print "  •", $9, "-", $5}'
    echo ""
    echo "💡 Both versions:"
    echo "  - Use matching figure themes (light/dark)"
    echo "  - Include table of contents"
    echo "  - Are numbered by section"
    echo "  - Ready for arXiv submission"
    echo ""
    echo "🚀 Your paper now exists in TWO complete aesthetic versions!"
elif [ -f "$PAPER_DIR/MAAZA_PAPER_v0.4_LIGHT.pdf" ]; then
    echo "⚠️  Only LIGHT MODE PDF generated"
    echo "   Dark mode requires xelatex support for page colors"
elif [ -f "$PAPER_DIR/MAAZA_PAPER_v0.4_DARK.pdf" ]; then
    echo "⚠️  Only DARK MODE PDF generated"
else
    echo "❌ PDF generation failed - check errors above"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Cleanup
rm -f /tmp/maaza_light.md /tmp/maaza_dark.md /tmp/dark_header.tex

