# Grok Prompt: Complete Maaza API (Batches 4-8)

**Context**: GPT already generated Batches 1-3 (foundation, database, auth). Continue from Batch 4.

---

## 📋 What We Have (Batches 1-3)

**Project structure**:
```
maaza-api/
├── app/
│   ├── main.py           # FastAPI app skeleton
│   ├── config.py         # Pydantic settings
│   ├── db/
│   │   ├── base.py       # SQLAlchemy Base
│   │   └── session.py    # Async DB session
│   ├── models/
│   │   ├── user.py       # User model
│   │   ├── api_key.py    # ApiKey model
│   │   ├── usage_log.py  # UsageLog model
│   │   └── billing_event.py  # BillingEvent model
│   └── auth/
│       ├── passwords.py  # bcrypt hashing
│       ├── jwt.py        # JWT tokens
│       ├── api_keys.py   # API key generation
│       └── dependencies.py  # FastAPI auth deps
├── alembic/              # Migrations configured
├── docker-compose.yml    # PostgreSQL + Redis
└── requirements.txt      # All dependencies
```

**Working**:
- ✅ Config loaded from `.env`
- ✅ Async PostgreSQL with SQLAlchemy 2.0
- ✅ JWT + API key authentication
- ✅ Alembic migrations ready

---

## 🎯 Generate Batches 4-8

### **Batch 4: Model Inference**

Create `app/services/inference.py`:

**Requirements**:
1. Load Maaza models on startup:
   - `CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1`
   - `CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1`
2. Use HuggingFace transformers library
3. Prompt template:
   ```
   Extract structured information from the text according to the schema.

   Text: {text}

   Schema:
   {schema_json}

   Extracted JSON:
   ```
4. Parse JSON from model output
5. Validate against provided schema (jsonschema library)
6. Cache results in Redis (key: hash(text + schema))
7. Return: extracted JSON + validation errors + usage stats

**Function signature**:
```python
async def extract_json(
    text: str,
    schema: dict,
    model: Literal["maaza-mlm-135m", "maaza-slm-360m"] = "maaza-slm-360m",
    redis_client: Redis,
) -> dict:
    """
    Extract JSON from text using Maaza models.
    
    Returns:
    {
        "extracted": dict,
        "validation": {"valid": bool, "errors": list},
        "usage": {"input_tokens": int, "output_tokens": int},
        "latency_ms": int,
        "cached": bool
    }
    """
```

---

### **Batch 5: API Routes**

Create `app/routes/extract.py`:

**POST /v1/extract**:
```python
from fastapi import APIRouter, Depends
from app.auth.dependencies import require_api_key
from app.services.inference import extract_json
from pydantic import BaseModel

class ExtractRequest(BaseModel):
    text: str
    schema: dict
    model: str = "maaza-slm-360m"
    temperature: float = 0.0
    validate: bool = True

class ExtractResponse(BaseModel):
    id: str  # Request ID
    extracted: dict
    validation: dict
    usage: dict
    latency_ms: int

@router.post("/extract", response_model=ExtractResponse)
async def extract_endpoint(
    request: ExtractRequest,
    api_key: ApiKey = Depends(require_api_key),
    db: AsyncSession = Depends(get_db),
):
    # 1. Rate limit check
    # 2. Call inference service
    # 3. Log usage to database
    # 4. Return result
```

**Also create**:
- `app/routes/health.py` - Health check endpoint
- `app/routes/models.py` - List available models

Wire routers in `app/main.py`:
```python
from app.routes import extract, health, models
app.include_router(extract.router, prefix="/v1", tags=["extract"])
app.include_router(health.router, tags=["health"])
app.include_router(models.router, prefix="/v1", tags=["models"])
```

---

### **Batch 6: Rate Limiting**

Create `app/middleware/rate_limit.py`:

**Requirements**:
1. Use Redis for rate limiting
2. Key: `rate_limit:{api_key_id}`
3. Limit: 60 requests/minute (configurable per API key)
4. Return 429 with `Retry-After` header when exceeded
5. Implement as FastAPI middleware

**Function**:
```python
async def rate_limit_middleware(request: Request, call_next):
    # Extract API key from request
    # Check Redis counter
    # Increment or reject
    # Return response or 429
```

Add to `app/main.py`:
```python
from app.middleware.rate_limit import rate_limit_middleware
app.middleware("http")(rate_limit_middleware)
```

---

### **Batch 7: Stripe Integration**

Create `app/routes/billing.py`:

**POST /webhooks/stripe**:
```python
@router.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    # 1. Verify signature
    # 2. Parse event
    # 3. Handle events:
    #    - checkout.session.completed → Upgrade user
    #    - customer.subscription.created → Activate subscription
    #    - customer.subscription.deleted → Downgrade user
    # 4. Log to billing_events table
    # 5. Return 200
```

**Handle these events**:
- `checkout.session.completed`
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.payment_succeeded`
- `invoice.payment_failed`

---

### **Batch 8: Tests + Dockerfile**

**Tests** (`tests/`):
```python
# tests/test_extract.py
def test_extract_simple_schema(client, test_api_key):
    response = client.post(
        "/v1/extract",
        headers={"X-API-Key": test_api_key},
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

# tests/test_auth.py
# tests/test_rate_limit.py
# tests/test_billing.py
```

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app/ app/
COPY alembic/ alembic/
COPY alembic.ini .

# Download models on build (optional, or do at runtime)
RUN python -c "from transformers import AutoModel; \
    AutoModel.from_pretrained('CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1'); \
    AutoModel.from_pretrained('CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📦 Deliverables

Generate complete, production-ready code for:

1. **Batch 4**: `app/services/inference.py` + model loading
2. **Batch 5**: `app/routes/extract.py`, `health.py`, `models.py`
3. **Batch 6**: `app/middleware/rate_limit.py`
4. **Batch 7**: `app/routes/billing.py` (Stripe webhooks)
5. **Batch 8**: `tests/`, `Dockerfile`, `.dockerignore`

---

## 🎨 Code Style

- **Async/await** throughout
- **Type hints** (Pydantic v2)
- **Error handling** with FastAPI HTTPException
- **Logging** with Python logging
- **Docstrings** for all functions
- **Security**: Input validation, SQL injection prevention

---

## 🚀 Integration with Batch 1-3

Your code should:
- Use `settings` from `app/config.py`
- Use `get_db()` from `app/db/session.py`
- Use `require_api_key` from `app/auth/dependencies.py`
- Use models from `app/models/`

---

**Ready? Generate Batches 4-8 with complete, copy-paste-ready code!**

