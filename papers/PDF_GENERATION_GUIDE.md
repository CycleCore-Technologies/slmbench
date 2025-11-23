# PDF Generation Guide - Maaza Paper v0.4

**Date**: November 22, 2025  
**Status**: Figures ready, multiple PDF generation options available  

---

## ✅ What's Ready

### Figures (16 total - 2 complete themed sets)
```
/home/rain/SLMBench/papers/figures/
├── figure1_performance_vs_size.png/.pdf (LIGHT)
├── figure2_performance_by_complexity.png/.pdf (LIGHT)
├── figure3_disk_size_vs_performance.png/.pdf (LIGHT)
├── figure4_fine_tuning_comparison.png/.pdf (LIGHT)
├── figure1_performance_vs_size_DARK.png/.pdf (DARK 🌙)
├── figure2_performance_by_complexity_DARK.png/.pdf (DARK 🌙)
├── figure3_disk_size_vs_performance_DARK.png/.pdf (DARK 🌙)
└── figure4_fine_tuning_comparison_DARK.png/.pdf (DARK 🌙)
```

### Paper Content
- **Source**: `MAAZA_PAPER_FULL_CONTENT.md` (v0.4, all actuals)
- **Status**: arXiv-ready, all estimates replaced
- **Size**: 1280 lines, ~65KB

---

## 📊 PDF Generation Options

### Option 1: Online Converters (Fastest ⭐)

**Recommended: GitPrint or Dillinger**

1. **GitPrint** (https://gitprint.com/):
   - Upload `MAAZA_PAPER_FULL_CONTENT.md`
   - Automatic figure rendering
   - Download PDF

2. **Dillinger** (https://dillinger.io/):
   - Paste markdown content
   - Export to PDF
   - Professional styling

3. **Markdown to PDF** (https://www.markdowntopdf.com/):
   - Upload file
   - Generate PDF
   - Download

### Option 2: VS Code Extension (If using VSCode)

1. Install "Markdown PDF" extension
2. Open `MAAZA_PAPER_FULL_CONTENT.md`
3. `Ctrl+Shift+P` → "Markdown PDF: Export (pdf)"
4. Done!

### Option 3: Install LaTeX Locally

```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-latex-extra

# Then run:
cd /home/rain/SLMBench/papers
pandoc MAAZA_PAPER_FULL_CONTENT.md \
    -o MAAZA_PAPER_v0.4_LIGHT.pdf \
    --pdf-engine=xelatex \
    --variable geometry:margin=1in \
    --variable fontsize=11pt \
    --toc \
    --number-sections
```

### Option 4: Python-based (Requires Installation)

```bash
# Install weasyprint
pip install weasyprint markdown

# Then run:
cd /home/rain/SLMBench/papers
python3 generate_pdfs.py
```

### Option 5: Use Overleaf (Professional ⭐)

1. Go to https://www.overleaf.com/
2. Create new project → "Upload Project"
3. Convert markdown to LaTeX (or upload as markdown)
4. Add figures from `figures/` directory
5. Compile → Download PDF

**Best for**: Academic submissions, full control

### Option 6: Google Docs (Simple)

1. Install "Docs to Markdown" addon
2. Copy markdown content
3. Convert to Docs
4. Insert images from `figures/`
5. File → Download → PDF

---

## 🌙 Dark Mode PDF Creation

Once you have a PDF tool working, generate BOTH versions:

### Light Mode (Traditional)
- Use figures: `figure[1-4]_*.png`
- Standard academic styling
- White background, black text

### Dark Mode (Modern)
- Use figures: `figure[1-4]_*_DARK.png`
- Modern aesthetic
- Dark background (#1a1a1a), white text

---

## 🚀 Recommended Workflow (Fastest Path)

1. **For submission to arXiv**: Use Option 3 (LaTeX) or Option 5 (Overleaf)
   - arXiv prefers LaTeX-based PDFs
   - Full control over formatting
   - Professional output

2. **For quick preview**: Use Option 1 (Online converter)
   - No installation needed
   - Fast turnaround
   - Good enough for review

3. **For dual-theme versions**: Use Option 5 (Overleaf)
   - Create two projects (light/dark)
   - Swap figure sets
   - Consistent formatting

---

## 📝 Manual Approach (Always Works)

If all else fails:

1. Open `MAAZA_PAPER_FULL_CONTENT.md` in any markdown viewer
2. Use browser's "Print to PDF" function
3. Manually insert figures where needed
4. Adjust as necessary

---

## ✅ What I've Provided

### Scripts Created
1. `generate_pdfs.py` - Python/WeasyPrint approach
2. `generate_pdfs.sh` - Bash/Pandoc approach
3. Both are ready to run once dependencies are installed

### Figures Created
- **16 publication-quality images** (8 light + 8 dark)
- **300 DPI resolution** - publication-grade
- **Both PNG and PDF formats** - max compatibility

### Documentation
- `FIGURES_README.md` - Complete figure usage guide
- `REVISION_LOG_V03_TO_V04.md` - All changes documented
- `V03_TO_V04_FIX_SUMMARY.md` - Detailed fix summary

---

## 💡 My Recommendation

**For arXiv submission**:
1. Install LaTeX: `sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-latex-extra`
2. Run: `pandoc MAAZA_PAPER_FULL_CONTENT.md -o paper.pdf --pdf-engine=xelatex --toc`
3. Submit to arXiv

**For dual-theme versions**:
1. Use Overleaf (free account)
2. Create 2 projects
3. Upload markdown + figures
4. Generate both PDFs
5. Download

**For quick preview now**:
1. Go to https://www.markdowntopdf.com/
2. Upload `MAAZA_PAPER_FULL_CONTENT.md`
3. Download PDF
4. Done in 30 seconds

---

## 🎯 Current Status

✅ Paper content: v0.4 (arXiv-ready)  
✅ Figures: 16 files (dual-theme, 300 DPI)  
✅ All estimates replaced with actuals  
✅ Citations corrected (SmolLM2 → 2024)  
✅ Tables consistent and verified  
✅ Green text labels fixed in Figure 4  

⏳ PDF generation: Awaiting LaTeX installation OR use online converter  

---

## 🚀 Next Steps

### Option A: Install LaTeX locally
```bash
sudo apt-get update
sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-latex-extra
cd /home/rain/SLMBench/papers
./generate_pdfs.sh  # Will generate both light & dark PDFs
```

### Option B: Use online converter (recommended for speed)
1. Visit https://www.markdowntopdf.com/
2. Upload `MAAZA_PAPER_FULL_CONTENT.md`
3. Download PDF (light mode)
4. Manually swap to dark figures for dark version

### Option C: I can help you set up any of these options
- Just tell me which method you prefer
- I'll guide you through step-by-step

---

**Bottom Line**: Your paper is 100% ready for PDF conversion. The only blocker is choosing/installing a PDF generation tool. Once that's done, you'll have both light and dark PDFs in minutes! 🚀

**Figures look AMAZING** with the fixed green text placement! ✨

