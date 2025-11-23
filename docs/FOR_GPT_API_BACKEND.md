# GPT Prompt #1: FastAPI Backend Core

**Task**: Generate complete FastAPI backend for Maaza JSON Extraction API

---

## Context

We're building a production API for JSON extraction using our fine-tuned language models (Maaza-MLM-135M and Maaza-SLM-360M). The API will:
- Accept text + JSON schema as input
- Return extracted JSON with validation
- Handle authentication, billing, rate limiting
- Integrate with Stripe for payments
- Track usage for billing

Models are already trained and available at:
- https://huggingface.co/CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1
- https://huggingface.co/CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1

---

## Requirements

### Project Structure
```
maaza-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Environment config
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py      # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── inference.py     # Model loading & inference
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── extract.py       # POST /v1/extract
│   │   ├── auth.py          # Authentication
│   │   ├── billing.py       # Stripe webhooks
│   │   └── health.py        # Health checks
│   ├── services/
│   │   ├── __init__.py
│   │   ├── inference.py     # Inference service
│   │   ├── validation.py    # Schema validation
│   │   └── usage.py         # Usage tracking
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt.py           # JWT handling
│   │   └── api_keys.py      # API key management
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py       # Database sessions
│   └── utils/
│       ├── __init__.py
│       ├── rate_limit.py    # Redis rate limiting
│       └── cache.py         # Redis caching
├── tests/
│   ├── __init__.py
│   ├── test_extract.py
│   ├── test_auth.py
│   └── test_billing.py
├── alembic/                 # Database migrations
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## Technical Specifications

### 1. Core API Endpoint

**POST /v1/extract**

Request:
```json
{
  "text": "Order #12345 placed by John Doe...",
  "schema": {
    "type": "object",
    "properties": {
      "order_id": {"type": "string"},
      "customer_name": {"type": "string"},
      "total": {"type": "number"}
    },
    "required": ["order_id", "customer_name"]
  },
  "model": "maaza-slm-360m",
  "temperature": 0.0,
  "validate": true
}
```

Response:
```json
{
  "id": "req_abc123",
  "object": "extraction",
  "created": 1732302000,
  "model": "maaza-slm-360m",
  "extracted": {
    "order_id": "12345",
    "customer_name": "John Doe",
    "total": 149.99
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

### 2. Authentication

**Two methods**:
1. **API Keys**: `Authorization: Bearer sk_live_...`
2. **JWT tokens**: For dashboard users

**API Key Format**:
- Prefix: `sk_live_` (production) or `sk_test_` (test mode)
- Hash in database (bcrypt)
- Store metadata: permissions, rate limits, user_id

### 3. Database Schema (PostgreSQL)

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    plan_tier VARCHAR(50) DEFAULT 'free',
    stripe_customer_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- API Keys table
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    key_prefix VARCHAR(20) NOT NULL,
    name VARCHAR(100),
    permissions JSONB DEFAULT '{}',
    rate_limit_per_minute INTEGER DEFAULT 10,
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

-- Usage logs table (partitioned by date)
CREATE TABLE usage_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    api_key_id UUID REFERENCES api_keys(id),
    request_id VARCHAR(50) UNIQUE NOT NULL,
    model VARCHAR(50) NOT NULL,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    latency_ms INTEGER NOT NULL,
    error BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Billing events table
CREATE TABLE billing_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    stripe_event_id VARCHAR(255) UNIQUE NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    amount_cents INTEGER,
    currency VARCHAR(3) DEFAULT 'usd',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_api_keys_user ON api_keys(user_id);
CREATE INDEX idx_api_keys_hash ON api_keys(key_hash);
CREATE INDEX idx_usage_logs_user ON usage_logs(user_id);
CREATE INDEX idx_usage_logs_created ON usage_logs(created_at);
```

### 4. Model Inference

**Load models on startup**:
```python
# Use transformers library + ONNX for optimization
from transformers import AutoTokenizer, AutoModelForCausalLM

models = {
    "maaza-mlm-135m": {
        "model": AutoModelForCausalLM.from_pretrained(
            "CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1"
        ),
        "tokenizer": AutoTokenizer.from_pretrained(
            "HuggingFaceTB/SmolLM2-135M"
        ),
        "max_tokens": 2048
    },
    "maaza-slm-360m": {
        "model": AutoModelForCausalLM.from_pretrained(
            "CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1"
        ),
        "tokenizer": AutoTokenizer.from_pretrained(
            "HuggingFaceTB/SmolLM2-360M"
        ),
        "max_tokens": 2048
    }
}
```

**Inference with prompt template**:
```python
def generate_prompt(text: str, schema: dict) -> str:
    schema_str = json.dumps(schema, indent=2)
    return f"""Extract structured information from the text according to the schema.

Text: {text}

Schema:
{schema_str}

Extracted JSON:"""

def extract(text: str, schema: dict, model: str = "maaza-slm-360m") -> dict:
    prompt = generate_prompt(text, schema)
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.0)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Parse JSON from response
    json_str = extract_json_from_text(response)
    extracted = json.loads(json_str)
    
    return extracted
```

### 5. Rate Limiting (Redis)

```python
import redis
from fastapi import HTTPException

redis_client = redis.Redis(host="localhost", port=6379, db=0)

async def check_rate_limit(api_key: str, limit: int = 10):
    key = f"rate_limit:{api_key}"
    current = redis_client.get(key)
    
    if current and int(current) >= limit:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )
    
    pipe = redis_client.pipeline()
    pipe.incr(key)
    pipe.expire(key, 60)  # 1 minute window
    pipe.execute()
```

### 6. Stripe Integration

**Webhook endpoint**:
```python
@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400)
    
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # Update user's plan tier
        await handle_checkout_complete(session)
    
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        # Downgrade user to free tier
        await handle_subscription_cancel(subscription)
    
    return {"status": "success"}
```

### 7. Error Handling

**Standard error response**:
```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "schema_validation_failed",
    "message": "Output does not conform to provided schema",
    "details": {
      "missing_fields": ["order_id"],
      "invalid_types": [
        {"field": "total", "expected": "number", "got": "string"}
      ]
    }
  }
}
```

**Error codes**:
- `invalid_api_key` (401)
- `rate_limit_exceeded` (429)
- `invalid_schema` (400)
- `text_too_long` (400)
- `extraction_failed` (500)
- `schema_validation_failed` (422)

---

## Environment Variables

```env
# .env.example
DATABASE_URL=postgresql://user:pass@localhost/maaza_api
REDIS_URL=redis://localhost:6379/0
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
JWT_SECRET=your-secret-key
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
```

---

## Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
    volumes:
      - ./app:/app
    command: uvicorn app.main:app --host 0.0.0.0 --reload

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: maaza_api
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

---

## Testing Requirements

**Pytest with 80% coverage**:
```python
# tests/test_extract.py
def test_extract_simple_schema():
    response = client.post(
        "/v1/extract",
        headers={"Authorization": f"Bearer {test_api_key}"},
        json={
            "text": "Order #12345 by John Doe",
            "schema": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "customer": {"type": "string"}
                }
            }
        }
    )
    assert response.status_code == 200
    assert response.json()["extracted"]["order_id"] == "12345"
```

---

## Deliverables

Please generate:
1. ✅ Complete project structure (all files)
2. ✅ FastAPI app with all routes
3. ✅ SQLAlchemy models & Alembic migrations
4. ✅ Authentication (JWT + API keys)
5. ✅ Rate limiting (Redis)
6. ✅ Stripe webhooks
7. ✅ Model inference service
8. ✅ Schema validation
9. ✅ Error handling
10. ✅ Docker setup
11. ✅ Tests (pytest)
12. ✅ README with setup instructions

---

## Notes

- Use async/await throughout
- Add Prometheus metrics (@prometheus decorator)
- Include OpenAPI docs (FastAPI auto-generates)
- Use Pydantic v2 for schemas
- Add comprehensive logging
- Follow REST best practices
- Security: Input validation, SQL injection prevention, rate limiting

---

**Ready to generate? Please create all files with production-ready code!**

