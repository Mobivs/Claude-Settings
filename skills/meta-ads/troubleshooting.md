# Meta Ads API - Troubleshooting

> **Official Docs**: [Error Reference](https://developers.facebook.com/docs/marketing-api/error-reference) | [Rate Limiting](https://developers.facebook.com/docs/marketing-api/overview/rate-limiting) | [Debugging](https://developers.facebook.com/docs/graph-api/using-graph-api/debugging)

Common errors, rate limits, debugging tips, and solutions for the Meta Marketing API.

## Error Response Format

All API errors return:

```json
{
  "error": {
    "message": "Human-readable error message",
    "type": "ErrorType",
    "code": 100,
    "error_subcode": 1234567,
    "fbtrace_id": "ABC123xyz"
  }
}
```

Save the `fbtrace_id` for support requests.

## Common Error Codes

### Authentication Errors (100-299)

| Code | Subcode | Message | Solution |
|------|---------|---------|----------|
| 190 | - | Invalid access token | Token expired or revoked; generate new token |
| 190 | 458 | App not installed | User hasn't authorized app |
| 190 | 460 | Password changed | User changed password; reauthorize |
| 190 | 463 | Token expired | Exchange for long-lived token |
| 190 | 467 | Invalid token | Token is malformed |
| 200 | - | Permission denied | Missing required permission scope |

### Parameter Errors (100)

| Subcode | Message | Solution |
|---------|---------|----------|
| 1487073 | Budget too low | Increase budget to minimum |
| 1487654 | Invalid image hash | Upload image first |
| 1487930 | Invalid objective | Use OUTCOME_* format |
| 1815265 | Targeting invalid | Fix targeting specification |
| 1815115 | Missing promoted object | Add pixel/app ID |
| 1815320 | Special ad category required | Add category to campaign |
| 1815327 | Invalid page | Page not accessible |
| 1815348 | Creative invalid | Recreate the creative |
| 2615 | Cannot modify field | Field not updatable |

### Rate Limit Errors (4, 17, 613, 80000-80999)

| Code | Message | Solution |
|------|---------|----------|
| 4 | App request limit reached | Wait and retry with backoff |
| 17 | User request limit reached | Per-user rate limit |
| 613 | Calls limit reached | Too many API calls |
| 80000 | Rate limit exceeded | General rate limit |
| 80003 | Too many requests | Reduce request frequency |
| 80004 | Too many calls | Heavy endpoint (insights) |
| 80005 | Too many IDs | Reduce batch size |

### Object Errors (803, 1200+)

| Code | Message | Solution |
|------|---------|----------|
| 275 | Cannot view ads | Check permissions |
| 803 | Object not found | Wrong ID or deleted object |
| 1200 | Object not found | Campaign/ad set/ad deleted |
| 1487390 | Campaign deleted | Use different campaign |
| 2446 | Ad account disabled | Contact support |

### Business/Account Errors

| Code | Message | Solution |
|------|---------|----------|
| 294 | Ad account not accessible | Check business manager access |
| 1487076 | Account is disabled | Payment or policy issue |
| 368 | Account disabled for policy violation | Appeal through Business Help Center |

## Rate Limits

### How Rate Limits Work

Meta uses a **scoring system** based on:
- Number of calls
- Complexity of calls
- Time window (rolling 1 hour)

### Rate Limit Formula
```
Limit = 60 + (400 × Active Ads) - (0.001 × User Errors)
```

### Checking Rate Limit Status

Look for headers in API responses:
```
x-business-use-case-usage: {"123456789": [{"type": "ads_insights", "call_count": 28, "total_cputime": 25, "total_time": 50, "estimated_time_to_regain_access": 0}]}
x-app-usage: {"call_count": 28, "total_cputime": 25, "total_time": 50}
```

### Rate Limit Best Practices

1. **Implement exponential backoff**
```python
def make_request_with_retry(url, max_retries=5):
    for attempt in range(max_retries):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 429:  # Rate limited
            wait_time = (2 ** attempt) * 60  # 1min, 2min, 4min...
            time.sleep(wait_time)
        else:
            raise Exception(f"Error: {response.status_code}")
    raise Exception("Max retries exceeded")
```

2. **Use batch requests**
```json
POST /

{
  "batch": [
    {"method": "GET", "relative_url": "campaign1"},
    {"method": "GET", "relative_url": "campaign2"},
    {"method": "GET", "relative_url": "campaign3"}
  ]
}
```

3. **Cache results** - Don't re-fetch unchanged data

4. **Use async for insights** - Heavy queries in background

5. **Reduce field requests** - Only request needed fields

## Debugging Tips

### Enable Debug Mode
```
GET /{ENDPOINT}?debug=all
```

Returns additional debug info in response.

### Graph API Explorer
Use https://developers.facebook.com/tools/explorer/ to:
- Test API calls interactively
- See exact request/response
- Debug permission issues

### Access Token Debugger
https://developers.facebook.com/tools/debug/accesstoken/

Shows:
- Token validity
- Expiration time
- Granted permissions
- Associated user/app

### Validate Before Creating
```
POST /act_{ACCOUNT_ID}/campaigns?validate_only=true

{
  "name": "Test",
  "objective": "OUTCOME_SALES",
  "special_ad_categories": []
}
```

Returns validation errors without creating.

## Common Issues and Solutions

### App in Development Mode (Cannot Create Ads)
**Error**: `"Application does not have permission for this action"` or creative creation fails silently

**Cause**: Your Meta Developer App is still in Development Mode. You can only create ads via API when the app is LIVE.

**Solution**:
1. Go to developers.facebook.com → My Apps → Your App
2. Navigate to **App settings > Basic**
3. Add a **Privacy Policy URL** (REQUIRED - Meta won't let you publish without one)
4. Click **Save Changes**
5. Find **Publish** in the left sidebar → Click Publish

**Key insight**: Without a privacy policy URL, the Publish button won't work.

### CBO Budget Conflict
**Error**: `"Daily budget and lifetime budget are unavailable for this ad set"`

**Cause**: You're trying to set a budget on an ad set, but the campaign uses Campaign Budget Optimization (CBO).

**Solution**: When using CBO, do NOT set `daily_budget` or `lifetime_budget` on the ad set - it inherits from the campaign.

```bash
# Campaign WITH budget (CBO)
curl -X POST ".../campaigns" -d "daily_budget=500" ...

# Ad Set WITHOUT budget
curl -X POST ".../adsets" ...  # No budget params!
```

### Advantage+ Audience Flag Required
**Error**: `"targeting_automation is required"` or similar targeting validation error

**Cause**: When using interest targeting with `flexible_spec`, Meta now requires you to declare whether you're using Advantage+ audience expansion.

**Solution**: Add `targeting_automation` to your targeting spec:
```json
{
  "targeting": {
    "geo_locations": {"countries": ["US"]},
    "flexible_spec": [{"interests": [{"id": "123", "name": "AI"}]}],
    "targeting_automation": {"advantage_audience": 0}
  }
}
```

Set `advantage_audience` to:
- `0` = Manual targeting (your exact specs)
- `1` = Meta can expand audience using AI

### Token Expires in ~1 Hour
**Error**: `"Error validating access token: Session has expired"`

**Cause**: Tokens from Graph API Explorer expire in 1-2 hours by default.

**Solution**:
1. Generate fresh token before each API session
2. For production: Use System User tokens (never expire)
3. Or implement token refresh flow with long-lived tokens

### "Invalid access token"
**Causes**:
- Token expired
- Token revoked
- Password changed
- App removed

**Solutions**:
1. Generate new token
2. Implement token refresh logic
3. Use System User tokens (never expire)

### "Insufficient permissions"
**Causes**:
- Missing permission scope
- Need Advanced Access
- Business not verified

**Solutions**:
1. Request needed permissions
2. Complete Business Verification
3. Submit for App Review

### "Ad account not accessible"
**Causes**:
- Wrong ad account ID
- No access granted
- Account in different Business Manager

**Solutions**:
1. Verify ad account ID
2. Check Business Manager access
3. Request access from account owner

### "Invalid targeting spec"
**Causes**:
- Malformed JSON
- Invalid location key
- Incompatible targeting combinations
- Audience too narrow

**Solutions**:
1. Validate JSON syntax
2. Search for correct location keys
3. Remove incompatible options
4. Broaden targeting

### "Creative disappeared"
**Causes**:
- Creative was deleted
- Image expired
- Policy violation

**Solutions**:
1. Create new creative
2. Re-upload images
3. Check creative for policy issues

### "Budget too low"
**Causes**:
- Below minimum daily budget
- Currency mismatch

**Solutions**:
1. Check minimum budget for country/optimization
2. Verify currency (amounts in cents)
3. Typical minimum: ~$1 USD/day

### "Campaign objective cannot be modified"
**Causes**:
- Objective is immutable

**Solutions**:
1. Create new campaign with desired objective
2. Move ad sets to new campaign

## API Version Issues

### Version Deprecation
- Versions supported for ~2 years
- Check current version at developers.facebook.com

### Upgrading Versions
```
# Old
GET https://graph.facebook.com/v18.0/...

# New
GET https://graph.facebook.com/v22.0/...
```

### Version-Specific Errors
If suddenly getting errors after long time:
1. Check if API version deprecated
2. Review breaking changes in release notes
3. Update to current version

## Policy Violations

### Common Policy Issues
- Prohibited content
- Misleading claims
- Personal attributes
- Low-quality landing page
- Circumventing systems

### Checking Ad Review Status
```
GET /{AD_ID}?fields=effective_status,review_feedback
```

### Appealing Disapproval
1. Fix the issue in creative/landing page
2. Request review in Ads Manager
3. Use Business Help Center for appeals

## Network/Timeout Issues

### Request Timeouts
**Solutions**:
1. Use async for long operations
2. Increase timeout settings
3. Break large requests into smaller batches

### SSL/TLS Errors
**Solutions**:
1. Update SSL certificates
2. Use TLS 1.2+
3. Check system time is correct

## SDK-Specific Issues

### Python SDK
```python
# Enable debug logging
from facebook_business.api import FacebookAdsApi
FacebookAdsApi.init(app_id, app_secret, access_token, debug=True)
```

### PHP SDK
```php
// Enable debug
$api = Api::init($appId, $appSecret, $accessToken);
$api->setLogger(new CurlLogger());
```

## Support Resources

### Documentation
- https://developers.facebook.com/docs/marketing-api

### Error Reference
- https://developers.facebook.com/docs/marketing-api/error-reference

### Business Help Center
- https://www.facebook.com/business/help

### Developer Community
- https://developers.facebook.com/community/

### Stack Overflow
- Tag: `facebook-marketing-api`

## Error Handling Best Practices

### Catch and Log All Errors
```python
try:
    result = api.call(...)
except FacebookRequestError as e:
    error = e.api_error_message()
    code = e.api_error_code()
    trace_id = e.api_error_fbtrace_id()

    logger.error(f"Meta API Error: {code} - {error}")
    logger.error(f"Trace ID: {trace_id}")

    if code == 190:
        # Token expired - refresh
        refresh_token()
    elif code in [4, 17, 613, 80004]:
        # Rate limit - back off
        time.sleep(300)
    else:
        raise
```

### Retry Logic
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=300)
)
def make_api_call():
    return api.call(...)
```

### Monitor and Alert
- Track error rates by code
- Alert on sudden spikes
- Log trace IDs for support

## Quick Troubleshooting Checklist

1. **Check token validity** - Use debugger tool
2. **Verify permissions** - Compare granted vs needed
3. **Validate request** - Use `validate_only=true`
4. **Check object exists** - GET the object first
5. **Review rate limits** - Check response headers
6. **Test in Explorer** - Isolate code vs API issues
7. **Check API version** - Ensure not deprecated
8. **Review recent changes** - Breaking changes?
9. **Check Business Manager** - Access and verification
10. **Save trace ID** - For support requests
