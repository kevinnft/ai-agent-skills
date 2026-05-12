# Review Workflow Preferences

## User: ryzen

### File/Asset Review Pattern

**Preference:** Don't send actual files immediately for review

**Workflow:**
1. User asks to create/review files or visual assets
2. **DON'T:** Send files via MEDIA: or create and push immediately
3. **DO:** Create analysis document or issue list first
   - Save as `.txt` or `.md` file
   - List what will be created
   - List issues found (if bug analysis)
   - Show preview/structure
4. User reviews the list
5. User approves or requests changes
6. **THEN:** Create actual files or push to repo

**Key Phrases:**
- "jangan send file" = don't send files
- "buatkan list yg perlu diperbaiki" = make list of issues to fix
- "buatkan contohnya dulu dong dalam file txt" = make example first in txt file

**Example Session:**
```
User: "Kirim sini aja filenya"
Agent: [Creates VISUAL_ASSETS_PREVIEW.txt with ASCII art examples]
       [Does NOT send actual HTML files yet]

User: "Jngn send file hanya buatkan list yg perlu diperbaiki"
Agent: [Creates comprehensive bug analysis list]
       [Does NOT send files for review]
       [Waits for approval before fixing]
```

**Rationale:**
- User wants to review plan/analysis before execution
- Avoids wasting time on wrong approach
- Allows user to provide feedback early
- More efficient iteration cycle

**Apply to:**
- Visual assets (diagrams, images, banners)
- Bug analysis (list issues before fixing)
- Code review (analysis before changes)
- Documentation (outline before writing)
- Any deliverable that needs approval

**Exception:**
- Simple fixes user explicitly approved
- Urgent production issues
- User says "gas" or "lanjut" (proceed immediately)
