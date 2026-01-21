# Meta Ads API - Authentication

> **Official Docs**: [Authorization Overview](https://developers.facebook.com/docs/marketing-api/overview/authorization) | [Access Tokens](https://developers.facebook.com/docs/facebook-login/guides/access-tokens) | [Permissions Reference](https://developers.facebook.com/docs/permissions/reference)

Complete guide to authentication, access tokens, and permissions for the Meta Marketing API.

## Overview

All Meta Marketing API requests require authentication via an access token. The token encodes:
- Your app credentials
- User permissions granted
- Scope of access (which ad accounts, etc.)

## Token Types

### Short-Lived User Token
- **Duration**: ~1-2 hours
- **Use case**: Testing, development, Graph API Explorer
- **Generation**: OAuth dialog or Graph API Explorer tool

### Long-Lived User Token
- **Duration**: ~60 days
- **Use case**: Server-side integrations with manual refresh
- **Generation**: Exchange short-lived token

### System User Token
- **Duration**: Never expires (until revoked)
- **Use case**: Production server-to-server integrations
- **Generation**: Business Manager > System Users
- **Recommended**: For all production applications

### Page Access Token
- **Duration**: Varies (can be long-lived)
- **Use case**: Posting as a Page
- **Generation**: Through user token with `pages_manage_ads` permission

## Required Permissions

### Standard Permissions

| Permission | Access Level | Description |
|------------|--------------|-------------|
| `ads_read` | Standard | Read ad performance data |
| `ads_management` | Standard | Create/edit/delete campaigns |
| `read_insights` | Standard | Access performance metrics |

### Advanced Permissions (Requires Business Verification)

| Permission | Description |
|------------|-------------|
| `business_management` | Manage Business Manager assets |
| `pages_manage_ads` | Manage ads for Pages |
| `pages_read_engagement` | Read ad comments |

## App Setup Steps

### 1. Create Developer Account
1. Go to https://developers.facebook.com/
2. Click "Get Started" or "My Apps"
3. Create or log into your Meta account

### 2. Create an App
1. Go to My Apps > Create App
2. Select use case: **Other**
3. Select app type: **Business**
4. Fill in app name and contact email
5. Complete security check

### 3. Add Marketing API
1. From app dashboard, click "Add Product"
2. Find "Marketing API" and click "Set Up"
3. Configure settings as needed

### 4. Generate Access Token

**For Testing (Graph API Explorer)**:
1. Go to https://developers.facebook.com/tools/explorer/
2. Select your app
3. Click "Generate Access Token"
4. Select required permissions:
   - `ads_management`
   - `ads_read`
   - `business_management` (if needed)
5. Click "Generate Token"
6. Authorize the permissions

**For Production (System User)**:
1. Go to Business Manager > Business Settings
2. Users > System Users
3. Create new System User
4. Assign assets (ad accounts)
5. Generate token with required permissions

### 5. Find Your Ad Account ID
```
GET /me/adaccounts?fields=account_id,name
```

Response:
```json
{
  "data": [
    {
      "account_id": "123456789",
      "name": "My Ad Account",
      "id": "act_123456789"
    }
  ]
}
```

**Note**: Use the format `act_123456789` (with prefix) in API calls.

## Token Exchange (Short to Long-Lived)

```
GET /oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id={APP_ID}
  &client_secret={APP_SECRET}
  &fb_exchange_token={SHORT_LIVED_TOKEN}
```

Response:
```json
{
  "access_token": "LONG_LIVED_TOKEN",
  "token_type": "bearer",
  "expires_in": 5183944
}
```

## Making Authenticated Requests

### Query Parameter Method
```
GET https://graph.facebook.com/v22.0/act_123456789/campaigns?access_token=YOUR_TOKEN
```

### Header Method (Recommended)
```
GET https://graph.facebook.com/v22.0/act_123456789/campaigns
Authorization: Bearer YOUR_TOKEN
```

## Token Debugging

Check token validity and permissions:
```
GET /debug_token?input_token={TOKEN}&access_token={APP_TOKEN}
```

Response includes:
- `is_valid`: Boolean
- `expires_at`: Unix timestamp
- `scopes`: Array of granted permissions
- `user_id`: Associated user
- `app_id`: Associated app

## Access Levels

### Standard Access
- Manage your own ad accounts only
- Default for new apps
- No approval required

### Advanced Access
- Manage other users' ad accounts
- Required for agencies/third-party tools
- Requires Business Verification
- Must complete App Review

## Business Verification

Required for:
- Advanced Access permissions
- Creating ad accounts programmatically
- Managing client ad accounts

Process:
1. Business Manager > Security Center
2. Start Verification
3. Provide business documentation
4. Wait for review (1-5 business days)

## Security Best Practices

1. **Never expose tokens in client-side code**
2. **Store tokens encrypted** at rest
3. **Use System User tokens** for production
4. **Implement token refresh logic** before expiration
5. **Use HTTPS** for all API calls
6. **Log and monitor** API access
7. **Rotate tokens** periodically
8. **Limit permissions** to minimum required

## Common Authentication Errors

| Code | Message | Solution |
|------|---------|----------|
| 190 | Invalid access token | Token expired or revoked; generate new one |
| 200 | Permission denied | Missing required permission scope |
| 4 | Application request limit reached | Rate limited; wait and retry |
| 17 | User request limit reached | Per-user rate limit; implement backoff |

## Environment Variables Example

Store credentials securely:
```bash
# .env file (never commit!)
META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret
META_ACCESS_TOKEN=your_access_token
META_AD_ACCOUNT_ID=act_123456789
```

## SDK Authentication Examples

### Python
```python
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

app_id = 'YOUR_APP_ID'
app_secret = 'YOUR_APP_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'

FacebookAdsApi.init(app_id, app_secret, access_token)
account = AdAccount('act_123456789')
```

### PHP
```php
use FacebookAds\Api;
use FacebookAds\Object\AdAccount;

Api::init($appId, $appSecret, $accessToken);
$account = new AdAccount('act_123456789');
```

### Node.js
```javascript
const bizSdk = require('facebook-nodejs-business-sdk');
const AdAccount = bizSdk.AdAccount;

const api = bizSdk.FacebookAdsApi.init(accessToken);
const account = new AdAccount('act_123456789');
```

## Refreshing Tokens

### Check Expiration
```
GET /me?fields=id&access_token={TOKEN}
```

If you get error 190, token is expired.

### Refresh Long-Lived Token
Long-lived tokens cannot be refreshed directly. Generate a new short-lived token and exchange it again.

### System User Tokens
Never expire unless:
- Manually revoked
- App is removed from Business Manager
- System User is deleted
