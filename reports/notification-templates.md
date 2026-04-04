# Enzo Health — Notification Templates
**For engineering reference — daily alert system**

---

## Daily Email Digest (7:00 AM — sent to DON + Admin)

**Subject:** `[Sunrise Home Health] Enzo Daily Brief — 3 items need attention · Apr 4`

---

**Good morning, [Name].**
Here's what needs your attention today at Sunrise Home Health.

---

**🔴 CRITICAL — Act Today (3 items)**

**1. LUPA Risk: Robert Davis (PT-2003)**
PT needs 1 more visit by Apr 9 to avoid a payment reduction of ~$2,800.
→ Contact scheduling coordinator immediately

**2. Recertification Order Needed: Margaret Chen (PT-2001)**
Certification expires Apr 12. Case conference note is ready — physician signature needed.
→ Send to Dr. [Physician] today

**3. High Audit Risk Note: PT-007 Ambulation visit**
Note scored 2/5 — would not survive ADR review. Correction needed before month end.
→ Review QA feedback and coach clinician

---

**🟡 IMPORTANT — This Week (2 items)**

- Case conference needed for Robert Williams (PT-2002) — cert ends Apr 9
- OASIS correction pending for PT-2003 ADL variance — document before billing

---

**📊 Your Survey Readiness Score: 78/100 — Moderate Risk**
Trending up +4 points over the last 7 days. Open deficiencies domain needs attention.

---

[View full dashboard →]  [Mark all as reviewed →]  [Notification settings →]

*Enzo Health · Unsubscribe · Sent daily at 7:00 AM*

---

## Slack Alert — CRITICAL (real-time)

**Channel:** `#enzo-alerts` or direct message to DON

```
🚨 *LUPA Risk Alert — Sunrise Home Health*

*Patient:* Robert Davis (PT-2003)
*Issue:* PT visit frequency behind — 3/4 required visits completed
*Days remaining in period:* 6
*Payment at risk:* ~$2,800

*Action needed:* Schedule 1 PT visit before Apr 9
*Contact:* Angela Torres (PT) — schedule coordinator

<View scheduling report | Dismiss>
```

---

## Slack Alert — IMPORTANT (daily digest, end of day)

**Channel:** `#enzo-ops`

```
📋 *Enzo Daily Summary — Sunrise Home Health*
*April 4, 2026*

✅ Survey Readiness: 78/100 (+4 this week)
⚠️ 2 patients need visits scheduled this week
💰 Revenue on track: $21,364 (3 active episodes)
📥 1 referral needs follow-up (conditional accept)

*Full action list:* [View dashboard →]
```

---

## Notification Routing Logic (for engineering)

| Event | Urgency | DON Channel | Admin Channel |
|---|---|---|---|
| LUPA risk, <5 days | Critical | Slack + Email | Slack + Email |
| Cert expiring <3 days, no order | Critical | Slack + Email | Email |
| Note scored 1–2/5 | Critical | Slack | — |
| Open deficiency due <3 days | Critical | Slack + Email | Slack + Email |
| LUPA risk, 5–10 days | Important | Daily digest | Daily digest |
| Conditional referral >48 hrs | Important | — | Daily digest |
| Clinician performance flag | Important | Daily digest | Daily digest |
| OASIS correction pending | Important | Daily digest | — |
| New regulatory digest | FYI | Weekly summary | — |
| Quality indicator shift >2% | FYI | Weekly summary | Weekly summary |
| PIP milestone due | FYI | Weekly summary | Weekly summary |

**Send times:**
- Critical Slack alerts: immediately when detected (overnight agent run completes ~6:45 AM)
- Daily email digest: 7:00 AM agency local time
- Weekly summary: Monday 8:00 AM

---

## Agency Configuration (per-agency settings needed in DB)

```json
{
  "agency_id": "SUNRISE",
  "notifications": {
    "don_email": "don@sunrisehomehealth.com",
    "admin_email": "admin@sunrisehomehealth.com",
    "slack_webhook": "https://hooks.slack.com/...",
    "slack_channel_critical": "#enzo-alerts",
    "slack_channel_ops": "#enzo-ops",
    "digest_time": "07:00",
    "timezone": "America/New_York",
    "critical_slack_enabled": true,
    "critical_email_enabled": true,
    "digest_email_enabled": true,
    "weekly_summary_enabled": true
  }
}
```
