# Paper Revision Plan: v0.1 → v0.2

**Date**: November 22, 2025  
**Status**: Change plan before editing  
**Current Version**: v0.1 (saved as backup)

---

## 🔍 **REVIEW FEEDBACK SUMMARY**

### **Critical Accuracy Issues**

1. **GPU Model**: 3090 → 4080 (throughout paper)
2. **Training Time**: Minimize/remove specific times (too much detail, may set wrong expectations)
3. **Gemma References**: Update to reflect late 2025 models (Gemma 3, including ~270M SLM)
4. **SmolLM2-360M**: Verify if results are estimated or actual (4.2.2, Table 1, 5.3)
5. **CPU vs GPU**: Clarify inference hardware (5.1.2 - "CPU-only evaluation")

### **Content Reduction ("Too Much Sauce")**

1. **Future Work (6.5.2)**: Consider removing researcher directions - we're releasing enough
2. **Speculation (6.3.2)**: Simplify "may excel in other domains" (SQL, regex, API) - too speculative
3. **Practical Advice (6.5.1)**: 
   - Simplify "Fine-tune on domain data" (item 3)
   - Remove "Reserve cloud models for exceptions" (item 4) - implied, not our business
4. **Broader Impact (6.6)**: 
   - Soften or remove "Privacy: avoids data leakage to cloud providers"
   - Consider removing entire "Potential Concerns" subsection
5. **Multilingual (Section 7)**: Don't specify languages for future work

### **Clarity & Framing**

1. **LLM Success (1.5a)**: Expand to "GPT line, Llamas, Qwen, others (Deepseek, Gemma, Claude, etc.)"
2. **Large Models (5.3)**: Specify "larger zero-shot models" vs "very large models (GPT-4, etc.) might succeed"
3. **Table Alignment (4.2.2)**: Check if needs better formatting
4. **Cloud Fallback**: Don't push edge-first, cloud-fallback strategy (it's implied)

### **Repository Questions**

1. **Git vs HF**: User thought everything was on HuggingFace, not sure about GitHub cleanliness
2. **Git Status**: Need to verify if repo is clean and public-ready

---

## ✅ **BEFORE WE EDIT: ACTION ITEMS**

### **1. Backup Current Version**
```bash
cp papers/MAAZA_PAPER_FULL_CONTENT.md papers/MAAZA_PAPER_V01_BACKUP.md
```

### **2. Verify Facts Before Changing**

| Item | Current Claim | Need to Verify |
|------|--------------|----------------|
| GPU | RTX 3090 | Should be RTX 4080 ✅ |
| Training Time | "<1 min", "<2 min" | Remove or generalize? |
| SmolLM2-360M | "~5%* (estimated)" | Is this accurate or do we have data? |
| Inference Hardware | "CPU-only evaluation" | Was it actually CPU-only? |
| Gemma Models | References to 2B | Update to Gemma 3, ~270M model |

### **3. Check Repository Status**

**Questions**:
- Is GitHub repo clean and ready for public linking?
- Are all models actually on HuggingFace Hub?
- Should we reference GitHub or just HuggingFace?

---

## 📝 **PROPOSED CHANGES (v0.2)**

### **Accuracy Fixes**

1. **Global Replace**: `RTX 3090` → `RTX 4080`
2. **Training Time Strategy**:
   - Option A: Remove all specific times
   - Option B: Say "rapid training (<minutes, not hours)"
   - Option C: Keep but add caveat "on RTX 4080; times vary by hardware"
   - **RECOMMENDATION**: Option B (remove specifics)

3. **Gemma Update**:
   - Current: "Gemma 2B"
   - New: "Gemma 2/3 series (including ~270M models in Gemma 3)"
   - Check: Is Gemma 3 actually released? Verify before claiming

4. **SmolLM2-360M Clarification**:
   - If estimated: Keep "~5%* (estimated from spot checks)"
   - If actual: Remove asterisk, add to evaluation section
   - **ACTION**: Confirm status before editing

### **Content Reduction**

1. **Section 6.5.2 (For Researchers)**:
   - **REMOVE ENTIRELY** or reduce to 1-2 sentences
   - Rationale: Don't give away research roadmap, we're releasing enough

2. **Section 6.3.2 (Code Generation Comparison)**:
   - Current: "This suggests that specialized micro models may excel in other structured domains (SQL generation, regex synthesis, API call construction)."
   - New: "This suggests potential for specialized models in other structured output tasks."
   - Rationale: Less specific, less speculative

3. **Section 6.5.1 (For Practitioners)**:
   - Item 3: "Fine-tune on domain data: Even 200-300 examples can provide significant gains"
   - New: "Fine-tune on domain data for notable benefits"
   - Item 4: **REMOVE** "Reserve cloud models for exceptions"
   - Rationale: Simplify, don't push cloud fallback strategy

4. **Section 6.6 (Broader Impact)**:
   - **Soften or REMOVE**: "Privacy: Local inference avoids data leakage to cloud providers"
   - **Consider REMOVING**: Entire "Potential Concerns" subsection
   - Rationale: Don't need to highlight privacy angle or potential negatives

5. **Section 7.3 (Future Work)**:
   - **REMOVE**: Specific languages (Spanish, Chinese, Arabic)
   - New: "Extend to multilingual scenarios"
   - Rationale: Don't specify future plans

### **Clarity Improvements**

1. **Section 1 (Introduction - LLM Success)**:
   - Add: "GPT series, Llama family, Qwen models, and others (Deepseek, Gemma, Claude, etc.)"
   - Rationale: More inclusive, acknowledges key players

2. **Section 5.3 (Zero-Shot Limitations)**:
   - Add caveat: "Note: Very large models (GPT-4, Claude-3, etc.) may succeed on complex schemas but are impractical for edge deployment"
   - Rationale: Clarify scope, don't overstate

3. **Table 4.2.2 (Hyperparameters)**:
   - **CHECK**: Does alignment need fixing?
   - **ACTION**: Verify rendering in markdown

### **Repository References**

**Current Claims**:
- "github.com/CycleCore/SLMBench"
- "huggingface.co/CycleCoreTechnologies"

**Questions**:
1. Is GitHub repo public and clean?
2. Should we reference both or just HuggingFace?
3. Is "CycleCore" the right GitHub org?

**RECOMMENDATION**: 
- If GitHub is clean: Keep both
- If GitHub is messy: Remove GitHub references, use only HuggingFace
- **ACTION**: Check repo status before finalizing

---

## 🎯 **EDITING STRATEGY**

### **Phase 1: Backup & Verify** (DO FIRST)
1. ✅ Backup v0.1 to separate file
2. ⏳ Verify GPU model (4080 vs 3090)
3. ⏳ Verify SmolLM2-360M results (estimated vs actual)
4. ⏳ Verify Gemma 3 release status
5. ⏳ Check GitHub repo cleanliness
6. ⏳ Confirm inference hardware (CPU vs GPU)

### **Phase 2: High-Priority Edits** (Accuracy)
1. Fix GPU model (3090 → 4080)
2. Update/remove training times
3. Update Gemma references (if Gemma 3 is real)
4. Clarify SmolLM2-360M status
5. Clarify inference hardware

### **Phase 3: Content Reduction** (Remove Sauce)
1. Remove/reduce Section 6.5.2 (For Researchers)
2. Simplify Section 6.3.2 (speculation)
3. Simplify Section 6.5.1 (practical advice)
4. Soften/remove Section 6.6 privacy angle
5. Remove specific languages from future work

### **Phase 4: Clarity Improvements**
1. Expand LLM list in Introduction
2. Add caveat about very large models
3. Fix table alignment (if needed)
4. Clean up repository references

### **Phase 5: Final Review**
1. Read through entire paper
2. Check for consistency
3. Verify all numbers match
4. Ensure no broken references

---

## ❓ **QUESTIONS FOR USER (BEFORE EDITING)**

1. **GPU Model**: Confirm it was RTX 4080 throughout? ✅
2. **Training Time**: Remove all specific times, or keep with caveat?
3. **SmolLM2-360M**: Do we have actual results, or is it truly estimated?
4. **Gemma 3**: Is this model actually released? Should we reference it?
5. **GitHub Repo**: Is it clean and public-ready, or should we remove GitHub references?
6. **Inference Hardware**: Was evaluation actually CPU-only, or mixed?
7. **Section 6.5.2**: Remove entirely, or just simplify?
8. **Section 6.6**: Remove privacy line, remove potential concerns, or keep but soften?

---

## 📦 **DELIVERABLE**

**After user confirms above questions**:
- `papers/MAAZA_PAPER_V01_BACKUP.md` (current version, preserved)
- `papers/MAAZA_PAPER_V02_REVISED.md` (new version with all changes)
- `papers/REVISION_LOG_V01_TO_V02.md` (changelog documenting all edits)

---

**Status**: ⏳ Awaiting user confirmation before editing  
**Next**: Answer questions above, then proceed with Phase 1-5 editing

