# Prerequisites, cost controls and teardown

## Before you create any hourly capacity
- [ ] Purview Audit on and records flowing (days ahead; not retroactive). Dehydrated orgs: `Enable-OrganizationCustomization`, then `Set-AdminAuditLogConfig -UnifiedAuditLogIngestionEnabled $true`. Allow time for replication.
- [ ] Security Copilot: Microsoft 365 E5 inclusion (400 SCUs per 1,000 paid licences per month) or Azure-provisioned capacity.
- [ ] Azure route: role on the subscription is **Active** (not Eligible) and **Contributor** is enough.
- [ ] Security Copilot > Owner > Plugin settings: allow access to Microsoft 365 data.
- [ ] Unified DSPM setup completed; collection policies (pay-as-you-go) reviewed with Edit before Start setup.
- [ ] Roles: compliance roles for summaries; content-level roles (for example Purview Content Analyst) to see matched content.
- [ ] Prompts written and data sources chosen.

## When creating capacity
- [ ] Overage **off** (defaults on, $6 per unit, no limit).
- [ ] "Help improve Copilot" data sharing reviewed (both default on).
- [ ] Every field checked before Create (fields can silently reset).
- [ ] Create at the top of the hour; billing is per clock hour started.
- [ ] Azure budget alert set (alerts warn, they do not stop spending).

## Teardown
- [ ] Delete the Security Copilot capacity (the workspace remains).
- [ ] Delete any Purview pay-as-you-go resource (this unlinks Purview pay-as-you-go billing).
- [ ] Remove elevated access for every account (Entra ID > Properties > Access management for Azure resources).
- [ ] Check Cost analysis after 24 to 48 hours, then cancel or move the subscription.
- [ ] DLP policy left in simulation or deleted.
