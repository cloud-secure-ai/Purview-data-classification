<#
.SYNOPSIS
    Uploads classifier seed content to dedicated positive and negative folders in a SharePoint site.

.DESCRIPTION
    Uploads the output of make_seed.py (or your own example files) to a SharePoint site for
    training a Microsoft Purview custom trainable classifier. Positive and negative samples go
    into separate folders, each used only for seed content. Existing files are skipped unless
    -Overwrite is used. Supports -WhatIf.

.PARAMETER SiteUrl
    The SharePoint site, for example https://contoso.sharepoint.com/sites/ClassifierSeed

.PARAMETER SeedPath
    Folder containing 'positive' and 'negative' sub-folders.

.PARAMETER Library
    Document library name. Default: Shared Documents

.PARAMETER PositiveFolder / NegativeFolder
    Target folder names. Default: DesignSpecs-Positive / DesignSpecs-Negative

.PARAMETER ClientId
    Entra ID app (client) ID registered for PnP PowerShell interactive sign-in.

.EXAMPLE
    .\Upload-ClassifierSeed.ps1 -SiteUrl https://contoso.sharepoint.com/sites/ClassifierSeed -SeedPath .\seed -ClientId <app-id> -WhatIf

.NOTES
    Author:   Seán O'Farrell
    Website:  https://cloud-secure.ai/
    Requires: PnP.PowerShell 2.x or later, Sites.FullControl delegated consent on the site
    Series:   Where do we start with data classification? Part 4
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)][string]$SiteUrl,
    [Parameter(Mandatory)][string]$SeedPath,
    [Parameter(Mandatory)][string]$ClientId,
    [string]$Library = 'Shared Documents',
    [string]$PositiveFolder = 'DesignSpecs-Positive',
    [string]$NegativeFolder = 'DesignSpecs-Negative',
    [switch]$Overwrite
)

$ErrorActionPreference = 'Stop'
$counts = @{ Uploaded = 0; Skipped = 0; Failed = 0 }

try {
    Write-Host "🔐 Connecting to $SiteUrl" -ForegroundColor Cyan
    Connect-PnPOnline -Url $SiteUrl -ClientId $ClientId -Interactive

    foreach ($pair in @(@{ Local = 'positive'; Remote = $PositiveFolder }, @{ Local = 'negative'; Remote = $NegativeFolder })) {
        $localDir = Join-Path $SeedPath $pair.Local
        if (-not (Test-Path $localDir)) { Write-Warning "⚠️ $localDir not found, skipping"; continue }

        $target = "$Library/$($pair.Remote)"
        if (-not (Get-PnPFolder -Url $target -ErrorAction SilentlyContinue)) {
            if ($PSCmdlet.ShouldProcess($target, 'Create folder')) {
                Resolve-PnPFolder -SiteRelativePath $target | Out-Null
                Write-Host "📁 Created $target" -ForegroundColor Green
            }
        }

        $existing = @()
        try { $existing = (Get-PnPFolderItem -FolderSiteRelativeUrl $target -ItemType File).Name } catch { }

        foreach ($file in Get-ChildItem $localDir -File) {
            if (-not $Overwrite -and $existing -contains $file.Name) { $counts.Skipped++; continue }
            if ($PSCmdlet.ShouldProcess("$target/$($file.Name)", 'Upload')) {
                try {
                    Add-PnPFile -Path $file.FullName -Folder $target | Out-Null
                    $counts.Uploaded++
                } catch {
                    Write-Warning "❌ $($file.Name): $($_.Exception.Message)"
                    $counts.Failed++
                }
            }
        }
    }
}
catch {
    Write-Error "❌ $($_.Exception.Message)"
}
finally {
    Write-Host "`n📊 Uploaded: $($counts.Uploaded)  Skipped: $($counts.Skipped)  Failed: $($counts.Failed)" -ForegroundColor Cyan
    Write-Host "⏳ Wait at least an hour for indexing before creating the classifier." -ForegroundColor Yellow
}
