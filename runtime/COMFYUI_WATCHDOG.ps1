$ErrorActionPreference = 'Continue'
$Url = 'http://127.0.0.1:8188'
$ComfyRoot = 'C:\AI\ComfyUI'
$LogDir = 'C:\AI\logs'
$StopFlag = Join-Path $LogDir '.manual_stop'
$WdLog = Join-Path $LogDir 'comfyui_watchdog.log'
$MaxRestarts = 2
$CheckEverySec = 60
$StableAfterMin = 10

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Write-Log([string]$msg) {
    $line = '{0} {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $msg
    Add-Content -Path $WdLog -Value $line
}

function Test-ComfyApi {
    try {
        Invoke-WebRequest "$Url/system_stats" -UseBasicParsing -TimeoutSec 3 | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Get-ComfyProcess {
    Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
        Where-Object {
            $_.CommandLine -match 'python.*ComfyUI[\\/]main\.py' -and
            $_.CommandLine -match [regex]::Escape($ComfyRoot)
        }
}

Write-Log 'watchdog started'
$restarts = 0
$lastStartTime = $null

# Initial ensure-start (no duplicate: START_COMFYUI.ps1 exits if API already up)
if (-not (Test-Path $StopFlag) -and -not (Test-ComfyApi)) {
    Write-Log 'initial start requested'
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File 'C:\AI\START_COMFYUI.ps1' -NoBrowser | Out-Null
    $lastStartTime = Get-Date
}

while ($true) {
    Start-Sleep -Seconds $CheckEverySec

    if (Test-Path $StopFlag) {
        # user stopped on purpose: stay dormant, never restart
        continue
    }

    if (Test-ComfyApi) {
        # reset crash counter after a stable period
        if ($restarts -gt 0 -and $lastStartTime -and ((Get-Date) - $lastStartTime).TotalMinutes -ge $StableAfterMin) {
            Write-Log "stable for $StableAfterMin min, reset restart counter (was $restarts)"
            $restarts = 0
        }
        continue
    }

    $proc = Get-ComfyProcess
    if ($proc) {
        # process alive but API not ready yet (startup in progress)
        continue
    }

    # process is gone without manual stop -> crash or unexpected exit
    if ($restarts -ge $MaxRestarts) {
        Write-Log "crash detected but restart limit ($MaxRestarts) reached; waiting for manual intervention"
        # keep loop dormant until flag or process state changes; avoid restart loop
        while (-not (Test-Path $StopFlag) -and -not (Get-ComfyProcess)) {
            Start-Sleep -Seconds $CheckEverySec
        }
        $restarts = 0
        continue
    }

    $restarts += 1
    Write-Log "crash detected, restarting (attempt $restarts of $MaxRestarts)"
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File 'C:\AI\START_COMFYUI.ps1' -NoBrowser | Out-Null
    $lastStartTime = Get-Date
}
