<#
.SYNOPSIS
    Exports recent unified audit log records to CSV as evidence of Posture Agent and classifier activity.

.DESCRIPTION
    Runs Search-UnifiedAuditLog over a time window and exports the results. Optionally filters to
    record types relevant to the series (Security Copilot, compliance RBAC checks, DLP and
    sensitive information type changes). Audit ingestion must already be on; it is not retroactive.

.PARAMETER Days
    How many days back to search. Default: 2

.PARAMETER OutFile
    CSV path. Default: .\audit-posture-agent.csv

.PARAMETER RecordTypes
    Optional record types to filter on, for example CopilotInteraction, SecurityComplianceRBAC.

.EXAMPLE
    Connect-ExchangeOnline
    .\Export-PostureAgentAudit.ps1 -Days 3

.NOTES
    Author:   Seán O'Farrell
    Website:  https://cloud-secure.ai/
    Requires: ExchangeOnlineManagement 3.x, View-Only Audit Logs or Audit Logs role
    Gotcha:   -SessionCommand ReturnLargeSet without -SessionId fails with BadRequest. Not used here
              (5,000 record limit per call).
    Series:   Where do we start with data classification? Part 5
#>
[CmdletBinding()]
param(
    [int]$Days = 2,
    [string]$OutFile = '.\audit-posture-agent.csv',
    [string[]]$RecordTypes
)

$ErrorActionPreference = 'Stop'
try {
    $cfg = Get-AdminAuditLogConfig
    if (-not $cfg.UnifiedAuditLogIngestionEnabled) {
        Write-Warning "⚠️ Unified audit log ingestion is off. Enable it first:"
        Write-Host  "   Enable-OrganizationCustomization   # if the org is dehydrated"
        Write-Host  "   Set-AdminAuditLogConfig -UnifiedAuditLogIngestionEnabled `$true"
        return
    }

    $start = (Get-Date).ToUniversalTime().AddDays(-$Days)
    $end   = (Get-Date).ToUniversalTime()
    Write-Host "🔎 Searching $start to $end (UTC)" -ForegroundColor Cyan

    $params = @{ StartDate = $start; EndDate = $end; ResultSize = 5000 }
    if ($RecordTypes) { $params.RecordType = $RecordTypes }
    $results = Search-UnifiedAuditLog @params

    if (-not $results) { Write-Host "ℹ️ No records found."; return }

    $results |
        Select-Object CreationDate, UserIds, RecordType, Operations, AuditData |
        Export-Csv $OutFile -NoTypeInformation -Encoding UTF8

    Write-Host "✅ Exported $($results.Count) records to $OutFile" -ForegroundColor Green
    $results | Group-Object RecordType | Sort-Object Count -Descending |
        Format-Table @{ n = 'RecordType'; e = { $_.Name } }, Count -AutoSize
}
catch {
    Write-Error "❌ $($_.Exception.Message)"
}
