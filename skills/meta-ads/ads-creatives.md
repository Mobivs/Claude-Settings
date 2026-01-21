# Meta Ads API - Ads and Creatives

> **Official Docs**: [Ad Reference](https://developers.facebook.com/docs/marketing-api/reference/adgroup) | [Ad Creative Reference](https://developers.facebook.com/docs/marketing-api/reference/ad-creative) | [Image Specs](https://developers.facebook.com/docs/marketing-api/reference/ad-image)

Complete reference for creating ads, uploading assets, and managing ad creatives.

## Understanding Ads vs Creatives

- **Ad Creative**: The visual/copy elements (image, video, text, headline, link)
- **Ad**: Links a creative to an ad set for delivery

Creatives are **immutable** - to change creative content, create a new creative.

## Upload Images

### Endpoint
```
POST /act_{ACCOUNT_ID}/adimages
```

### Upload Single Image
```
POST /act_123456789/adimages
Content-Type: multipart/form-data

file: [binary image data]
```

Response:
```json
{
  "images": {
    "filename.jpg": {
      "hash": "abc123def456...",
      "url": "https://..."
    }
  }
}
```

**Save the `hash`** - you'll use it when creating creatives.

### Image Requirements

| Requirement | Value |
|-------------|-------|
| File types | JPG, PNG |
| Max file size | 30 MB |
| Min dimensions | 600 x 600 pixels |
| Recommended ratio | 1.91:1 (feed), 9:16 (stories) |
| Max dimensions | 8192 x 8192 pixels |

### Upload Multiple Images
```
POST /act_123456789/adimages
Content-Type: multipart/form-data

file1: [binary]
file2: [binary]
file3: [binary]
```

### Get Image by Hash
```
GET /act_{ACCOUNT_ID}/adimages?hashes=['abc123def456']
```

### Delete Image
```
DELETE /act_{ACCOUNT_ID}/adimages?hash=abc123def456
```

## Upload Videos

### Endpoint
```
POST /act_{ACCOUNT_ID}/advideos
```

### Upload Video
```
POST /act_123456789/advideos
Content-Type: multipart/form-data

file: [binary video data]
name: "My Video"
```

Response:
```json
{
  "id": "123456789"
}
```

**Save the `id`** - you'll use it when creating creatives.

### Video Requirements

| Requirement | Value |
|-------------|-------|
| File types | MP4, MOV, GIF |
| Max file size | 4 GB |
| Max duration | 240 minutes |
| Recommended duration | 15 seconds (Stories), 15-60 seconds (Feed) |
| Min dimensions | 120 x 120 pixels |
| Aspect ratios | 16:9, 1:1, 4:5, 9:16 |

### Check Video Processing Status
```
GET /{VIDEO_ID}?fields=status
```

Status values:
- `processing` - Still being processed
- `ready` - Ready to use
- `error` - Processing failed

### Large Video Upload (Chunked)

For videos > 1GB, use chunked upload:

```
# 1. Start upload session
POST /act_123456789/advideos
{
  "upload_phase": "start",
  "file_size": 104857600
}

# Response: {"upload_session_id": "xyz", "video_id": "456"}

# 2. Upload chunks
POST /act_123456789/advideos
{
  "upload_phase": "transfer",
  "upload_session_id": "xyz",
  "start_offset": 0,
  "video_file_chunk": [binary data]
}

# 3. Finish upload
POST /act_123456789/advideos
{
  "upload_phase": "finish",
  "upload_session_id": "xyz"
}
```

## Create Ad Creative

### Endpoint
```
POST /act_{ACCOUNT_ID}/adcreatives
```

### Image Ad Creative

```json
POST /act_123456789/adcreatives

{
  "name": "Summer Sale Creative",
  "object_story_spec": {
    "page_id": "123456789",
    "link_data": {
      "image_hash": "abc123def456...",
      "link": "https://example.com/sale",
      "message": "Summer Sale! Up to 50% off everything.",
      "name": "Shop Summer Sale",
      "description": "Limited time offer",
      "call_to_action": {
        "type": "SHOP_NOW",
        "value": {
          "link": "https://example.com/sale"
        }
      }
    }
  }
}
```

### Video Ad Creative

```json
POST /act_123456789/adcreatives

{
  "name": "Video Ad Creative",
  "object_story_spec": {
    "page_id": "123456789",
    "video_data": {
      "video_id": "987654321",
      "image_hash": "abc123...",
      "title": "Watch Our Story",
      "message": "See what makes us different.",
      "link_description": "Learn more about us",
      "call_to_action": {
        "type": "LEARN_MORE",
        "value": {
          "link": "https://example.com"
        }
      }
    }
  }
}
```

### Carousel Ad Creative

```json
POST /act_123456789/adcreatives

{
  "name": "Carousel Creative",
  "object_story_spec": {
    "page_id": "123456789",
    "link_data": {
      "link": "https://example.com",
      "message": "Check out our products",
      "child_attachments": [
        {
          "link": "https://example.com/product1",
          "image_hash": "hash1...",
          "name": "Product 1",
          "description": "$29.99",
          "call_to_action": {
            "type": "SHOP_NOW",
            "value": {"link": "https://example.com/product1"}
          }
        },
        {
          "link": "https://example.com/product2",
          "image_hash": "hash2...",
          "name": "Product 2",
          "description": "$39.99",
          "call_to_action": {
            "type": "SHOP_NOW",
            "value": {"link": "https://example.com/product2"}
          }
        },
        {
          "link": "https://example.com/product3",
          "image_hash": "hash3...",
          "name": "Product 3",
          "description": "$49.99",
          "call_to_action": {
            "type": "SHOP_NOW",
            "value": {"link": "https://example.com/product3"}
          }
        }
      ]
    }
  }
}
```

### Instagram-Only Creative

```json
POST /act_123456789/adcreatives

{
  "name": "Instagram Creative",
  "object_story_spec": {
    "instagram_actor_id": "17841400000000000",
    "link_data": {
      "image_hash": "abc123...",
      "link": "https://example.com",
      "message": "Shop our collection"
    }
  }
}
```

## Call to Action Types

| Type | Description |
|------|-------------|
| `SHOP_NOW` | E-commerce |
| `LEARN_MORE` | General info |
| `SIGN_UP` | Registration |
| `BOOK_NOW` | Appointments |
| `DOWNLOAD` | App downloads |
| `GET_OFFER` | Promotions |
| `CONTACT_US` | Lead gen |
| `SUBSCRIBE` | Subscriptions |
| `WATCH_MORE` | Video content |
| `SEND_MESSAGE` | Messenger |
| `WHATSAPP_MESSAGE` | WhatsApp |
| `GET_QUOTE` | Services |
| `APPLY_NOW` | Applications |
| `ORDER_NOW` | Food/delivery |
| `BUY_TICKETS` | Events |

## Dynamic Creative

Let Meta automatically test combinations:

```json
POST /act_123456789/adcreatives

{
  "name": "Dynamic Creative",
  "object_story_spec": {
    "page_id": "123456789",
    "link_data": {
      "link": "https://example.com",
      "call_to_action": {"type": "SHOP_NOW"}
    }
  },
  "asset_feed_spec": {
    "images": [
      {"hash": "hash1..."},
      {"hash": "hash2..."},
      {"hash": "hash3..."}
    ],
    "bodies": [
      {"text": "Message variation 1"},
      {"text": "Message variation 2"}
    ],
    "titles": [
      {"text": "Headline 1"},
      {"text": "Headline 2"}
    ],
    "descriptions": [
      {"text": "Description 1"},
      {"text": "Description 2"}
    ]
  }
}
```

## Create Ad

### Endpoint
```
POST /act_{ACCOUNT_ID}/ads
```

### Basic Ad
```json
POST /act_123456789/ads

{
  "name": "Summer Sale Ad",
  "adset_id": "34567890123456",
  "creative": {
    "creative_id": "56789012345678"
  },
  "status": "PAUSED"
}
```

### Ad with Inline Creative

Create creative and ad in one call:

```json
POST /act_123456789/ads

{
  "name": "Ad with Inline Creative",
  "adset_id": "34567890123456",
  "creative": {
    "object_story_spec": {
      "page_id": "123456789",
      "link_data": {
        "image_hash": "abc123...",
        "link": "https://example.com",
        "message": "Check this out!"
      }
    }
  },
  "status": "PAUSED"
}
```

### Ad with Tracking

```json
POST /act_123456789/ads

{
  "name": "Tracked Ad",
  "adset_id": "34567890123456",
  "creative": {"creative_id": "56789012345678"},
  "tracking_specs": [
    {
      "action.type": ["offsite_conversion"],
      "fb_pixel": ["987654321"]
    }
  ],
  "status": "PAUSED"
}
```

## Read Ads and Creatives

### Get Ad
```
GET /{AD_ID}?fields=id,name,status,effective_status,creative{id,name,thumbnail_url}
```

### List Ads in Ad Set
```
GET /{ADSET_ID}/ads?fields=id,name,status,creative
```

### Get Creative Details
```
GET /{CREATIVE_ID}?fields=id,name,object_story_spec,thumbnail_url,image_url
```

### Get Creative Preview
```
GET /{CREATIVE_ID}/previews?ad_format=DESKTOP_FEED_STANDARD
```

Ad format options:
- `DESKTOP_FEED_STANDARD`
- `MOBILE_FEED_STANDARD`
- `INSTAGRAM_STANDARD`
- `INSTAGRAM_STORY`
- `RIGHT_COLUMN_STANDARD`
- `MARKETPLACE_MOBILE`

## Update Ad

### Endpoint
```
POST /{AD_ID}
```

### Updatable Fields
- `name`
- `status`
- `creative` (swap to different creative)
- `tracking_specs`

### Example: Pause Ad
```json
POST /45678901234567

{
  "status": "PAUSED"
}
```

### Example: Swap Creative
```json
POST /45678901234567

{
  "creative": {
    "creative_id": "67890123456789"
  }
}
```

## Delete Ad

### Soft Delete
```json
POST /{AD_ID}

{
  "status": "DELETED"
}
```

### Hard Delete
```
DELETE /{AD_ID}
```

## Ad Review and Approval

Ads are reviewed before delivery:

### Check Review Status
```
GET /{AD_ID}?fields=effective_status,review_feedback
```

### Review Feedback Object
```json
{
  "effective_status": "DISAPPROVED",
  "review_feedback": {
    "global": {
      "POLICY_NAME": "Description of violation"
    }
  }
}
```

### Common Disapproval Reasons
- Policy violation (prohibited content)
- Landing page issues
- Text in image > 20% (legacy, less strict now)
- Misleading claims
- Low-quality creative

## Ad Limits

| Limit | Value |
|-------|-------|
| Ads per ad set | 50 |
| Carousel cards | 2-10 |
| Primary text | 125 chars (recommended) |
| Headline | 40 chars (recommended) |
| Description | 30 chars (recommended) |
| Image text | < 20% (recommendation) |

## Text Recommendations

| Element | Recommended | Maximum |
|---------|-------------|---------|
| Primary text | 125 chars | 2,200 chars |
| Headline | 40 chars | 255 chars |
| Description | 30 chars | 30 chars |
| Link description | 30 chars | 30 chars |

## Error Handling

### Common Errors

| Code | Message | Solution |
|------|---------|----------|
| 100 | Invalid parameter | Check creative spec format |
| 1487654 | Invalid image hash | Image not uploaded or wrong hash |
| 1815327 | Invalid page | Page not accessible to app |
| 1815348 | Creative disappeared | Recreate the creative |
| 275 | Cannot view ads | Check permissions |

## SDK Examples

### Python
```python
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount

account = AdAccount('act_123456789')

# Upload image
image = account.create_ad_image(
    params={'filename': 'path/to/image.jpg'}
)
image_hash = image['hash']

# Create creative
creative = account.create_ad_creative(params={
    'name': 'My Creative',
    'object_story_spec': {
        'page_id': '123456789',
        'link_data': {
            'image_hash': image_hash,
            'link': 'https://example.com',
            'message': 'Check this out!',
            'call_to_action': {
                'type': 'SHOP_NOW',
                'value': {'link': 'https://example.com'}
            }
        }
    }
})

# Create ad
ad = account.create_ad(params={
    'name': 'My Ad',
    'adset_id': '34567890123456',
    'creative': {'creative_id': creative.get_id()},
    'status': Ad.Status.paused
})
```

### PHP
```php
use FacebookAds\Object\AdImage;
use FacebookAds\Object\AdCreative;
use FacebookAds\Object\Ad;
use FacebookAds\Object\AdAccount;

$account = new AdAccount('act_123456789');

// Upload image
$image = $account->createAdImage([], [
    'filename' => 'path/to/image.jpg',
]);
$imageHash = $image->hash;

// Create creative
$creative = $account->createAdCreative([], [
    'name' => 'My Creative',
    'object_story_spec' => [
        'page_id' => '123456789',
        'link_data' => [
            'image_hash' => $imageHash,
            'link' => 'https://example.com',
            'message' => 'Check this out!',
        ],
    ],
]);

// Create ad
$ad = $account->createAd([], [
    'name' => 'My Ad',
    'adset_id' => '34567890123456',
    'creative' => ['creative_id' => $creative->id],
    'status' => Ad::STATUS_PAUSED,
]);
```
