# Categories Overview

Auto-generated catalog of every skill, grouped by category.
Run `python3 scripts/generate_catalog.py` to refresh after editing frontmatter.

**Totals:** 191 skills across 28 categories.

Legend: 🟦 aggregated · 🟩 original · 🟧 adapted · 🟥 unknown · 🇨🇳 zh

---

## `mattpocock/` — 28 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [caveman](https://github.com/mattpocock/skills) | Ultra-compressed communication mode. Cuts token usage ~75% by dropping filler, articles, and pleasantries while keeping full technical accu… | 🟦 |
| [design-an-interface](https://github.com/mattpocock/skills) | Generate multiple radically different interface designs for a module using parallel sub-agents. Use when user wants to design an API, explo… | 🟦 |
| [diagnose](https://github.com/mattpocock/skills) | Disciplined diagnosis loop for hard bugs and performance regressions. Reproduce → minimise → hypothesise → instrument → fix → regression-te… | 🟦 |
| [edit-article](https://github.com/mattpocock/skills) | Edit and improve articles by restructuring sections, improving clarity, and tightening prose. Use when user wants to edit, revise, or impro… | 🟦 |
| [git-guardrails-claude-code](https://github.com/mattpocock/skills) | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wa… | 🟦 |
| [grill-me](https://github.com/mattpocock/skills) | Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use… | 🟦 |
| [grill-with-docs](https://github.com/mattpocock/skills) | Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md… | 🟦 |
| [handoff](https://github.com/mattpocock/skills) | Compact the current conversation into a handoff document for another agent to pick up. | 🟦 |
| [improve-codebase-architecture](https://github.com/mattpocock/skills) | Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. Use when the user… | 🟦 |
| [migrate-to-shoehorn](https://github.com/mattpocock/skills) | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests… | 🟦 |
| [obsidian-vault](https://github.com/mattpocock/skills) | Search, create, and manage notes in the Obsidian vault with wikilinks and index notes. Use when user wants to find, create, or organize not… | 🟦 |
| [prototype](https://github.com/mattpocock/skills) | Build a throwaway prototype to flush out a design before committing to it. Routes between two branches — a runnable terminal app for state/… | 🟦 |
| [qa](https://github.com/mattpocock/skills) | Interactive QA session where user reports bugs or issues conversationally, and the agent files GitHub issues. Explores the codebase in the… | 🟦 |
| [request-refactor-plan](https://github.com/mattpocock/skills) | Create a detailed refactor plan with tiny commits via user interview, then file it as a GitHub issue. Use when user wants to plan a refacto… | 🟦 |
| [review](https://github.com/mattpocock/skills) | Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's do… | 🟦 |
| [scaffold-exercises](https://github.com/mattpocock/skills) | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold… | 🟦 |
| [setup-matt-pocock-skills](https://github.com/mattpocock/skills) | Sets up an `## Agent skills` block in AGENTS.md/CLAUDE.md and `docs/agents/` so the engineering skills know this repo's issue tracker (GitH… | 🟦 |
| [setup-pre-commit](https://github.com/mattpocock/skills) | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-com… | 🟦 |
| [tdd](https://github.com/mattpocock/skills) | Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refa… | 🟦 |
| [to-issues](https://github.com/mattpocock/skills) | Break a plan, spec, or PRD into independently-grabbable issues on the project issue tracker using tracer-bullet vertical slices. Use when u… | 🟦 |
| [to-prd](https://github.com/mattpocock/skills) | Turn the current conversation context into a PRD and publish it to the project issue tracker. Use when user wants to create a PRD from the… | 🟦 |
| [triage](https://github.com/mattpocock/skills) | Triage issues through a state machine driven by triage roles. Use when user wants to create an issue, triage issues, review incoming bugs o… | 🟦 |
| [ubiquitous-language](https://github.com/mattpocock/skills) | Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms. Saves t… | 🟦 |
| [write-a-skill](https://github.com/mattpocock/skills) | Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or buil… | 🟦 |
| [writing-beats](https://github.com/mattpocock/skills) | Shape an article as a journey of beats, choose-your-own-adventure style. The user picks a starting beat from the raw material, you write on… | 🟦 |
| [writing-fragments](https://github.com/mattpocock/skills) | Grilling session that mines the user for fragments — heterogeneous nuggets of writing (claims, vignettes, sharp sentences, half-thoughts) —… | 🟦 |
| [writing-shape](https://github.com/mattpocock/skills) | Take a markdown file of raw material and shape it into an article through a conversational session — drafting candidate openings, growing t… | 🟦 |
| [zoom-out](https://github.com/mattpocock/skills) | Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or nee… | 🟦 |

## `addyosmani/` — 22 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [addyosmani-tdd](https://github.com/addyosmani/agent-skills) | Drives development with tests. Use when implementing any logic, fixing any bug, or changing any behavior. Use when you need to prove that c… | 🟦 |
| [api-and-interface-design](https://github.com/addyosmani/agent-skills) | Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or Grap… | 🟦 |
| [browser-testing-with-devtools](https://github.com/addyosmani/agent-skills) | Tests in real browsers. Use when building or debugging anything that runs in a browser. Use when you need to inspect the DOM, capture conso… | 🟦 |
| [ci-cd-and-automation](https://github.com/addyosmani/agent-skills) | Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate quality gate… | 🟦 |
| [code-review-and-quality](https://github.com/addyosmani/agent-skills) | Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use… | 🟦 |
| [code-simplification](https://github.com/addyosmani/agent-skills) | Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to read, ma… | 🟦 |
| [context-engineering](https://github.com/addyosmani/agent-skills) | Optimizes agent context setup. Use when starting a new session, when agent output quality degrades, when switching between tasks, or when y… | 🟦 |
| [debugging-and-error-recovery](https://github.com/addyosmani/agent-skills) | Guides systematic root-cause debugging. Use when tests fail, builds break, behavior doesn't match expectations, or you encounter any unexpe… | 🟦 |
| [deprecation-and-migration](https://github.com/addyosmani/agent-skills) | Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementation to an… | 🟦 |
| [documentation-and-adrs](https://github.com/addyosmani/agent-skills) | Records decisions and documentation. Use when making architectural decisions, changing public APIs, shipping features, or when you need to… | 🟦 |
| [doubt-driven-development](https://github.com/addyosmani/agent-skills) | Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when correctness matters more than speed, w… | 🟦 |
| [frontend-ui-engineering](https://github.com/addyosmani/agent-skills) | Builds production-quality UIs. Use when building or modifying user-facing interfaces. Use when creating components, implementing layouts, m… | 🟦 |
| [git-workflow-and-versioning](https://github.com/addyosmani/agent-skills) | Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, or when you need t… | 🟦 |
| [idea-refine](https://github.com/addyosmani/agent-skills) | Refines ideas iteratively. Refine ideas through structured divergent and convergent thinking. Use "idea-refine" or "ideate" to trigger. | 🟦 |
| [incremental-implementation](https://github.com/addyosmani/agent-skills) | Delivers changes incrementally. Use when implementing any feature or change that touches more than one file. Use when you're about to write… | 🟦 |
| [performance-optimization](https://github.com/addyosmani/agent-skills) | Optimizes application performance. Use when performance requirements exist, when you suspect performance regressions, or when Core Web Vita… | 🟦 |
| [planning-and-task-breakdown](https://github.com/addyosmani/agent-skills) | Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a… | 🟦 |
| [security-and-hardening](https://github.com/addyosmani/agent-skills) | Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations. Use when buildi… | 🟦 |
| [shipping-and-launch](https://github.com/addyosmani/agent-skills) | Prepares production launches. Use when preparing to deploy to production. Use when you need a pre-launch checklist, when setting up monitor… | 🟦 |
| [source-driven-development](https://github.com/addyosmani/agent-skills) | Grounds every implementation decision in official documentation. Use when you want authoritative, source-cited code free from outdated patt… | 🟦 |
| [spec-driven-development](https://github.com/addyosmani/agent-skills) | Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when requ… | 🟦 |
| [using-agent-skills](https://github.com/addyosmani/agent-skills) | Discovers and invokes agent skills. Use when starting a session or when you need to discover which skill applies to the current task. This… | 🟦 |

## `creative/` — 22 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [architecture-diagram](https://cocoon-ai.com) | Dark-themed SVG architecture/cloud/infra diagrams as HTML. | 🟧 |
| [ascii-art](https://github.com/NousResearch/hermes-agent/tree/main/skills/creative/ascii-art) | ASCII art: pyfiglet, cowsay, boxes, image-to-ascii. | 🟦 |
| [ascii-video](https://github.com/NousResearch/hermes-agent/tree/main/skills/creative/ascii-video) | ASCII video: convert video/audio to colored ASCII MP4/GIF. | 🟦 |
| [baoyu-comic](https://github.com/JimLiu/baoyu-skills/tree/main/skills/creative/baoyu-comic) 🇨🇳 | Knowledge comics (知识漫画): educational, biography, tutorial. | 🟦 |
| [baoyu-infographic](https://github.com/JimLiu/baoyu-skills/tree/main/skills/creative/baoyu-infographic) 🇨🇳 | Infographics: 21 layouts x 21 styles (信息图, 可视化). | 🟦 |
| [claude-design](https://github.com/NousResearch/hermes-agent/tree/main/skills/creative/claude-design) | Design one-off HTML artifacts (landing, deck, prototype). | 🟦 |
| [comfyui](https://github.com/NousResearch/hermes-agent/tree/main/skills/creative/comfyui) | Generate images, video, and audio with ComfyUI — install, launch, manage nodes/models, run workflows with parameter injection. Uses the off… | 🟦 |
| [creative-ideation](https://github.com/NousResearch/hermes-agent/tree/main/skills/creative/creative-ideation) | Generate project ideas via creative constraints. | 🟦 |
| [design-md](https://github.com/kevinnft/ai-agent-skills) | Author/validate/export Google's DESIGN.md token spec files. | 🟩 |
| `drawio-headless` | Generate architecture diagrams with draw.io in headless/server environments (WSL2, VPS, Docker) | 🟥 |
| [excalidraw](https://github.com/kevinnft/ai-agent-skills) | Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). | 🟩 |
| [humanizer](https://github.com/blader/humanizer) | Humanize text: strip AI-isms and add real voice. | 🟧 |
| [manim-video](https://github.com/NousResearch/hermes-agent/tree/main/skills/creative/manim-video) | Manim CE animations: 3Blue1Brown math/algo videos. | 🟦 |
| [p5js](https://github.com/NousResearch/hermes-agent/tree/main/skills/creative/p5js) | p5.js sketches: gen art, shaders, interactive, 3D. | 🟦 |
| [pixel-art](https://github.com/NousResearch/hermes-agent/tree/main/skills/creative/pixel-art) | Pixel art w/ era palettes (NES, Game Boy, PICO-8). | 🟦 |
| [popular-web-designs](https://github.com/VoltAgent/awesome-design-md) | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. | 🟧 |
| [pretext](https://github.com/kevinnft/ai-agent-skills) | Use when building creative browser demos with @chenglou/pretext — DOM-free text layout for ASCII art, typographic flow around obstacles, te… | 🟩 |
| [sketch](https://github.com/gsd-build/get-shit-done) | Throwaway HTML mockups: 2-3 design variants to compare. | 🟧 |
| `social-media-slideshow-video` | PIL + ffmpeg slideshow videos: product reviews, promos, TikTok/Reels/Shorts. | 🟥 |
| [songwriting-and-ai-music](https://github.com/NousResearch/hermes-agent/tree/main/skills/creative/songwriting-and-ai-music) | Songwriting craft and Suno AI music prompts. | 🟦 |
| [touchdesigner-mcp](https://github.com/NousResearch/hermes-agent/tree/main/skills/creative/touchdesigner-mcp) | Control a running TouchDesigner instance via twozero MCP — create operators, set parameters, wire connections, execute Python, build real-t… | 🟦 |
| `visual-assets-generation` | Generate visual assets (ASCII art, diagrams, banners) for repos and documentation | 🟥 |

## `software-development/` — 16 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| `api-testing` | REST/GraphQL API testing with automated validation — test endpoints, validate responses, check status codes, and ensure API contracts | 🟥 |
| [contributing-to-ide-projects](https://github.com/kevinnft/ai-agent-skills) | Comprehensive workflow for contributing features to open-source IDE and coding tool projects | 🟩 |
| [debugging-hermes-tui-commands](https://github.com/kevinnft/ai-agent-skills) | Debug Hermes TUI slash commands: Python, gateway, Ink UI. | 🟩 |
| [dev-requesting-code-review](https://github.com/obra/superpowers) | Pre-commit review: security scan, quality gates, auto-fix. | 🟧 |
| [dev-subagent-driven-development](https://github.com/obra/superpowers) | Execute plans via delegate_task subagents (2-stage review). | 🟧 |
| [dev-systematic-debugging](https://github.com/obra/superpowers) | 4-phase root cause debugging: understand bugs before fixing. | 🟧 |
| [dev-tdd](https://github.com/obra/superpowers) | TDD: enforce RED-GREEN-REFACTOR, tests before code. | 🟧 |
| [dev-writing-plans](https://github.com/obra/superpowers) | Write implementation plans: bite-sized tasks, paths, code. | 🟧 |
| [ecosystem-tool-evaluation](https://github.com/kevinnft/ai-agent-skills) | Evaluate and install ecosystem tools (Hermes plugins, skills, integrations) — assess complexity vs. benefit before installation, show examp… | 🟩 |
| [hermes-agent-skill-authoring](https://github.com/kevinnft/ai-agent-skills) | Author in-repo SKILL.md: frontmatter, validator, structure. | 🟩 |
| [node-inspect-debugger](https://github.com/kevinnft/ai-agent-skills) | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. | 🟩 |
| [open-source-contribution](https://github.com/kevinnft/ai-agent-skills) | Comprehensive workflow for contributing to open-source projects with quality checks | 🟩 |
| [plan](https://github.com/kevinnft/ai-agent-skills) | Plan mode: write markdown plan to .hermes/plans/, no exec. | 🟩 |
| [python-debugpy](https://github.com/kevinnft/ai-agent-skills) | Debug Python: pdb REPL + debugpy remote (DAP). | 🟩 |
| [spike](https://github.com/gsd-build/get-shit-done) | Throwaway experiments to validate an idea before build. | 🟧 |
| [user-ryzen-preferences](https://github.com/kevinnft/ai-agent-skills) | User ryzen's workflow preferences, communication style, and anti-patterns to avoid | 🟩 |

## `mlops/` — 15 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [audiocraft](https://github.com/kevinnft/ai-agent-skills) | AudioCraft: MusicGen text-to-music, AudioGen text-to-sound. | 🟩 |
| [axolotl](https://github.com/kevinnft/ai-agent-skills) | Axolotl: YAML LLM fine-tuning (LoRA, DPO, GRPO). | 🟩 |
| `crypto-mining-setup` | Setup and optimize cryptocurrency mining operations — AI-powered mining (soul.md protocol), parallel agent deployment, accumulation strateg… | 🟥 |
| [dspy](https://github.com/kevinnft/ai-agent-skills) | DSPy: declarative LM programs, auto-optimize prompts, RAG. | 🟩 |
| [huggingface-hub](https://github.com/kevinnft/ai-agent-skills) | HuggingFace hf CLI: search/download/upload models, datasets. | 🟩 |
| [llama-cpp](https://github.com/kevinnft/ai-agent-skills) | llama.cpp local GGUF inference + HF Hub model discovery. | 🟩 |
| [lm-evaluation-harness](https://github.com/kevinnft/ai-agent-skills) | lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.). | 🟩 |
| [obliteratus](https://github.com/kevinnft/ai-agent-skills) | OBLITERATUS: abliterate LLM refusals (diff-in-means). | 🟩 |
| [outlines](https://github.com/kevinnft/ai-agent-skills) | Outlines: structured JSON/regex/Pydantic LLM generation. | 🟩 |
| [segment-anything](https://github.com/kevinnft/ai-agent-skills) | SAM: zero-shot image segmentation via points, boxes, masks. | 🟩 |
| [trl-fine-tuning](https://github.com/kevinnft/ai-agent-skills) | TRL: SFT, DPO, PPO, GRPO, reward modeling for LLM RLHF. | 🟩 |
| [unsloth](https://github.com/kevinnft/ai-agent-skills) | Unsloth: 2-5x faster LoRA/QLoRA fine-tuning, less VRAM. | 🟩 |
| [vllm](https://github.com/kevinnft/ai-agent-skills) | vLLM: high-throughput LLM serving, OpenAI API, quantization. | 🟩 |
| [weights-and-biases](https://github.com/kevinnft/ai-agent-skills) | W&B: log ML experiments, sweeps, model registry, dashboards. | 🟩 |
| [windows-local-ai-services](https://github.com/kevinnft/ai-agent-skills) | Run local AI services on Windows — port binding, firewall, WSL2 networking, and common pitfalls. | 🟩 |

## `superpowers/` — 14 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [brainstorming](https://github.com/obra/superpowers) | You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores… | 🟦 |
| [dispatching-parallel-agents](https://github.com/obra/superpowers) | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies | 🟦 |
| [executing-plans](https://github.com/obra/superpowers) | Use when you have a written implementation plan to execute in a separate session with review checkpoints | 🟦 |
| [finishing-a-development-branch](https://github.com/obra/superpowers) | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development wo… | 🟦 |
| [receiving-code-review](https://github.com/obra/superpowers) | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable… | 🟦 |
| [superpowers-requesting-code-review](https://github.com/obra/superpowers) | Use when completing tasks, implementing major features, or before merging to verify work meets requirements | 🟦 |
| [superpowers-subagent-driven-development](https://github.com/obra/superpowers) | Use when executing implementation plans with independent tasks in the current session | 🟦 |
| [superpowers-systematic-debugging](https://github.com/obra/superpowers) | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes | 🟦 |
| [superpowers-tdd](https://github.com/obra/superpowers) | Use when implementing any feature or bugfix, before writing implementation code | 🟦 |
| [superpowers-writing-plans](https://github.com/obra/superpowers) | Use when you have a spec or requirements for a multi-step task, before touching code | 🟦 |
| [using-git-worktrees](https://github.com/obra/superpowers) | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated w… | 🟦 |
| [using-superpowers](https://github.com/obra/superpowers) | Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including… | 🟦 |
| [verification-before-completion](https://github.com/obra/superpowers) | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and… | 🟦 |
| [writing-skills](https://github.com/obra/superpowers) | Use when creating new skills, editing existing skills, or verifying skills work before deployment | 🟦 |

## `research/` — 11 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [arxiv](https://github.com/kevinnft/ai-agent-skills) | Search arXiv papers by keyword, author, category, or ID. | 🟩 |
| [blogwatcher](https://github.com/Hyaxia/blogwatcher) | Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool. | 🟧 |
| `credential-pooling-analysis` | Analyze credential pooling operations and API reseller business models — economics, risks, detection patterns, and sustainability | 🟥 |
| `crypto-token-analysis` | Deep-dive framework for analyzing crypto tokens — market data, liquidity health, tokenomics, unlock schedules, and risk assessment. Combine… | 🟥 |
| [llm-wiki](https://github.com/kevinnft/ai-agent-skills) | Karpathy's LLM Wiki: build/query interlinked markdown KB. | 🟩 |
| `nft-analysis` | Analyze NFT projects for investment decisions — evaluate fundamentals, identify red flags, assess risk, and provide buy/hold/avoid recommen… | 🟥 |
| [polymarket](https://github.com/kevinnft/ai-agent-skills) | Query Polymarket: markets, prices, orderbooks, history. | 🟩 |
| [research-paper-writing](https://github.com/kevinnft/ai-agent-skills) | Write ML papers for NeurIPS/ICML/ICLR: design→submit. | 🟩 |
| `telegram-bot-security-analysis` | Reverse engineer and security-test Telegram bots — API analysis, callback interception, exploit discovery, and vulnerability documentation | 🟥 |
| `trending-repos-discovery` | Discover and analyze trending GitHub repositories from TrendShift and other sources — evaluate usefulness, extract learnings, and identify… | 🟥 |
| `web-scraping` | Extract data from websites, including JavaScript-rendered SPAs and dynamic content | 🟥 |

## `github/` — 10 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [codebase-inspection](https://github.com/kevinnft/ai-agent-skills) | Inspect codebases w/ pygount: LOC, languages, ratios. | 🟩 |
| [comprehensive-public-repo-setup](https://github.com/kevinnft/ai-agent-skills) | Create production-ready public repos with complete documentation, automated setup, bundled dependencies, and user-friendly installation. | 🟩 |
| [github-auth](https://github.com/kevinnft/ai-agent-skills) | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. | 🟩 |
| [github-code-review](https://github.com/kevinnft/ai-agent-skills) | Review PRs: diffs, inline comments via gh or REST. | 🟩 |
| [github-issues](https://github.com/kevinnft/ai-agent-skills) | Create, triage, label, assign GitHub issues via gh or REST. | 🟩 |
| [github-pr-workflow](https://github.com/kevinnft/ai-agent-skills) | GitHub PR lifecycle: branch, commit, open, CI, merge. | 🟩 |
| [github-repo-management](https://github.com/kevinnft/ai-agent-skills) | Clone/create/fork repos; manage remotes, releases. | 🟩 |
| [github-repo-visual-assets](https://github.com/kevinnft/ai-agent-skills) | Create professional visual assets for GitHub repositories — architecture diagrams, social cards, and README banners. | 🟩 |
| `public-repo-creation` | Create production-ready public GitHub repositories with comprehensive documentation, automated setup, and quality assurance | 🟥 |
| [repo-quality-maksimalisasi](https://github.com/kevinnft/ai-agent-skills) | Evaluate and maximize GitHub repo quality from 7/10 to 10/10 perfect | 🟩 |

## `devops/` — 9 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| `api-monitoring-bots` | Build monitoring bots that poll APIs and send notifications on state changes (new listings, price alerts, status updates) | 🟥 |
| `cloud-browser-automation` | Use cloud browser services (Browserbase) for Cloudflare bypass, JavaScript rendering, and stealth scraping when local tools fail | 🟥 |
| `docker-compose` | Multi-container Docker applications with docker-compose — define services, networks, volumes, and orchestrate local development environments | 🟥 |
| [kanban-orchestrator](https://github.com/NousResearch/hermes-agent/tree/main/skills/devops/kanban-orchestrator) | Decomposition playbook + specialist-roster conventions + anti-temptation rules for an orchestrator profile routing work through Kanban. The… | 🟦 |
| [kanban-worker](https://github.com/NousResearch/hermes-agent/tree/main/skills/devops/kanban-worker) | Pitfalls, examples, and edge cases for Hermes Kanban workers. The lifecycle itself is auto-injected into every worker's system prompt as KA… | 🟦 |
| `tinyfish-integration` | Integrate TinyFish web toolkit (search, fetch, browser automation) into Hermes Agent | 🟥 |
| `vps-cleanup` | Systematic VPS cleanup — analyze files, categorize by importance, safely delete temporary/old data to free disk space | 🟥 |
| `vps-security-hardening` | Audit and harden VPS security — fail2ban, SSH hardening, firewall setup | 🟥 |
| [webhook-subscriptions](https://github.com/NousResearch/hermes-agent/tree/main/skills/devops/webhook-subscriptions) | Webhook subscriptions: event-driven agent runs. | 🟦 |

## `productivity/` — 8 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [airtable](https://github.com/kevinnft/ai-agent-skills) | Airtable REST API via curl. Records CRUD, filters, upserts. | 🟩 |
| [google-workspace](https://github.com/kevinnft/ai-agent-skills) | Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python. | 🟩 |
| [linear](https://github.com/kevinnft/ai-agent-skills) | Linear: manage issues, projects, teams via GraphQL + curl. | 🟩 |
| [maps](https://github.com/NousResearch/hermes-agent/tree/main/skills/productivity/maps) | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. | 🟦 |
| [nano-pdf](https://github.com/kevinnft/ai-agent-skills) | Edit PDF text/typos/titles via nano-pdf CLI (NL prompts). | 🟩 |
| [notion](https://github.com/kevinnft/ai-agent-skills) | Notion API via curl: pages, databases, blocks, search. | 🟩 |
| [ocr-and-documents](https://github.com/kevinnft/ai-agent-skills) | Extract text from PDFs/scans (pymupdf, marker-pdf). | 🟩 |
| [powerpoint](https://github.com/NousResearch/hermes-agent/tree/main/skills/productivity/powerpoint) | Create, read, edit .pptx decks, slides, notes, templates. | 🟦 |

## `media/` — 5 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [gif-search](https://github.com/kevinnft/ai-agent-skills) | Search/download GIFs from Tenor via curl + jq. | 🟩 |
| [heartmula](https://github.com/NousResearch/hermes-agent/tree/main/skills/media/heartmula) | HeartMuLa: Suno-like song generation from lyrics + tags. | 🟦 |
| [songsee](https://github.com/kevinnft/ai-agent-skills) | Audio spectrograms/features (mel, chroma, MFCC) via CLI. | 🟩 |
| [spotify](https://github.com/kevinnft/ai-agent-skills) | Spotify: play, search, queue, manage playlists and devices. | 🟩 |
| [youtube-content](https://github.com/NousResearch/hermes-agent/tree/main/skills/media/youtube-content) | YouTube transcripts to summaries, threads, blogs. | 🟦 |

## `obsidian-skills/` — 5 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| `defuddle` | Extract clean markdown content from web pages using Defuddle CLI, removing clutter and navigation to save tokens. Use instead of WebFetch w… | 🟥 |
| `json-canvas` | Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. Use when working with .canvas files, creating visua… | 🟥 |
| `obsidian-bases` | Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries. Use when working with .base files, creating data… | 🟥 |
| `obsidian-cli` | Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, properties, and more. Also supports… | 🟥 |
| `obsidian-markdown` | Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax. Use when worki… | 🟥 |

## `apple/` — 4 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [apple-notes](https://github.com/kevinnft/ai-agent-skills) | Manage Apple Notes via memo CLI: create, search, edit. | 🟩 |
| [apple-reminders](https://github.com/kevinnft/ai-agent-skills) | Apple Reminders via remindctl: add, list, complete. | 🟩 |
| [findmy](https://github.com/kevinnft/ai-agent-skills) | Track Apple devices/AirTags via FindMy.app on macOS. | 🟩 |
| [imessage](https://github.com/kevinnft/ai-agent-skills) | Send and receive iMessages/SMS via the imsg CLI on macOS. | 🟩 |

## `autonomous-ai-agents/` — 4 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [claude-code](https://github.com/kevinnft/ai-agent-skills) | Delegate coding to Claude Code CLI (features, PRs). | 🟩 |
| [codex](https://github.com/kevinnft/ai-agent-skills) | Delegate coding to OpenAI Codex CLI (features, PRs). | 🟩 |
| [hermes-agent](https://github.com/kevinnft/ai-agent-skills) | Configure, extend, or contribute to Hermes Agent. | 🟩 |
| [opencode](https://github.com/kevinnft/ai-agent-skills) | Delegate coding to OpenCode CLI (features, PR review). | 🟩 |

## `gaming/` — 2 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [minecraft-modpack-server](https://github.com/NousResearch/hermes-agent/tree/main/skills/gaming/minecraft-modpack-server) | Host modded Minecraft servers (CurseForge, Modrinth). | 🟦 |
| [pokemon-player](https://github.com/NousResearch/hermes-agent/tree/main/skills/gaming/pokemon-player) | Play Pokemon via headless emulator + RAM reads. | 🟦 |

## `note-taking/` — 2 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [obsidian](https://github.com/NousResearch/hermes-agent/tree/main/skills/note-taking/obsidian) | Read, search, create, and edit notes in the Obsidian vault. | 🟦 |
| `obsidian-mobile-sync` | Setup Obsidian mobile sync via GitHub (free) or Obsidian Sync (paid). Includes GitHub CLI automation, MGit/Working Copy setup, and Mnemosyn… | 🟥 |

## `social-media/` — 2 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| `social-media-account-audit` | Audit social media accounts (TikTok, IG, etc.): scrape profiles, calculate engagement metrics, diagnose performance drops, interpret analyt… | 🟥 |
| [xurl](https://github.com/NousResearch/hermes-agent/tree/main/skills/social-media/xurl) | X/Twitter via xurl CLI: post, search, DM, media, v2 API. | 🟦 |

## `software-copyright/` — 2 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| `docx-toolkit` 🇨🇳 | Professional DOCX document creation, editing, and formatting using OpenXML SDK (.NET). Three pipelines: (A) create new documents from scrat… | 🟥 |
| `software-copyright` 🇨🇳 | Generate guided Chinese software copyright application materials from a real project. Use this skill when the user asks for 软件著作权, 软著申请资料… | 🟥 |

## `data-science/` — 1 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [jupyter-live-kernel](https://github.com/kevinnft/ai-agent-skills) | Iterative Python via live Jupyter kernel (hamelnb). | 🟩 |

## `dogfood/` — 1 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [dogfood](https://github.com/NousResearch/hermes-agent/tree/main/skills/dogfood) | Exploratory QA of web apps: find bugs, evidence, reports. | 🟦 |

## `domain/` — 1 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| `domain-intel` | Passive domain reconnaissance using Python stdlib. Use this skill for subdomain discovery, SSL certificate inspection, WHOIS lookups, DNS r… | 🟩 |

## `email/` — 1 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [himalaya](https://github.com/kevinnft/ai-agent-skills) | Himalaya CLI: IMAP/SMTP email from terminal. | 🟩 |

## `inference-sh/` — 1 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [inference-sh](https://inference.sh) | Run 150+ AI applications in the cloud via the inference.sh platform. Triggers on "generate image with FLUX", "create video", "use Veo/Seeda… | 🟩 |

## `mcp/` — 1 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [native-mcp](https://github.com/kevinnft/ai-agent-skills) | MCP client: connect servers, register tools (stdio/HTTP). | 🟩 |

## `patent-disclosure-skill/` — 1 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| `patent-disclosure-skill` | 通用中国专利挖掘发现与交底书生成全流程：扫描项目文档挖掘专利点、讨论融合、基于脱敏模版生成技术交底书、联网查新、生成后自检含逻辑闭环与公式参数一致性。| Patent mining, disclosure drafting, prior-art search, and cons… | 🟥 |

## `red-teaming/` — 1 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [godmode](https://github.com/kevinnft/ai-agent-skills) | Jailbreak LLMs: Parseltongue, GODMODE, ULTRAPLINIAN. | 🟩 |

## `smart-home/` — 1 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [openhue](https://github.com/kevinnft/ai-agent-skills) | Control Philips Hue lights, scenes, rooms via OpenHue CLI. | 🟩 |

## `yuanbao/` — 1 skill(s)

| Skill | Description | Origin |
|---|---|:--:|
| [yuanbao](https://github.com/NousResearch/hermes-agent/tree/main/skills/yuanbao) 🇨🇳 | Yuanbao (元宝) groups: @mention users, query info/members. | 🟦 |

---
_Last regenerated automatically. Edit `SKILL.md` frontmatter, then run `python3 scripts/generate_catalog.py`._
