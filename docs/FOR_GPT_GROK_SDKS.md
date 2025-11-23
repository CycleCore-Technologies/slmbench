# GPT/Grok Prompt #2: SDKs & Documentation

**Task**: Create client SDKs (Python, JavaScript/TypeScript) and comprehensive API documentation

---

## Context

We have a FastAPI backend for JSON extraction (see FOR_GPT_API_BACKEND.md). Now we need:
1. Python SDK (sync + async)
2. JavaScript/TypeScript SDK (Node + Browser)
3. API documentation site
4. Code examples & tutorials

API Base: `https://api.cyclecore.ai`

---

## Task 1: Python SDK

### Requirements
- **Package name**: `maaza-sdk` (PyPI)
- **Python**: 3.8+
- **Features**:
  - Sync and async clients
  - Type hints throughout
  - Automatic retries
  - Error handling
  - Rate limit handling
  - Response streaming (future)

### Project Structure
```
maaza-sdk/
├── maaza/
│   ├── __init__.py
│   ├── client.py          # Main client class
│   ├── async_client.py    # Async client
│   ├── resources/
│   │   ├── __init__.py
│   │   ├── extract.py     # Extract resource
│   │   └── models.py      # Models resource
│   ├── types/
│   │   ├── __init__.py
│   │   ├── extract.py     # Extract types
│   │   └── errors.py      # Error classes
│   └── utils/
│       ├── __init__.py
│       ├── retry.py       # Retry logic
│       └── validation.py  # Schema validation
├── tests/
│   ├── test_client.py
│   ├── test_extract.py
│   └── test_async.py
├── examples/
│   ├── basic_usage.py
│   ├── async_usage.py
│   └── batch_processing.py
├── docs/
│   └── api.md
├── pyproject.toml
├── README.md
└── LICENSE
```

### Usage Examples

**Sync Client**:
```python
from maaza import MaazaClient

client = MaazaClient(api_key="sk_live_...")

result = client.extract(
    text="Order #12345 for $500.00 to Acme Corp",
    schema={
        "type": "object",
        "properties": {
            "order_id": {"type": "string"},
            "amount": {"type": "number"},
            "customer": {"type": "string"}
        },
        "required": ["order_id", "amount"]
    },
    model="maaza-slm-360m"
)

print(result.extracted)
# {'order_id': '12345', 'amount': 500.0, 'customer': 'Acme Corp'}

print(result.usage)
# Usage(input_tokens=23, output_tokens=12, total_tokens=35)

print(result.latency_ms)
# 142
```

**Async Client**:
```python
from maaza import AsyncMaazaClient
import asyncio

async def main():
    client = AsyncMaazaClient(api_key="sk_live_...")
    
    # Single request
    result = await client.extract(
        text="...",
        schema={...}
    )
    
    # Batch requests
    tasks = [
        client.extract(text=t, schema=s)
        for t, s in zip(texts, schemas)
    ]
    results = await asyncio.gather(*tasks)

asyncio.run(main())
```

**Error Handling**:
```python
from maaza import MaazaClient
from maaza.errors import (
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIError
)

client = MaazaClient(api_key="sk_live_...")

try:
    result = client.extract(text="...", schema={...})
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except ValidationError as e:
    print(f"Schema validation failed: {e.details}")
except APIError as e:
    print(f"API error: {e.message}")
```

### Features to Implement

**1. Automatic Retries**:
- Retry on 429 (rate limit) with exponential backoff
- Retry on 500/502/503 (server errors)
- Max 3 retries
- Configurable via `max_retries` parameter

**2. Timeout Handling**:
- Default: 30 seconds
- Configurable per-request
- Separate timeout for connection vs read

**3. Response Validation**:
- Validate extracted JSON against provided schema
- Optional client-side validation before API call
- Detailed error messages

**4. Type Hints**:
- Use Pydantic for request/response models
- Full typing support for IDE autocomplete
- Runtime type checking (optional)

---

## Task 2: JavaScript/TypeScript SDK

### Requirements
- **Package name**: `@cyclecore/maaza` (npm)
- **Node**: 16+
- **Browser**: Modern browsers (ES2020+)
- **Features**:
  - TypeScript-first
  - Works in Node and browser
  - Tree-shakeable
  - Auto-retry
  - Fetch-based (no axios dependency)

### Project Structure
```
maaza-js/
├── src/
│   ├── index.ts
│   ├── client.ts
│   ├── resources/
│   │   ├── extract.ts
│   │   └── models.ts
│   ├── types/
│   │   ├── extract.ts
│   │   ├── errors.ts
│   │   └── index.ts
│   └── utils/
│       ├── retry.ts
│       └── fetch.ts
├── tests/
│   ├── client.test.ts
│   └── extract.test.ts
├── examples/
│   ├── node.ts
│   ├── browser.html
│   └── nextjs.tsx
├── package.json
├── tsconfig.json
├── README.md
└── LICENSE
```

### Usage Examples

**Node.js**:
```typescript
import { MaazaClient } from '@cyclecore/maaza';

const client = new MaazaClient({ 
  apiKey: 'sk_live_...' 
});

const result = await client.extract({
  text: 'Order #12345 for $500.00',
  schema: {
    type: 'object',
    properties: {
      order_id: { type: 'string' },
      amount: { type: 'number' }
    }
  },
  model: 'maaza-slm-360m'
});

console.log(result.extracted);
// { order_id: '12345', amount: 500.0 }
```

**Browser**:
```html
<script type="module">
import { MaazaClient } from 'https://cdn.jsdelivr.net/npm/@cyclecore/maaza/+esm';

const client = new MaazaClient({ apiKey: 'sk_live_...' });

const result = await client.extract({
  text: document.querySelector('#input').value,
  schema: { /* ... */ }
});

document.querySelector('#output').textContent = 
  JSON.stringify(result.extracted, null, 2);
</script>
```

**Next.js**:
```typescript
// app/api/extract/route.ts
import { MaazaClient } from '@cyclecore/maaza';

const client = new MaazaClient({
  apiKey: process.env.MAAZA_API_KEY!
});

export async function POST(request: Request) {
  const { text, schema } = await request.json();
  
  const result = await client.extract({ text, schema });
  
  return Response.json(result);
}
```

### Type Definitions

```typescript
// src/types/extract.ts
export interface ExtractRequest {
  text: string;
  schema: JSONSchema;
  model?: 'maaza-mlm-135m' | 'maaza-slm-360m';
  temperature?: number;
  validate?: boolean;
  return_confidence?: boolean;
}

export interface ExtractResponse {
  id: string;
  object: 'extraction';
  created: number;
  model: string;
  extracted: Record<string, any>;
  validation: {
    valid: boolean;
    errors: ValidationError[];
  };
  usage: {
    input_tokens: number;
    output_tokens: number;
    total_tokens: number;
  };
  latency_ms: number;
}

export interface JSONSchema {
  type: 'object';
  properties: Record<string, JSONSchemaProperty>;
  required?: string[];
}

// ... full type definitions
```

---

## Task 3: API Documentation Site

### Requirements
- **Stack**: Next.js + MDX (or similar)
- **Host**: Vercel or Cloudflare Pages
- **URL**: https://docs.cyclecore.ai

### Pages Structure
```
docs-site/
├── pages/
│   ├── index.mdx              # Home
│   ├── quickstart.mdx         # 5-min quickstart
│   ├── authentication.mdx     # API keys, JWT
│   ├── api-reference/
│   │   ├── index.mdx
│   │   ├── extract.mdx        # POST /v1/extract
│   │   ├── models.mdx         # GET /v1/models
│   │   └── errors.mdx         # Error codes
│   ├── sdks/
│   │   ├── python.mdx
│   │   ├── javascript.mdx
│   │   └── curl.mdx
│   ├── guides/
│   │   ├── use-cases.mdx      # 10 examples
│   │   ├── best-practices.mdx
│   │   ├── rate-limits.mdx
│   │   └── migration.mdx      # From self-hosted
│   └── examples/
│       ├── invoice.mdx
│       ├── support-tickets.mdx
│       └── api-responses.mdx
├── components/
│   ├── CodeBlock.tsx
│   ├── ApiPlayground.tsx      # Interactive tester
│   └── SchemaBuilder.tsx      # Visual schema builder
└── public/
    └── openapi.json           # OpenAPI spec
```

### Key Features

**1. Interactive API Playground**:
```tsx
// Try it now widget on every endpoint page
<ApiPlayground 
  endpoint="/v1/extract"
  defaultRequest={{
    text: "Order #12345...",
    schema: { /* ... */ }
  }}
  requiresAuth={true}
/>
```

**2. Schema Builder**:
- Visual drag-and-drop schema creation
- Generates JSON Schema from UI
- Copy code button
- Live validation

**3. Code Examples**:
- Every endpoint has examples in Python, JavaScript, cURL
- Copy button for each example
- Syntax highlighting
- Live API keys (user's own key)

**4. Search**:
- Algolia DocSearch or similar
- Instant search across all docs
- Keyboard shortcuts (Cmd+K)

---

## Task 4: Tutorials & Examples

### Tutorial 1: Invoice Extraction
```markdown
# Extract Invoice Data

Learn how to extract structured data from invoices.

## Problem
You receive invoices in various formats (email, PDF, screenshots) 
and need to extract key fields for accounting.

## Solution
Use Maaza to extract invoice data into a structured format.

## Schema Design
[Python code example]
[JavaScript code example]

## Full Example
[Complete working code]

## Tips
- Handle missing fields gracefully
- Validate totals match (line items sum)
- Use SLM-360M for complex invoices
```

### Tutorial 2: Support Ticket Triage
### Tutorial 3: API Response Parsing
### Tutorial 4: E-commerce Order Processing
### Tutorial 5: Medical Records Extraction

Each tutorial should have:
- Problem statement
- Solution approach
- Complete working code (Python + JS)
- Expected output
- Tips & best practices

---

## Task 5: CLI Tool (Bonus)

**Package**: `maaza-cli` (pip/npm)

```bash
# Install
pip install maaza-cli

# Configure
maaza configure
# Prompts for API key, saves to ~/.maaza/config

# Extract
maaza extract --text "Order #123..." --schema schema.json

# Batch processing
maaza batch --input invoices.jsonl --schema invoice.json --output results.jsonl

# Test schema
maaza validate-schema schema.json

# Check usage
maaza usage --month 2025-11
```

---

## Deliverables

Please generate:

### **Python SDK**
- [ ] Complete package with sync + async clients
- [ ] Type hints and Pydantic models
- [ ] Retry logic and error handling
- [ ] Tests with 80%+ coverage
- [ ] README with examples
- [ ] PyPI-ready (pyproject.toml)

### **JavaScript SDK**
- [ ] TypeScript-first implementation
- [ ] Node + Browser support
- [ ] Full type definitions
- [ ] Tests (Jest)
- [ ] README with examples
- [ ] npm-ready (package.json)

### **Documentation Site**
- [ ] Next.js + MDX setup
- [ ] All pages (15+ pages)
- [ ] Interactive API playground
- [ ] Schema builder component
- [ ] Search integration
- [ ] OpenAPI spec

### **Tutorials**
- [ ] 5 complete tutorials
- [ ] Each with Python + JS examples
- [ ] Real-world use cases
- [ ] Copy-paste ready code

### **CLI Tool** (if time permits)
- [ ] Basic commands
- [ ] Config management
- [ ] Batch processing

---

## Success Criteria

- ✅ Developer can get started in <5 minutes
- ✅ SDKs feel native to each language
- ✅ Documentation answers 90% of questions
- ✅ Examples are copy-paste ready
- ✅ Search finds relevant info instantly

---

**Ready? Generate SDKs and docs that developers will love!**

