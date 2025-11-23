# Naming Conventions & Brand Hierarchy

**Document**: Official naming standards for CycleCore Technologies products  
**Date**: November 2025  
**Status**: Canonical Reference

---

## 🏢 Organization Names

### HuggingFace
- **Organization**: `CycleCoreTechnologies`
- **Display Name**: CycleCore Technologies
- **URL**: https://huggingface.co/CycleCoreTechnologies

### Legal Entity
- **Full Name**: CycleCore Technologies LLC
- **Short Name**: CycleCore Technologies
- **Abbreviation**: CycleCore (informal)

### GitHub
- **Organization**: `CycleCore` (preferred)
- **Alternative**: `CycleCoreTechnologies` (if CycleCore unavailable)
- **URL**: https://github.com/CycleCore/SLMBench

---

## 📦 Product Hierarchy

```
CycleCore Technologies (Company)
    └── SLMBench (Benchmark Suite)
            ├── EdgeJSON (JSON Extraction Benchmark)
            ├── EdgeIntent (Intent Classification) [Coming Soon]
            └── EdgeFuncCall (Function Calling) [Coming Soon]
```

---

## 🎯 Product Names

### SLMBench (Primary Product)
- **Full Name**: SLMBench
- **Alternative**: SLM-Bench (with hyphen, less preferred)
- **Description**: Benchmark suite for Small Language Models
- **Repository**: `SLMBench` (no hyphen)
- **Domain**: slmbench.com

**Usage:**
- ✅ "SLMBench is an open-source benchmark suite..."
- ✅ "We evaluated the model on SLMBench"
- ⚠️ "SLM-Bench" (acceptable but less preferred)
- ❌ "SLM Bench" (no space)

### EdgeJSON (Benchmark Task)
- **Full Name**: EdgeJSON
- **Alternative**: Edge JSON (with space, less preferred)
- **Description**: JSON extraction benchmark (part of SLMBench)
- **Directory**: `benchmarks/edge_json/`

**Usage:**
- ✅ "EdgeJSON evaluates structured data extraction"
- ✅ "Trained on EdgeJSON v3 dataset"
- ⚠️ "Edge JSON" (acceptable in prose)
- ❌ "edge-json" (no hyphen)

### EdgeIntent
- **Full Name**: EdgeIntent
- **Description**: Intent classification benchmark

### EdgeFuncCall
- **Full Name**: EdgeFuncCall
- **Description**: Function calling benchmark

---

## 🤖 Model Names

### Naming Pattern
```
Maaza-{SIZE}-{TASK}-v{VERSION}
```

**Components:**
- **Maaza**: Model series name (means "pride" in Swahili)
- **SIZE**: MLM (Micro, <200M) or SLM (Small, 200M-500M)
- **TASK**: JSON, Intent, FuncCall, etc.
- **VERSION**: Semantic versioning (v1.0.0, v1.1.0, etc.)

### Current Models
1. **Maaza-MLM-135M-JSON-v1**
   - Full: `Maaza-MLM-135M-JSON-v1.0.0`
   - Short: `Maaza-MLM-135M-JSON-v1`
   - HuggingFace: `CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1`

2. **Maaza-SLM-360M-JSON-v1**
   - Full: `Maaza-SLM-360M-JSON-v1.0.0`
   - Short: `Maaza-SLM-360M-JSON-v1`
   - HuggingFace: `CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1`

### Model Size Categories
- **MLM** (Micro Language Model): <200M parameters
- **SLM** (Small Language Model): 200M-500M parameters
- **NLM** (Nano Language Model): <100M parameters (future)

---

## 📝 Capitalization Rules

### Product Names
- **SLMBench**: Always capitalize S, L, M, B (camelCase)
- **EdgeJSON**: Always capitalize E, J, S, O, N (camelCase)
- **Maaza**: Always capitalize first letter only

### Company Names
- **CycleCore Technologies**: Always capitalize both words
- **CycleCore**: Always capitalize C (both instances)

### Abbreviations
- **SLM**: Always uppercase (Small Language Model)
- **MLM**: Always uppercase (Micro Language Model)
- **JSON**: Always uppercase (JavaScript Object Notation)

---

## 🔗 URLs & Domains

### Current
- **HuggingFace**: https://huggingface.co/CycleCoreTechnologies
- **GitHub**: https://github.com/CycleCore/SLMBench (to be created)

### Future
- **Website**: slmbench.com
- **Company**: cyclecore.tech
- **Email**: hi@cyclecore.ai

---

## 📄 File Naming

### Repositories
- **Main**: `SLMBench` (no hyphen)
- **Benchmarks**: `edge_json`, `edge_intent`, `edge_funccall` (snake_case)

### Documentation
- **Markdown**: `UPPERCASE_WITH_UNDERSCORES.md` (e.g., `README.md`, `LICENSE.md`)
- **Code**: `lowercase_with_underscores.py` (Python snake_case)

### Datasets
- **Format**: `{benchmark}_{split}_v{version}.jsonl`
- **Examples**: 
  - `edgejson_train_v3.jsonl`
  - `edgejson_test_v3.jsonl`

---

## 🎨 Branding Guidelines

### Logo Usage
- **File**: `cyclecore-logo-400x400.png`
- **Location**: `assets/logos/`
- **Style**: Black background, white text
- **Format**: PNG (400x400) or SVG

### Color Scheme
- **Primary**: Black (#000000)
- **Secondary**: White (#FFFFFF)
- **Accent**: (To be defined)

### Typography
- **Headers**: Bold, sans-serif
- **Body**: Regular, sans-serif
- **Code**: Monospace

---

## 📊 Citation Format

### SLMBench (Benchmark Suite)
```bibtex
@misc{cyclecore2025slmbench,
  title={SLMBench: Practical Benchmarks for Small Language Models},
  author={CycleCore Technologies},
  year={2025},
  howpublished={\url{https://github.com/CycleCore/SLMBench}}
}
```

### Maaza Models
```bibtex
@misc{cyclecore2025maaza,
  title={Maaza: Task-Specialized Small Language Models for Edge Deployment},
  author={CycleCore Technologies},
  year={2025},
  howpublished={\url{https://huggingface.co/CycleCoreTechnologies}}
}
```

---

## ✅ Quick Reference

| Item | Correct | Incorrect |
|------|---------|-----------|
| Company | CycleCore Technologies | Cycle Core, cyclecore |
| Product | SLMBench | SLM-Bench, SLM Bench, slmbench |
| Benchmark | EdgeJSON | Edge-JSON, edge json |
| Model Series | Maaza | MAAZA, maaza |
| Size Class | MLM, SLM | Mlm, slm, mlm |
| HF Org | CycleCoreTechnologies | CycleCore, cyclecore |
| GitHub Org | CycleCore | CycleCoreTechnologies |

---

## 🔄 Historical Names (Deprecated)

### Old Names (Do Not Use)
- ❌ "SLM-Bench Edge Pack" (too long, deprecated)
- ❌ "Edge Pack v1.0" (confusing, deprecated)
- ❌ "CycleCore-Maaza-MLM" (old format, use new format)

### Migration Notes
- Old model cards may reference "SLM-Bench Edge Pack" - update to "SLMBench"
- Internal docs may use "Edge Pack" - replace with "SLMBench"

---

## 📞 Contact & Support

### Public
- **HuggingFace**: https://huggingface.co/CycleCoreTechnologies
- **Email**: hi@cyclecore.ai

### Internal
- **Federation SuperBus**: (internal communication)
- **Territory**: Puerto Rico Model (Lexopoly Federation)

---

## 📚 Related Documents

- **Licensing Strategy**: `/docs/LICENSING_STRATEGY.md`
- **Launch Status**: `/LAUNCH_STATUS.md`
- **Upload Success**: `/UPLOAD_SUCCESS.md`
- **Company Profile**: `/docs/CycleCoreTechnologies_Profile.pdf`

---

*Last updated: November 2025*  
*Maintained by: CycleCore Technologies*  
*Version: 1.0*

