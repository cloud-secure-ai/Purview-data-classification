# Where do we start with data classification?

Companion files for the five-part series on [cloud-secure.ai](https://cloud-secure.ai/) by Seán O'Farrell. The series uses the Microsoft Purview Data Security Posture Agent (preview) to discover what an organisation holds, then turns the findings into sensitive information types (SITs), a trainable classifier and a DLP policy in simulation mode.

All data in the series is fictional and was created in a Microsoft CDX demo tenant.

| Folder | What it is | Part |
|---|---|---|
| `seed-content/make_seed.py` | Generates fictional positive (design specifications) and negative (business documents, including hard negatives) seed files | 4 |
| `sharepoint/Upload-ClassifierSeed.ps1` | Uploads seed files to dedicated SharePoint folders with PnP PowerShell | 4 |
| `sit-test/` | SIT definitions and a test file with real and decoy references | 3 |
| `audit/Export-PostureAgentAudit.ps1` | Exports unified audit log records as evidence | 5 |
| `CHECKLIST.md` | Prerequisites, cost controls and teardown | 2, 5 |

## Quick start

```bash
pip install python-docx
python seed-content/make_seed.py --out ./seed --positive 60 --negative 160
```

```powershell
.\sharepoint\Upload-ClassifierSeed.ps1 -SiteUrl https://<tenant>.sharepoint.com/sites/ClassifierSeed -SeedPath .\seed -ClientId <app-id>
```

## Credit

Written by Seán O'Farrell - [cloud-secure.ai](https://cloud-secure.ai/)
