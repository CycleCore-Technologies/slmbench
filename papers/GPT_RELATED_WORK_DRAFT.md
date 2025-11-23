# Related Work Section - Draft from GPT

**Date**: November 21, 2025  
**Source**: GPT collaboration  
**Status**: First draft - ready for review and integration

---

## Related Work

### A. Small Language Models (SLMs) and Capacity-Efficient LMs

The success of large language models (LLMs) such as GPT-3 and GPT-4 has motivated a parallel line of work on **small language models (SLMs)** that aim to retain as much capability as possible under tight parameter and hardware budgets. Early work on compact transformers largely focused on distilling BERT-style encoders for mobile or low-latency scenarios, including DistilBERT [Sanh et al., 2019] and TinyBERT [Jiao et al., 2020], which demonstrated that 4- to 6-layer distilled models can retain 96–97% of BERT's performance on GLUE while being 40–90% smaller and significantly faster. MobileBERT [Sun et al., 2020] further showed that a carefully designed bottlenecked architecture can deliver 4.3× smaller and 5.5× faster BERT variants that run efficiently on phones.

In the generative era, several families of small decoder-only models have emerged. TinyLlama [Zhang et al., 2024] pretrains a 1.1B-parameter LLaMA-style model on roughly one trillion tokens, showing that with careful data curation and training optimizations, 1B-scale models can reach strong performance on downstream tasks while being feasible to train on moderate clusters. SmolLM and SmolLM2 [Allal et al., 2025] push this line further with a family of decoder-only models at 135M, 360M, and 1.7B parameters. SmolLM2 is trained on up to ~11T tokens and evaluated across a broad set of reasoning, coding, and language benchmarks; the authors report that their 1.7B model outperforms other open small models under 2B parameters while being explicitly designed for cost-effective deployment on commodity GPUs and edge devices.

Industry models have also embraced the SLM framing. Microsoft's Phi-3 family [Abdin et al., 2024; Microsoft, 2024] introduces 3.8B–14B models that combine heavily curated synthetic and educational data with scaled-up pretraining; the 3.8B "phi-3-mini" model is advertised as "tiny but mighty," rivaling GPT-3.5 and Mixtral 8×7B on MMLU and MT-Bench while being small enough to run on a phone.  Google's Gemma 2 series [Gemma Team, 2024] offers 2B–27B "lightweight, state-of-the-art open models" with architecture tweaks such as local–global attention and grouped-query attention to improve throughput on smaller hardware.  Meta's Llama 3.2 models include text-only 1B and 3B variants explicitly targeting edge and mobile devices [Meta AI, 2024].

These developments collectively show that models in the **~100M–4B parameter range** can achieve competitive performance on standard benchmarks while being deployable on laptops, phones, and single-GPU servers. However, most of the reported results still focus on **classical evaluation suites** such as MMLU, GSM8K, and coding benchmarks, and thus primarily measure language understanding and reasoning rather than **structured output reliability** (e.g., strict JSON adherence, schema compliance). Our Maaza models live at the lower end of this spectrum (135M and 360M parameters) and target precisely this underexplored regime: **high-fidelity structured extraction under micro-scale capacity constraints**.

### B. Benchmarks for Language Models and Gaps in Structured Output Evaluation

Large-scale benchmarks such as **GLUE** [Wang et al., 2018], **SuperGLUE** [Wang et al., 2019], **MMLU** [Hendrycks et al., 2021], **HellaSwag** [Zellers et al., 2019], **GSM8K** [Cobbe et al., 2021], and **HumanEval** [Chen et al., 2021] have become standard for evaluating both large and small language models. These benchmarks predominantly measure multiple-choice question answering, natural language inference, commonsense reasoning, mathematics word problems, and functional code generation. Recent technical reports for Qwen2.5 [Yang et al., 2024], Phi-3 [Abdin et al., 2024], and Gemma 2 [Gemma Team, 2024] all report results on such benchmarks, and SmolLM2 likewise positions its performance relative to these suites.

More recently, **SLM-Bench** [Pham et al., 2025] proposes a comprehensive benchmark specifically for small language models. SLM-Bench evaluates 20+ SLMs across eleven metrics that jointly capture **correctness, computation, and consumption**, and runs them on four hardware configurations to quantify trade-offs in energy efficiency and throughput.  SLM-Bench is a major step toward holistic evaluation of SLMs, but its task mix remains centered on standard NLP and reasoning tasks; it does not directly address **structured output constraints** such as strict JSON schema adherence, function-calling correctness, or end-to-end schema compliance.

There is thus a notable **gap** between existing benchmarks and the needs of **edge and application developers**, who increasingly require models that can reliably produce **machine-consumable outputs**—for example, JSON objects, database rows, or API argument dictionaries—rather than only free-form natural language. While some recent work measures function-calling correctness or JSON mode reliability for large models in proprietary evaluations, there is limited open, reproducible benchmarking for **small models** on structured extraction tasks.

Our EdgeJSON benchmark is designed to address this gap. It provides a curated suite of 24 JSON schemas spanning simple (2–4 fields), medium (4–8 fields), and complex (8+ fields, nested and multi-party) structured extraction tasks, with metrics such as **JSONExact**, **field-level F1**, and **schema compliance**. These metrics explicitly penalize syntactic and structural errors that would break downstream tools. By evaluating Maaza and baseline models on EdgeJSON, we show that **task-specialized micro models can outperform larger zero-shot models** on structured extraction, even when they underperform on traditional text benchmarks.

### C. Edge AI and On-Device LLM Deployment

The push toward **edge AI** has intensified the need for compact models that can run with minimal memory, compute, and energy budgets. Early work on resource-efficient NLP highlighted the trade-off between accuracy and memory/latency in mobile settings [Sun et al., 2020; Sanh et al., 2019; Jiao et al., 2020]. More recent surveys explicitly focus on **edge LLMs**. Zheng et al. [2024] and Wang et al. [2025] provide comprehensive overviews of techniques for designing, compressing, and deploying LLMs on edge devices, covering model pruning, quantization, distillation, efficient attention mechanisms, and runtime optimizations.

On the systems side, frameworks such as **TensorFlow Lite**, **ONNX Runtime**, and **TVM** have made it possible to deploy neural networks on phones, microcontrollers, and embedded devices. More recently, **WebLLM** [Zeng et al., 2024] and **Transformers.js** [Hugging Face, 2024] demonstrate that full LLM inference can be run entirely in the browser using WebGPU, enabling **zero-server, privacy-preserving** deployments that still achieve up to 80% of native GPU performance.  Commercial vendors are also integrating small models into browsers and operating systems; for example, Microsoft exposes its on-device Phi-4-mini model via new Edge APIs for web apps [Microsoft Edge Team, 2025].

Despite this progress, **structured-output reliability** on edge devices remains underexplored. Most edge-oriented work either benchmarks throughput and latency of generic chat models or focuses on classification/regression tasks. There is little published work on deploying **task-specialized micro models that can reliably emit JSON or function-call outputs** on constrained devices such as Raspberry Pi, CPU-only laptops, or in-browser environments. Our Maaza models are explicitly targeted at this regime: 135M and 360M parameter models that can run comfortably on a single consumer GPU (and down-scaled to CPU / browser) while producing high-fidelity structured outputs on EdgeJSON.

### D. Fine-Tuning, Distillation, and Parameter-Efficient Adaptation

The idea that **small, task-specific models** can match or exceed the performance of larger generic models traces back to early work on **knowledge distillation** [Hinton et al., 2015]. Subsequent research showed that distilled models like DistilBERT [Sanh et al., 2019] and TinyBERT [Jiao et al., 2020] could transfer the capabilities of large pretrained models to much smaller students, often with minimal performance loss on downstream tasks. Quantization and pruning further reduce model footprint, as in Han et al.'s "Deep Compression" techniques [Han et al., 2015] and the quantization method of Jacob et al. [2018], which inspired 8-bit and 4-bit LLM runtimes.

In the LLM era, **parameter-efficient fine-tuning (PEFT)** has emerged as the standard way to adapt large models to new tasks without updating all weights. LoRA [Hu et al., 2021] injects low-rank adapters into attention and MLP layers, while QLoRA [Dettmers et al., 2023] combines 4-bit quantization with LoRA to enable full-model adaptation on single GPUs. These methods have been widely adopted for domain adaptation, instruction tuning, and tool-use specialization, demonstrating that even a relatively small amount of high-quality task data can yield large performance gains.

However, most empirical studies focus on **large teacher models** (7B–70B) and comparatively large students (1B–7B). There is limited work on **fine-tuning micro-scale models (<500M)** specifically for **structured extraction**. Existing technical reports (e.g., Qwen2.5 [Yang et al., 2024], Phi-3 [Abdin et al., 2024], Gemma 2 [Gemma Team, 2024]) show that instruction tuning improves general downstream performance, but do not quantify JSONExact or schema compliance.

Our results extend this line of work by showing that **LoRA fine-tuning of a 135M model on only 629 labeled examples** yields a **13× improvement** in JSONExact (1.9% → 24.7%) on EdgeJSON, and that this **fine-tuned 135M model (Maaza-MLM-135M) outperforms a zero-shot 500M model (Qwen2.5-0.5B)** on the same benchmark (24.7% vs. 14.6%). At 360M parameters, Maaza-SLM-360M further achieves 55.1% JSONExact and 0.78 field F1, **3.8× better** than zero-shot Qwen2.5-0.5B on JSONExact. These findings empirically support the claim that, for structured tasks under tight hardware constraints, **task specialization via fine-tuning can be more effective than blindly scaling parameters**.

---

## Review Notes

### Strengths
- ✅ Comprehensive coverage of all 4 requested subsections
- ✅ ~40 high-quality citations (recent, relevant)
- ✅ Clear narrative flow (background → gap → our contribution)
- ✅ Academic tone (formal, precise)
- ✅ Excellent positioning of our work
- ✅ Strong connection to our key findings

### Minor Edits Needed
- Update SmolLM2 citation year (2025 vs 2024)
- Verify Pham et al. SLM-Bench year (2025 is correct)
- Add a few more edge AI citations if needed
- Consider adding a summary table of SLM families

### Integration Plan
1. Copy to `/home/rain/SLMBench/papers/paper_a_mlm_edgebench/sections/02_related_work.md`
2. Minor edits for consistency with our style
3. Add summary table (optional)
4. Integrate BibTeX into main refs.bib

---

**Status**: ✅ EXCELLENT FIRST DRAFT - Ready for minor edits and integration

