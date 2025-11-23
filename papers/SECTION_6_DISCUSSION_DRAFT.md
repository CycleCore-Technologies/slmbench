# Section 6: Discussion (Draft)

**Date**: November 22, 2025  
**Status**: Draft  
**Word count**: ~800 words

---

## **6. Discussion**

Our experiments demonstrate that task-specialized micro models can outperform larger zero-shot models on structured data extraction. We now discuss the implications of these findings, their limitations, and directions for future work.

### **6.1 When Do Micro Models Excel?**

Our results identify three conditions under which fine-tuned micro models (135M-360M params) excel:

#### **6.1.1 Task-Specific Requirements**

Structured extraction tasks have well-defined success criteria: exact field matching, schema compliance, and JSON validity. Unlike open-ended generation (where "better" is subjective), structured tasks allow focused optimization. Fine-tuning on 629 examples provides sufficient signal for models to learn:
- Field recognition patterns
- JSON formatting conventions
- Schema structure memorization

This contrasts with reasoning tasks (GSM8K, MMLU) where broader world knowledge and multi-step inference favor larger models.

#### **6.1.2 Resource-Constrained Deployment**

For edge AI scenarios with hard constraints:
- **Memory**: 270MB (MLM-135M) vs. 954MB (Qwen-0.5B)
- **Latency**: 48ms vs. 9,480ms
- **Cost**: Local inference vs. API calls ($0.01/request)

Task-specialized micro models enable applications that would otherwise be infeasible (Raspberry Pi, browser-based inference, offline devices).

#### **6.1.3 Rapid Iteration Requirements**

Training time matters for practitioners:
- Maaza-MLM-135M: 49 seconds
- Maaza-SLM-360M: 90 seconds

This enables fast experimentation, A/B testing, and domain adaptation—critical for production systems where requirements evolve rapidly.

### **6.2 Capacity Thresholds for Structured Tasks**

Our results reveal a **qualitative capacity boundary** around 300M parameters:

**Below 200M** (e.g., Maaza-MLM-135M):
- Excellent on simple schemas (44.7%)
- Usable on medium schemas (13.5%)
- **Zero capability on complex schemas (0.0%)**

**Above 300M** (e.g., Maaza-SLM-360M):
- Strong on simple schemas (78.9%)
- Reliable on medium schemas (51.4%)
- **First non-zero on complex schemas (4.0%)**

This threshold appears earlier than in traditional benchmarks (MMLU, HellaSwag), where model capabilities scale more gradually. We hypothesize that structured extraction requires **explicit memory capacity** for:
- Tracking multiple field dependencies
- Maintaining nested object structures
- Coordinating array elements with parent objects

Future work should investigate whether architectural changes (e.g., attention mechanisms, memory augmentation) can lower this threshold.

### **6.3 Comparison to Related Work**

#### **6.3.1 SLM-Bench (Pham et al., 2025)**

Pham et al.'s SLM-Bench evaluates small models on general NLP tasks (MMLU, GSM8K, HellaSwag). Our EdgeJSON complements their work by focusing on **structured output reliability**—a gap in existing benchmarks. Key differences:

| Aspect | SLM-Bench (Pham) | EdgeJSON (Ours) |
|--------|-----------------|-----------------|
| **Focus** | Reasoning, knowledge | Structured extraction |
| **Metrics** | Accuracy, perplexity | JSONExact, Field F1 |
| **Task Type** | Multiple-choice, QA | JSON generation |
| **Use Case** | General capability | Edge AI deployment |

Both benchmarks are valuable: SLM-Bench for broad capability assessment, EdgeJSON for deployment-specific validation.

#### **6.3.2 Code Generation Models**

Our approach shares similarities with code generation models (CodeLlama, StarCoder) that are fine-tuned on structured output (code). However, JSON extraction differs in key ways:
- **Shorter outputs**: JSON objects are typically 50-200 tokens vs. 500+ for code
- **Stricter constraints**: Invalid JSON fails completely; syntax errors in code are debuggable
- **Domain-specific**: JSON schemas vary widely across applications

This suggests that specialized micro models may excel in other structured domains (SQL generation, regex synthesis, API call construction).

### **6.4 Limitations**

#### **6.4.1 Dataset**

**Synthetic Data**: While validated for mathematical consistency, our synthetic data may not capture:
- Linguistic diversity of real-world prompts
- Edge cases and adversarial inputs
- Domain-specific terminology

**English-Only**: EdgeJSON includes only English prompts. Multilingual evaluation remains future work.

**Scale**: 787 examples is moderate. Larger datasets (10K+ examples) may reveal different scaling behaviors.

#### **6.4.2 Baseline Selection**

We evaluated one zero-shot baseline (Qwen2.5-0.5B). Additional baselines would strengthen claims:
- **Instruction-tuned models**: Qwen2.5-0.5B-Instruct, Llama-3.2-1B-Instruct
- **Larger SLMs**: Phi-3-mini (3.8B), Gemma-2B
- **Commercial APIs**: GPT-3.5-turbo, Claude-3-haiku

However, our focus on **edge-deployable models** (<1GB) justifies the current scope.

#### **6.4.3 Task Scope**

EdgeJSON measures single-turn extraction. Real-world applications may require:
- **Multi-turn clarification**: Model asks for missing information
- **Error recovery**: Model detects and corrects invalid outputs
- **Partial extraction**: Model handles incomplete or noisy inputs

Future benchmarks should address these scenarios.

### **6.5 Practical Implications**

#### **6.5.1 For Practitioners**

Our results suggest a deployment strategy:
1. **Prototype with micro models**: Test Maaza-MLM-135M (270MB) for simple schemas
2. **Scale to small models**: Use Maaza-SLM-360M (720MB) for complex schemas
3. **Fine-tune on domain data**: Even 200-300 examples can provide significant gains
4. **Reserve cloud models for exceptions**: Use GPT-4/Claude only when edge models fail

This "edge-first, cloud-fallback" approach balances cost, latency, and privacy.

#### **6.5.2 For Researchers**

Our findings open several research directions:
- **NLM exploration**: Can <50M models handle ultra-simple schemas?
- **Architectural improvements**: Can attention mechanisms reduce capacity thresholds?
- **Multi-task learning**: Can one model handle multiple schema types?
- **Cross-lingual transfer**: How well do fine-tuned models generalize across languages?

### **6.6 Broader Impact**

**Positive**:
- **Privacy**: Local inference avoids data leakage to cloud providers
- **Accessibility**: Low-resource organizations can deploy AI without API costs
- **Sustainability**: Smaller models reduce energy consumption

**Potential Concerns**:
- **Automation**: Structured extraction may automate tasks currently done by humans
- **Bias**: Synthetic training data may not reflect demographic diversity
- **Misuse**: Efficient extraction tools could enable large-scale data scraping

We advocate for responsible deployment with human oversight, especially in high-stakes domains (healthcare, finance, legal).

---

**End of Section 6**

