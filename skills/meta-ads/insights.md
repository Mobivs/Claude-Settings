# Meta Ads API - Insights and Reporting

> **Official Docs**: [Insights API](https://developers.facebook.com/docs/marketing-api/insights) | [Metrics Reference](https://developers.facebook.com/docs/marketing-api/insights/parameters/v22.0) | [Async Reports](https://developers.facebook.com/docs/marketing-api/insights/best-practices)

Complete reference for querying performance data, metrics, and reports.

## Insights Overview

The Insights API provides performance data for:
- Ad Accounts
- Campaigns
- Ad Sets
- Ads

## Basic Insights Query

### Endpoint
```
GET /{OBJECT_ID}/insights
```

### Simple Example
```
GET /23456789012345/insights?fields=impressions,reach,clicks,spend
```

Response:
```json
{
  "data": [
    {
      "impressions": "15234",
      "reach": "12450",
      "clicks": "523",
      "spend": "127.45",
      "date_start": "2025-01-01",
      "date_stop": "2025-01-15"
    }
  ]
}
```

## Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `fields` | string | Comma-separated metrics to retrieve |
| `date_preset` | enum | Predefined date range |
| `time_range` | object | Custom date range |
| `time_increment` | int/string | Granularity of data |
| `level` | enum | Object level for aggregation |
| `breakdowns` | array | Dimensions to break down by |
| `filtering` | array | Filter results |
| `sort` | array | Sort results |
| `limit` | int | Results per page |

## Date Ranges

### Date Presets
```
GET /{OBJECT_ID}/insights?date_preset=last_7d
```

| Preset | Description |
|--------|-------------|
| `today` | Current day |
| `yesterday` | Previous day |
| `this_month` | Current month |
| `last_month` | Previous month |
| `this_quarter` | Current quarter |
| `last_3d` | Last 3 days |
| `last_7d` | Last 7 days |
| `last_14d` | Last 14 days |
| `last_28d` | Last 28 days |
| `last_30d` | Last 30 days |
| `last_90d` | Last 90 days |
| `last_week_mon_sun` | Last full week |
| `last_week_sun_sat` | Last full week (Sun-Sat) |
| `last_year` | Last 365 days |
| `maximum` | All available data |

### Custom Date Range
```
GET /{OBJECT_ID}/insights?time_range={"since":"2025-01-01","until":"2025-01-31"}
```

## Time Increment

Break data into time periods:

```
GET /{OBJECT_ID}/insights?time_increment=1&date_preset=last_7d
```

| Value | Description |
|-------|-------------|
| `1` | Daily |
| `7` | Weekly |
| `monthly` | Monthly |
| `all_days` | One row for entire range |

## Core Metrics

### Delivery Metrics

| Metric | Description |
|--------|-------------|
| `impressions` | Number of times ads displayed |
| `reach` | Unique users who saw ads |
| `frequency` | Average impressions per user |

### Engagement Metrics

| Metric | Description |
|--------|-------------|
| `clicks` | All clicks on ad |
| `link_clicks` | Clicks on ad link |
| `ctr` | Click-through rate (%) |
| `post_engagement` | All post interactions |
| `page_engagement` | Page interactions from ad |

### Video Metrics

| Metric | Description |
|--------|-------------|
| `video_p25_watched_actions` | 25% video views |
| `video_p50_watched_actions` | 50% video views |
| `video_p75_watched_actions` | 75% video views |
| `video_p100_watched_actions` | 100% video views |
| `video_thruplay_watched_actions` | ThruPlay views (15+ sec) |
| `video_avg_time_watched_actions` | Average watch time |

### Cost Metrics

| Metric | Description |
|--------|-------------|
| `spend` | Total amount spent |
| `cpm` | Cost per 1,000 impressions |
| `cpc` | Cost per click |
| `cpp` | Cost per purchase |
| `cost_per_action_type` | Cost per action (array) |

### Conversion Metrics

| Metric | Description |
|--------|-------------|
| `actions` | All conversion actions (array) |
| `conversions` | Standard conversions |
| `conversion_values` | Conversion value totals |
| `purchase_roas` | Return on ad spend (array) |
| `website_purchase_roas` | Website ROAS (array) |

## Actions and Conversions

Actions are returned as arrays:

```
GET /{OBJECT_ID}/insights?fields=actions,action_values
```

Response:
```json
{
  "actions": [
    {"action_type": "link_click", "value": "523"},
    {"action_type": "landing_page_view", "value": "412"},
    {"action_type": "purchase", "value": "45"},
    {"action_type": "add_to_cart", "value": "89"}
  ],
  "action_values": [
    {"action_type": "purchase", "value": "2847.50"},
    {"action_type": "add_to_cart", "value": "3456.00"}
  ]
}
```

### Common Action Types

| Type | Description |
|------|-------------|
| `link_click` | Link clicks |
| `landing_page_view` | Landing page views |
| `purchase` | Purchases |
| `add_to_cart` | Add to cart |
| `initiate_checkout` | Checkout initiated |
| `add_payment_info` | Payment info added |
| `lead` | Lead submissions |
| `complete_registration` | Registrations |
| `view_content` | Content views |
| `search` | Searches |
| `contact` | Contact actions |
| `app_install` | App installs |

## Breakdowns

Split data by dimensions:

```
GET /{OBJECT_ID}/insights
  ?fields=impressions,clicks,spend
  &breakdowns=age,gender
  &date_preset=last_7d
```

### Available Breakdowns

| Breakdown | Description |
|-----------|-------------|
| `age` | Age ranges |
| `gender` | Male/Female |
| `country` | Countries |
| `region` | Regions/states |
| `dma` | Designated Market Areas |
| `publisher_platform` | Facebook, Instagram, etc. |
| `platform_position` | Feed, Stories, etc. |
| `device_platform` | Mobile, Desktop |
| `impression_device` | Device type |
| `product_id` | Catalog products |
| `frequency_value` | Frequency buckets |
| `hourly_stats_aggregated_by_advertiser_time_zone` | Hour of day |

### Breakdown Combinations

Some breakdowns can be combined:
```
breakdowns=age,gender
breakdowns=publisher_platform,platform_position
breakdowns=country,region
```

**Warning**: Breakdowns multiply rows exponentially and can hit rate limits.

## Level Parameter

Query at different object levels:

```
GET /act_{ACCOUNT_ID}/insights?level=campaign&fields=campaign_name,impressions
```

| Level | Description |
|-------|-------------|
| `account` | Account totals |
| `campaign` | Per-campaign data |
| `adset` | Per-ad set data |
| `ad` | Per-ad data |

## Filtering

Filter results by field values:

```
GET /act_{ACCOUNT_ID}/insights
  ?level=campaign
  &fields=campaign_name,impressions,spend
  &filtering=[{"field":"spend","operator":"GREATER_THAN","value":"100"}]
```

### Filter Operators

| Operator | Description |
|----------|-------------|
| `EQUAL` | Exact match |
| `NOT_EQUAL` | Not equal |
| `GREATER_THAN` | Greater than |
| `LESS_THAN` | Less than |
| `GREATER_THAN_OR_EQUAL` | >= |
| `LESS_THAN_OR_EQUAL` | <= |
| `IN` | In array |
| `NOT_IN` | Not in array |
| `CONTAIN` | Contains string |
| `NOT_CONTAIN` | Doesn't contain |

### Filter Examples

```json
// Active campaigns only
[{"field":"campaign.effective_status","operator":"IN","value":["ACTIVE"]}]

// Campaigns with spend
[{"field":"spend","operator":"GREATER_THAN","value":"0"}]

// Specific campaign IDs
[{"field":"campaign.id","operator":"IN","value":["123","456"]}]
```

## Sorting

Sort results:

```
GET /{OBJECT_ID}/insights
  ?fields=campaign_name,impressions,spend
  &sort=spend_descending
```

Format: `{field}_{direction}`
- Direction: `ascending` or `descending`

## Attribution Windows

Specify conversion attribution:

```
GET /{OBJECT_ID}/insights
  ?fields=actions
  &action_attribution_windows=["1d_click","7d_click","1d_view"]
```

| Window | Description |
|--------|-------------|
| `1d_click` | 1-day click |
| `7d_click` | 7-day click |
| `1d_view` | 1-day view |

**2026 Changes**: Some view-through windows being deprecated.

## Async Reports

For large queries, use async mode:

### Start Async Report
```
POST /{OBJECT_ID}/insights

{
  "fields": ["impressions", "clicks", "spend", "actions"],
  "date_preset": "last_90d",
  "time_increment": 1,
  "level": "ad",
  "breakdowns": ["age", "gender"]
}
```

Response:
```json
{
  "report_run_id": "123456789"
}
```

### Check Report Status
```
GET /{REPORT_RUN_ID}
```

Response:
```json
{
  "id": "123456789",
  "account_id": "act_123456789",
  "async_status": "Job Completed",
  "async_percent_completion": 100
}
```

Status values:
- `Job Not Started`
- `Job Running`
- `Job Completed`
- `Job Failed`

### Get Report Results
```
GET /{REPORT_RUN_ID}/insights?limit=500
```

## Complete Examples

### Campaign Performance Report
```
GET /act_123456789/insights
  ?level=campaign
  &fields=campaign_id,campaign_name,objective,impressions,reach,clicks,spend,cpm,cpc,ctr,actions
  &date_preset=last_30d
  &filtering=[{"field":"spend","operator":"GREATER_THAN","value":"0"}]
  &sort=spend_descending
```

### Daily Performance Trend
```
GET /23456789012345/insights
  ?fields=impressions,reach,clicks,spend,cpm
  &date_preset=last_14d
  &time_increment=1
```

### Demographics Breakdown
```
GET /23456789012345/insights
  ?fields=impressions,clicks,spend,actions
  &breakdowns=age,gender
  &date_preset=last_7d
```

### Platform Performance
```
GET /23456789012345/insights
  ?fields=impressions,clicks,spend,actions
  &breakdowns=publisher_platform,platform_position
  &date_preset=last_7d
```

### Conversion Funnel
```
GET /23456789012345/insights
  ?fields=actions,action_values,cost_per_action_type,website_purchase_roas
  &date_preset=last_30d
```

## Account-Level Insights

Get overall account performance:

```
GET /act_123456789/insights
  ?fields=account_name,impressions,reach,spend,actions
  &date_preset=this_month
```

## Lifetime Insights

For campaign/adset/ad lifetime totals:

```
GET /{OBJECT_ID}/insights?date_preset=lifetime
```

## Data Freshness

- Most metrics: 15-minute delay
- Some metrics (reach, frequency): Up to 48 hours
- Historical data: May be revised up to 28 days

## Rate Limits for Insights

Insights queries are heavier than standard calls:
- Use `limit` parameter to control page size
- Use async for large date ranges or many breakdowns
- Cache results where possible

## Error Handling

### Common Errors

| Code | Message | Solution |
|------|---------|----------|
| 100 | Invalid metric | Check field name spelling |
| 100 | Invalid breakdown | Incompatible breakdown combo |
| 190 | Token expired | Refresh access token |
| 613 | Rate limit | Wait and retry with backoff |
| 80004 | Too many calls | Reduce request frequency |

### Handling Empty Data

No data returns empty `data` array:
```json
{
  "data": []
}
```

## SDK Examples

### Python
```python
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights

account = AdAccount('act_123456789')

insights = account.get_insights(
    fields=[
        AdsInsights.Field.impressions,
        AdsInsights.Field.reach,
        AdsInsights.Field.clicks,
        AdsInsights.Field.spend,
        AdsInsights.Field.cpm,
        AdsInsights.Field.cpc,
        AdsInsights.Field.actions,
    ],
    params={
        'level': 'campaign',
        'date_preset': 'last_30d',
        'time_increment': 1,
    }
)

for insight in insights:
    print(insight)
```

### PHP
```php
use FacebookAds\Object\AdAccount;
use FacebookAds\Object\Fields\AdsInsightsFields;

$account = new AdAccount('act_123456789');

$insights = $account->getInsights([
    AdsInsightsFields::IMPRESSIONS,
    AdsInsightsFields::REACH,
    AdsInsightsFields::CLICKS,
    AdsInsightsFields::SPEND,
    AdsInsightsFields::CPM,
    AdsInsightsFields::CPC,
    AdsInsightsFields::ACTIONS,
], [
    'level' => 'campaign',
    'date_preset' => 'last_30d',
    'time_increment' => 1,
]);

foreach ($insights as $insight) {
    print_r($insight->getData());
}
```
