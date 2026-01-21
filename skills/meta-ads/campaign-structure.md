# Meta Ads API - Campaign Structure

> **Official Docs**: [Campaign Structure](https://developers.facebook.com/docs/marketing-api/campaign-structure) | [Ad Account](https://developers.facebook.com/docs/marketing-api/reference/ad-account)

Understanding the hierarchical structure of Meta advertising objects.

## The Object Hierarchy

```
Business Manager
    └── Ad Account (act_XXXXX)
            └── Campaign
                    └── Ad Set
                            └── Ad
                                    └── Ad Creative
```

## Object Relationships

### Business Manager
- Top-level container for business assets
- Can contain multiple ad accounts, Pages, pixels
- Manages user access and permissions
- Not directly used in most API calls

### Ad Account (`act_XXXXX`)
- Container for all advertising activity
- Has its own billing and spend limits
- One ad account can have many campaigns
- ID format: `act_` prefix + numeric ID

### Campaign
- Groups ad sets under a single objective
- Defines the advertising goal
- Can use Campaign Budget Optimization (CBO)
- One campaign can have many ad sets

### Ad Set
- Defines WHO sees ads (targeting)
- Defines WHEN ads run (schedule)
- Defines HOW MUCH to spend (budget if not CBO)
- Defines bidding and optimization
- One ad set can have many ads

### Ad
- The actual advertisement shown to users
- References an ad creative
- Can be active/paused independently
- One ad references one creative

### Ad Creative
- Visual and copy elements
- Images, videos, text, headlines, links
- Reusable across multiple ads
- Immutable once created (create new to change)

## Visual Example

```
Ad Account: act_123456789 (My Business)
│
├── Campaign: "Summer Sale 2025" (OUTCOME_SALES)
│   │
│   ├── Ad Set: "US Women 25-45"
│   │   │   Budget: $100/day
│   │   │   Targeting: US, Female, 25-45
│   │   │
│   │   ├── Ad: "Lifestyle Image v1"
│   │   │       Creative: cr_111 (lifestyle photo)
│   │   │
│   │   └── Ad: "Product Image v1"
│   │           Creative: cr_222 (product photo)
│   │
│   └── Ad Set: "US Men 25-45"
│       │   Budget: $75/day
│       │   Targeting: US, Male, 25-45
│       │
│       └── Ad: "Lifestyle Image v1"
│               Creative: cr_111 (same creative reused)
│
└── Campaign: "Brand Awareness" (OUTCOME_AWARENESS)
    │
    └── Ad Set: "Broad US"
            Budget: $50/day
            Targeting: US, 18-65+
```

## API Node Structure

Each object is a "node" in the Graph API:

| Object | Node ID Format | Example |
|--------|---------------|---------|
| Ad Account | `act_{ID}` | `act_123456789` |
| Campaign | `{ID}` | `23456789012345` |
| Ad Set | `{ID}` | `34567890123456` |
| Ad | `{ID}` | `45678901234567` |
| Ad Creative | `{ID}` | `56789012345678` |

## Edges (Connections Between Objects)

Edges connect parent to child objects:

```
GET /act_{ACCOUNT_ID}/campaigns     → List all campaigns in account
GET /{CAMPAIGN_ID}/adsets           → List all ad sets in campaign
GET /{ADSET_ID}/ads                 → List all ads in ad set
GET /{AD_ID}/adcreatives            → Get creative for an ad
```

## Fields (Object Properties)

Each object has readable/writable fields:

### Campaign Fields
- `id` - Unique identifier (read-only)
- `name` - Campaign name
- `objective` - Advertising objective
- `status` - ACTIVE, PAUSED, DELETED
- `buying_type` - AUCTION, RESERVED
- `daily_budget` / `lifetime_budget` (if CBO)
- `created_time` (read-only)

### Ad Set Fields
- `id` - Unique identifier (read-only)
- `campaign_id` - Parent campaign
- `name` - Ad set name
- `targeting` - Targeting specification
- `daily_budget` / `lifetime_budget`
- `start_time` / `end_time`
- `optimization_goal`
- `billing_event`
- `bid_amount` / `bid_strategy`
- `status` - ACTIVE, PAUSED, DELETED

### Ad Fields
- `id` - Unique identifier (read-only)
- `adset_id` - Parent ad set
- `name` - Ad name
- `creative` - Reference to ad creative
- `status` - ACTIVE, PAUSED, DELETED
- `tracking_specs` - Conversion tracking

### Ad Creative Fields
- `id` - Unique identifier (read-only)
- `name` - Creative name
- `object_story_spec` - Page post specification
- `image_hash` / `image_url`
- `video_id`
- `title` / `body` / `link_url`
- `call_to_action`

## Creating the Hierarchy

Objects must be created in order (parent before child):

### 1. Create Campaign
```
POST /act_{ACCOUNT_ID}/campaigns
{
  "name": "My Campaign",
  "objective": "OUTCOME_SALES",
  "status": "PAUSED",
  "special_ad_categories": []
}
```

### 2. Create Ad Set
```
POST /act_{ACCOUNT_ID}/adsets
{
  "campaign_id": "{CAMPAIGN_ID}",
  "name": "My Ad Set",
  "targeting": {...},
  "daily_budget": 10000,  // cents
  "billing_event": "IMPRESSIONS",
  "optimization_goal": "OFFSITE_CONVERSIONS",
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
  "status": "PAUSED"
}
```

### 3. Upload Image (for creative)
```
POST /act_{ACCOUNT_ID}/adimages
Content-Type: multipart/form-data

file: [image binary data]
```

Returns `image_hash` to use in creative.

### 4. Create Ad Creative
```
POST /act_{ACCOUNT_ID}/adcreatives
{
  "name": "My Creative",
  "object_story_spec": {
    "page_id": "{PAGE_ID}",
    "link_data": {
      "image_hash": "{IMAGE_HASH}",
      "link": "https://example.com",
      "message": "Check out our sale!",
      "call_to_action": {
        "type": "SHOP_NOW",
        "value": {"link": "https://example.com"}
      }
    }
  }
}
```

### 5. Create Ad
```
POST /act_{ACCOUNT_ID}/ads
{
  "adset_id": "{ADSET_ID}",
  "name": "My Ad",
  "creative": {"creative_id": "{CREATIVE_ID}"},
  "status": "PAUSED"
}
```

## Campaign Budget Optimization (CBO)

When CBO is enabled, budget is set at campaign level:

```
POST /act_{ACCOUNT_ID}/campaigns
{
  "name": "CBO Campaign",
  "objective": "OUTCOME_SALES",
  "status": "PAUSED",
  "special_ad_categories": [],
  "daily_budget": 50000,  // $500/day at campaign level
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP"
}
```

Ad sets under CBO campaigns:
- Do NOT set `daily_budget` or `lifetime_budget`
- CAN set `bid_amount` for bid caps
- Budget is distributed automatically across ad sets

## Status Inheritance

Child objects inherit parent status:

| Parent Status | Child Status | Delivery |
|--------------|--------------|----------|
| Campaign: ACTIVE | Ad Set: ACTIVE, Ad: ACTIVE | Delivering |
| Campaign: PAUSED | Ad Set: ACTIVE, Ad: ACTIVE | **Not delivering** |
| Campaign: ACTIVE | Ad Set: PAUSED, Ad: ACTIVE | **Not delivering** |
| Campaign: ACTIVE | Ad Set: ACTIVE, Ad: PAUSED | **Not delivering** |

**All three levels must be ACTIVE for ads to deliver.**

## Effective Status

The `effective_status` field shows actual delivery status considering parent states:

```
GET /{AD_ID}?fields=status,effective_status
```

Possible values:
- `ACTIVE` - Delivering
- `PAUSED` - Manually paused
- `DELETED` - Deleted
- `PENDING_REVIEW` - Under review
- `DISAPPROVED` - Policy violation
- `PREAPPROVED` - Approved but not started
- `PENDING_BILLING_INFO` - Needs payment method
- `CAMPAIGN_PAUSED` - Parent campaign paused
- `ADSET_PAUSED` - Parent ad set paused
- `IN_PROCESS` - Being processed
- `WITH_ISSUES` - Has warnings/errors

## Batch Operations

Create multiple objects in one request:

```
POST /
{
  "batch": [
    {
      "method": "POST",
      "relative_url": "act_123456789/campaigns",
      "body": "name=Campaign1&objective=OUTCOME_SALES&status=PAUSED"
    },
    {
      "method": "POST",
      "relative_url": "act_123456789/campaigns",
      "body": "name=Campaign2&objective=OUTCOME_TRAFFIC&status=PAUSED"
    }
  ]
}
```

## Reading the Hierarchy

### Get Full Structure
```
GET /act_{ACCOUNT_ID}/campaigns?fields=id,name,adsets{id,name,ads{id,name,creative{id,name}}}
```

This returns campaigns with nested ad sets, ads, and creatives.

### Pagination
Large results are paginated:
```json
{
  "data": [...],
  "paging": {
    "cursors": {
      "before": "xxx",
      "after": "yyy"
    },
    "next": "https://graph.facebook.com/v22.0/..."
  }
}
```

Use the `next` URL to get more results.
