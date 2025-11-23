# Maaza JSON Extraction API - Specification v0.1

**Host**: `api.cyclecore.ai`  
**Status**: Planning Phase  
**Target Launch**: Q1 2025  
**Alternative**: Apache 2.0 self-hosted models available at HuggingFace

---

## Overview

The Maaza API provides production-ready JSON extraction powered by our task-specialized micro language models. Built on DigitalOcean infrastructure for low-latency, high-reliability inference.

### Key Features
- ✅ Schema-validated JSON extraction
- ✅ Two model sizes (135M fast, 360M accurate)
- ✅ Sub-200ms p95 latency (US East)
- ✅ Apache 2.0 licensed models (self-host alternative)
- ✅ Usage-based pricing ($0.001-$0.01 per request)

---

## Base Endpoint

```
POST https://api.cyclecore.ai/v1/extract
```

---

## Authentication

All requests require an API key via Bearer token:

```bash
curl -X POST https://api.cyclecore.ai/v1/extract \
  -H "Authorization: Bearer sk_live_..." \
  -H "Content-Type: application/json" \
  -d '{...}'
```

**Get API Key**: https://cyclecore.ai/dashboard/api-keys

---

## Request Format

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | Input text to extract from (max 2048 tokens) |
| `schema` | object | JSON schema defining expected output structure |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `model` | string | `maaza-slm-360m` | Model to use: `maaza-mlm-135m` or `maaza-slm-360m` |
| `temperature` | float | 0.0 | Sampling temperature (0.0 = deterministic) |
| `validate` | boolean | true | Validate output against schema before returning |
| `return_confidence` | boolean | false | Include per-field confidence scores |

### Example Request

```json
{
  "text": "Order #12345 placed by John Doe (john@example.com) on Nov 22, 2025. Total: $149.99. Items: 2x Widget ($49.99 each), 1x Gadget ($50.01). Shipping to 123 Main St, NYC.",
  "schema": {
    "type": "object",
    "properties": {
      "order_id": {"type": "string"},
      "customer_name": {"type": "string"},
      "customer_email": {"type": "string"},
      "order_date": {"type": "string"},
      "total": {"type": "number"},
      "items": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "quantity": {"type": "integer"},
            "price": {"type": "number"}
          }
        }
      }
    },
    "required": ["order_id", "customer_name", "total"]
  },
  "model": "maaza-slm-360m",
  "validate": true
}
```

---

## Response Format

### Success Response (200)

```json
{
  "id": "req_abc123",
  "object": "extraction",
  "created": 1732302000,
  "model": "maaza-slm-360m",
  "extracted": {
    "order_id": "12345",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "order_date": "Nov 22, 2025",
    "total": 149.99,
    "items": [
      {"name": "Widget", "quantity": 2, "price": 49.99},
      {"name": "Gadget", "quantity": 1, "price": 50.01}
    ]
  },
  "validation": {
    "valid": true,
    "errors": []
  },
  "usage": {
    "input_tokens": 87,
    "output_tokens": 45,
    "total_tokens": 132
  },
  "latency_ms": 142
}
```

### Error Response (4xx/5xx)

```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "schema_validation_failed",
    "message": "Output does not conform to provided schema",
    "details": {
      "missing_fields": ["order_id"],
      "invalid_types": [{"field": "total", "expected": "number", "got": "string"}]
    }
  }
}
```

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `invalid_api_key` | 401 | API key missing or invalid |
| `rate_limit_exceeded` | 429 | Too many requests |
| `invalid_schema` | 400 | JSON schema is malformed |
| `text_too_long` | 400 | Input text exceeds token limit |
| `extraction_failed` | 500 | Model failed to extract |
| `schema_validation_failed` | 422 | Output doesn't match schema |

---

## Model Comparison

| Model | Params | Speed | Accuracy | Best For | Cost/1K Req |
|-------|--------|-------|----------|----------|-------------|
| `maaza-mlm-135m` | 135M | ~80ms | 24.7% JSONExact | Simple schemas, high volume | $1 |
| `maaza-slm-360m` | 360M | ~140ms | 55.1% JSONExact | Complex schemas, accuracy | $5 |

**Benchmark**: EdgeJSON v3 (158 test cases, 24 schemas)  
**Latency**: p95, US East region  
**Self-host**: Both models available free at HuggingFace (Apache 2.0)

---

## Rate Limits

### Free Tier
- 100 requests/day
- 10 requests/minute
- Best effort latency

### Starter ($29/month)
- 10,000 requests/month included
- $0.01 per additional request (MLM-135M)
- $0.05 per additional request (SLM-360M)
- 100 requests/minute
- P95 latency < 200ms

### Pro ($299/month)
- 100,000 requests/month included
- $0.005 per additional request (MLM-135M)
- $0.025 per additional request (SLM-360M)
- 1,000 requests/minute
- P95 latency < 150ms
- Priority support

### Enterprise (Custom)
- Volume discounts
- Dedicated instances
- Custom SLA
- On-prem deployment support
- Contact: hi@cyclecore.ai

---

## SDK Examples

### Python

```python
from cyclecore import MaazaClient

client = MaazaClient(api_key="sk_live_...")

result = client.extract(
    text="Invoice #INV-2025-001 for $500.00 to Acme Corp...",
    schema={
        "type": "object",
        "properties": {
            "invoice_id": {"type": "string"},
            "amount": {"type": "number"},
            "customer": {"type": "string"}
        }
    },
    model="maaza-slm-360m"
)

print(result.extracted)
# {'invoice_id': 'INV-2025-001', 'amount': 500.0, 'customer': 'Acme Corp'}
```

### JavaScript/TypeScript

```typescript
import { MaazaClient } from '@cyclecore/maaza';

const client = new MaazaClient({ apiKey: 'sk_live_...' });

const result = await client.extract({
  text: 'Order details...',
  schema: {
    type: 'object',
    properties: {
      order_id: { type: 'string' },
      total: { type: 'number' }
    }
  },
  model: 'maaza-slm-360m'
});

console.log(result.extracted);
```

### cURL

```bash
curl -X POST https://api.cyclecore.ai/v1/extract \
  -H "Authorization: Bearer sk_live_..." \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Customer: Jane Smith, Email: jane@example.com",
    "schema": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"}
      }
    },
    "model": "maaza-mlm-135m"
  }'
```

---

## Infrastructure

**Hosting**: DigitalOcean (US East, EU West, Asia Pacific)  
**Runtime**: NVIDIA GPU instances (for SLM-360M) + CPU instances (for MLM-135M)  
**Framework**: FastAPI + ONNX Runtime  
**Cache**: Redis (for common schema patterns)  
**Monitoring**: Prometheus + Grafana  

---

## Self-Hosting Alternative

Don't want to use our API? Both models are **Apache 2.0 licensed** and available for self-hosting:

### HuggingFace
- [Maaza-MLM-135M](https://huggingface.co/CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1)
- [Maaza-SLM-360M](https://huggingface.co/CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1)

### Quick Start (Self-Hosted)

```bash
# Install dependencies
pip install transformers torch

# Download model
git clone https://huggingface.co/CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1

# Run inference
python -m maaza.inference \
  --model ./Maaza-SLM-360M-JSON-v1 \
  --text "..." \
  --schema schema.json
```

**Performance**: 
- CPU: ~500ms (MLM-135M), ~1200ms (SLM-360M)
- GPU (T4): ~80ms (MLM-135M), ~140ms (SLM-360M)

---

## Roadmap

### Q1 2025
- [x] Release Maaza models (Apache 2.0)
- [x] Publish EdgeJSON benchmark
- [ ] Launch API beta (100 beta testers)
- [ ] Python & JS SDKs

### Q2 2025
- [ ] Add batch processing endpoint
- [ ] Streaming extraction for long documents
- [ ] Fine-tuning API (custom domains)
- [ ] EU & APAC regions

### Q3 2025
- [ ] Multi-modal extraction (images → JSON)
- [ ] Real-time websocket API
- [ ] Enterprise on-prem deployment kits

---

## Support

**Documentation**: https://cyclecore.ai/docs/api  
**Status Page**: https://status.cyclecore.ai  
**Email**: api-support@cyclecore.ai  
**Discord**: https://discord.gg/cyclecore  
**GitHub**: https://github.com/CycleCore/maaza-sdk  

---

## Legal

**Terms**: https://cyclecore.ai/terms  
**Privacy**: https://cyclecore.ai/privacy  
**SLA**: https://cyclecore.ai/sla  
**License**: Models are Apache 2.0, API is proprietary  

---

**Status**: 📋 Draft Specification (v0.1)  
**Last Updated**: November 22, 2025  
**Next Review**: Implementation planning with CC-WEB team

