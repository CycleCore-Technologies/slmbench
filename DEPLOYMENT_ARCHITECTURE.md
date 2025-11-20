# SLMBench Deployment Architecture

## Current Deployment: GitHub Pages

**Status**: Active (as of 2025-11-19)
**URL**: https://cyclecore-technologies.github.io/slmbench (temporary) → slmbench.com (custom domain)
**Repository**: https://github.com/CycleCore-Technologies/slmbench (private)

### Why GitHub Pages?

**Simplicity**: Zero-configuration static hosting directly from Git repository
**Cost**: Free for public repositories, $0/month for private repos on Pro plan
**Proven Stack**: Same deployment method as cyclecore.ai (successfully deployed Nov 19)
**No Permissions Issues**: No OAuth integration blockers
**Developer Experience**: Changes deploy automatically on git push

### Deployment Pipeline

```
Local Changes → Git Commit → Push to GitHub → GitHub Pages Auto-Deploy → Live Site
```

**Source Directory**: `/docs` (GitHub Pages convention)
**Branch**: `main`
**Auto-deploy**: Enabled on push

---

## Pivot History: DigitalOcean App Platform → GitHub Pages

### Original Plan: DigitalOcean App Platform

**Target**: Deploy via DO App Platform using free trial ($200 credit)
**Referral Link**: Used Lexopoly's referral (https://m.do.co/c/6bd45beb23a1)
**Configuration**: Created `.do/app.yaml` for static site deployment

### Blocker Encountered

**Error**: `GitHub user does not have access to CycleCore-Technologies/slmbench`
**Root Cause**: DigitalOcean App Platform requires explicit GitHub OAuth authorization for organization repositories
**Impact**: Cannot deploy without granting DO access to CycleCore GitHub org

### Decision: Pivot to GitHub Pages

**Date**: 2025-11-19
**Rationale**:
- **Immediate Deployment**: No OAuth troubleshooting required
- **Zero Risk**: No third-party access to GitHub org
- **Cost Effective**: Free hosting (DO credit preserved for future use)
- **Migration Path**: Can move to DO later if needed for advanced features

**User Quote**: "easy option is fine we can migrate later if needed for security or other reasons"

---

## Future Migration Options

### When to Consider DigitalOcean App Platform

**Server-Side Logic**: If SLMBench needs API endpoints, backend processing
**Advanced CDN**: If global edge caching becomes critical
**Container Deployment**: If moving to containerized architecture
**Team Scaling**: If needing staging environments, preview deployments

### Migration Path

1. Enable GitHub Pages → DigitalOcean OAuth integration
2. Create new DO App Platform deployment
3. Test staging deployment at `slmbench-staging.ondigitalocean.app`
4. Update DNS to point to DO when validated
5. Keep GitHub Pages as backup/rollback option

**Preserved Assets**:
- `.do/app.yaml` configuration file (ready to use)
- DigitalOcean account with $200 credit
- Repository structure compatible with both platforms

---

## DNS Configuration

### Current Setup (Pending)

**Domain**: slmbench.com (owned, managed via Porkbun)
**Target**: GitHub Pages custom domain

**Required DNS Records**:
```
Type: CNAME
Name: www
Value: cyclecore-technologies.github.io

Type: A (Apex/Root)
Name: @
Value: 185.199.108.153
       185.199.109.153
       185.199.110.153
       185.199.111.153
```

**GitHub Pages Custom Domain**: slmbench.com (configured in repository settings)

### SSL/TLS

**Provider**: GitHub Pages (automatic Let's Encrypt certificates)
**HTTPS**: Enforced after DNS propagation
**Renewal**: Automatic (zero maintenance)

---

## Deployment Checklist

- [x] Create GitHub repository (CycleCore-Technologies/slmbench)
- [x] Push website code to GitHub
- [x] Create `/docs` directory with website files
- [ ] Commit and push `/docs` to GitHub
- [ ] Enable GitHub Pages in repository settings
- [ ] Configure custom domain (slmbench.com)
- [ ] Update Porkbun DNS records
- [ ] Verify HTTPS certificate provisioning
- [ ] Test site at slmbench.com
- [ ] Update SUPER_BUS_OPS.md with deployment status

---

## Technical Stack

**Static Site Generator**: None (hand-coded HTML/CSS/JS)
**Design System**: Custom tokens + base + components CSS architecture
**JavaScript**: Vanilla JS (no framework dependencies)
**Assets**: Self-hosted (no external CDN dependencies)
**Analytics**: None (privacy-first approach)

---

## Maintenance Notes

**Deployment**: `git push origin main` auto-deploys to production
**Rollback**: `git revert` or `git reset` to previous commit
**DNS Changes**: Propagation takes 5-60 minutes via Porkbun
**Certificate Renewal**: Automatic via GitHub Pages
**Monitoring**: GitHub Pages status page (https://www.githubstatus.com)

**Point of Contact**: CC-WEB agent (marketing/deployment)
**Product Owner**: CC-SLM agent (content/features)
