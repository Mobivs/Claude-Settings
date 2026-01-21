---
name: vibe9-publish
description: Interact with the Vibe9 community site - publish articles, create AI guides, share lessons, create forum threads, and more. Use when the user wants to interact with Vibe9.net from their AI coding environment.
allowed-tools: Bash(curl:*), AskUserQuestion
version: 1.2.1
last_updated: 2025-01-13
---

# Vibe9 Community Skill

Interact with the Vibe9.net community directly from Claude Code - publish articles, share lessons learned, showcase projects, create forum threads, and engage with discussions without leaving your coding environment.

## When to Use This Skill

Use this skill when the user:
- Wants to "publish an article about X"
- Says "post this to Vibe9"
- Wants to "share a lesson I learned"
- Wants to "showcase my project"
- Wants to "create an AI guide" or "share a guide"
- Wants to "start a forum thread about X"
- Asks to "reply to a thread"
- Wants to "check the forum" or "see new articles"
- Says "update my article/lesson/project/guide"
- Wants to "upvote" or "downvote" content
- Wants to interact with the Vibe9 community

**Publishing Flow**: When creating content (articles, lessons, projects), ALWAYS:
1. Draft the content first
2. Show it to the user for review
3. Wait for user approval or edits
4. Only publish after explicit user confirmation

## Auto-Update Check (REQUIRED)

**IMPORTANT**: At the start of EVERY session using this skill, check for updates:

```bash
curl -s "https://vibe9.net/api/skill-version.php"
```

Compare the returned `version` with this file's version (1.2.1). If a newer version exists:

1. **Notify the user**: "A newer version of the Vibe9 skill is available (vX.X.X). Would you like me to update it?"
2. If they agree, run the appropriate update command:
   - **Global install**: `curl -o "$HOME/.claude/skills/vibe9-publish/SKILL.md" https://vibe9.net/skill/SKILL.md`
   - **Project install**: `curl -o "$(pwd)/.claude/skills/vibe9-publish/SKILL.md" https://vibe9.net/skill/SKILL.md`
3. After updating, re-read the skill file to use the latest instructions

This ensures you always have the latest API endpoints, features, and bug fixes.

## Prerequisites

The user needs a Vibe9 API token. Check for `$VIBE9_API_TOKEN` environment variable, or ask:

"To interact with Vibe9, I need your API token. Get one at https://vibe9.net/profile/api-token.php"

---

## API Reference

**Base URL**: `https://vibe9.net/api`

**Authentication**: Header `X-API-Token: your_token`

**Public endpoints** (no auth required): GET requests for reading content
**Protected endpoints** (auth required): POST, PUT, DELETE for writing

---

## Articles API

### List Articles (Public)
```bash
curl "https://vibe9.net/api/articles.php?page=1&limit=10"
```

Query params:
- `page` - Page number (default: 1)
- `limit` - Results per page (default: 10, max: 50)
- `sort` - newest, oldest, popular, updated

### List YOUR Articles (Auth Required)
```bash
curl "https://vibe9.net/api/articles.php?mine=1" \
  -H "X-API-Token: $VIBE9_API_TOKEN"
```

**Owners can always see ALL their own articles** regardless of status (draft, pending, approved, rejected).

Query params:
- `mine=1` - Required to list your articles
- `status` - Filter by: draft, pending, approved, rejected

### Get Single Article
```bash
# Public (approved articles only):
curl "https://vibe9.net/api/articles.php?id=1"

# With auth (owners can see their own regardless of status):
curl "https://vibe9.net/api/articles.php?id=1" \
  -H "X-API-Token: $VIBE9_API_TOKEN"
```

By slug:
```bash
curl "https://vibe9.net/api/articles.php?slug=my-article-title"
```

### Create Article (Auth Required)
```bash
curl -X POST "https://vibe9.net/api/articles.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{
    "title": "Article Title",
    "content": "Full markdown content...",
    "status": "pending"
  }'
```

Status options: `draft`, `pending`, `approved` (admin only)

### Update Article (Auth Required)
```bash
curl -X PUT "https://vibe9.net/api/articles.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{
    "id": 1,
    "title": "Updated Title",
    "content": "Updated content..."
  }'
```

**Owners can always update their own articles** regardless of approval status.

**Edit Request Flow**: When you edit an already-approved article, it automatically goes back to `pending` status for admin re-review. This ensures all published content is vetted.

Admins can also set `status` to approve/reject articles.

### Delete Article (Auth Required)
```bash
curl -X DELETE "https://vibe9.net/api/articles.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{"id": 1}'
```

---

## Learned API

Lessons are structured experiences - what worked, what didn't, and what you learned.
Content appears at `/learned/` on the website.

### List Lessons (Public)
```bash
curl "https://vibe9.net/api/lessons.php?page=1&limit=10"
```

Query params:
- `page` - Page number (default: 1)
- `limit` - Results per page (default: 10, max: 50)
- `sort` - newest, oldest, popular, updated
- `category` - Filter by category (PHP, CSS, DevOps, etc.)
- `difficulty` - Filter by: beginner, intermediate, advanced

### List YOUR Lessons (Auth Required)
```bash
curl "https://vibe9.net/api/lessons.php?mine=1" \
  -H "X-API-Token: $VIBE9_API_TOKEN"
```

Query params:
- `mine=1` - Required to list your lessons
- `status` - Filter by: draft, pending, approved, rejected

### Get Single Lesson
```bash
# By ID:
curl "https://vibe9.net/api/lessons.php?id=1"

# By slug:
curl "https://vibe9.net/api/lessons.php?slug=my-lesson-title"
```

### Create Lesson (Auth Required)
```bash
curl -X POST "https://vibe9.net/api/lessons.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{
    "title": "Lesson Title",
    "category": "PHP",
    "context": "What were you trying to do? (markdown)",
    "challenge": "What went wrong or was hard? (markdown)",
    "journey": "What you tried along the way (optional, markdown)",
    "solution": "What actually worked (markdown with code)",
    "takeaway": "The key lesson or insight (markdown)",
    "difficulty": "intermediate",
    "tags": "debugging, performance, api",
    "status": "pending"
  }'
```

**Required fields**: title, category, context, challenge, solution, takeaway
**Optional fields**: journey, difficulty, tags, status

**Difficulty options**: `beginner`, `intermediate`, `advanced`
**Status options**: `draft`, `pending`, `approved` (admin only)

### Update Lesson (Auth Required)
```bash
curl -X PUT "https://vibe9.net/api/lessons.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{
    "id": 1,
    "title": "Updated Title",
    "solution": "Updated solution..."
  }'
```

### Delete Lesson (Auth Required)
```bash
curl -X DELETE "https://vibe9.net/api/lessons.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{"id": 1}'
```

---

## Showcase API

Showcase what you're building - from early experiments to launched products.
Content appears at `/showcase/` on the website.

### List Projects (Public)
```bash
curl "https://vibe9.net/api/projects.php?page=1&limit=10"
```

Query params:
- `page` - Page number (default: 1)
- `limit` - Results per page (default: 10, max: 50)
- `sort` - newest, oldest, popular, updated
- `status` - Filter by project status: just_started, wip, launched, growing

### List YOUR Projects (Auth Required)
```bash
curl "https://vibe9.net/api/projects.php?mine=1" \
  -H "X-API-Token: $VIBE9_API_TOKEN"
```

Query params:
- `mine=1` - Required to list your projects
- `approval_status` - Filter by: draft, pending, approved, rejected

### Get Single Project
```bash
# By ID:
curl "https://vibe9.net/api/projects.php?id=1"

# By slug:
curl "https://vibe9.net/api/projects.php?slug=my-project-name"
```

### Create Project (Auth Required)
```bash
curl -X POST "https://vibe9.net/api/projects.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{
    "name": "Project Name",
    "tagline": "One-liner description of what it does",
    "description": "Full description - what it does, who it is for (markdown)",
    "tech_stack": "PHP, MySQL, Tailwind CSS, Docker",
    "project_url": "https://myproject.com",
    "repo_url": "https://github.com/user/repo",
    "status": "wip",
    "feedback_wanted": "What input are you seeking from the community? (markdown)",
    "tags": "saas, productivity, api",
    "approval_status": "pending"
  }'
```

**Required fields**: name, tagline, description, tech_stack
**Optional fields**: project_url, repo_url, status, feedback_wanted, tags, approval_status

**Project status options**: `just_started`, `wip`, `launched`, `growing`
**Approval status options**: `draft`, `pending`, `approved` (admin only)

### Update Project (Auth Required)
```bash
curl -X PUT "https://vibe9.net/api/projects.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{
    "id": 1,
    "name": "Updated Name",
    "status": "launched",
    "project_url": "https://myproject.com"
  }'
```

### Delete Project (Auth Required)
```bash
curl -X DELETE "https://vibe9.net/api/projects.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{"id": 1}'
```

---

## AI Guides API

AI Guides are context-driven documentation designed for AI assistants to execute - featuring kickoff prompts, machine-readable instructions, and verification steps.
Content appears at `/guides/` on the website.

### List Guides (Public)
```bash
curl "https://vibe9.net/api/guides.php?page=1&limit=10"
```

Query params:
- `page` - Page number (default: 1)
- `limit` - Results per page (default: 10, max: 50)
- `sort` - newest, oldest, popular, updated
- `category` - Filter by: coding, devops, writing, research, debugging, testing
- `target_tool` - Filter by: claude-code, cursor, windsurf, copilot, general
- `difficulty` - Filter by: beginner, intermediate, advanced

### List YOUR Guides (Auth Required)
```bash
curl "https://vibe9.net/api/guides.php?mine=1" \
  -H "X-API-Token: $VIBE9_API_TOKEN"
```

Query params:
- `mine=1` - Required to list your guides
- `status` - Filter by: draft, pending, approved, rejected

### Get Single Guide
```bash
# By ID:
curl "https://vibe9.net/api/guides.php?id=1"

# By slug:
curl "https://vibe9.net/api/guides.php?slug=my-guide-title"
```

### Create Guide (Auth Required)
```bash
curl -X POST "https://vibe9.net/api/guides.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{
    "title": "Guide Title",
    "tagline": "Short description",
    "description": "Full description (markdown)",
    "category": "coding",
    "target_tools": "claude-code,cursor,general",
    "difficulty": "beginner",
    "kickoff_prompt": "The prompt users copy-paste to their AI to start",
    "guide_content": "Machine-readable instructions (markdown)",
    "prerequisites": "What users need before starting (optional)",
    "verification_steps": "How to verify success (optional)",
    "resources": "Links to external docs (optional)",
    "tags": "nextjs, react, typescript",
    "status": "pending"
  }'
```

**Required fields**: title, category, kickoff_prompt, guide_content
**Optional fields**: tagline, description, target_tools, difficulty, prerequisites, verification_steps, resources, tags, status

**Category options**: `coding`, `devops`, `writing`, `research`, `debugging`, `testing`
**Target tool options**: `claude-code`, `cursor`, `windsurf`, `copilot`, `general` (comma-separated)
**Difficulty options**: `beginner`, `intermediate`, `advanced`
**Status options**: `draft`, `pending`, `approved` (admin only)

### Update Guide (Auth Required)
```bash
curl -X PUT "https://vibe9.net/api/guides.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{
    "id": 1,
    "title": "Updated Title",
    "guide_content": "Updated instructions..."
  }'
```

### Delete Guide (Auth Required)
```bash
curl -X DELETE "https://vibe9.net/api/guides.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{"id": 1}'
```

---

## Voting API

### Get Vote Counts (Public)
```bash
curl "https://vibe9.net/api/articles/vote.php?article_id=1"
```

Response includes `upvotes`, `downvotes`, `score`, and `user_vote` (if authenticated).

### Vote on Article (Auth Required)
```bash
# Upvote
curl -X POST "https://vibe9.net/api/articles/vote.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{"article_id": 1, "vote": "up"}'

# Downvote
curl -X POST "https://vibe9.net/api/articles/vote.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{"article_id": 1, "vote": "down"}'

# Remove vote
curl -X POST "https://vibe9.net/api/articles/vote.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{"article_id": 1, "vote": "none"}'
```

**Note**: You cannot vote on your own content. Content must be approved to receive votes.

All content responses include a `votes` object with `upvotes`, `downvotes`, and `score`.

---

## Forum API

### List Categories (Public)
```bash
curl "https://vibe9.net/api/forum/categories.php"
```

Returns all active forum categories with thread counts.

**Forum Categories:**
- General Discussion, Help & Support, Interesting Finds, Resources, Off Topic (user-initiated)
- Article Discussions, Learned Discussions, Showcase Discussions (auto-created from content)

### List Threads (Public)
```bash
curl "https://vibe9.net/api/forum/threads.php?category=general&page=1"
```

Query params:
- `category` - Filter by category slug
- `page`, `limit` - Pagination
- `sort` - latest, oldest, popular, active

### Get Thread with Posts (Public)
```bash
curl "https://vibe9.net/api/forum/threads.php?id=1"
# OR by slug:
curl "https://vibe9.net/api/forum/threads.php?slug=my-thread-title"
```

### Create Thread (Auth Required)
```bash
curl -X POST "https://vibe9.net/api/forum/threads.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{
    "category_id": 1,
    "title": "Thread Title",
    "content": "First post content..."
  }'
```

### Reply to Thread (Auth Required)
```bash
curl -X POST "https://vibe9.net/api/forum/posts.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $VIBE9_API_TOKEN" \
  -d '{
    "thread_id": 1,
    "content": "My reply...",
    "parent_id": null
  }'
```

Use `parent_id` to reply to a specific post (nested replies).

---

## Content Formatting

Use markdown in content fields:
- `## Heading` for section headings
- `**bold**` for emphasis
- `` `code` `` for inline code
- ` ```language ` for code blocks
- `- item` for bullet lists
- `1. item` for numbered lists

---

## Common Workflows

**IMPORTANT: Always show content to the user for review before publishing!**

The user must approve all content before it goes live. Never post directly without user confirmation.

### Publish an Article
1. Draft the article content in markdown
2. **Show the complete draft to the user** - display the full title and content
3. **Ask for approval**: "Does this look good? Would you like to make any changes before publishing?"
4. If user wants changes, make edits and show again
5. Only after user confirms → POST to `/api/articles.php`
6. Report the URL to user

### Share Something You Learned
1. Gather/draft the lesson details:
   - **Title**: Descriptive title
   - **Category**: PHP, CSS, DevOps, JavaScript, etc.
   - **Context**: What were you trying to do?
   - **Challenge**: What went wrong or was hard?
   - **Journey** (optional): What you tried along the way
   - **Solution**: What actually worked (with code)
   - **Takeaway**: The key insight
2. **Show the complete draft to the user** - display all sections formatted nicely
3. **Ask for approval**: "Does this lesson capture what you learned? Any changes before publishing?"
4. If user wants changes, make edits and show again
5. Only after user confirms → POST to `/api/lessons.php`
6. Report the URL to user (content appears at `/learned/view.php?slug=...`)

### Showcase a Project
1. Gather/draft the project details:
   - **Name**: Project name
   - **Tagline**: One-liner description
   - **Description**: What it does, who it's for
   - **Tech Stack**: Technologies used
   - **Status**: just_started, wip, launched, growing
   - **URLs** (optional): Project URL, repo URL
   - **Feedback Wanted** (optional): What input are you seeking?
2. **Show the complete draft to the user** - display all project details
3. **Ask for approval**: "Does this showcase your project well? Any changes before publishing?"
4. If user wants changes, make edits and show again
5. Only after user confirms → POST to `/api/projects.php`
6. Report the URL to user (content appears at `/showcase/view.php?slug=...`)

### Create an AI Guide
AI Guides are context-driven documentation for AI assistants - they help other developers automate tasks.

1. Gather/draft the guide details:
   - **Title**: Descriptive title for the guide
   - **Tagline**: One-liner description
   - **Category**: coding, devops, writing, research, debugging, testing
   - **Target Tools**: Which AI tools this works with
   - **Difficulty**: beginner, intermediate, advanced
   - **Kickoff Prompt**: The prompt users copy-paste to start (CRITICAL - make it clear and actionable)
   - **Guide Content**: Step-by-step machine-readable instructions
   - **Prerequisites** (optional): What users need before starting
   - **Verification Steps** (optional): How to confirm success
2. **Show the complete draft to the user** - especially the kickoff prompt
3. **Ask for approval**: "Does this guide look ready? Test the kickoff prompt - would it trigger the right workflow?"
4. If user wants changes, make edits and show again
5. Only after user confirms → POST to `/api/guides.php`
6. Report the URL to user (content appears at `/guides/view.php?slug=...`)

### Check Your Content (Any Status)
1. GET `/api/articles.php?mine=1` (or lessons.php, projects.php)
2. See all your content: drafts, pending, approved, rejected
3. Filter by status if needed

### Start a Discussion
1. GET `/api/forum/categories.php` to find the right category
2. POST to `/api/forum/threads.php` with category_id, title, content
3. Report the thread URL to user

### Reply to Discussion
1. GET thread with `/api/forum/threads.php?slug=xxx`
2. POST reply to `/api/forum/posts.php`
3. Confirm reply was posted

---

## Response Format

All endpoints return JSON:

Success:
```json
{
  "success": true,
  "message": "Action completed",
  "article": { ... }  // or "lesson", "project", "thread", "post", etc.
}
```

Error:
```json
{
  "error": "Error message"
}
```

---

## Rate Limits

- Articles: 5 per hour
- Lessons: 5 per hour
- Projects: 5 per hour
- Guides: 5 per hour
- Threads: 10 per hour
- Posts: 20 per hour

Admins have no rate limits.

---

## Version & Updates

**Current Version**: 1.2.1 (January 13, 2025)

### Check for Updates
```bash
curl -s "https://vibe9.net/api/skill-version.php" | head -1
```

Compare the version returned with the version in your installed skill file's YAML frontmatter.

### Update Instructions

**Claude Code (Project-Level)**:
```bash
# Re-download the skill file
curl -o .claude/skills/vibe9-publish/SKILL.md https://vibe9.net/skill/SKILL.md
```

**Claude Code (Global)**:
```bash
curl -o ~/.claude/skills/vibe9-publish/SKILL.md https://vibe9.net/skill/SKILL.md
```

**Cursor**: Re-fetch and update your `.cursor/rules/vibe9.mdc` file with the latest content.

**Windsurf**: Re-fetch and update your `.windsurf/rules/vibe9.md` file with the latest content.

### Changelog

**v1.2.1** (2025-01-13)
- **Auto-update check**: Skill now automatically checks for updates at the start of each session
- Prompts user to update when newer version is available

**v1.2.0** (2025-01-13)
- **AI Guides API**: New content type for context-driven AI documentation
- Guides feature kickoff prompts, machine-readable instructions, verification steps
- Filter guides by category, target tool, and difficulty
- Full CRUD support for guides

**v1.1.0** (2025-01-11)
- **User review before publishing**: AI now shows drafts to user for approval before posting
- Explicit confirmation required for all content creation (articles, lessons, projects)
- Updated workflow documentation

**v1.0.0** (2025-01-10)
- Initial public release
- Articles, Lessons, Projects, Forum APIs
- Voting system
- Token authentication

---

## Resources

- **Posting Guidelines**: https://vibe9.net/docs/posting-guidelines.php - What to share and quality standards
- **Cheat Sheet**: https://vibe9.net/skill/cheatsheet.php - Quick reference for common commands
- **Setup Guide**: https://vibe9.net/skill/setup/ - Installation and configuration
- **Token Recovery**: https://vibe9.net/skill/setup/token-recovery/ - Lost your token?
- **Test Endpoint**: https://vibe9.net/api/test-token.php - Verify your token works
- **Community Forum**: https://vibe9.net/forum/category/skill-setup - Get help from the community
