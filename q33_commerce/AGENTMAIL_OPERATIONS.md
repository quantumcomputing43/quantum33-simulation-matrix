# AgentMail operations — Q33 Commerce / VELTRIX

## Current verified state (2026-10-11)

- Sending inbox: `veltrix@agentmail.to` (display name: VELTRIX).
- Owner/test address: `baddiayoub1266@gmail.com`.
- Outbound smoke test: sent subject `VELTRIX / AgentMail — test message`; AgentMail returned a message ID.
- Inbound smoke test: the owner replied `Okay`; that reply is visible in the AgentMail thread. This confirms the send-and-reply path for this test account.
- External company outreach: **NONE SENT**.
- AgentMail's human-attachment tool reported that verification is not required for the selected organization. This does not guarantee inbox placement or delivery to every recipient.
- No API key or credentials are stored in this repository.

## Safe operating procedure

1. Select one prospect from the appropriate Q33 prospect file.
2. Require its state to be `READY_FOR_HUMAN_REVIEW` (or equivalent) only after a current public contact route and a specific, dated, source-backed issue are checked. A directory listing alone is not a reason to contact.
3. Keep the first message individual and factual. Do not claim lost revenue, lost bookings, or a confirmed business problem unless the company has confirmed it.
4. Show the exact recipient, subject, and complete message to the owner and obtain explicit approval **for that specific send**.
5. Send one message only after approval. No bulk send, automated prospect campaign, guessed email address, or unsolicited repeated follow-up.
6. Log the sent date, channel, recipient, approved message, message/thread ID, and response in the relevant prospect record. Start the seven-day validation window only after a valid first outreach.
7. Honor a rejection or opt-out immediately. Never request passwords, payment credentials, or access to the prospect's hosting/domain account.
8. Never send company messages merely because the connector can send email; technical capability is not authorization.

## Message template (draft only; not sent)

Subject: Question about your online service information

Salam,

I’m reaching out from VELTRIX. I was reviewing the public information available for your business and noticed the following item: [insert one specific, currently verified observation and source/date].

Would improving this part of the mobile experience be useful to your team? If it is relevant, I can share a small, clearly scoped proposal for a mobile-friendly service/contact page. This would not involve changes to your existing domain, hosting, or booking/payment systems, and I would not promise traffic or sales.

If this is not relevant, no problem; I will not follow up.

Best regards,
VELTRIX

## Current prospect restriction

Bounty Tours remains `HOLD_RESEARCH`: its retrieved website-suspension evidence may be stale and the public directory contact details have not been independently confirmed as current. Do not send to Bounty Tours until a fresh check confirms the issue and contact route, then obtain explicit owner approval of the final message.

## Manual operation note

The current setup is an AgentMail inbox operated through the connected AgentMail tool. This repository does not yet contain a deployed mail-sending service or an AgentMail API secret. GitHub Actions must not send real mail. Keep the workflow manual and human-approved.
