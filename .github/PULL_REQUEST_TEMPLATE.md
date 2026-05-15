# Pull Request

## What
Brief description of what this PR changes.

## Why
Why is this change useful? Link related issues with `Fixes #123` if applicable.

## Type of contribution

- [ ] Original skill (authored by me — `author:` field set)
- [ ] Aggregated skill (pulled from upstream — `source_repo:`, `source_url:`, `source_license:` set)
- [ ] Translation of an existing skill (`translation_of:` set)
- [ ] Tooling / CI / docs change (no skill content)
- [ ] Bug fix
- [ ] Other:

## Attribution checklist (for skill PRs)

- [ ] If derived from an upstream public repo, the upstream license **permits redistribution** (MIT, Apache-2.0, BSD, CC-BY, etc.)
- [ ] `source_url:` points to a real, reachable upstream URL
- [ ] `source_license:` matches the upstream license (SPDX identifier)
- [ ] If I substantively edited the upstream content, I used `derived_from:` instead of `source_url:` and explained the changes below
- [ ] I am **not misrepresenting** an upstream author as a contributor to this repo

## Verification

- [ ] Ran `./scripts/validate.sh` — passes
- [ ] CI passes
- [ ] No new same-name conflicts with existing skills (checked via `find skills -name SKILL.md | xargs grep -l "name: <my-name>"`)

## Original skill: how I tested it

(Skip for aggregated skills.) Describe one real session where this skill was used and what it produced. Be specific — do not write "tested it works".

## Notes for reviewer
