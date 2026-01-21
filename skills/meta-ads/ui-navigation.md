# Meta Ads - UI Navigation Guide

> **Official Docs**: [Ads Manager Guide](https://www.facebook.com/business/help/200000840044554) | [Events Manager](https://www.facebook.com/business/help/898185560232180)

Mapping API concepts to where they live in the Meta Ads Manager UI.

## The Core Problem

The API has clean concepts:
- Campaign → Ad Set → Ad → Creative
- Pixel → Events → Conversions

But the UI scatters these across multiple tools:
- **Ads Manager** - Campaigns, ad sets, ads
- **Events Manager** - Pixels, conversions, events
- **Business Settings** - Accounts, permissions, assets
- **Audiences** - Custom audiences, lookalikes

---

## Connecting Your Pixel to a Campaign

This is where most people get stuck. Here's the path:

### Step 1: Verify Pixel Exists (Events Manager)

1. Go to: **facebook.com/events_manager**
2. Or: Ads Manager → hamburger menu (☰) → **Events Manager**
3. You should see your pixel listed under "Data Sources"
4. Click it to verify it's receiving events

### Step 2: Create Campaign with Conversion Objective

1. Go to: **Ads Manager** → **+ Create**
2. Choose objective: **Sales** (for conversions) or **Leads**
   - API equivalent: `OUTCOME_SALES` or `OUTCOME_LEADS`
3. Click **Continue**

### Step 3: Connect Pixel at Ad Set Level

**This is the confusing part** - the pixel connection happens in the Ad Set, not the Campaign.

1. In the Ad Set section, look for **"Conversion location"**
   - Select: **Website**

2. Then look for **"Pixel"** or **"Dataset"**
   - Click the dropdown
   - Select your Vibe9 pixel
   - If you don't see it: Check Business Settings → Data Sources

3. Choose **"Conversion event"**
   - Options: Purchase, Lead, CompleteRegistration, ViewContent, etc.
   - For Vibe9 signups: **CompleteRegistration** or **Lead**

4. Set **Attribution setting**
   - Default: 7-day click, 1-day view
   - This determines how conversions are counted

### Visual Guide: Where to Find Pixel Selection

```
Campaign Level (top)
├── Campaign name
├── Objective: Sales ✓
└── Special ad categories

    ↓

Ad Set Level (middle) ← PIXEL GOES HERE
├── Conversion location: Website ✓
├── Pixel: [SELECT YOUR PIXEL HERE] ← This dropdown!
├── Conversion event: Lead/CompleteRegistration
├── Attribution: 7-day click
├── Budget & schedule
├── Audience (targeting)
└── Placements

    ↓

Ad Level (bottom)
├── Ad name
├── Identity (Page)
├── Ad creative
└── Destination URL
```

---

## Events Manager Navigation

### Finding Your Pixel
```
facebook.com/events_manager
    └── Data Sources (left sidebar)
            └── Your Pixel Name
                    ├── Overview (event activity)
                    ├── Test Events (debugging)
                    └── Settings (pixel ID, etc.)
```

### Testing Your Pixel
1. Events Manager → Your Pixel → **Test Events**
2. Enter your website URL
3. Open your site in a new tab
4. Perform actions (page view, signup, etc.)
5. Events should appear in Test Events within seconds

### Common Events to Track

| Event | When to Fire | Vibe9 Usage |
|-------|--------------|-------------|
| PageView | Every page load | Auto (base pixel) |
| ViewContent | Article/lesson view | When user reads content |
| Lead | Form submission | Newsletter signup |
| CompleteRegistration | Account created | User creates account |
| Search | User searches | Forum/article search |

---

## Business Settings Navigation

Where to find account-level settings:

```
business.facebook.com/settings
    ├── Users
    │   ├── People (team access)
    │   └── Partners (agency access)
    │
    ├── Accounts
    │   ├── Ad Accounts (your ad accounts)
    │   ├── Pages (connected pages)
    │   └── Instagram Accounts
    │
    ├── Data Sources
    │   ├── Pixels ← Your tracking pixels
    │   ├── Catalogs
    │   └── Datasets
    │
    └── Brand Safety
        └── Domains (verified domains)
```

### Connecting Pixel to Ad Account

If your pixel isn't showing in Ads Manager:

1. Business Settings → **Data Sources** → **Pixels**
2. Select your pixel
3. Click **Add Assets**
4. Select your **Ad Account**
5. Now it will appear in Ads Manager

---

## Audiences Navigation

```
Ads Manager → hamburger (☰) → Audiences
    ├── Custom Audiences
    │   ├── Website (pixel-based)
    │   ├── Customer List (upload)
    │   ├── App Activity
    │   └── Engagement (video, page, etc.)
    │
    └── Lookalike Audiences
        └── Based on custom audiences
```

### Creating Website Custom Audience

1. Audiences → **Create Audience** → **Custom Audience**
2. Select **Website**
3. Choose your pixel
4. Define rules:
   - All website visitors (last 30 days)
   - People who visited specific pages
   - Visitors by time spent
5. Name it and save

---

## Campaign Creation Flow

### Full UI Path
```
1. ads.facebook.com or business.facebook.com/adsmanager

2. Click "+ Create" (green button)

3. CAMPAIGN LEVEL
   ├── Choose objective (Sales, Leads, Traffic, etc.)
   ├── Campaign name
   ├── A/B test? (usually no)
   ├── Campaign budget optimization (CBO)?
   │   └── If yes, set budget here
   └── Continue

4. AD SET LEVEL
   ├── Ad set name
   ├── Conversion location → Website
   ├── Pixel → [SELECT HERE] ← !!!
   ├── Conversion event → Lead/CompleteRegistration
   ├── Budget (if not CBO)
   ├── Schedule (start/end dates)
   ├── Audience
   │   ├── Locations
   │   ├── Age
   │   ├── Gender
   │   ├── Detailed targeting (interests)
   │   └── Custom audiences
   ├── Placements (Advantage+ or manual)
   └── Continue

5. AD LEVEL
   ├── Ad name
   ├── Identity
   │   ├── Facebook Page
   │   └── Instagram account
   ├── Ad setup (create new or use existing)
   ├── Creative
   │   ├── Media (images/videos)
   │   ├── Primary text
   │   ├── Headline
   │   ├── Description
   │   └── Call to action
   ├── Destination (URL)
   └── Tracking (URL parameters)

6. Review → Publish
```

---

## Common "Where Is It?" Questions

| I'm looking for... | It's in... |
|--------------------|------------|
| My pixel | Events Manager → Data Sources |
| Pixel ID | Events Manager → Pixel → Settings |
| Connect pixel to ad | Ad Set → Conversion section → Pixel dropdown |
| Conversion events | Ad Set → Conversion event dropdown |
| Custom audiences | Ads Manager → ☰ → Audiences |
| Website visitors audience | Audiences → Custom → Website |
| Ad account ID | Business Settings → Accounts → Ad Accounts |
| Page selection | Ad level → Identity → Facebook Page |
| Instagram account | Ad level → Identity → Instagram |
| Billing/payment | Business Settings → Payments |
| Domain verification | Business Settings → Brand Safety → Domains |
| User permissions | Business Settings → Users → People |

---

## Troubleshooting UI Issues

### "I can't see my pixel in the dropdown"

1. Check Events Manager - does the pixel exist?
2. Business Settings → Data Sources → Pixels
3. Is pixel assigned to this ad account?
4. Click pixel → Add Assets → Add your ad account

### "Conversion event dropdown is empty"

1. Pixel needs to have received events
2. Go to Events Manager → Test Events
3. Visit your site to trigger events
4. Wait a few minutes, then refresh Ads Manager

### "I can't select my Facebook Page"

1. Business Settings → Accounts → Pages
2. Is the page connected to this Business Manager?
3. Do you have admin access to the page?

### "Campaign objective options look different"

Meta updates the UI frequently. Current objectives (2025):
- **Awareness** → OUTCOME_AWARENESS
- **Traffic** → OUTCOME_TRAFFIC
- **Engagement** → OUTCOME_ENGAGEMENT
- **Leads** → OUTCOME_LEADS
- **App promotion** → OUTCOME_APP_PROMOTION
- **Sales** → OUTCOME_SALES

---

## Quick Links

| Tool | URL |
|------|-----|
| Ads Manager | facebook.com/adsmanager |
| Events Manager | facebook.com/events_manager |
| Business Settings | business.facebook.com/settings |
| Audiences | facebook.com/adsmanager/audiences |
| Billing | business.facebook.com/billing |
| Creative Hub | facebook.com/ads/creativehub |
| Ad Library | facebook.com/ads/library |
