$ProjectDir = "C:\Users\USER\Documents\Github\skalday-autonews"
$LogFile = "$ProjectDir\logs\scheduler.log"
$Python = "C:\Users\USER\AppData\Local\Programs\Python\Python313\python.exe"

New-Item -ItemType Directory -Force -Path "$ProjectDir\logs" | Out-Null

$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# 只在 21:00–23:59 之間執行，超過 00:00 跳過
$Hour = (Get-Date).Hour
if ($Hour -lt 21) {
    Add-Content -Path $LogFile -Value "[$Timestamp] Outside execution window (after midnight), skipping."
    exit 0
}

Add-Content -Path $LogFile -Value ""
Add-Content -Path $LogFile -Value "=== Run started at $Timestamp ==="

Set-Location $ProjectDir

try {
    & $Python run.py 2>&1 | Tee-Object -FilePath $LogFile -Append
    $ExitCode = $LASTEXITCODE
    $EndTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $LogFile -Value "=== Run finished at $EndTime (exit code: $ExitCode) ==="
} catch {
    Add-Content -Path $LogFile -Value "ERROR: $_"
}
