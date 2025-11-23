# v0.3 → v0.4 Fix Summary

**Date**: November 22, 2025  
**Status**: Ready to fix  
**Estimated Time**: 30 minutes

---

## ✅ GOOD NEWS: We Have All the Data!

### Actual SmolLM2-360M Results (Full 158 Examples)
From `/home/rain/SLMBench/results/base_smollm2_360m_v3_evaluation.json`:

- **JSONExact**: 11.4%
- **Field F1**: 0.240
- **Schema Compliance**: 15.2%
- **By Complexity**:
  - Simple: 23.7% JSONExact, 0.436 F1
  - Medium: 0.0% JSONExact, 0.131 F1
  - Complex: 0.0% JSONExact, 0.000 F1

### Current State of v0.3
**MIXED**: Some tables have actual numbers, some still have estimates.

#### ✅ Tables WITH Actual Numbers (Lines 1228-1250)
```
| SmolLM2-360M (base) | 360M | Zero-shot | 11.4% | 0.240 | 23.7% | 720MB | - |
```

#### ❌ Tables WITH Estimates (Need Fixing)
1. **Line 667**: Base → Fine-tuned comparison
   ```
   | SmolLM2-360M | ~5% | **55.1%** | **11×** |
   ```
   Should be: `11.4%` and multiplier should be `4.8×` (55.1/11.4)

2. **Line 751-755**: Main results table
   ```
   | SmolLM2-360M (base) | 360M | ~5%* | ~0.15* | ~12%* | 110 |
   * SmolLM2-360M results estimated from spot checks (full evaluation pending)
   ```
   Should be: `11.4%`, `0.240`, `15.2%` (remove asterisk and footnote)

3. **Line 778-779**: Complexity breakdown
   ```
   | **SmolLM2-360M (base)** |
   | JSONExact | ~10%* | ~2%* | ~0%* |
   | Field F1 | ~0.25* | ~0.10* | ~0.05* |
   ```
   Should be:
   ```
   | JSONExact | 23.7% | 0.0% | 0.0% |
   | Field F1 | 0.436 | 0.131 | 0.000 |
   ```

4. **Line 861-862**: ASCII Figure 1
   ```
   | ◆ SmolLM2-360M (~5%)
   ```
   Should be: `11.4%`

5. **Line 1177**: ASCII Figure near end
   ```
   | ◆ SmolLM2-360M (~5%, 360M)
   ```
   Should be: `11.4%`

---

## 🔧 ALL FIXES NEEDED

### Fix 1: Replace ALL Estimates with Actuals
**Find/Replace Operations**:

| Find | Replace | Context |
|------|---------|---------|
| `~5%` | `11.4%` | All SmolLM2-360M JSONExact references |
| `~0.15*` | `0.240` | Field F1 |
| `~0.25*` | `0.436` | Simple complexity F1 |
| `~0.10*` | `0.131` | Medium complexity F1 |
| `~0.05*` | `0.000` | Complex complexity F1 |
| `~12%*` | `15.2%` | Schema compliance |
| `~10%*` | `23.7%` | Simple complexity JSONExact |
| `~2%*` | `0.0%` | Medium complexity JSONExact |
| `~0%*` | `0.0%` | Complex complexity JSONExact |
| `**11×**` | `**4.8×**` | Fine-tuning multiplier (line 667) |

**Delete**: 
- Line 755: `* SmolLM2-360M results estimated from spot checks (full evaluation pending)`

### Fix 2: Remove/Fix Latency References
**Current**: 10 instances found (including 9,480 ms for Qwen)

**Options**:
A. Remove latency column entirely from Table 2 (line 751)
B. Keep latency but add footnote explaining CPU-only, cold-start included
C. Replace with "Disk Size" column (more relevant for edge)

**RECOMMENDATION**: Option A (remove) - we already removed from key findings, should remove from tables too.

### Fix 3: Update SmolLM2 Citation Year
**Find**: `[Allal et al., 2025]`  
**Replace**: `[Allal et al., 2024]`  
**Note**: Also update in `references.bib`

### Fix 4: ✅ Already Fixed
Train/test split statement exists at line 294:
> "The train/test split is stratified by schema type and complexity level... No test example or schema variant appears in the training set, eliminating data contamination risk."

---

## 📊 Impact Analysis: What Else Changes?

### Narrative Impact
When we change ~5% → 11.4%, the story gets BETTER:

**Before (with estimates)**:
- "Fine-tuning improves SmolLM2-360M from ~5% to 55.1%" (11× improvement)

**After (with actuals)**:
- "Fine-tuning improves SmolLM2-360M from 11.4% to 55.1%" (4.8× improvement)

**Analysis**: 4.8× is still a strong multiplier, and 11.4% base is more credible than ~5%.

### Comparison with Qwen
**Before**: Maaza-360M (55.1%) vs Qwen-0.5B (14.6%) = 3.8× better  
**After**: UNCHANGED (Qwen numbers stay the same)

### Key Claims Still Hold
1. ✅ Fine-tuned 360M beats zero-shot 500M
2. ✅ Task specialization > raw size
3. ✅ Edge deployment favors fine-tuned models
4. ✅ Capacity boundary at ~300M params

---

## 🎯 OTHER ITEMS FROM GROK REVIEW

### Taxonomy (NLM/MLM/SLM/LLM)
**Grok's concern**: "Feels arbitrary, not justified with evidence"

**Options**:
A. Drop entirely
B. Keep but de-emphasize (one mention)
C. Add justification

**Current status**: Mentioned in Introduction and Discussion, not heavily relied upon.

**RECOMMENDATION**: Keep but add one sentence in Discussion:
> "We propose these categories based on observed capability transitions: models below 200M struggle with complex schemas, while models above 300M show first non-zero performance, suggesting architectural capacity thresholds."

### Additional Baseline
**Grok's suggestion**: Add Llama-3.2-1B or Qwen-Instruct

**Status**: Not critical for v1  
**Recommendation**: Defer to post-arXiv revision

### ASCII Figures
**Grok's suggestion**: Convert to matplotlib

**Status**: Functional but unprofessional  
**Recommendation**: Defer to post-arXiv or journal version

### Paper Date
**Current**: November 22, 2025  
**Action**: Verify and update to actual submission date

---

## ✅ VERIFICATION CHECKLIST

Before making changes:
- [x] Located actual SmolLM2-360M results (11.4%, 0.240, 23.7%)
- [x] Identified all ~5%, ~10% instances (5 locations)
- [x] Confirmed train/test statement exists
- [ ] Check SmolLM2 citation year in references.bib
- [ ] Decide on latency column removal
- [ ] Decide on taxonomy handling

---

## 🚀 PROPOSED WORKFLOW

### Step 1: Quick Fixes (15 min)
1. Replace all ~5% → 11.4% (5 locations)
2. Replace all ~10% → 23.7%, ~0% → 0.0%, etc.
3. Fix multiplier 11× → 4.8× (line 667)
4. Delete footnote (line 755)

### Step 2: Latency Decision (5 min)
- Remove latency column from Table 2 (line 751)
- Verify no other latency mentions in key claims

### Step 3: Citation Fix (5 min)
- Update SmolLM2 to 2024 in paper and references.bib

### Step 4: Taxonomy (5 min)
- Add one-sentence justification in Discussion

### Step 5: Final Verification (5 min)
- Search for remaining "~" or "estimated"
- Verify all tables consistent
- Update paper date

### Step 6: Create v0.4
- Save changes to MAAZA_PAPER_FULL_CONTENT.md
- Mark as v0.4 (arXiv-ready)

---

## 📈 EXPECTED OUTCOME

**Before**: v0.3 with estimates (9.2/10)  
**After**: v0.4 with actuals (9.8/10) → Submit to arXiv

**Key improvements**:
- ✅ All estimates replaced with actual evaluation results
- ✅ No latency confusion
- ✅ Correct citation years
- ✅ Justified taxonomy
- ✅ Ready for arXiv submission

---

## 🎓 SCIENTIFIC IMPACT

### What Gets Better
1. **Credibility**: Actual numbers > estimates
2. **Reproducibility**: Full evaluation documented
3. **Honesty**: 4.8× multiplier more accurate than 11×
4. **Comparison**: 11.4% base more credible than ~5%

### Story Strength
**STRONGER**: Higher base (11.4%) shows the base model isn't completely failing, making the fine-tuning gain (→55.1%) even more impressive because:
- It's not just "fixing a broken model"
- It's "taking a functional model and making it excellent"
- The 360M architecture clearly has capacity, fine-tuning unlocks it

---

**READY TO PROCEED**: All data verified, fixes identified, workflow planned.  
**Next Step**: User approval → Execute fixes → v0.4 → arXiv

