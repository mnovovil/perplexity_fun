<#
setup_perplexity_global.ps1
Sets up the global `px` command by adding it to your PowerShell profile.

Usage (run in an elevated or normal PowerShell):
  powershell -ExecutionPolicy Bypass -File .\scripts\setup_perplexity_global.ps1
#>

$perplexityScriptPath = "C:\miguel\perplexity\scripts\perplexity.ps1"

if (-not (Test-Path $perplexityScriptPath)) {
    Write-Error "Perplexity script not found at: $perplexityScriptPath"
    exit 1
}

# Get the current user's PowerShell profile path
$profilePath = $PROFILE

# Create profile directory if it doesn't exist
$profileDir = Split-Path -Parent $profilePath
if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    Write-Host "Created profile directory: $profileDir" -ForegroundColor Green
}

# Function to add to profile
$functionCode = @"

# ===== Perplexity CLI =====
# Global command to run Perplexity queries from anywhere
function px {
    param(
        [Parameter(ValueFromRemainingArguments=`$true)]
        [string[]]`$Arguments
    )
    & "$perplexityScriptPath" @Arguments
}

# Or, if you prefer a one-liner alias instead of a function:
# Set-Alias -Name px -Value "$perplexityScriptPath"

"@

# Check if the function is already in the profile
if (Test-Path $profilePath) {
    $profileContent = Get-Content $profilePath -Raw
    if ($profileContent -match "function px") {
        Write-Host "px function already exists in profile." -ForegroundColor Yellow
        $addToProfile = Read-Host "Overwrite existing profile entry? (y/n)"
        if ($addToProfile -ne 'y') {
            Write-Host "Setup cancelled." -ForegroundColor Yellow
            exit 0
        }
    }
}

# Backup existing profile if it exists
if (Test-Path $profilePath) {
    $backupPath = "$profilePath.backup"
    Copy-Item $profilePath $backupPath
    Write-Host "Created backup of existing profile at: $backupPath" -ForegroundColor Green
}

# Add the function to the profile (append if file exists, create if not)
Add-Content -Path $profilePath -Value $functionCode -Encoding UTF8

Write-Host "PowerShell profile updated successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "The 'px' command is now available in all PowerShell terminals." -ForegroundColor Cyan
Write-Host ""
Write-Host "Usage:" -ForegroundColor Yellow
Write-Host "  px 'your query here'" -ForegroundColor White
Write-Host "  or"
Write-Host "  px (for interactive mode)" -ForegroundColor White
Write-Host ""
Write-Host "Note: You may need to restart PowerShell or run the following to reload the profile:" -ForegroundColor Yellow
Write-Host "  . `$PROFILE" -ForegroundColor White
