# Analyzing Trending Repositories (TrendShift Pattern)

When user asks to analyze trending repos from TrendShift.io or similar platforms:

## Data Extraction

TrendShift uses client-side rendering with embedded JSON:
- Fetch HTML: `curl -s "https://trendshift.io/"`
- Extract JSON from `<script>` tags containing repo data
- Parse embedded data structure (usually in `self.__next_f.push()` calls)

## Analysis Framework

### 1. Categorization
Group repos by:
- **Type:** AI agent, tools, learning resources, libraries, frameworks
- **Domain:** DevOps, ML/AI, web dev, security, data science
- **Language:** Python, TypeScript, Rust, Go, etc.
- **Tags:** From repo metadata

### 2. Quality Indicators
Assess each repo:
- **Stars:** Popularity signal
- **Forks:** Community engagement
- **Score:** TrendShift engagement score (if available)
- **Social mentions:** Reddit, HackerNews validation
- **Recency:** Last updated, creation date
- **Activity:** Commit frequency, issue response

### 3. Trend Analysis
Identify patterns:
- **Dominant categories:** What's hot right now?
- **Language preferences:** Which languages trending?
- **Community signals:** Social mention correlation
- **Emerging patterns:** New paradigms, approaches

### 4. Practical Assessment
For each category, answer:
- **Bagus gak?** (Is it good?) — Star rating
- **Why it matters:** Practical value
- **Use cases:** When to use
- **Top picks:** Best repos in category

## Output Format

User prefers:
- **Bahasa Indonesia** (casual style)
- **Direct, no-BS** explanations
- **Practical focus:** "Gunanya apa?" not just "What is it?"
- **Clear recommendations:** Top 5 must-try
- **Visual aids:** Tables, comparisons
- **Actionable insights:** What to do next

## Deliverables

Generate:
1. **Main report** (Bahasa Indonesia, comprehensive)
2. **Quick summary** (TL;DR version)
3. **Data tables** (structured reference)
4. **Raw data** (JSON for further analysis)
5. **Categorized data** (organized by type)

## Pitfalls

- **Don't scrape rendered content:** TrendShift is client-side rendered, extract from embedded JSON
- **Don't just list repos:** Provide analysis, insights, recommendations
- **Don't use English:** User prefers Bahasa Indonesia (casual)
- **Don't be verbose:** Direct, practical, actionable
