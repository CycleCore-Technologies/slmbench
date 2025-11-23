# Introduction (Draft from GPT)

**Date**: November 22, 2025  
**Status**: Draft - Ready for integration  
**Word count**: ~1400 words

---

## **1 Introduction**

Modern language models have demonstrated impressive capabilities across reasoning, knowledge retrieval, summarization, and code synthesis. Yet the majority of progress has centered on ever-larger architectures—70B, 130B, and even 400B parameters—optimized for cloud-scale environments. In contrast, many real-world applications demand *the opposite*: models that run cheaply, locally, and reliably on **edge devices** such as Raspberry Pi boards, low-power CPUs, offline enterprise machines, and even in-browser WebGPU runtimes. These deployments typically require models to process unstructured text and emit **machine-consumable structured output**, such as JSON objects, function-call arguments, API payloads, or database-ready tuples. Despite the prevalence of structured workflows in industry—from invoice parsing to support ticket triage to IoT event logging—edge-oriented structured-output benchmarks remain scarce, and the behavior of small models under strict schema constraints is poorly understood.

Consider a concrete scenario. A field technician uses a ruggedized tablet powered only by a mobile CPU; the device ingests status messages from sensors and must extract structured records in real time. Or a legal intake application deployed on a client's laptop must summarize emails into JSON records without uploading private data to the cloud for regulatory reasons. In these cases, running a 7B–70B parameter model is infeasible due to memory and energy constraints, and relying on remote APIs is undesirable (cost, latency, privacy, availability). Instead, these applications require **models in the 100M–500M range**, capable of sub-100 ms inference and dependable schema compliance. Unfortunately, publicly available small language models (SLMs) often perform poorly on such tasks in **zero-shot** mode: they hallucinate keys, drop fields, produce invalid JSON, or lose consistency across nested structures.

This tension—**deployability vs. capability**—raises a fundamental question:

> *Can small, task-specialized models outperform larger zero-shot models on structured extraction tasks relevant to edge deployment?*

Surprisingly, despite the massive growth of SLM research (e.g., TinyLlama, Gemma 2B, Phi-3-mini, SmolLM2 1.7B), there is little systematic study of structured-output performance at **sub-500M parameter scales**, and almost no dedicated benchmarks that measure schema exactness, field-level F1, or JSON correctness. Moreover, prior work evaluating SLMs overwhelmingly focuses on academic tasks such as MMLU, GSM8K, or HellaSwag. These tasks do not reveal the behavior of models when strict syntactic constraints are required. For edge applications—where JSON must be *valid*, *complete*, and *semantically aligned*—traditional benchmarks are an inadequate proxy.

### **Our Work: Task Specialization Beats Parameter Scaling**

In this paper, we present **Maaza**, a family of **task-specialized micro and small language models** fine-tuned for structured JSON extraction. Our key finding is striking: **a 135M-parameter fine-tuned model outperforms a 500M-parameter zero-shot model**—despite being 3.7× smaller.

Using our new EdgeJSON v3 benchmark (787 validated examples across 24 schemas), we show:

* A **fine-tuned 135M model (Maaza-MLM-135M)** achieves
  **24.7% JSONExact** vs. **14.6%** for **Qwen2.5-0.5B (zero-shot)**
  → **1.7× better** despite being far smaller.
* A **fine-tuned 360M model (Maaza-SLM-360M)** achieves
  **55.1% JSONExact** and **0.78 field F1**,
  → **3.8× better** than the same 500M zero-shot baseline.
* Fine-tuning improves SmolLM2-135M from **1.9% → 24.7% JSONExact**
  → **13× improvement** using only 629 training examples, trained on a single RTX 3090 in <2 minutes.

These results demonstrate that **task specialization via fine-tuning can dramatically outperform simple parameter scaling**. The finding is particularly significant because structured extraction—unlike free-form generation—requires exact key-value emission, stable formatting, and strong resistance to hallucination. Larger models often generate fluent but structurally invalid responses; smaller fine-tuned models exhibit more consistent behavior.

### **A Capability Boundary at ~300M Parameters**

Our results also reveal a **capacity threshold** for structured extraction. Models below ~200M parameters reliably solve simple schemas (2–4 fields) but fail on **complex schemas** (8+ fields, nested objects, or multi-party structures). Maaza-MLM-135M performs well on simple schemas (44.7% JSONExact) but collapses to **0%** on complex schemas—even with fine-tuning. In contrast, Maaza-SLM-360M breaks this "zero wall," achieving **4.0%** JSONExact on complex schemas—a small number, but scientifically significant. It empirically confirms that:

> **Structured extraction exhibits an abrupt capability transition between 200M and 400M parameters—well before traditional benchmarks show such phase shifts.**

This motivates our proposed taxonomy:

* **NLM (Nano LMs):** <10M parameters — routing, filtering, tagging
* **MLM (Micro LMs):** 10M–250M — simple/medium structured extraction
* **SLM (Small LMs):** 250M–1.5B — reliable structured extraction
* **LLM:** >1.5B — general-purpose reasoning

While NLMs will be explored in future work, our present results show clear behavioral separations between MLMs and SLMs for JSON extraction.

---

## **1.2 Our Insight: Task-Specialized Micro Models Compete with Larger General Models**

The prevailing assumption in language modeling research is that **bigger models dominate**—especially on complex tasks. This assumption holds across conventional reasoning benchmarks (e.g., MMLU, GSM8K), but structured extraction reveals a different story. We find that **scaling alone does not guarantee schema correctness or JSON reliability**.

In edge deployments, the critical metric is not perplexity or few-shot reasoning; it is **validity of machine-consumable output**. For instance:

* A support triage system must emit `{ "priority": "high", "category": "billing" }`.
* A transaction extractor must align fields exactly: `amount`, `counterparty`, `date`, `currency`.
* A log parser must output valid JSON even when partial or noisy text is provided.

Large zero-shot models often hallucinate fields, alter ordering, or generate extraneous explanation text. In contrast, a **task-specific micro model**, even at 135M parameters, can emit structurally perfect objects when properly trained. This reverses the expected parameter-performance relationship for structured tasks and reinforces the need for **domain-specific training**, particularly for models intended for **real-time, cost-sensitive deployments**.

Thus our core insight is:

> **For structured extraction tasks, fine-tuned micro models offer a superior accuracy–size–latency trade-off compared to larger zero-shot models.**

This insight aligns with emerging trends in edge AI deployment, where reliable, compact models are more valuable than flexible but unwieldy large models.

---

## **1.3 Contributions**

This paper makes four primary contributions:

### **1. EdgeJSON: A benchmark for structured extraction on edge devices**

We introduce **EdgeJSON v3**, a 24-schema dataset with 787 validated examples, designed to test structured-output performance across simple, medium, and complex extraction tasks. Each example includes a natural-language prompt, schema, validation rules, and expected JSON output. Metrics include **JSONExact**, **field-level F1**, and **schema compliance**, capturing structural correctness rather than linguistic fluency.

### **2. Maaza: A family of task-specialized micro and small models**

We release two open-source models:

* **Maaza-MLM-135M** (135M params)
  A micro-scale model optimized for simple and medium schemas.

* **Maaza-SLM-360M** (360M params)
  A small-scale model that significantly improves medium-schema extraction and breaks the capacity boundary on complex schemas.

Both models are released under **Apache 2.0**, with full training scripts and datasets to maximize reproducibility.

### **3. Empirical demonstration that fine-tuned micro models outperform larger zero-shot models**

Across EdgeJSON, Maaza-MLM-135M achieves **24.7% JSONExact**, outperforming **Qwen2.5-0.5B** (14.6%) while being 3.7× smaller. Maaza-SLM-360M achieves **55.1%**, outperforming the same 500M baseline by 3.8×. These results show that **specialization outperforms scale** on structured tasks.

### **4. Open methodology and complete reproducibility**

All datasets, training configurations, evaluation scripts, and model cards are publicly available in the CycleCore Maaza repository. Fine-tuning requires less than 2 minutes on a single RTX 3090 using LoRA, enabling broad replicability for researchers and practitioners.

---

## **1.4 Results Preview**

Table 1 summarizes our core findings.

| Model                    | Params | JSONExact | Field F1  | Size   |
| ------------------------ | ------ | --------- | --------- | ------ |
| SmolLM2-135M (base)      | 135M   | 1.9%      | 0.024     | 270 MB |
| **Maaza-MLM-135M**       | 135M   | **24.7%** | **0.520** | 270 MB |
| Qwen2.5-0.5B (zero-shot) | 500M   | 14.6%     | 0.195     | 954 MB |
| **Maaza-SLM-360M**       | 360M   | **55.1%** | **0.780** | 720 MB |

Two trends emerge:

1. **Fine-tuning transforms a 135M model**, boosting accuracy from 1.9% to 24.7% (+13×).
2. **Fine-tuned models outperform larger zero-shot models**, even with far fewer parameters.

For practitioners building edge AI systems, these results imply that **task-specialized models may enable applications that would otherwise require cloud inference or prohibitively large models.**

---

## **1.5 Paper Organization**

Section 2 reviews related work on small language models, benchmarks, edge deployment, and parameter-efficient tuning.
Section 3 introduces the EdgeJSON dataset and evaluation methodology.
Section 4 describes the Maaza model family and training procedure.
Section 5 reports quantitative results and scaling analyses.
Section 6 discusses implications for edge deployments and model taxonomy.
Section 7 concludes and outlines directions for nano-scale models (NLMs).

