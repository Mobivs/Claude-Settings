---
name: meta-ads
description: Meta Marketing API reference for Facebook and Instagram advertising. Use when working with Meta ads, campaigns, ad sets, creatives, targeting, or reporting. Provides layered documentation to explore API concepts without loading everything at once.
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Bash(curl:*)
---

# Meta Ads API Skill

A comprehensive reference for the Meta Marketing API (formerly Facebook Marketing API). This skill provides layered documentation so you can explore specific areas without loading the entire API context.

## Quick Navigation

This skill contains multiple reference files. Read only the ones relevant to your current task:

| File | Use When | Official Docs |
|------|----------|---------------|
| [ui-navigation.md](ui-navigation.md) | **Lost in the UI?** Finding pixels, connecting conversions, where things live | [Ads Manager Guide](https://www.facebook.com/business/help/200000840044554) |
| [authentication.md](authentication.md) | Setting up access tokens, permissions, app configuration | [Access Tokens](https://developers.facebook.com/docs/marketing-api/overview/authorization) |
| [campaign-structure.md](campaign-structure.md) | Understanding hierarchy: Account > Campaign > AdSet > Ad | [API Structure](https://developers.facebook.com/docs/marketing-api/campaign-structure) |
| [campaigns.md](campaigns.md) | Creating, reading, updating campaigns and objectives | [Campaign API](https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group) |
| [adsets.md](adsets.md) | Budget, schedule, bidding, optimization goals | [Ad Set API](https://developers.facebook.com/docs/marketing-api/reference/ad-campaign) |
| [ads-creatives.md](ads-creatives.md) | Creating ads, uploading images/videos, ad creative specs | [Ad Creative API](https://developers.facebook.com/docs/marketing-api/reference/ad-creative) |
| [targeting.md](targeting.md) | Audiences, demographics, interests, behaviors, locations | [Targeting API](https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting-search) |
| [insights.md](insights.md) | Performance metrics, reporting, breakdowns, attribution | [Insights API](https://developers.facebook.com/docs/marketing-api/insights) |
| [troubleshooting.md](troubleshooting.md) | Error codes, rate limits, common issues | [Error Reference](https://developers.facebook.com/docs/marketing-api/error-reference) |

## When to Use This Skill

Use this skill when the user:
- Asks about Meta/Facebook/Instagram advertising API
- Needs to create or manage ad campaigns programmatically
- Wants to understand campaign structure or hierarchy
- Needs help with targeting options
- Wants to pull performance reports or insights
- Encounters Meta API errors
- Asks about authentication or access tokens

## API Basics

**Base URL**: `https://graph.facebook.com/v{VERSION}/`

**Current Version**: v22.0 (as of early 2025, updates quarterly)

**Authentication**: All requests require an access token passed as `?access_token=TOKEN` or in the Authorization header.

**Request Format**: REST API using GET, POST, DELETE methods with JSON responses.

## Object Hierarchy

```
Ad Account (act_XXXXX)
    └── Campaign (objective, budget at campaign level if CBO)
            └── Ad Set (targeting, budget, schedule, bidding)
                    └── Ad (creative reference)
                            └── Ad Creative (image/video, copy, links)
```

## Quick Start Checklist

1. **Setup** (see [authentication.md](authentication.md))
   - Create Meta Developer App
   - Add Marketing API product
   - Get access token with required permissions
   - Identify your Ad Account ID

2. **Create Campaign** (see [campaigns.md](campaigns.md))
   - Choose objective (OUTCOME_AWARENESS, OUTCOME_TRAFFIC, etc.)
   - Set buying type (usually AUCTION)
   - Enable Campaign Budget Optimization if desired

3. **Create Ad Set** (see [adsets.md](adsets.md))
   - Define targeting (see [targeting.md](targeting.md))
   - Set budget and schedule
   - Choose optimization goal and bid strategy

4. **Create Ad** (see [ads-creatives.md](ads-creatives.md))
   - Upload creative assets (images/videos)
   - Create ad creative with copy
   - Link creative to ad

5. **Monitor Performance** (see [insights.md](insights.md))
   - Query insights endpoint
   - Apply date ranges and breakdowns
   - Track key metrics

## Common Endpoints Quick Reference

| Action | Endpoint | Method |
|--------|----------|--------|
| List ad accounts | `/me/adaccounts` | GET |
| Get account details | `/act_{ACCOUNT_ID}` | GET |
| Create campaign | `/act_{ACCOUNT_ID}/campaigns` | POST |
| List campaigns | `/act_{ACCOUNT_ID}/campaigns` | GET |
| Create ad set | `/act_{ACCOUNT_ID}/adsets` | POST |
| Create ad | `/act_{ACCOUNT_ID}/ads` | POST |
| Upload image | `/act_{ACCOUNT_ID}/adimages` | POST |
| Get insights | `/{OBJECT_ID}/insights` | GET |

## Important 2025 Changes

**Unified Advantage+ Structure** (May 2025):
- Single campaign creation system replaces separate ASC/AAC workflows
- Three automation levers: budget, audience, placement

**Legacy API Deprecation** (Q1 2026):
- ASC and AAC APIs deprecated in Marketing API v25.0
- Migrate to new Advantage+ structure before then

**Attribution Changes** (January 2026):
- Some view-through attribution windows being removed
- Historical data retention limits imposed

## SDK Options

Meta provides official SDKs that handle auth, pagination, and error handling:
- **Python**: `facebook-business`
- **PHP**: `facebook-php-business-sdk`
- **Node.js**: `facebook-nodejs-business-sdk`
- **Ruby**: `facebook-ruby-business-sdk`

## Getting Help

**Official Resources**:
- Meta for Developers: https://developers.facebook.com/
- Marketing API Docs: https://developers.facebook.com/docs/marketing-api
- Graph API Explorer: https://developers.facebook.com/tools/explorer/

**Community Resources**:
- Stack Overflow: [facebook-marketing-api] tag
- Meta Developer Community: https://developers.facebook.com/community/

---

## How to Use This Skill

1. **Start here** for overview and navigation
2. **Read specific files** based on your task
3. **Don't load everything** - only read what you need
4. **Check troubleshooting.md** when you hit errors

Example workflow:
```
User: "Help me create a campaign targeting US women 25-45"

Assistant actions:
1. Read campaigns.md for campaign creation
2. Read targeting.md for demographic targeting
3. Read adsets.md for ad set configuration
```
