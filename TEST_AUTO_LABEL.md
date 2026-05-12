# Test Auto-Label Bot

This is a test file to demonstrate the Auto-Label Bot functionality.

## What This Tests

- Documentation label (because it's a .md file)
- Size label (based on lines changed)
- Enhancement label (because "Add" in PR title)

## Expected Labels

When this PR is created, the bot should automatically apply:
- `documentation`
- `enhancement`
- `size/XS`

## How It Works

The Auto-Label Bot analyzes:
1. File extensions (.md → documentation)
2. PR title keywords ("Add" → enhancement)
3. Lines changed (<10 → size/XS)

And applies labels automatically within 2 seconds!
