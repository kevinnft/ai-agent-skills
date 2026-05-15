---
name: zoom-out
description: Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or need to understand how it fits into the bigger picture.
disable-model-invocation: true
source_repo: "mattpocock/skills"
source_url: "https://github.com/mattpocock/skills"
source_license: "MIT"
origin: aggregated
language: en
---

# Zoom Out

## Request

I don't know this area of code well. Go up a layer of abstraction. Give me a map of all the relevant modules and callers, using the project's domain glossary vocabulary.

## Output

- Start with a concise system map: major modules, responsibilities, and data flow.
- Identify the entry points, downstream callers, and external dependencies.
- Call out the key domain terms used by this area of the codebase.
- End with the next files or tests I should read to go deeper.
