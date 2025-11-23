# Copy-Paste Prompts for GPT & Grok

**Quick Reference**: Exact text to copy and paste into GPT/Grok

---

## 🤖 FOR GPT (ChatGPT)

### Prompt #1: FastAPI Backend

Copy and paste this entire message:

```
I need you to generate a complete production-ready FastAPI backend for our Maaza JSON Extraction API. 

We're building an API that uses our fine-tuned language models (Maaza-MLM-135M and Maaza-SLM-360M) to extract structured JSON from unstructured text based on user-provided schemas.

The models are already available on HuggingFace:
- https://huggingface.co/CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1
- https://huggingface.co/CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1

Please generate all files for a production-ready FastAPI application with:

1. **Core API Endpoint**: POST /v1/extract
   - Accept text + JSON schema
   - Return extracted JSON with validation
   - Track usage (tokens, latency)

2. **Authentication**: 
   - API keys (Bearer tokens)
   - JWT for dashboard users
   - Bcrypt hashing

3. **Database (PostgreSQL)**:
   - Users table
   - API keys table
   - Usage logs (partitioned by date)
   - Billing events table

4. **Stripe Integration**:
   - Webhook handlers
   - Checkout session complete
   - Subscription management

5. **Rate Limiting (Redis)**:
   - Per-API-key limits
   - 429 responses when exceeded

6. **Model Inference**:
   - Load models on startup (transformers library)
   - Generate with prompt template
   - Parse JSON from output
   - Validate against schema

7. **Error Handling**:
   - Standard error format
   - Error codes (invalid_api_key, rate_limit_exceeded, etc.)
   - Detailed validation errors

8. **Testing**:
   - Pytest with 80% coverage
   - Test all endpoints
   - Mock external services

9. **Docker**:
   - Dockerfile
   - docker-compose.yml with Postgres + Redis

10. **Project Structure**:
```
maaza-api/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models/ (SQLAlchemy)
│   ├── routes/ (endpoints)
│   ├── services/ (inference, validation)
│   ├── auth/ (JWT, API keys)
│   └── utils/ (rate limit, cache)
├── tests/
├── alembic/ (migrations)
├── requirements.txt
└── README.md
```

Please generate all files with complete, production-ready code. I need:
- Full type hints (Pydantic v2)
- Async/await throughout
- Comprehensive error handling
- Security best practices
- OpenAPI documentation
- Logging setup

For the prompt template, use:
```
Extract structured information from the text according to the schema.

Text: {text}

Schema:
{schema_json}

Extracted JSON:
```

Start with the complete project structure and all Python files. I'll use this in production immediately.
```

---

## 🤖 FOR GROK (grok.x.ai)

### Prompt #1: Infrastructure

Copy and paste this entire message:

```
Help me design and optimize infrastructure for the Maaza API deployment on DigitalOcean.

Context:
- FastAPI backend for JSON extraction using fine-tuned language models
- Two models: MLM-135M (270MB, ~80ms) and SLM-360M (720MB, ~140ms)
- Expected load: 10K req/day Month 1 → 100K req/day Month 3
- Peak: 100 req/s
- Cost target: <$500/month
- Latency target: <200ms p95

I need you to generate:

1. **Terraform Files for DigitalOcean**:
   - Load balancer (SSL termination, health checks)
   - API servers (2-4 droplets, CPU-optimized)
   - GPU worker for SLM-360M (T4 or similar)
   - Managed PostgreSQL
   - Managed Redis
   - S3-compatible storage

2. **ONNX Optimization**:
   - Convert models from PyTorch to ONNX
   - INT8 quantization
   - Performance benchmarks (throughput, latency)
   - Batching implementation

3. **Request Batching**:
   - Dynamic batching (wait up to 10ms for batch)
   - Separate queues for MLM vs SLM
   - Python implementation

4. **Monitoring Stack**:
   - Prometheus metrics (system + app + business)
   - 4 Grafana dashboards (health, performance, ML, business)
   - Alert rules (critical + warning)

5. **Load Testing (k6)**:
   - Baseline test (10 req/s, 10 min)
   - Ramp test (10→100 req/s)
   - Spike test (sudden 10→200 req/s)
   - Soak test (50 req/s, 2 hours)
   - Realistic mix (70% MLM, 30% SLM)

6. **CI/CD Pipeline (GitHub Actions)**:
   - Run tests on PR
   - Build + deploy to staging on main
   - Manual approval for production

Structure:
```
infrastructure/
├── terraform/
│   ├── main.tf
│   ├── modules/
│   └── environments/
├── optimization/
│   ├── convert_to_onnx.py
│   └── batching.py
├── monitoring/
│   ├── prometheus.yml
│   └── grafana_dashboards/
├── loadtests/
│   └── *.js (k6 scripts)
└── .github/workflows/
    └── deploy.yml
```

Focus first on:
1. Terraform for DigitalOcean (what droplet sizes?)
2. ONNX conversion + batching (2-3× speedup)
3. Cost breakdown ($/month for each component)

Please generate complete, production-ready configs and code!
```

---

## 📝 After Sending Prompts

### When GPT Responds:
1. **Save all generated files** to `/home/rain/maaza-api/`
2. **Test locally**: 
   ```bash
   cd /home/rain/maaza-api
   docker-compose up
   ```
3. **Review** critical files (auth, billing, inference)
4. **Send Prompt #2** (Python SDK) once backend is working

### When Grok Responds:
1. **Save Terraform** to `/home/rain/maaza-infrastructure/`
2. **Review** cost estimates
3. **Test ONNX conversion** locally
4. **Send follow-up** with any questions
5. **Request JavaScript SDK** once infrastructure is clear

---

## 🚀 Timeline After Prompts

**Tonight**: Send both prompts
**Tomorrow AM**: Review responses, test locally  
**Tomorrow PM**: Deploy to DO staging  
**Day 3-4**: SDKs and polish  
**Week 2**: Launch! 🎉

---

**Files Ready**:
- ✅ `/home/rain/SLMBench/docs/FOR_GPT_API_BACKEND.md` (detailed specs)
- ✅ `/home/rain/SLMBench/docs/FOR_GROK_INFRASTRUCTURE.md` (detailed specs)
- ✅ `/home/rain/SLMBench/docs/API_KICKOFF_MASTER_PLAN.md` (coordination)

**Next**: Copy the prompts above and send to GPT + Grok!

