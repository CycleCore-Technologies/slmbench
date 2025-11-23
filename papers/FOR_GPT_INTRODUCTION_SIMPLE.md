# GPT: Draft Introduction Section

**Context**: You already have the full context from our previous memo (Related Work section, paper plan, results).

---

## 🎯 Assignment

Draft the **Introduction** section for our academic paper (1000-1500 words).

---

## 📊 Key Results (Use These Numbers)

| Model | Params | JSONExact | Field F1 | Size |
|-------|--------|-----------|----------|------|
| SmolLM2-135M (base) | 135M | 1.9% | 0.024 | 270MB |
| **Maaza-MLM-135M** | 135M | **24.7%** | **0.520** | 270MB |
| Qwen2.5-0.5B (zero-shot) | 500M | 14.6% | 0.195 | 954MB |
| **Maaza-SLM-360M** | 360M | **55.1%** | **0.780** | 720MB |

**Key finding**: Fine-tuned 135M beats zero-shot 500M (24.7% vs 14.6%)

**EdgeJSON**: 787 examples (629 train, 158 test), 24 schemas, validated

**Training**: <2 min, LoRA, single RTX 3090

---

## 📝 Structure

**1.1 Motivation** (~400 words)
- Open with edge AI scenario (Raspberry Pi needs JSON extraction)
- Problem: LLMs too big, SLMs struggle zero-shot
- Tension: capability vs. deployability

**1.2 Our Insight** (~300 words)
- Task specialization > parameter scaling (for structured tasks)
- Fine-tuned micro models beat larger zero-shot models
- Practical edge deployment

**1.3 Contributions** (~300 words)
1. EdgeJSON benchmark (first for edge JSON extraction)
2. Maaza MLM series (135M, 360M, open-source)
3. Key empirical finding (135M fine-tuned > 500M zero-shot)
4. Open methodology (reproducible, Apache 2.0)

**1.4 Results Preview** (~200 words)
- Show main table
- Emphasize: 1.7× better, 3.7× smaller
- Practical impact

**1.5 Organization** (~100 words)
- Brief roadmap

---

## 🎨 Style

- **Hook**: Concrete scenario (Raspberry Pi, 270MB model, 50ms inference)
- **Precise claims**: "Fine-tuned 135M beats zero-shot 500M" not "small models work"
- **Active voice**: "We present...", "We demonstrate..."
- **Lead with numbers**: Results early and often

---

## ✅ Success Criteria

- Hooks reviewers (surprising result!)
- Clear gap (structured output for edge AI)
- Strong contributions (not just "we built models")
- Citation-ready (precise numbers, proper framing)

---

**Ready? Draft away!** 🚀

