# Maaza API - Business Strategy & Implementation Plan

**Date**: November 22, 2025  
**Status**: Planning Phase  
**Target**: Q1 2025 Beta Launch  

---

## Strategic Decision: cyclecore.ai vs slmbench.com

### ✅ **RECOMMENDATION: cyclecore.ai for API**

**Rationale**:
1. **Brand Separation**: Keep SLMBench.com as open research/benchmark platform
2. **Business Clarity**: All paid services under CycleCore brand
3. **Future-Proof**: Can expand to multiple products beyond Maaza
4. **Trust**: Clear separation between "open science" and "commercial services"

### Site Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ slmbench.com (Open Benchmark Platform)                      │
├─────────────────────────────────────────────────────────────┤
│ • EdgeJSON benchmark (free)                                 │
│ • Community leaderboard (free)                              │
│ • Verified leaderboard ($20/model verification)             │
│ • Documentation & research papers                           │
│ • → "Deploy via API" CTA → cyclecore.ai/api               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ cyclecore.ai (Commercial Platform)                          │
├─────────────────────────────────────────────────────────────┤
│ • Maaza JSON Extraction API                                 │
│ • Pricing & billing                                         │
│ • API dashboard & keys                                      │
│ • Usage analytics                                           │
│ • Support & enterprise                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Business Model

### Revenue Streams

1. **API Usage** (Primary)
   - Pay-per-request: $0.001-$0.05/request
   - Monthly tiers: $29-$299/month
   - Enterprise: Custom pricing

2. **Benchmark Verification** (Secondary)
   - $20/model on slmbench.com
   - Drives API adoption

3. **Enterprise Services** (Future)
   - Custom model training
   - On-prem deployment
   - Support contracts

### Pricing Strategy

| Tier | Monthly | Included Requests | Overage (MLM) | Overage (SLM) |
|------|---------|-------------------|---------------|---------------|
| **Free** | $0 | 100/day | N/A | N/A |
| **Starter** | $29 | 10,000 | $0.010 | $0.050 |
| **Pro** | $299 | 100,000 | $0.005 | $0.025 |
| **Enterprise** | Custom | Custom | Custom | Custom |

**Target Customers**:
- Startups: Starter tier
- Scale-ups: Pro tier  
- Enterprise: Custom contracts

**Revenue Projections** (Year 1):

| Customers | Tier | ARR per Customer | Total ARR |
|-----------|------|------------------|-----------|
| 100 | Starter | $348 | $34,800 |
| 20 | Pro | $3,588 | $71,760 |
| 2 | Enterprise | $25,000 | $50,000 |
| **Total** | | | **$156,560** |

*Conservative estimate, assumes modest growth*

---

## Technical Architecture

### Infrastructure (DigitalOcean)

```
┌─────────────────────────────────────────────────────────┐
│ Load Balancer (nginx)                                    │
└────────────┬────────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────┐      ┌────▼────┐
│ API    │      │ API     │
│ Server │      │ Server  │
│ (FastAPI)     │ (FastAPI)│
└───┬────┘      └────┬────┘
    │                │
    └────────┬────────┘
             │
    ┌────────▼────────────────────────────────┐
    │                                          │
┌───▼──────────┐  ┌──────────┐  ┌───────────┐
│ Model Workers│  │  Redis   │  │ PostgreSQL│
│ (GPU/CPU)    │  │  (Cache) │  │  (Billing)│
│              │  │          │  │           │
│ • MLM-135M   │  └──────────┘  └───────────┘
│ • SLM-360M   │
└──────────────┘
```

### Components

**API Layer**:
- FastAPI (Python)
- Authentication (JWT)
- Rate limiting (Redis)
- Request validation

**Model Serving**:
- ONNX Runtime (optimized inference)
- GPU instances for SLM-360M (NVIDIA T4)
- CPU instances for MLM-135M (8-core)
- Auto-scaling based on load

**Storage**:
- PostgreSQL (billing, usage, API keys)
- Redis (caching, rate limits)
- S3 (logs, backups)

**Monitoring**:
- Prometheus (metrics)
- Grafana (dashboards)
- Sentry (error tracking)
- Uptime monitoring

---

## Implementation Plan

### Phase 1: MVP (Weeks 1-4)

**Week 1-2: Core API**
- [ ] FastAPI server setup
- [ ] Model loading & inference
- [ ] Basic authentication
- [ ] Schema validation
- [ ] Error handling

**Week 3: Billing Integration**
- [ ] Stripe integration
- [ ] Usage tracking
- [ ] API key management
- [ ] Rate limiting

**Week 4: Testing & Docs**
- [ ] Load testing (100 req/s)
- [ ] API documentation (OpenAPI)
- [ ] Example code (Python, JS)
- [ ] Beta tester signup

### Phase 2: Beta (Weeks 5-8)

**Week 5-6: Infrastructure**
- [ ] Deploy to DigitalOcean
- [ ] Set up monitoring
- [ ] Configure auto-scaling
- [ ] SSL/DNS setup

**Week 7: Beta Launch**
- [ ] Invite 100 beta testers
- [ ] Dashboard UI (API keys, usage)
- [ ] Email notifications
- [ ] Support system

**Week 8: Feedback & Iteration**
- [ ] Collect feedback
- [ ] Fix bugs
- [ ] Optimize performance
- [ ] Improve documentation

### Phase 3: Public Launch (Weeks 9-12)

**Week 9-10: Polish**
- [ ] SDKs (Python, JavaScript)
- [ ] Batch processing endpoint
- [ ] Additional examples
- [ ] Marketing materials

**Week 11: Soft Launch**
- [ ] Blog post announcement
- [ ] Social media campaign
- [ ] HackerNews post
- [ ] Email to waitlist

**Week 12: Post-Launch**
- [ ] Monitor usage
- [ ] Respond to feedback
- [ ] Scale infrastructure
- [ ] Plan v2 features

---

## Resource Requirements

### Development
- **Solo dev time**: 150-200 hours over 12 weeks
- **AI assistance**: Claude for API code, CC-WEB for frontend

### Infrastructure Costs (Monthly)

| Component | Specs | Cost |
|-----------|-------|------|
| API Servers (2x) | 4 CPU, 8GB RAM | $80 |
| GPU Worker (1x) | NVIDIA T4, 16GB | $200 |
| CPU Workers (2x) | 8 CPU, 16GB RAM | $80 |
| PostgreSQL | Managed, 2GB | $15 |
| Redis | Managed, 1GB | $15 |
| Load Balancer | Basic | $12 |
| S3 Storage | 50GB | $5 |
| Monitoring | Grafana Cloud | $0 (free tier) |
| **Total** | | **~$407/month** |

**Break-even**: ~15 Starter customers or 2-3 Pro customers

### Tools & Services
- DigitalOcean (hosting)
- Stripe (payments)
- Cloudflare (DNS, CDN)
- GitHub (code)
- Sentry (error tracking)
- Postman (API testing)

---

## Go-to-Market Strategy

### Target Audience

1. **Early Adopters** (Beta)
   - SLMBench leaderboard users
   - HuggingFace community
   - Reddit r/MachineLearning

2. **Primary Market**
   - Startups building AI apps
   - SaaS companies adding extraction
   - Agencies building client solutions

3. **Enterprise** (Year 2)
   - Financial services (invoice processing)
   - Healthcare (medical records)
   - Legal (document parsing)

### Marketing Channels

**Organic**:
- arXiv paper (credibility)
- HuggingFace models (discovery)
- SLMBench.com (conversion funnel)
- GitHub repos (technical trust)
- Blog posts & tutorials

**Paid** (Post-Launch):
- Google Ads (targeted keywords)
- Reddit ads (r/MachineLearning)
- Dev.to sponsorships
- Conference booths

**Community**:
- Discord server
- Weekly office hours
- Open-source contributions
- Guest posts on AI blogs

---

## Competitive Landscape

### Direct Competitors

| Competitor | Strength | Weakness | Our Edge |
|------------|----------|----------|----------|
| OpenAI API | General-purpose | Expensive, slow | 10x cheaper, faster |
| Anthropic Claude | High quality | Not specialized | Task-specific accuracy |
| Hugging Face Inference | Many models | No guarantees | Schema validation |
| Custom solutions | Full control | High complexity | Easy API, low overhead |

### Differentiation

1. **Specialized**: Built for JSON extraction only
2. **Transparent**: Open-source models (Apache 2.0)
3. **Affordable**: 10x cheaper than GPT-4 for this task
4. **Fast**: Sub-200ms latency, edge-optimized
5. **Validated**: Schema compliance guaranteed

---

## Risk Assessment

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Model quality issues | Low | High | Extensive testing, beta period |
| Infrastructure costs | Medium | Medium | Auto-scaling, usage alerts |
| Performance bottlenecks | Medium | High | Load testing, caching |
| Security vulnerabilities | Low | High | Security audit, rate limiting |

### Business Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Low adoption | Medium | High | Free tier, great docs |
| Competitor undercuts | Low | Medium | Value-add: validation, support |
| Churn | Medium | Medium | Usage analytics, retention hooks |
| Regulatory (AI) | Low | Medium | Compliance documentation |

---

## Success Metrics

### Phase 1 (Beta)
- 100 beta signups
- 10 active users
- 10,000 API calls
- <5% error rate
- <200ms p95 latency

### Phase 2 (Launch)
- 500 signups (3 months)
- 50 paying customers
- 100,000 API calls/month
- $2,000 MRR
- 4.5+ star rating

### Phase 3 (Growth)
- 2,000 signups (6 months)
- 150 paying customers
- 1M API calls/month
- $10,000 MRR
- 10+ enterprise pilots

---

## Next Steps

### Immediate (This Week)
1. ✅ Create API specification
2. [ ] Review with CC-WEB for frontend input
3. [ ] Set up DigitalOcean account
4. [ ] Design API dashboard mockups
5. [ ] Write FastAPI skeleton code

### Short-term (Next 2 Weeks)
1. [ ] Build MVP API endpoint
2. [ ] Test with local models
3. [ ] Create landing page (cyclecore.ai/api)
4. [ ] Set up Stripe test mode
5. [ ] Document onboarding flow

### Medium-term (Month 1)
1. [ ] Deploy to DigitalOcean
2. [ ] Invite beta testers
3. [ ] Build dashboard UI
4. [ ] Create Python SDK
5. [ ] Launch beta program

---

## Open Questions

1. **Pricing**: Is $29 starter too high? Too low?
2. **Models**: Should we offer fine-tuning API later?
3. **Regions**: Start with US East only, or add EU immediately?
4. **Support**: Email-only or add Discord/Slack?
5. **Free tier**: 100/day enough for testing? Too generous?

---

## Alignment with Paper Launch

**Synergy**:
- Paper establishes credibility
- API provides revenue
- Self-host option builds trust
- Research → Product pipeline

**Timeline**:
- Paper submission: Next week
- API MVP: 4 weeks
- Beta launch: 8 weeks
- Public launch: 12 weeks

**Cross-promotion**:
- Paper abstract mentions API option
- HuggingFace model cards link to API
- SLMBench.com has "Deploy" CTA
- API docs cite paper for benchmarks

---

**Status**: 📋 Strategic Plan (v0.1)  
**Owner**: Rain (solo dev + AI assistance)  
**Review**: Share with CC-WEB for infrastructure input  
**Next Review**: After paper submission complete

