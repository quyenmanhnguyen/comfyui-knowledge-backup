param(
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"

$ComfyRoot = "C:\AI\ComfyUI"
$Url = "http://127.0.0.1:8188"
$Port = 8188
$LogDir = "C:\AI\logs"
$OutLog = Join-Path $LogDir "comfyui_start.out.log"
$ErrLog = Join-Path $LogDir "comfyui_start.err.log"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
Remove-Item (Join-Path $LogDir ".manual_stop") -Force -ErrorAction SilentlyContinue
Set-Location $ComfyRoot

function Test-ComfyApi {
    try {
        Invoke-WebRequest "$Url/system_stats" -UseBasicParsing -TimeoutSec 2 | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Get-ComfyProcess {
    Get-CimInstance Win32_Process |
        Where-Object {
            $_.CommandLine -match 'python.*ComfyUI\\main.py|python.*ComfyUI/main.py' -and
            $_.CommandLine -match [regex]::Escape($ComfyRoot)
        }
}

if (Test-ComfyApi) {
    Write-Host "ComfyUI is already running: $Url"
    if (-not $NoBrowser) { Start-Process $Url }
    exit 0
}

$portOwner = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
if ($portOwner) {
    $owner = Get-Process -Id $portOwner.OwningProcess -ErrorAction SilentlyContinue
    Write-Host "Port $Port is already used by PID $($portOwner.OwningProcess) $($owner.ProcessName)."
    Write-Host "Use C:\AI\STOP_COMFYUI.bat, then start again."
    exit 1
}

$old = Get-ComfyProcess
if ($old) {
    Write-Host "Old ComfyUI process exists but API is not ready. Stopping stale process..."
    $old | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
    Start-Sleep -Seconds 2
}

$env:TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL = "1"
$args = @(
    "-s", "ComfyUI\main.py",
    "--windows-standalone-build",
    "--listen", "127.0.0.1",
    "--port", "$Port",
    "--disable-auto-launch",
    "--use-pytorch-cross-attention"
)

Write-Host "Starting ComfyUI..."
$p = Start-Process -FilePath "C:\AI\python_embeded\python.exe" -ArgumentList $args -WorkingDirectory "C:\AI" -RedirectStandardOutput $OutLog -RedirectStandardError $ErrLog -PassThru -WindowStyle Hidden

for ($i = 0; $i -lt 90; $i++) {
    Start-Sleep -Seconds 2
    if (Test-ComfyApi) {
        Write-Host "ComfyUI ready: $Url"
        if (-not $NoBrowser) { Start-Process $Url }
        exit 0
    }
    if ($p.HasExited) {
        Write-Host "ComfyUI exited early. Check logs:"
        Write-Host $OutLog
        Write-Host $ErrLog
        exit 1
    }
}

Write-Host "ComfyUI is still starting. Check logs:"
Write-Host $OutLog
Write-Host $ErrLog
exit 2
