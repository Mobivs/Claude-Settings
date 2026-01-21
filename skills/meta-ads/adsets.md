# Meta Ads API - Ad Sets

> **Official Docs**: [Ad Set Reference](https://developers.facebook.com/docs/marketing-api/reference/ad-campaign) | [Optimization Goals](https://developers.facebook.com/docs/marketing-api/bidding/overview)

Complete reference for creating and managing ad sets (budgets, schedules, bidding, optimization).

## Ad Set Overview

Ad sets control:
- **WHO** sees your ads (targeting)
- **WHEN** ads run (schedule)
- **HOW MUCH** you spend (budget, unless CBO)
- **HOW** to optimize delivery (bidding, optimization goal)

## Create Ad Set

### Endpoint
```
POST /act_{ACCOUNT_ID}/adsets
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `campaign_id` | string | Parent campaign ID |
| `name` | string | Ad set name |
| `targeting` | object | Targeting specification (see [targeting.md](targeting.md)) |
| `optimization_goal` | enum | What to optimize for |
| `billing_event` | enum | When you're charged |
| `bid_strategy` | enum | How to bid |
| `status` | enum | ACTIVE or PAUSED |

### Budget Fields (Pick One)

| Field | Type | Description |
|-------|------|-------------|
| `daily_budget` | integer | Daily budget in cents |
| `lifetime_budget` | integer | Total budget in cents |

**Note**: If parent campaign uses CBO, omit budget fields from ad set.

### Schedule Fields

| Field | Type | Description |
|-------|------|-------------|
| `start_time` | datetime | Start time (ISO 8601) |
| `end_time` | datetime | End time (required for lifetime_budget) |

## Optimization Goals

Must be compatible with campaign objective:

### OUTCOME_AWARENESS
| Goal | Description |
|------|-------------|
| `REACH` | Maximum unique users |
| `IMPRESSIONS` | Maximum impressions |
| `AD_RECALL_LIFT` | Estimated ad recall lift |

### OUTCOME_TRAFFIC
| Goal | Description |
|------|-------------|
| `LINK_CLICKS` | Maximum link clicks |
| `LANDING_PAGE_VIEWS` | Maximum page loads |
| `REACH` | Maximum unique users |

### OUTCOME_ENGAGEMENT
| Goal | Description |
|------|-------------|
| `POST_ENGAGEMENT` | Likes, comments, shares |
| `VIDEO_VIEWS` | Maximum 3-second views |
| `THRUPLAY` | Maximum 15-second views |

### OUTCOME_LEADS
| Goal | Description |
|------|-------------|
| `LEAD_GENERATION` | Maximum form submissions |
| `QUALITY_LEAD` | Higher-quality leads |
| `CONVERSATIONS` | Messenger/WhatsApp leads |

### OUTCOME_APP_PROMOTION
| Goal | Description |
|------|-------------|
| `APP_INSTALLS` | Maximum app installs |
| `APP_EVENTS` | Maximum in-app actions |
| `VALUE` | Maximum app purchase value |

### OUTCOME_SALES
| Goal | Description |
|------|-------------|
| `OFFSITE_CONVERSIONS` | Maximum website conversions |
| `VALUE` | Maximum conversion value |
| `CONVERSATIONS` | Messenger/WhatsApp sales |

## Billing Events

| Event | Description | Common Pairings |
|-------|-------------|-----------------|
| `IMPRESSIONS` | Charged per 1,000 impressions | Most optimization goals |
| `LINK_CLICKS` | Charged per click | LINK_CLICKS goal only |
| `THRUPLAY` | Charged per 15-sec view | THRUPLAY goal only |

**Most common**: Use `IMPRESSIONS` for all modern campaigns.

## Bid Strategies

| Strategy | Description | Example |
|----------|-------------|---------|
| `LOWEST_COST_WITHOUT_CAP` | Auto-bid for lowest cost | Default, most common |
| `LOWEST_COST_WITH_BID_CAP` | Max bid per action | `bid_amount`: 500 ($5.00) |
| `COST_CAP` | Target average CPA | `bid_amount`: 1000 ($10.00 target CPA) |
| `LOWEST_COST_WITH_MIN_ROAS` | Minimum ROAS target | `roas_average_floor`: 200 (2.0x ROAS) |

## Basic Example

```json
POST /act_123456789/adsets

{
  "campaign_id": "23456789012345",
  "name": "US Women 25-45",
  "daily_budget": 5000,
  "billing_event": "IMPRESSIONS",
  "optimization_goal": "OFFSITE_CONVERSIONS",
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
  "targeting": {
    "geo_locations": {
      "countries": ["US"]
    },
    "genders": [2],
    "age_min": 25,
    "age_max": 45
  },
  "status": "PAUSED",
  "start_time": "2025-01-20T00:00:00-0500"
}
```

## Complete Example with All Options

```json
POST /act_123456789/adsets

{
  "campaign_id": "23456789012345",
  "name": "Detailed Ad Set Example",
  "daily_budget": 10000,
  "billing_event": "IMPRESSIONS",
  "optimization_goal": "OFFSITE_CONVERSIONS",
  "bid_strategy": "COST_CAP",
  "bid_amount": 1500,
  "targeting": {
    "geo_locations": {
      "countries": ["US"],
      "regions": [{"key": "3847"}],
      "cities": [{"key": "2420379", "radius": 25, "distance_unit": "mile"}]
    },
    "genders": [2],
    "age_min": 25,
    "age_max": 55,
    "interests": [
      {"id": "6003139266461", "name": "Yoga"}
    ],
    "behaviors": [
      {"id": "6002714895372", "name": "Engaged Shoppers"}
    ],
    "publisher_platforms": ["facebook", "instagram"],
    "facebook_positions": ["feed", "story"],
    "instagram_positions": ["stream", "story"]
  },
  "promoted_object": {
    "pixel_id": "987654321",
    "custom_event_type": "PURCHASE"
  },
  "attribution_spec": [
    {"event_type": "CLICK_THROUGH", "window_days": 7},
    {"event_type": "VIEW_THROUGH", "window_days": 1}
  ],
  "status": "PAUSED",
  "start_time": "2025-01-20T00:00:00-0500",
  "end_time": "2025-02-20T23:59:59-0500"
}
```

## Promoted Object

Defines conversion tracking for the ad set:

### Website Conversions
```json
{
  "promoted_object": {
    "pixel_id": "987654321",
    "custom_event_type": "PURCHASE"
  }
}
```

Custom event types:
- `PURCHASE`
- `ADD_TO_CART`
- `LEAD`
- `COMPLETE_REGISTRATION`
- `INITIATED_CHECKOUT`
- `ADD_PAYMENT_INFO`
- `VIEW_CONTENT`
- `SEARCH`
- `CONTACT`
- `SUBSCRIBE`
- `START_TRIAL`

### App Events
```json
{
  "promoted_object": {
    "application_id": "123456789",
    "object_store_url": "https://play.google.com/store/apps/..."
  }
}
```

### Page Likes/Engagement
```json
{
  "promoted_object": {
    "page_id": "123456789"
  }
}
```

## Placements

Control where ads appear:

### Automatic Placements (Recommended)
Omit placement fields to let Meta optimize.

### Manual Placements
```json
{
  "targeting": {
    "publisher_platforms": ["facebook", "instagram", "audience_network", "messenger"],
    "facebook_positions": ["feed", "story", "marketplace", "video_feeds", "right_hand_column"],
    "instagram_positions": ["stream", "story", "explore", "reels"],
    "device_platforms": ["mobile", "desktop"]
  }
}
```

## Read Ad Set

### Get Single Ad Set
```
GET /{ADSET_ID}?fields=id,name,daily_budget,targeting,optimization_goal,status,effective_status
```

### List Ad Sets in Campaign
```
GET /{CAMPAIGN_ID}/adsets?fields=id,name,status,daily_budget
```

### List All Ad Sets in Account
```
GET /act_{ACCOUNT_ID}/adsets?fields=id,name,campaign_id,status
```

### Filter by Status
```
GET /act_{ACCOUNT_ID}/adsets
  ?fields=id,name,status
  &filtering=[{"field":"effective_status","operator":"IN","value":["ACTIVE"]}]
```

## Update Ad Set

### Endpoint
```
POST /{ADSET_ID}
```

### Updatable Fields
- `name`
- `status`
- `daily_budget` / `lifetime_budget`
- `bid_amount`
- `bid_strategy`
- `targeting`
- `end_time`
- `optimization_goal` (limited changes)

### Example: Update Budget
```json
POST /34567890123456

{
  "daily_budget": 15000
}
```

### Example: Update Targeting
```json
POST /34567890123456

{
  "targeting": {
    "geo_locations": {
      "countries": ["US", "CA"]
    },
    "age_min": 25,
    "age_max": 55
  }
}
```

### Example: Pause Ad Set
```json
POST /34567890123456

{
  "status": "PAUSED"
}
```

## Delete Ad Set

### Soft Delete (Recommended)
```json
POST /{ADSET_ID}

{
  "status": "DELETED"
}
```

### Hard Delete
```
DELETE /{ADSET_ID}
```

## Attribution Settings

Control how conversions are attributed:

```json
{
  "attribution_spec": [
    {"event_type": "CLICK_THROUGH", "window_days": 7},
    {"event_type": "VIEW_THROUGH", "window_days": 1}
  ]
}
```

Options for `window_days`:
- Click-through: 1, 7
- View-through: 1 (0 to disable)

**Note**: Meta is removing some view-through windows in January 2026.

## Frequency Controls

Limit how often users see ads:

```json
{
  "frequency_control_specs": [
    {
      "event": "IMPRESSIONS",
      "interval_days": 7,
      "max_frequency": 3
    }
  ]
}
```

## Delivery Schedule

Show ads only during specific hours:

```json
{
  "pacing_type": ["day_parting"],
  "adset_schedule": [
    {
      "days": [0, 1, 2, 3, 4],
      "start_minute": 540,
      "end_minute": 1080,
      "timezone_type": "USER"
    }
  ]
}
```

- `days`: 0=Sunday through 6=Saturday
- `start_minute`/`end_minute`: Minutes from midnight (540 = 9:00 AM)
- `timezone_type`: `USER` (viewer's timezone) or `ADVERTISER`

## Ad Set Limits

| Limit | Value |
|-------|-------|
| Ad sets per campaign | 70 (150 for Advantage+) |
| Ads per ad set | 50 |
| Minimum daily budget | ~$1 USD (varies by country/optimization) |
| Name length | 400 characters |

## Error Handling

### Common Errors

| Code | Message | Solution |
|------|---------|----------|
| 100 | Invalid parameter | Check field types and values |
| 2615 | Cannot modify field | Field not updatable post-creation |
| 1487073 | Budget too low | Increase budget to minimum |
| 1815265 | Targeting invalid | Fix targeting specification |
| 1815115 | Missing promoted_object | Add pixel/app for conversion campaigns |

## SDK Examples

### Python
```python
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.targeting import Targeting

account = AdAccount('act_123456789')

targeting = {
    'geo_locations': {'countries': ['US']},
    'age_min': 25,
    'age_max': 45,
}

adset = account.create_ad_set(params={
    'name': 'US Adults 25-45',
    'campaign_id': '23456789012345',
    'daily_budget': 5000,
    'billing_event': AdSet.BillingEvent.impressions,
    'optimization_goal': AdSet.OptimizationGoal.offsite_conversions,
    'bid_strategy': AdSet.BidStrategy.lowest_cost_without_cap,
    'targeting': targeting,
    'status': AdSet.Status.paused,
    'promoted_object': {
        'pixel_id': '987654321',
        'custom_event_type': 'PURCHASE',
    },
})
```

### PHP
```php
use FacebookAds\Object\AdSet;
use FacebookAds\Object\AdAccount;
use FacebookAds\Object\Fields\AdSetFields;

$account = new AdAccount('act_123456789');

$adset = $account->createAdSet([], [
    AdSetFields::NAME => 'US Adults 25-45',
    AdSetFields::CAMPAIGN_ID => '23456789012345',
    AdSetFields::DAILY_BUDGET => 5000,
    AdSetFields::BILLING_EVENT => AdSet::BILLING_EVENT_IMPRESSIONS,
    AdSetFields::OPTIMIZATION_GOAL => AdSet::OPTIMIZATION_GOAL_OFFSITE_CONVERSIONS,
    AdSetFields::BID_STRATEGY => AdSet::BID_STRATEGY_LOWEST_COST_WITHOUT_CAP,
    AdSetFields::TARGETING => [
        'geo_locations' => ['countries' => ['US']],
        'age_min' => 25,
        'age_max' => 45,
    ],
    AdSetFields::STATUS => AdSet::STATUS_PAUSED,
    AdSetFields::PROMOTED_OBJECT => [
        'pixel_id' => '987654321',
        'custom_event_type' => 'PURCHASE',
    ],
]);
```
