# SLMBench Hosting Setup Guide

**Purpose**: Deploy slmbench.com website to DigitalOcean via Porkbun DNS
**Owner**: CC-WEB (execution), CC-SLM (documentation)
**Date**: 2025-11-19
**Status**: READY FOR EXECUTION

---

## Overview

This guide walks through deploying the SLMBench website:
- **Domain**: slmbench.com (registered on Porkbun)
- **Hosting**: DigitalOcean Droplet
- **Website**: Static HTML/CSS (located in `/home/rain/SLMBench/website/`)

---

## Prerequisites

**Required Access**:
- [x] Porkbun account (domain registered)
- [ ] DigitalOcean account
- [ ] SSH key for server access
- [ ] Local copy of website files

**Website Files** (already created):
```
/home/rain/SLMBench/website/
├── static/
│   └── css/
│       ├── slmbench-tokens.css
│       ├── slmbench-base.css
│       └── slmbench-components.css
├── templates/
│   └── index.html
└── content/
    └── 01-introducing-slmbench.md
```

---

## Step 1: Create DigitalOcean Droplet

### 1.1 Log into DigitalOcean

Visit: https://cloud.digitalocean.com/

### 1.2 Create New Droplet

**Droplet Settings**:
- **Image**: Ubuntu 22.04 LTS (x64)
- **Plan**: Basic
- **CPU Options**: Regular (Shared CPU)
- **Size**: $6/month (1 GB RAM, 1 vCPU, 25 GB SSD)
- **Datacenter**: Choose closest to target audience (e.g., New York, San Francisco)
- **Authentication**: SSH Key (recommended) or Password
- **Hostname**: `slmbench-web-01`
- **Tags**: `slmbench`, `production`, `web`

### 1.3 Add SSH Key (if needed)

**Generate SSH key locally**:
```bash
ssh-keygen -t ed25519 -C "slmbench@cyclecore.tech"
# Save to: ~/.ssh/slmbench_ed25519
# Copy public key to clipboard:
cat ~/.ssh/slmbench_ed25519.pub
```

**Add to DigitalOcean**:
- Click "New SSH Key" during droplet creation
- Paste public key
- Name: "SLMBench Deploy Key"

### 1.4 Create Droplet

- Click "Create Droplet"
- Wait 30-60 seconds for provisioning
- **Note the IP address** (e.g., `159.89.123.45`)

---

## Step 2: Configure Server

### 2.1 SSH into Droplet

```bash
ssh root@159.89.123.45
# (Replace with your droplet IP)
```

### 2.2 Update System

```bash
apt update && apt upgrade -y
```

### 2.3 Install Nginx

```bash
apt install nginx -y
systemctl status nginx
# Should show "active (running)"
```

### 2.4 Install Certbot (SSL/TLS)

```bash
apt install certbot python3-certbot-nginx -y
```

### 2.5 Configure Firewall

```bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
ufw status
```

**Expected Output**:
```
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
Nginx Full                 ALLOW       Anywhere
```

---

## Step 3: Deploy Website Files

### 3.1 Create Website Directory

```bash
mkdir -p /var/www/slmbench.com
chown -R www-data:www-data /var/www/slmbench.com
chmod -R 755 /var/www/slmbench.com
```

### 3.2 Copy Website Files from Local

**On your local machine** (from `/home/rain/SLMBench/`):

```bash
# Copy static files
scp -r website/static root@159.89.123.45:/var/www/slmbench.com/

# Copy index.html
scp website/templates/index.html root@159.89.123.45:/var/www/slmbench.com/

# Verify structure on server
ssh root@159.89.123.45 'ls -R /var/www/slmbench.com'
```

**Expected Structure on Server**:
```
/var/www/slmbench.com/
├── index.html
└── static/
    └── css/
        ├── slmbench-tokens.css
        ├── slmbench-base.css
        └── slmbench-components.css
```

---

## Step 4: Configure Nginx

### 4.1 Create Nginx Config

```bash
nano /etc/nginx/sites-available/slmbench.com
```

**Paste this configuration**:

```nginx
server {
    listen 80;
    listen [::]:80;

    server_name slmbench.com www.slmbench.com;

    root /var/www/slmbench.com;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/css text/javascript application/javascript application/json;

    # Static files
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # HTML files
    location / {
        try_files $uri $uri/ =404;
        expires 1h;
        add_header Cache-Control "public, must-revalidate";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/slmbench.access.log;
    error_log /var/log/nginx/slmbench.error.log;
}
```

**Save and exit**: `Ctrl+X`, `Y`, `Enter`

### 4.2 Enable Site

```bash
ln -s /etc/nginx/sites-available/slmbench.com /etc/nginx/sites-enabled/
```

### 4.3 Test Nginx Config

```bash
nginx -t
```

**Expected Output**:
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 4.4 Restart Nginx

```bash
systemctl restart nginx
systemctl status nginx
```

---

## Step 5: Configure DNS (Porkbun)

### 5.1 Log into Porkbun

Visit: https://porkbun.com/account/domainsSpeedy

### 5.2 Manage DNS for slmbench.com

- Click "slmbench.com"
- Go to "DNS" tab

### 5.3 Add A Records

**Delete existing records** (if any), then add:

| Type | Host | Answer | TTL |
|------|------|--------|-----|
| A    | @    | 159.89.123.45 | 600 |
| A    | www  | 159.89.123.45 | 600 |

**Replace `159.89.123.45` with your actual droplet IP**

### 5.4 Save Changes

- Click "Save" or "Update"
- DNS propagation takes 5-60 minutes (usually fast with Porkbun)

### 5.5 Verify DNS Propagation

**Wait 5-10 minutes**, then test:

```bash
# Check A record
dig slmbench.com +short
# Should return: 159.89.123.45

# Check www subdomain
dig www.slmbench.com +short
# Should return: 159.89.123.45
```

---

## Step 6: Enable HTTPS (SSL/TLS)

### 6.1 Obtain SSL Certificate

**Wait until DNS is propagated**, then:

```bash
certbot --nginx -d slmbench.com -d www.slmbench.com
```

### 6.2 Follow Certbot Prompts

- **Email address**: (enter CycleCore email)
- **Terms of Service**: `Y` (yes)
- **Share email with EFF**: `N` (no, optional)
- **Redirect HTTP to HTTPS**: `2` (yes, recommended)

### 6.3 Verify SSL

**Certbot will automatically**:
- Obtain certificate from Let's Encrypt
- Update Nginx config to use HTTPS
- Set up auto-renewal (cron job)

**Test HTTPS**:
Visit: https://slmbench.com (should show green padlock)

### 6.4 Test Auto-Renewal

```bash
certbot renew --dry-run
```

**Expected Output**:
```
Congratulations, all simulated renewals succeeded
```

---

## Step 7: Verify Deployment

### 7.1 Test Website

**Visit these URLs**:
- http://slmbench.com (should redirect to HTTPS)
- https://slmbench.com (should show homepage)
- https://www.slmbench.com (should work)
- https://slmbench.com/static/css/slmbench-tokens.css (should show CSS)

### 7.2 Check HTTP Headers

```bash
curl -I https://slmbench.com
```

**Expected Headers**:
```
HTTP/2 200
server: nginx
content-type: text/html
x-frame-options: SAMEORIGIN
x-content-type-options: nosniff
x-xss-protection: 1; mode=block
```

### 7.3 Test Performance

**Google PageSpeed Insights**:
Visit: https://pagespeed.web.dev/
Test: https://slmbench.com

**Expected Score**: 90+ (static HTML/CSS is very fast)

---

## Step 8: Post-Deployment Tasks

### 8.1 Post to Super Bus (CC-WEB)

```bash
cat >> /home/rain/federation/ops/bus/LEXOPOLY_SUPER_BUS.jsonl << 'EOF'
{"timestamp":"2025-11-19T[TIME]Z","agent":"CC-WEB","type":"MILESTONE","event":"DEPLOYMENT_COMPLETE","status":"LIVE","impact":"HIGH","environment":"production","url":"https://slmbench.com","version":"v1.0.0 (initial launch)","project":"SLMBench"}
EOF
```

### 8.2 Update Documentation

**CC-WEB**: Update `/home/rain/SLMBench/docs/WEEK1_DAY1-2_SUMMARY.md`:
- Add deployment timestamp
- Add production URL
- Note any issues encountered

### 8.3 Monitor for 24 Hours

**Check these metrics**:
- Uptime (server stays online)
- SSL renewal cron job (check `/var/log/letsencrypt/`)
- Nginx error logs (`/var/log/nginx/slmbench.error.log`)

---

## Maintenance

### Regular Updates (Monthly)

```bash
# System updates
apt update && apt upgrade -y

# Check SSL expiration
certbot certificates

# Check disk space
df -h

# Check Nginx logs
tail -n 50 /var/log/nginx/slmbench.error.log
```

### Updating Website Content

**To update the website**:

```bash
# From local machine
scp website/templates/index.html root@159.89.123.45:/var/www/slmbench.com/

# No need to restart Nginx (static files)
```

### SSL Certificate Renewal

**Automatic**: Certbot creates a cron job that runs twice daily

**Manual (if needed)**:
```bash
certbot renew
systemctl reload nginx
```

---

## Troubleshooting

### Website Not Loading

**Check DNS**:
```bash
dig slmbench.com +short
# Should return droplet IP
```

**Check Nginx**:
```bash
systemctl status nginx
nginx -t
curl -I http://localhost
```

**Check Firewall**:
```bash
ufw status
# Should allow "Nginx Full"
```

### SSL Certificate Errors

**Check certificate status**:
```bash
certbot certificates
```

**Renew manually**:
```bash
certbot renew --force-renewal
systemctl reload nginx
```

### 502 Bad Gateway

**Usually means Nginx config error**:
```bash
nginx -t
tail -n 50 /var/log/nginx/slmbench.error.log
```

---

## Cost Estimate

**Monthly Costs**:
- DigitalOcean Droplet: $6/month (1 GB RAM)
- Domain (slmbench.com): ~$10/year ($0.83/month)
- SSL Certificate: FREE (Let's Encrypt)

**Total**: ~$7/month

---

## Next Steps (After Deployment)

1. **Add Blog System** (Week 2+)
   - Convert markdown blog posts to HTML
   - Add blog index page
   - Set up RSS feed

2. **Add Leaderboard** (Week 3)
   - Dynamic JSON-based leaderboard
   - Auto-update from benchmark results

3. **Add Evaluation Service** (Week 4)
   - API endpoint for model evaluation
   - May need larger droplet (2GB+ RAM)

---

**Status**: READY FOR CC-WEB EXECUTION
**Created By**: CC-SLM
**Date**: 2025-11-19
**Estimated Time**: 45-60 minutes (including DNS propagation wait)
