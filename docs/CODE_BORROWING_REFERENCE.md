# Code Borrowing Reference - Federation Resources

**Agent**: CC-SLM (SLM-Bench Edge Pack)
**Authority**: Constitutional Amendment 001 Section 5.2 + DOCK-025 Section 4.3
**Policy**: SLM-Bench can freely copy code from Lexopoly federation products

---

## CycleCore.ai Website Design System

**Location**: `/home/rain/LangManus/cyclecore-site/`
**Agent Owner**: CC-WEB
**Last Updated**: 2025-11-18 (Phase 2: Product Pages + Transparency Refinements)

### Available Resources

**CSS Design System** (`css/`):
1. **cyclecore-tokens.css** - Design tokens
   - Pure black background: `#0a0a0a`
   - Color system: blacks, grays, cyan accent
   - Typography: Inter (display), JetBrains Mono (code)
   - Spacing, shadows, borders, transitions

2. **cyclecore-base.css** - Base styles
   - Reset, typography, layout fundamentals
   - Responsive grid system

3. **cyclecore-components.css** - Reusable components
   - Buttons, cards, navigation, footer
   - Forms, tables, code blocks

**Design Philosophy**:
- Aggressive minimalism (luxury through space)
- Ultra-high contrast (black + white + single accent)
- Developer-focused aesthetic
- Privacy-first branding

**Key Design Tokens**:
```css
--cc-black: #0a0a0a;          /* Pure black background */
--cc-gray-900: #1a1a1a;       /* Elevated surfaces */
--cc-text-primary: #ffffff;   /* Headlines, body */
--cc-accent-cyan: #00d4ff;    /* Primary actions, links */
--cc-font-display: 'Inter', sans-serif;
--cc-font-mono: 'JetBrains Mono', monospace;
```

### What to Borrow for slmbench.com

**Recommended**:
- ✅ All 3 CSS files (tokens, base, components)
- ✅ Color scheme (pure black `#0a0a0a`)
- ✅ Typography system (Inter + JetBrains Mono)
- ✅ Component patterns (buttons, cards, navigation)
- ✅ Spacing and layout principles

**Customization Needed**:
- Update branding (CycleCore → CycleCore Technologies SLMBench)
- Adjust color accents if desired (keep cyan or change)
- Add SLMBench-specific components (leaderboard table, benchmark cards)

**How to Use**:
1. Copy CSS files to `website/static/css/`
2. Rename: `cyclecore-*.css` → `slmbench-*.css` (or keep names)
3. Update CSS custom properties as needed
4. Link in HTML templates
5. Document source in git commit message

---

## Orchestra Project (GPU Management)

**Location**: TBD (need to locate Orchestra codebase)
**Agent Owner**: CC-ORCH
**Last Activity**: 2025-11-18 (UI replacement, GPU VRAM auto-unload)

### Potential Resources

**GPU Auto-Unload** (from Super Bus event):
- 30s idle timeout → frees ~14GB VRAM
- Activity tracking for resource management
- Could borrow for 4080 MLM training coordination

**Flask UI Patterns**:
- Dark mode implementation
- Code analysis display
- File loading, verification badges
- Markdown rendering

**Action**: Need to locate Orchestra codebase to identify specific code to borrow.

---

## ComplianceLogger Project (Web UI)

**Location**: TBD (need to locate ComplianceLogger codebase)
**Agent Owner**: CC-CL
**Status**: V1.2.1 production-ready

### Potential Resources

**UI Components**:
- NextAuth authentication patterns
- Admin analytics (funnels, cohorts, segmentation)
- PDF generation (single + bulk)
- Photo upload (BYTEA storage)

**Action**: Evaluate if any patterns useful for SLMBench evaluation service.

---

## MCPBodega Project

**Location**: TBD (need to locate MCPBodega codebase)
**Agent Owner**: CC-MCP
**Last Activity**: 2025-11-18 (FCO_INQ_009 strategic response)

### Potential Resources

**Platform Patterns**:
- SaaS infrastructure
- Marketplace patterns (if applicable to SLMBench evaluation service)
- Policy/compliance layers

**Action**: Evaluate after MVP launch if relevant to SLMBench business model.

---

## Federation Code Sharing Process

Per Constitutional Amendment 001 Section 5.2 and DOCK-025 Section 4.3:

### Rules

1. **Direct Copy Allowed**: No pre-approval required
2. **Document Source**: Note in git commit message
3. **Respect Boundaries**: Don't edit other codebases (read-only)
4. **Attribute**: Clear source documentation

### Commit Message Template

```
feat: Add dark mode design (borrowed from cyclecore.ai)

Copied CycleCore design system CSS files:
- cyclecore-tokens.css → slmbench-tokens.css
- cyclecore-base.css → slmbench-base.css
- cyclecore-components.css → slmbench-components.css

Source: /home/rain/LangManus/cyclecore-site/css/
Agent: CC-WEB (last updated 2025-11-18)
Authority: Constitutional Amendment 001 Section 5.2

Customizations:
- Updated branding (CycleCore → SLMBench)
- Retained pure black (#0a0a0a) background
- Kept cyan accent (#00d4ff)
```

---

## Domain Management (Porkbun)

**Registrar**: Porkbun
**Domains**:
- slmbench.com (ACQUIRED - ready for DNS setup)
- cyclecore.ai (hosted via CC-WEB)
- (others TBD)

**DNS Setup Required**:
- Point slmbench.com to hosting provider
- Configure SSL certificate
- Verify HTTPS access

**Action**: User needs to configure DNS in Porkbun dashboard.

---

## Next Steps

**Immediate** (Week 1):
1. ✅ Copy CycleCore CSS files to slmbench.com
2. Adapt design tokens for SLMBench branding
3. Build homepage using borrowed components
4. Test responsive design

**Future** (Post-MVP):
1. Locate Orchestra codebase → evaluate GPU management patterns
2. Locate ComplianceLogger → evaluate if UI patterns useful
3. Document any additional code borrowed from federation products

---

**Status**: REFERENCE COMPLETE
**Last Updated**: 2025-11-19
**Agent**: CC-SLM
