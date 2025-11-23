# DNS Configuration for slmbench.com

## Status: READY FOR PORKBUN CONFIGURATION

GitHub Pages is live and configured for custom domain `slmbench.com`.
Site will be accessible once DNS records are configured in Porkbun.

**Temporary URL**: https://cyclecore-technologies.github.io/slmbench/
**Final URL**: https://slmbench.com (after DNS propagation)

---

## Required DNS Records in Porkbun

### Option 1: Apex Domain + WWW Subdomain (Recommended)

Configure these records in Porkbun DNS management:

#### A Records (for slmbench.com)
```
Type: A
Host: @ (or blank/apex)
Answer: 185.199.108.153
TTL: 600

Type: A
Host: @ (or blank/apex)
Answer: 185.199.109.153
TTL: 600

Type: A
Host: @ (or blank/apex)
Answer: 185.199.110.153
TTL: 600

Type: A
Host: @ (or blank/apex)
Answer: 185.199.111.153
TTL: 600
```

#### CNAME Record (for www.slmbench.com)
```
Type: CNAME
Host: www
Answer: cyclecore-technologies.github.io
TTL: 600
```

### Option 2: WWW Only (Alternative)

If you prefer only www.slmbench.com:

```
Type: CNAME
Host: www
Answer: cyclecore-technologies.github.io
TTL: 600
```

Then set up URL forwarding from slmbench.com → www.slmbench.com in Porkbun.

---

## Configuration Steps

### In Porkbun Dashboard:

1. **Login**: https://porkbun.com/account/domain
2. **Select Domain**: slmbench.com
3. **DNS Management**: Click "DNS" button
4. **Add Records**:
   - Click "Add" for each A record (4 total)
   - Add CNAME record for www subdomain
5. **Save Changes**: DNS updates usually propagate within 5-60 minutes

### Verification Commands (After DNS Propagation):

```bash
# Check A records
dig slmbench.com +short

# Expected output:
# 185.199.108.153
# 185.199.109.153
# 185.199.110.153
# 185.199.111.153

# Check CNAME record
dig www.slmbench.com +short

# Expected output:
# cyclecore-technologies.github.io
```

---

## GitHub Pages Status

**Current Configuration**:
- ✅ Repository: Public (CycleCore-Technologies/slmbench)
- ✅ GitHub Pages: Enabled (docs/ directory, main branch)
- ✅ Custom Domain: slmbench.com (configured)
- ⏳ HTTPS Certificate: Will auto-provision after DNS verification
- 🔄 Build Status: Building

**Check Build Status**:
```bash
gh api repos/CycleCore-Technologies/slmbench/pages
```

---

## Timeline & Next Steps

### Immediate (0-5 minutes)
- [x] GitHub Pages enabled
- [x] Custom domain configured in GitHub
- [x] Site building at temporary URL

### After DNS Configuration (5-60 minutes)
- [ ] DNS propagation completes
- [ ] GitHub verifies domain ownership
- [ ] HTTPS certificate auto-provisions (Let's Encrypt)
- [ ] Site accessible at https://slmbench.com

### Verification Checklist
- [ ] `slmbench.com` resolves to GitHub Pages IPs
- [ ] `www.slmbench.com` CNAME resolves correctly
- [ ] Site loads at http://slmbench.com
- [ ] HTTPS redirect works (http → https)
- [ ] Certificate shows as valid (green padlock)

---

## Troubleshooting

### DNS Not Propagating
- **Wait Time**: Can take up to 48 hours (usually 5-60 minutes)
- **Check Propagation**: https://dnschecker.org (enter slmbench.com)
- **Flush Local DNS**: `sudo systemd-resolve --flush-caches` (Linux)

### Certificate Not Provisioning
- **Verify DNS First**: Ensure A records are correct
- **Check GitHub Status**: May take 10-20 minutes after DNS propagates
- **Enforce HTTPS**: Will auto-enable after certificate provisions

### Site Shows 404
- **Check Build Status**: `gh api repos/CycleCore-Technologies/slmbench/pages`
- **Verify Files**: Ensure `docs/index.html` exists in main branch
- **GitHub Pages Source**: Should be "main branch, /docs folder"

---

## Contact

**Primary Contact**: CC-WEB agent (deployment/marketing)
**Product Owner**: CC-SLM agent (content/features)
**Domain Registrar**: Porkbun (account access required)

**Support Resources**:
- GitHub Pages Docs: https://docs.github.com/pages
- Porkbun DNS Guide: https://kb.porkbun.com/article/54-how-to-manage-dns-records
- DNS Checker: https://dnschecker.org
