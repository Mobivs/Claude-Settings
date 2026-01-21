# Meta Ads API - Targeting

> **Official Docs**: [Targeting Search](https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting-search) | [Targeting Specs](https://developers.facebook.com/docs/marketing-api/audiences/reference/basic-targeting) | [Custom Audiences](https://developers.facebook.com/docs/marketing-api/audiences/guides/custom-audiences)

Complete reference for audience targeting options in Meta advertising.

## Targeting Overview

Targeting is defined in the ad set's `targeting` field as a JSON object. All targeting options are optional - omit them for broader reach.

## Basic Targeting Structure

```json
{
  "targeting": {
    "geo_locations": {...},
    "age_min": 25,
    "age_max": 54,
    "genders": [1, 2],
    "interests": [...],
    "behaviors": [...],
    "custom_audiences": [...],
    "excluded_custom_audiences": [...],
    "publisher_platforms": [...],
    "facebook_positions": [...],
    "device_platforms": [...]
  }
}
```

## Geographic Targeting

### Countries
```json
{
  "geo_locations": {
    "countries": ["US", "CA", "GB"]
  }
}
```

Use ISO 3166-1 alpha-2 country codes.

### Regions/States
```json
{
  "geo_locations": {
    "regions": [
      {"key": "3847"},
      {"key": "3866"}
    ]
  }
}
```

Find region keys via:
```
GET /search?type=adgeolocation&location_types=["region"]&q=California
```

### Cities
```json
{
  "geo_locations": {
    "cities": [
      {
        "key": "2420379",
        "radius": 25,
        "distance_unit": "mile"
      }
    ]
  }
}
```

Find city keys:
```
GET /search?type=adgeolocation&location_types=["city"]&q=Los Angeles
```

### Zip Codes
```json
{
  "geo_locations": {
    "zips": [
      {"key": "US:90210"},
      {"key": "US:10001"}
    ]
  }
}
```

### DMA (Designated Market Areas)
```json
{
  "geo_locations": {
    "geo_markets": [
      {"key": "DMA:501"}
    ]
  }
}
```

### Location Radius
```json
{
  "geo_locations": {
    "custom_locations": [
      {
        "latitude": 34.0522,
        "longitude": -118.2437,
        "radius": 10,
        "distance_unit": "mile"
      }
    ]
  }
}
```

### Exclude Locations
```json
{
  "geo_locations": {
    "countries": ["US"]
  },
  "excluded_geo_locations": {
    "regions": [
      {"key": "3847"}
    ]
  }
}
```

### Location Types
```json
{
  "geo_locations": {
    "countries": ["US"],
    "location_types": ["home", "recent"]
  }
}
```

Options:
- `home` - People living in location
- `recent` - Recently in location
- `travel_in` - Traveling to location

## Demographics

### Age
```json
{
  "age_min": 25,
  "age_max": 54
}
```

- Minimum: 13 (some countries 18+)
- Maximum: 65 (means 65+)
- Omit for all ages

### Gender
```json
{
  "genders": [1]
}
```

Values:
- `1` - Male
- `2` - Female
- Omit or `[1, 2]` for all genders

### Languages
```json
{
  "locales": [6, 24]
}
```

Find locale IDs:
```
GET /search?type=adlocale&q=english
```

### Education Level
```json
{
  "education_statuses": [3, 4, 5]
}
```

Values:
- `1` - High school
- `2` - Some college
- `3` - In college
- `4` - College grad
- `5` - Some grad school
- `6` - Master's degree
- `7` - Professional degree
- `8` - Doctorate
- `9` - Unspecified
- `10` - Some high school

### Relationship Status
```json
{
  "relationship_statuses": [1, 2]
}
```

Values:
- `1` - Single
- `2` - In a relationship
- `3` - Married
- `4` - Engaged
- `6` - Not specified

## Interests

Target users based on interests:

```json
{
  "interests": [
    {"id": "6003139266461", "name": "Yoga"},
    {"id": "6003107902433", "name": "Fitness and wellness"}
  ]
}
```

### Search for Interests
```
GET /search?type=adinterest&q=yoga
```

Response:
```json
{
  "data": [
    {
      "id": "6003139266461",
      "name": "Yoga",
      "audience_size_lower_bound": 310000000,
      "audience_size_upper_bound": 365000000,
      "path": ["Interests", "Sports and outdoors", "Yoga"]
    }
  ]
}
```

### Interest Categories

Find interest categories:
```
GET /search?type=adinterestsuggestion&interest_list=["6003139266461"]
```

## Behaviors

Target users based on behaviors:

```json
{
  "behaviors": [
    {"id": "6002714895372", "name": "Engaged Shoppers"},
    {"id": "6002714898572", "name": "Frequent Travelers"}
  ]
}
```

### Search for Behaviors
```
GET /search?type=adbehavior&q=shopper
```

### Common Behavior Categories
- Purchase behavior
- Travel habits
- Device usage
- Digital activities
- Seasonal/event behavior

## Detailed Targeting Expansion

Allow Meta to expand beyond specified targeting:

```json
{
  "targeting_optimization": "expansion_all"
}
```

Options:
- `none` - Strict targeting
- `expansion_all` - Expand all criteria

## Custom Audiences

### Include Custom Audience
```json
{
  "custom_audiences": [
    {"id": "23456789012345"}
  ]
}
```

### Exclude Custom Audience
```json
{
  "excluded_custom_audiences": [
    {"id": "34567890123456"}
  ]
}
```

### Create Custom Audience (separate endpoint)
```
POST /act_{ACCOUNT_ID}/customaudiences

{
  "name": "Website Visitors",
  "subtype": "WEBSITE",
  "description": "All website visitors last 30 days",
  "retention_days": 30,
  "rule": {
    "inclusions": {
      "operator": "or",
      "rules": [
        {
          "event_sources": [{"id": "PIXEL_ID", "type": "pixel"}],
          "retention_seconds": 2592000,
          "filter": {"operator": "and", "filters": []}
        }
      ]
    }
  }
}
```

## Lookalike Audiences

### Create Lookalike
```
POST /act_{ACCOUNT_ID}/customaudiences

{
  "name": "Lookalike - Purchasers",
  "subtype": "LOOKALIKE",
  "origin_audience_id": "SOURCE_AUDIENCE_ID",
  "lookalike_spec": {
    "type": "similarity",
    "country": "US",
    "ratio": 0.01
  }
}
```

Ratio options:
- `0.01` - Top 1% (most similar)
- `0.02` - Top 2%
- `0.05` - Top 5%
- `0.10` - Top 10%

### Use Lookalike in Targeting
```json
{
  "custom_audiences": [
    {"id": "LOOKALIKE_AUDIENCE_ID"}
  ]
}
```

## Connections Targeting

### Target Page Fans
```json
{
  "connections": [
    {"id": "PAGE_ID"}
  ]
}
```

### Exclude Page Fans
```json
{
  "excluded_connections": [
    {"id": "PAGE_ID"}
  ]
}
```

### Friends of Page Fans
```json
{
  "friends_of_connections": [
    {"id": "PAGE_ID"}
  ]
}
```

## Placements

### Publisher Platforms
```json
{
  "publisher_platforms": ["facebook", "instagram", "audience_network", "messenger"]
}
```

### Facebook Positions
```json
{
  "facebook_positions": [
    "feed",
    "story",
    "marketplace",
    "video_feeds",
    "right_hand_column",
    "search",
    "instant_article",
    "instream_video"
  ]
}
```

### Instagram Positions
```json
{
  "instagram_positions": [
    "stream",
    "story",
    "explore",
    "reels",
    "profile_feed",
    "search"
  ]
}
```

### Audience Network Positions
```json
{
  "audience_network_positions": [
    "classic",
    "rewarded_video",
    "instream_video"
  ]
}
```

### Messenger Positions
```json
{
  "messenger_positions": [
    "messenger_home",
    "story",
    "inbox"
  ]
}
```

## Device Targeting

### Device Platforms
```json
{
  "device_platforms": ["mobile", "desktop"]
}
```

### Mobile Devices
```json
{
  "user_device": ["iPhone", "iPad", "Android_Smartphone"]
}
```

### Operating Systems
```json
{
  "user_os": ["iOS", "Android"]
}
```

### Minimum OS Version
```json
{
  "user_os": ["iOS"],
  "os_version_min": "14.0"
}
```

## Flexible Spec (OR Logic)

Combine targeting with OR logic:

```json
{
  "flexible_spec": [
    {
      "interests": [{"id": "123", "name": "Yoga"}],
      "behaviors": [{"id": "456", "name": "Engaged Shoppers"}]
    }
  ]
}
```

Users must match at least ONE item from the flexible_spec.

## Exclusions

### Exclude Interests
```json
{
  "exclusions": {
    "interests": [
      {"id": "789", "name": "Competitor Brand"}
    ]
  }
}
```

### Exclude Behaviors
```json
{
  "exclusions": {
    "behaviors": [
      {"id": "101112", "name": "Some Behavior"}
    ]
  }
}
```

## Special Ad Categories

Some targeting is restricted for special ad categories:

### Housing, Employment, Credit Ads
Restricted:
- Age targeting
- Gender targeting
- Zip code targeting
- Multicultural affinity
- Some interests/behaviors

Required:
```json
{
  "geo_locations": {
    "countries": ["US"],
    "location_types": ["home"]
  }
}
```

Radius: Minimum 15 miles for addresses.

## Targeting Validation

### Check Reach Estimate
```
GET /act_{ACCOUNT_ID}/reachestimate
  ?targeting_spec={...targeting JSON...}
  &optimize_for=IMPRESSIONS
```

Response:
```json
{
  "users_lower_bound": 1200000,
  "users_upper_bound": 1400000
}
```

### Validate Targeting
```
POST /act_{ACCOUNT_ID}/adsets?validate_only=true

{
  "campaign_id": "123",
  "targeting": {...},
  ...other fields...
}
```

## Complete Targeting Example

```json
{
  "targeting": {
    "geo_locations": {
      "countries": ["US"],
      "regions": [{"key": "3847"}],
      "location_types": ["home", "recent"]
    },
    "excluded_geo_locations": {
      "cities": [{"key": "777555", "radius": 10, "distance_unit": "mile"}]
    },
    "age_min": 25,
    "age_max": 54,
    "genders": [2],
    "locales": [6],
    "interests": [
      {"id": "6003139266461", "name": "Yoga"},
      {"id": "6003107902433", "name": "Fitness and wellness"}
    ],
    "behaviors": [
      {"id": "6002714895372", "name": "Engaged Shoppers"}
    ],
    "custom_audiences": [
      {"id": "23456789012345"}
    ],
    "excluded_custom_audiences": [
      {"id": "34567890123456"}
    ],
    "publisher_platforms": ["facebook", "instagram"],
    "facebook_positions": ["feed", "story"],
    "instagram_positions": ["stream", "story", "reels"],
    "device_platforms": ["mobile"]
  }
}
```

## Targeting Search Endpoints

| Type | Endpoint |
|------|----------|
| Countries | `GET /search?type=adcountry` |
| Regions | `GET /search?type=adgeolocation&location_types=["region"]&q=...` |
| Cities | `GET /search?type=adgeolocation&location_types=["city"]&q=...` |
| Zip codes | `GET /search?type=adgeolocation&location_types=["zip"]&q=...` |
| Interests | `GET /search?type=adinterest&q=...` |
| Behaviors | `GET /search?type=adbehavior&q=...` |
| Education | `GET /search?type=adeducationschool&q=...` |
| Employers | `GET /search?type=adworkemployer&q=...` |
| Locales | `GET /search?type=adlocale&q=...` |

## Error Handling

### Common Targeting Errors

| Code | Message | Solution |
|------|---------|----------|
| 100 | Invalid targeting spec | Check JSON structure |
| 1815265 | Audience too narrow | Broaden targeting |
| 1815266 | Audience too small | Minimum ~1,000 users |
| 1815276 | Invalid geo location | Check location keys |
| 2635015 | Restricted for special ad | Remove restricted targeting |

## SDK Examples

### Python
```python
targeting = {
    'geo_locations': {
        'countries': ['US'],
    },
    'age_min': 25,
    'age_max': 54,
    'genders': [2],
    'interests': [
        {'id': '6003139266461', 'name': 'Yoga'},
    ],
    'publisher_platforms': ['facebook', 'instagram'],
    'facebook_positions': ['feed', 'story'],
}

adset = account.create_ad_set(params={
    'campaign_id': campaign_id,
    'name': 'Yoga Enthusiasts',
    'targeting': targeting,
    'daily_budget': 5000,
    ...
})
```

### PHP
```php
$targeting = [
    'geo_locations' => [
        'countries' => ['US'],
    ],
    'age_min' => 25,
    'age_max' => 54,
    'genders' => [2],
    'interests' => [
        ['id' => '6003139266461', 'name' => 'Yoga'],
    ],
    'publisher_platforms' => ['facebook', 'instagram'],
    'facebook_positions' => ['feed', 'story'],
];

$adset = $account->createAdSet([], [
    AdSetFields::CAMPAIGN_ID => $campaignId,
    AdSetFields::NAME => 'Yoga Enthusiasts',
    AdSetFields::TARGETING => $targeting,
    AdSetFields::DAILY_BUDGET => 5000,
    ...
]);
```
