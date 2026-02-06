<#
perplexity.ps1
Global wrapper script to run Perplexity queries from any terminal.

Usage:
  perplexity "your query here"
  or simply: perplexity
#>
param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$repoPath = "C:\miguel\perplexity"

# Join remaining arguments into a single prompt string
$prompt = $Arguments -join " "

if (-not (Test-Path $repoPath)) {
    Write-Error "Perplexity repository not found at $repoPath"
    exit 1
}

Set-Location $repoPath

# Call the build_perplexity.ps1 script with the prompt
if ([string]::IsNullOrWhiteSpace($prompt)) {
    # No arguments provided, run interactively
    & ".\scripts\build_perplexity.ps1"
} else {
    # Arguments provided, pass them through
    # Note: This requires modifying build_perplexity.ps1 to accept a -Prompt parameter
    Write-Host "Querying: $prompt" -ForegroundColor Cyan
    
    # For now, we'll create a session dir and run the container directly
    $sessionDir = Join-Path $repoPath ".perplexity"
    if (-not (Test-Path $sessionDir)) {
        New-Item -ItemType Directory -Path $sessionDir | Out-Null
    }
    
    $dockerArgs = @(
        "run", "--rm", "-it",
        "--env-file", ".env",
        "-v", "$($sessionDir):/root/.perplexity",
        "-w", "/app",
        "perplexity-api",
        "python", "-m", "src.query",
        $prompt
    )
    
    docker @dockerArgs
}
