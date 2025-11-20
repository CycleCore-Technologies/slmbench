# EdgeJSON Dataset Generation - Run Instructions

## Quick Start

Once Qwen3-14B finishes downloading, run this single command:

```bash
cd /home/rain/SLMBench
./benchmarks/edge_json/scripts/run_generation.sh
```

That's it! The script will:
- ✅ Wait for Qwen3-14B if still downloading
- ✅ Verify all 3 models are ready
- ✅ Generate 1,500 examples (750 template + 750 LLM)
- ✅ Validate and filter to best 1,000
- ✅ Split into 800 train / 200 test
- ✅ Save everything with timestamps and logs

## Expected Runtime

**15-25 minutes total**

- Template generation: ~2 minutes
- LLM generation: ~10-15 minutes
- Validation: ~3 minutes
- Saving: ~1 minute

## Output Files

All files will be saved to: `/home/rain/SLMBench/benchmarks/edge_json/data/`

- `edgejson_train_v2.jsonl` - 800 training examples
- `edgejson_test_v2.jsonl` - 200 test examples
- `dataset_metadata.json` - Dataset info and statistics

## Logs

Full generation logs saved to:
`/home/rain/SLMBench/benchmarks/edge_json/logs/generation_YYYY-MM-DD_HH-MM-SS.log`

## Checking Qwen3 Download Status

To check if Qwen3-14B is still downloading:

```bash
ls -lh /home/rain/SLMBench/models/qwen3-14b/ | head -20
```

Look for `config.json` - when it exists, the model is ready.

## Manual Run (without waiting)

If you want to run immediately (assuming Qwen3 is ready):

```bash
cd /home/rain/SLMBench
source venv/bin/activate
python benchmarks/edge_json/scripts/generate_dataset_v2.py
```

## Troubleshooting

**Script won't start:**
```bash
chmod +x /home/rain/SLMBench/benchmarks/edge_json/scripts/run_generation.sh
```

**Check model status:**
```bash
ls -d /home/rain/SLMBench/models/*/config.json
```

All 3 models should show their `config.json` file.

## What Happens Next

After dataset generation completes:
1. ✅ Review generation logs
2. ✅ Verify train/test files created
3. ⏭️ Run baseline evaluations (Phase 3 next step)
4. ⏭️ Document and commit

---

**Ready to run!** Just execute the script when Qwen3 download completes.
