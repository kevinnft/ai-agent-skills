#!/bin/bash

# Create GitHub Labels for ai-agent-skills
# This script creates all labels used by the auto-label bot

set -e

REPO="kevinnft/ai-agent-skills"
TOKEN="${GITHUB_TOKEN:-$(gh auth token)}"

echo "🏷️  Creating labels for $REPO..."
echo ""

# Function to create label
create_label() {
    local name="$1"
    local color="$2"
    local description="$3"
    
    echo "Creating label: $name"
    
    curl -s -X POST \
        -H "Authorization: token $TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/$REPO/labels" \
        -d "{\"name\":\"$name\",\"color\":\"$color\",\"description\":\"$description\"}" \
        > /dev/null 2>&1 || echo "  (already exists or error)"
}

# Type labels
echo "📋 Type labels..."
create_label "bug" "d73a4a" "Something isn't working"
create_label "enhancement" "a2eeef" "New feature or request"
create_label "maintenance" "fbca04" "Maintenance and updates"
create_label "cleanup" "fef2c0" "Code cleanup and refactoring"
create_label "refactor" "1d76db" "Code refactoring"
create_label "security" "ee0701" "Security related"
create_label "performance" "0e8a16" "Performance improvements"
create_label "tests" "bfd4f2" "Testing related"
create_label "question" "d876e3" "Further information is requested"

# Component labels
echo ""
echo "🔧 Component labels..."
create_label "documentation" "0075ca" "Documentation improvements"
create_label "skills" "7057ff" "Related to skills"
create_label "scripts" "c5def5" "Related to scripts"
create_label "github-actions" "000000" "GitHub Actions workflows"
create_label "config" "ededed" "Configuration files"

# Language labels
echo ""
echo "💻 Language labels..."
create_label "python" "3572A5" "Python code"
create_label "javascript" "f1e05a" "JavaScript/TypeScript code"
create_label "bash" "89e051" "Bash/Shell scripts"

# Category labels
echo ""
echo "📁 Category labels..."
create_label "research" "0052cc" "Research category"
create_label "devops" "1d76db" "DevOps category"
create_label "creative" "e99695" "Creative category"
create_label "development" "5319e7" "Development category"
create_label "mlops" "d4c5f9" "MLOps category"
create_label "github" "000000" "GitHub category"
create_label "productivity" "c2e0c6" "Productivity category"
create_label "ai-agents" "0e8a16" "AI Agents category"

# Special labels
echo ""
echo "⭐ Special labels..."
create_label "new-skill" "0e8a16" "New skill addition"
create_label "installation" "fbca04" "Installation related"
create_label "validation" "bfd4f2" "Validation related"
create_label "help-wanted" "008672" "Extra attention is needed"
create_label "good-first-issue" "7057ff" "Good for newcomers"
create_label "priority: high" "d93f0b" "High priority"

# Size labels
echo ""
echo "📏 Size labels..."
create_label "size/XS" "c2e0c6" "Extra small changes (<10 lines)"
create_label "size/S" "bfd4f2" "Small changes (10-50 lines)"
create_label "size/M" "fbca04" "Medium changes (50-200 lines)"
create_label "size/L" "fef2c0" "Large changes (200-500 lines)"
create_label "size/XL" "d73a4a" "Extra large changes (>500 lines)"

echo ""
echo "✅ All labels created successfully!"
echo ""
echo "Total labels: 35"
