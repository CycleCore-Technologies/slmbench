# Grok Prompt #1: Infrastructure & Optimization

**Task**: Design infrastructure and optimize Maaza API for production deployment on DigitalOcean

---

## Context

We're deploying a FastAPI-based JSON extraction API. GPT is generating the core backend code. Your role is to:
1. Design production infrastructure (DigitalOcean)
2. Optimize inference performance
3. Create monitoring & observability stack
4. Generate load testing scripts
5. Design CI/CD pipeline

**Models**:
- Maaza-MLM-135M: 135M params, 270MB, ~80ms inference
- Maaza-SLM-360M: 360M params, 720MB, ~140ms inference

**Expected load**:
- Month 1: ~10K requests/day
- Month 3: ~100K requests/day
- Peak: 100 req/s

---

## Task 1: DigitalOcean Infrastructure Design

### Requirements
- **Cost target**: <$500/month initial
- **Latency target**: <200ms p95
- **Availability**: 99.9% uptime
- **Auto-scaling**: Handle 10x traffic spikes
- **Regions**: US East (primary), EU West (future)

### Components Needed

**Load Balancer**:
- Distribute traffic across API servers
- Health checks
- SSL termination

**API Servers** (2-4 instances):
- CPU-optimized for MLM-135M
- What specs? (CPU, RAM, disk)
- How many initially?

**GPU Worker** (for SLM-360M):
- GPU type (T4? A10?)
- How to batch requests?
- Fallback to CPU if GPU busy?

**Database** (PostgreSQL):
- Managed vs self-hosted?
- Size estimation (1M requests = ~?)
- Backup strategy?

**Cache** (Redis):
- Size needed?
- Eviction policy?
- What to cache?

**Storage** (S3-compatible):
- Logs
- Model weights
- Backup retention?

### Terraform/IaC

Please generate Terraform files for:
```
infrastructure/
├── main.tf
├── variables.tf
├── outputs.tf
├── modules/
│   ├── api_server/
│   ├── gpu_worker/
│   ├── database/
│   ├── redis/
│   └── load_balancer/
└── environments/
    ├── staging.tfvars
    └── production.tfvars
```

---

## Task 2: Inference Optimization

### Current Setup (Baseline)
```python
# Naive inference
model = AutoModelForCausalLM.from_pretrained("...")
tokenizer = AutoTokenizer.from_pretrained("...")

def extract(text: str):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=512)
    return tokenizer.decode(outputs[0])
```

**Problems**:
- Slow (no batching)
- High memory
- CPU-only (for MLM-135M)
- No caching

### Optimization Goals
1. **Speed**: 2-3× faster inference
2. **Throughput**: 100 req/s per instance
3. **Memory**: Efficient model loading
4. **Cost**: CPU for 135M, GPU for 360M

### Techniques to Apply

**1. ONNX Runtime**
- Convert models to ONNX
- Quantization (INT8?)
- Optimized operators

**2. Request Batching**
- Batch multiple requests
- Dynamic batching (wait 10ms for batch)
- Separate queues for MLM/SLM

**3. Model Caching**
- Cache common prompts
- Redis: `cache_key = hash(text + schema)`
- TTL: 1 hour

**4. Prompt Optimization**
- Minimize token count
- Reuse tokenized schemas

Please generate:
```python
# inference/optimizer.py
class OptimizedInference:
    """Optimized inference with batching, caching, ONNX"""
    
    def __init__(self, model_name: str):
        # Load ONNX model
        # Setup batching queue
        # Connect to Redis cache
        pass
    
    async def extract_batch(self, requests: List[Request]) -> List[Response]:
        # Check cache
        # Batch uncached requests
        # Run inference
        # Update cache
        # Return results
        pass
```

---

## Task 3: Monitoring & Observability

### Metrics to Track

**System Metrics** (Prometheus):
- CPU/GPU utilization
- Memory usage
- Disk I/O
- Network I/O

**Application Metrics**:
- Request rate (req/s)
- Error rate (%)
- Latency (p50, p95, p99)
- Model inference time
- Cache hit rate
- Queue depth

**Business Metrics**:
- API calls per user
- Revenue (from usage)
- Cost per request
- Billing usage

### Grafana Dashboards

Please generate JSON configs for:

**1. System Health Dashboard**
- Server status (up/down)
- CPU/Memory graphs
- Error rate alerts
- Traffic patterns

**2. API Performance Dashboard**
- Request rate (last hour, day, week)
- Latency heatmap
- Error breakdown (by type)
- Top users by usage

**3. ML Performance Dashboard**
- Model inference time (MLM vs SLM)
- Batch sizes
- Cache hit rate
- GPU utilization (for SLM-360M)

**4. Business Dashboard**
- API calls (by tier: free, starter, pro)
- Revenue tracking
- Cost analysis
- User growth

### Alerting Rules

**Critical** (PagerDuty):
- API down (>1 min)
- Error rate >5%
- Latency p95 >500ms
- GPU offline

**Warning** (Slack):
- Error rate >2%
- Latency p95 >300ms
- Cache hit rate <50%
- Disk >80% full

---

## Task 4: Load Testing

### Test Scenarios

**1. Baseline Test**
- 10 req/s steady
- Duration: 10 minutes
- Measure: baseline latency

**2. Ramp Test**
- 10 → 100 req/s over 5 minutes
- Hold 100 req/s for 5 minutes
- Measure: breaking point

**3. Spike Test**
- Sudden jump 10 → 200 req/s
- Duration: 2 minutes
- Measure: recovery time

**4. Soak Test**
- 50 req/s
- Duration: 2 hours
- Measure: memory leaks, degradation

**5. Realistic Mix**
- 70% MLM-135M (simple schemas)
- 30% SLM-360M (complex schemas)
- Variable request sizes
- Measure: real-world performance

### k6 Load Testing Scripts

Please generate:
```javascript
// loadtests/baseline.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 10 },  // Warm up
    { duration: '10m', target: 10 }, // Steady
    { duration: '1m', target: 0 },   // Cool down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'], // 95% under 200ms
    http_req_failed: ['rate<0.01'],   // <1% errors
  },
};

export default function () {
  const payload = JSON.stringify({
    text: 'Order #12345 by John Doe...',
    schema: { /* ... */ },
    model: 'maaza-mlm-135m'
  });
  
  const res = http.post('https://api.cyclecore.ai/v1/extract', payload, {
    headers: { 
      'Authorization': 'Bearer sk_test_...',
      'Content-Type': 'application/json' 
    },
  });
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'has extracted data': (r) => r.json().extracted !== undefined,
  });
  
  sleep(1);
}
```

Generate scripts for all 5 scenarios + realistic mix.

---

## Task 5: CI/CD Pipeline

### GitHub Actions Workflow

**On Push to `main`**:
1. Run tests (pytest)
2. Build Docker image
3. Push to registry
4. Deploy to staging
5. Run smoke tests
6. Deploy to production (manual approval)

**On Pull Request**:
1. Run tests
2. Run linter (ruff)
3. Check test coverage (>80%)
4. Build Docker image (don't push)

Please generate:
```yaml
# .github/workflows/deploy.yml
name: Deploy API

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
  
  build:
    # Build Docker image
    
  deploy-staging:
    # Deploy to DO staging
    
  smoke-test:
    # Run smoke tests
    
  deploy-production:
    # Deploy to production (manual)
```

---

## Task 6: Performance Benchmarks

### Optimization Comparison

Please create a benchmarking script that compares:

| Approach | Throughput | Latency p95 | Memory | Cost/1K req |
|----------|------------|-------------|--------|-------------|
| Baseline (PyTorch CPU) | ? | ? | ? | ? |
| ONNX INT8 | ? | ? | ? | ? |
| ONNX + Batching | ? | ? | ? | ? |
| GPU (SLM-360M only) | ? | ? | ? | ? |
| Full stack (optimal) | ? | ? | ? | ? |

**Script should**:
- Run each approach with same test data
- Measure throughput (req/s)
- Measure latency (p50, p95, p99)
- Measure memory usage
- Calculate cost per 1K requests

---

## Deliverables

Please generate:

1. **Infrastructure**
   - [ ] Terraform files for DigitalOcean
   - [ ] Architecture diagram (Mermaid)
   - [ ] Cost breakdown ($$/month)
   - [ ] Scaling strategy (10x growth)

2. **Optimization**
   - [ ] ONNX conversion script
   - [ ] Batching implementation
   - [ ] Caching layer
   - [ ] Performance comparison

3. **Monitoring**
   - [ ] Prometheus config
   - [ ] Grafana dashboards (4 JSONs)
   - [ ] Alert rules
   - [ ] Logging setup (structured logs)

4. **Load Testing**
   - [ ] k6 scripts (5 scenarios)
   - [ ] Realistic traffic generator
   - [ ] Results analysis script

5. **CI/CD**
   - [ ] GitHub Actions workflows
   - [ ] Deployment scripts
   - [ ] Rollback procedure
   - [ ] Smoke tests

6. **Documentation**
   - [ ] Infrastructure README
   - [ ] Deployment guide
   - [ ] Monitoring runbook
   - [ ] Incident response playbook

---

## Success Criteria

After your optimizations:
- ✅ Latency: <150ms p95 (target: <200ms)
- ✅ Throughput: 100 req/s per API server
- ✅ Cost: <$400/month for 10K req/day
- ✅ Reliability: 99.9% uptime
- ✅ Scalability: Handle 10x spike without manual intervention

---

**Ready? Please generate all infrastructure and optimization code!**

