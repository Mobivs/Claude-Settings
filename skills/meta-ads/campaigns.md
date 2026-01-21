# Meta Ads API - Campaigns

> **Official Docs**: [Campaign Reference](https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group) | [Campaign Objectives](https://developers.facebook.com/docs/marketing-api/campaign-structure/objectives)

Complete reference for creating, reading, updating, and managing campaigns.

## Campaign Objectives (2025)

Meta uses **outcome-based objectives**. Legacy objectives are deprecated.

### Current Valid Objectives

| Objective | Description | Optimization Goals |
|-----------|-------------|-------------------|
| `OUTCOME_AWARENESS` | Brand awareness, reach | REACH, AD_RECALL_LIFT, IMPRESSIONS |
| `OUTCOME_TRAFFIC` | Drive website/app visits | LINK_CLICKS, LANDING_PAGE_VIEWS |
| `OUTCOME_ENGAGEMENT` | Post engagement, video views | POST_ENGAGEMENT, VIDEO_VIEWS, THRUPLAY |
| `OUTCOME_LEADS` | Lead generation | LEAD_GENERATION, CONVERSATIONS |
| `OUTCOME_APP_PROMOTION` | App installs, engagement | APP_INSTALLS, APP_EVENTS |
| `OUTCOME_SALES` | Conversions, catalog sales | OFFSITE_CONVERSIONS, VALUE |

### Deprecated Objectives (Will Error)
- `BRAND_AWARENESS` → Use `OUTCOME_AWARENESS`
- `LINK_CLICKS` → Use `OUTCOME_TRAFFIC`
- `CONVERSIONS` → Use `OUTCOME_SALES`
- `APP_INSTALLS` → Use `OUTCOME_APP_PROMOTION`
- `LEAD_GENERATION` → Use `OUTCOME_LEADS`
- `VIDEO_VIEWS` → Use `OUTCOME_ENGAGEMENT`

## Create Campaign

### Endpoint
```
POST /act_{ACCOUNT_ID}/campaigns
```

### Required Fields
| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Campaign name |
| `objective` | enum | One of OUTCOME_* values |
| `special_ad_categories` | array | Required even if empty `[]` |

### Optional Fields
| Field | Type | Description |
|-------|------|-------------|
| `status` | enum | ACTIVE, PAUSED (default: PAUSED) |
| `buying_type` | enum | AUCTION (default), RESERVED |
| `daily_budget` | integer | Daily budget in cents (for CBO) |
| `lifetime_budget` | integer | Lifetime budget in cents (for CBO) |
| `bid_strategy` | enum | Bid strategy (for CBO) |
| `spend_cap` | integer | Maximum campaign spend in cents |
| `start_time` | datetime | Campaign start (ISO 8601) |
| `stop_time` | datetime | Campaign end (ISO 8601) |

### Special Ad Categories

Required for certain ad types:
```json
{
  "special_ad_categories": ["HOUSING"]
}
```

Values:
- `HOUSING` - Real estate ads
- `EMPLOYMENT` - Job ads
- `CREDIT` - Financial/credit ads
- `ISSUES_ELECTIONS_POLITICS` - Political ads
- `[]` - None (still required)

### Basic Example
```json
POST /act_123456789/campaigns

{
  "name": "Summer Sale 2025",
  "objective": "OUTCOME_SALES",
  "status": "PAUSED",
  "special_ad_categories": []
}
```

Response:
```json
{
  "id": "23456789012345"
}
```

### Campaign with CBO
```json
POST /act_123456789/campaigns

{
  "name": "CBO Campaign",
  "objective": "OUTCOME_SALES",
  "status": "PAUSED",
  "special_ad_categories": [],
  "daily_budget": 10000,
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP"
}
```

## Bid Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| `LOWEST_COST_WITHOUT_CAP` | Maximize results within budget | General use, let Meta optimize |
| `LOWEST_COST_WITH_BID_CAP` | Cap max bid per action | Control costs when CPAs vary |
| `COST_CAP` | Target average cost per action | Stable CPA goal |
| `LOWEST_COST_WITH_MIN_ROAS` | Minimum return on ad spend | E-commerce with ROAS target |

## Read Campaign

### Get Single Campaign
```
GET /{CAMPAIGN_ID}?fields=id,name,objective,status,daily_budget,created_time
```

### List All Campaigns
```
GET /act_{ACCOUNT_ID}/campaigns?fields=id,name,objective,status,effective_status
```

### Filter by Status
```
GET /act_{ACCOUNT_ID}/campaigns
  ?fields=id,name,status
  &filtering=[{"field":"effective_status","operator":"IN","value":["ACTIVE","PAUSED"]}]
```

### Common Fields to Request
```
id,name,objective,status,effective_status,
daily_budget,lifetime_budget,budget_remaining,
spend_cap,buying_type,bid_strategy,
start_time,stop_time,created_time,updated_time
```

## Update Campaign

### Endpoint
```
POST /{CAMPAIGN_ID}
```

### Updatable Fields
- `name`
- `status`
- `daily_budget` (if CBO)
- `lifetime_budget` (if CBO)
- `spend_cap`
- `bid_strategy`
- `stop_time`

### Example: Pause Campaign
```json
POST /23456789012345

{
  "status": "PAUSED"
}
```

### Example: Update Budget
```json
POST /23456789012345

{
  "daily_budget": 20000
}
```

### Cannot Update
- `objective` - Create new campaign instead
- `buying_type` - Create new campaign instead
- `special_ad_categories` - Create new campaign instead

## Delete Campaign

### Soft Delete (Recommended)
```json
POST /{CAMPAIGN_ID}

{
  "status": "DELETED"
}
```

Campaign is archived but recoverable for 90 days.

### Hard Delete
```
DELETE /{CAMPAIGN_ID}
```

Permanently removes campaign. **Irreversible**.

## Campaign Insights

Get performance data:
```
GET /{CAMPAIGN_ID}/insights
  ?fields=impressions,reach,clicks,spend,cpm,cpc
  &date_preset=last_7d
```

See [insights.md](insights.md) for full details.

## Advantage+ Campaigns (2025)

### Unified Structure

Meta's new unified system automatically enables Advantage+ features based on settings:

```json
POST /act_123456789/campaigns

{
  "name": "Advantage+ Campaign",
  "objective": "OUTCOME_SALES",
  "status": "PAUSED",
  "special_ad_categories": [],
  "smart_promotion_type": "GUIDED_CREATION"
}
```

### Advantage+ Shopping Campaigns
```json
{
  "name": "ASC Campaign",
  "objective": "OUTCOME_SALES",
  "buying_type": "AUCTION",
  "smart_promotion_type": "GUIDED_CREATION",
  "special_ad_categories": []
}
```

### Migration Note
Legacy ASC/AAC APIs will be deprecated in API v25.0 (Q1 2026). Start using the unified structure now.

## Campaign Limits

| Limit | Value |
|-------|-------|
| Campaigns per ad account | 5,000 active |
| Ad sets per campaign | 70 (Advantage+ allows up to 150) |
| Characters in name | 400 max |
| Minimum daily budget | Varies by country (~$1 USD) |

## Error Handling

### Common Errors

| Code | Message | Solution |
|------|---------|----------|
| 100 | Invalid parameter | Check objective spelling, field types |
| 1487930 | Invalid objective | Use OUTCOME_* format, not legacy |
| 2615 | Cannot modify field | Field not updatable, create new |
| 1815320 | Special ad category required | Add appropriate category |

### Validation Before Create
```
POST /act_{ACCOUNT_ID}/campaigns?validate_only=true

{
  "name": "Test Campaign",
  "objective": "OUTCOME_SALES",
  "special_ad_categories": []
}
```

Returns validation errors without creating campaign.

## Batch Operations

### Create Multiple Campaigns
```json
POST /

{
  "batch": [
    {
      "method": "POST",
      "relative_url": "act_123456789/campaigns",
      "body": "name=Campaign1&objective=OUTCOME_SALES&status=PAUSED&special_ad_categories=[]"
    },
    {
      "method": "POST",
      "relative_url": "act_123456789/campaigns",
      "body": "name=Campaign2&objective=OUTCOME_TRAFFIC&status=PAUSED&special_ad_categories=[]"
    }
  ]
}
```

### Update Multiple Campaigns
```json
POST /

{
  "batch": [
    {
      "method": "POST",
      "relative_url": "23456789012345",
      "body": "status=ACTIVE"
    },
    {
      "method": "POST",
      "relative_url": "34567890123456",
      "body": "status=ACTIVE"
    }
  ]
}
```

## SDK Examples

### Python
```python
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adaccount import AdAccount

account = AdAccount('act_123456789')

campaign = account.create_campaign(params={
    'name': 'Summer Sale 2025',
    'objective': Campaign.Objective.outcome_sales,
    'status': Campaign.Status.paused,
    'special_ad_categories': [],
})

print(campaign.get_id())
```

### PHP
```php
use FacebookAds\Object\Campaign;
use FacebookAds\Object\AdAccount;
use FacebookAds\Object\Fields\CampaignFields;

$account = new AdAccount('act_123456789');

$campaign = $account->createCampaign([], [
    CampaignFields::NAME => 'Summer Sale 2025',
    CampaignFields::OBJECTIVE => Campaign::OBJECTIVE_OUTCOME_SALES,
    CampaignFields::STATUS => Campaign::STATUS_PAUSED,
    CampaignFields::SPECIAL_AD_CATEGORIES => [],
]);

echo $campaign->id;
```

### Node.js
```javascript
const AdAccount = require('facebook-nodejs-business-sdk').AdAccount;
const Campaign = require('facebook-nodejs-business-sdk').Campaign;

const account = new AdAccount('act_123456789');

account.createCampaign([], {
  name: 'Summer Sale 2025',
  objective: 'OUTCOME_SALES',
  status: 'PAUSED',
  special_ad_categories: [],
}).then(campaign => {
  console.log(campaign.id);
});
```
