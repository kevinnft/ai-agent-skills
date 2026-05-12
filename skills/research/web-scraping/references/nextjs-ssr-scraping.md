# Next.js SSR Site Scraping Example

## Case: MegaETH KPIs Page

**URL:** https://flux.megaeth.com/kpis  
**Framework:** Next.js with server-side rendering  
**Challenge:** Content rendered client-side, no API endpoint available

## Failed Approaches

### 1. Browser Tool (Playwright via Hermes)
```
Error: Chrome exited early without writing DevToolsActivePort
FATAL: No usable sandbox! Ubuntu 23.10+ AppArmor restrictions
```

**Root cause:** WSL2 Ubuntu 24.04 lacks unprivileged user namespaces for Chrome sandbox.

### 2. Python + Playwright
```
Error: externally-managed-environment
python3-venv package not installed
```

**Root cause:** Ubuntu 24.04 requires explicit `python3.12-venv` package.

## Working Solution: Node.js + Puppeteer

### Setup
```bash
cd /tmp && mkdir scraper && cd scraper
npm init -y
npm install puppeteer
```

### Script
```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']  // Critical for WSL2
  });
  
  const page = await browser.newPage();
  
  try {
    await page.goto('https://flux.megaeth.com/kpis', {
      waitUntil: 'networkidle2',
      timeout: 60000
    });
    
    // Wait for React hydration
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    // Extract all text
    const content = await page.evaluate(() => document.body.innerText);
    console.log(content);
    
    // Extract structured data
    const kpiData = await page.evaluate(() => {
      const percentages = Array.from(document.querySelectorAll('*'))
        .filter(el => el.innerText && el.innerText.includes('%'))
        .map(el => el.innerText.trim());
      
      return { percentages: [...new Set(percentages)] };
    });
    
    console.log(JSON.stringify(kpiData, null, 2));
    
  } finally {
    await browser.close();
  }
})();
```

### Key Learnings

1. **`--no-sandbox` is mandatory** in WSL2/containers — Chrome won't launch without it
2. **Wait after networkidle2** — React/Next.js needs time to hydrate
3. **Extract text first** — verify content is present before refining selectors
4. **Use `new Promise(setTimeout)` not `page.waitForTimeout`** — Puppeteer API changed

## Results

Successfully extracted:
- 13 KPIs with 0% completion
- 5.3B MEGA total rewards ($834.93M)
- All tranche milestones and requirements
- No date-based unlocks (all milestone-based)

## Takeaway

For Next.js/React sites in WSL2:
1. Skip browser tool if sandbox errors appear
2. Use Node.js + Puppeteer with `--no-sandbox`
3. Always wait 3-5 seconds post-load for hydration
4. Extract incrementally (text → structured data)
