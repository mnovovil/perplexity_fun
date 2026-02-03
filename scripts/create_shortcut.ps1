<#
create_shortcut.ps1
Creates a Desktop shortcut that runs the build_perplexity script in PowerShell.
Then attempts to pin the shortcut to the taskbar (best-effort; may require user confirmation).

Usage (run in an elevated or normal PowerShell):
  powershell -ExecutionPolicy Bypass -File .\scripts\create_shortcut.ps1
#>
param(
    [string]$ScriptPath = "C:\miguel\perplexity\scripts\build_perplexity.ps1",
    [string]$ShortcutName = "Build Perplexity",
    [switch]$AttemptPinToTaskbar
)

if (-not (Test-Path $ScriptPath)) {
    Write-Error "Script path not found: $ScriptPath"
    exit 1
}

$desktop = [Environment]::GetFolderPath('Desktop')
$lnkPath = Join-Path $desktop ("$ShortcutName.lnk")

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($lnkPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-NoExit -ExecutionPolicy Bypass -File `"$ScriptPath`""
$shortcut.WorkingDirectory = Split-Path $ScriptPath
$shortcut.IconLocation = "%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe,0"
$shortcut.Save()

Write-Host "Created shortcut on Desktop: $lnkPath" -ForegroundColor Green

if ($AttemptPinToTaskbar) {
    try {
        # Try to pin the shortcut to the taskbar (best-effort)
        $shell = New-Object -ComObject Shell.Application
        $folder = $shell.Namespace((Split-Path $lnkPath))
        $item = $folder.ParseName((Split-Path $lnkPath -Leaf))
        $verbs = $item.Verbs()
        $pinned = $false
        for ($i = 0; $i -lt $verbs.Count; $i++) {
            $verb = $verbs.Item($i)
            $name = $verb.Name -replace '&',''
            if ($name -match 'Pin to.*taskbar|Pin to taskbar|Pin to tas?kbar') {
                $verb.DoIt()
                $pinned = $true
                break
            }
        }
        if ($pinned) {
            Write-Host "Attempted to pin shortcut to taskbar." -ForegroundColor Green
        } else {
            Write-Host "Pin-to-taskbar verb not found; please pin manually by right-clicking the shortcut and selecting 'Pin to taskbar'." -ForegroundColor Yellow
        }
    } catch {
        Write-Warning "Pin attempt failed: $_. Pin manually via the shortcut context menu."
    }
}

Read-Host "Press Enter to close"
