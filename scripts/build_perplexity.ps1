<#
build_perplexity.ps1
Builds the Docker image for the `perplexity` project and leaves the console open.
Usage:
  powershell -ExecutionPolicy Bypass -File .\scripts\build_perplexity.ps1
  or double-click the shortcut created by `create_shortcut.ps1`.
#>
param(
    [string]$Repo = "C:\miguel\perplexity",
    [string]$ImageName = "perplexity-api"
)

if (-not (Test-Path $Repo)) {
    Write-Error "Repository path '$Repo' not found. Update the script or provide -Repo parameter."
    exit 1
}

Set-Location $Repo

Write-Host "Building Docker image '$ImageName' from $Repo" -ForegroundColor Cyan

try {
    docker build -t $ImageName .
    $rc = $LASTEXITCODE
} catch {
    Write-Error "Docker build failed: $_"
    exit 1
}

if ($rc -eq 0) {
    Write-Host "Build succeeded." -ForegroundColor Green

    while ($true) {
        $prompt = Read-Host "Enter prompt to send to Perplexity (leave empty to finish)"
        if ([string]::IsNullOrWhiteSpace($prompt)) {
            break
        }

        Write-Host "Querying: $prompt" -ForegroundColor Cyan

        # Run the container using the environment python binary so arguments work reliably
        # Use -it to allocate a TTY so the script prefers argv over empty stdin
        docker run --rm -it --env-file .env --entrypoint /opt/conda/envs/appenv/bin/python $ImageName /app/src/query.py "$prompt"

        if ($LASTEXITCODE -ne 0) {
            Write-Warning "docker run exited with code $LASTEXITCODE"
        }

        Write-Host ""
    }

    Write-Host "Done." -ForegroundColor Green
} else {
    Write-Host "Build failed (exit code $rc)." -ForegroundColor Red
}

Read-Host "Press Enter to close"
