param(
    [Parameter(Mandatory = $true)]
    [string]$TargetDir
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

$PortableDir = Join-Path $TargetDir "py"
$BuildDir = Join-Path $env:TEMP "biblical_py_build"
$PythonVersion = "3.12.9"
$EmbedUrl = "https://www.python.org/ftp/python/$PythonVersion/python-${PythonVersion}-embed-amd64.zip"
$GetPipUrl = "https://bootstrap.pypa.io/get-pip.py"
$EmbedZip = Join-Path $env:TEMP "python-${PythonVersion}-embed-amd64.zip"
$GetPipScript = Join-Path $env:TEMP "get-pip.py"

# Skip if already installed and working
if (Test-Path (Join-Path $PortableDir "python.exe")) {
    Write-Host "[OK] Portable Python already exists at $PortableDir"
    & (Join-Path $PortableDir "python.exe") -c "import fastapi, uvicorn; print('verified')" 2>$null
    if ($LASTEXITCODE -eq 0) {
        return
    }
    Write-Host "[INFO] Existing installation incomplete, rebuilding..."
}

# Clean build dir
if (Test-Path $BuildDir) { Remove-Item -Recurse -Force $BuildDir -ErrorAction SilentlyContinue }

Write-Host "[INFO] Downloading Portable Python $PythonVersion embed amd64..."
try {
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
    (New-Object System.Net.WebClient).DownloadFile($EmbedUrl, $EmbedZip)
    Write-Host "[INFO] Download complete."
} catch {
    Write-Host "[WARN] Download failed: $_"
    return
}

Write-Host "[INFO] Extracting to $BuildDir..."
try {
    Expand-Archive -LiteralPath $EmbedZip -DestinationPath $BuildDir -Force
} catch {
    Write-Host "[WARN] Extraction failed: $_"
    return
}

$PyExe = Join-Path $BuildDir "python.exe"
if (-not (Test-Path $PyExe)) {
    Write-Host "[WARN] python.exe not found after extraction"
    return
}

# Enable site-packages
$PthFiles = Get-ChildItem (Join-Path $BuildDir "python*._pth") -ErrorAction SilentlyContinue
foreach ($pf in $PthFiles) {
    $content = Get-Content $pf.FullName -Raw
    $content = $content -replace '#import site', 'import site'
    Set-Content $pf.FullName -Value $content
    Write-Host "[INFO] Modified $($pf.Name) - site-packages enabled"
}

# Verify site-packages
$result = & $PyExe -c "import site; print('OK')" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARN] Failed to enable site-packages"
}

Write-Host "[INFO] Downloading get-pip.py..."
try {
    (New-Object System.Net.WebClient).DownloadFile($GetPipUrl, $GetPipScript)
} catch {
    Write-Host "[WARN] Failed to download get-pip.py: $_"
}

if (Test-Path $GetPipScript) {
    Write-Host "[INFO] Installing pip..."
    & $PyExe $GetPipScript "--no-warn-script-location" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[INFO] Pip installed."
        & $PyExe -m pip --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[INFO] Installing Python dependencies (backend only)..."
            & $PyExe -m pip install requests python-dotenv fastapi uvicorn fpdf2 cryptography --no-warn-script-location 2>$null
            if ($LASTEXITCODE -ne 0) {
                Write-Host "[WARN] pip install exit code $LASTEXITCODE (may be due to long paths, but core packages may still work)"
            } else {
                Write-Host "[INFO] pip install completed successfully."
            }
        }
    } else {
        Write-Host "[WARN] pip installation failed"
    }
}

# Copy to final target
Write-Host "[INFO] Copying portable Python to $PortableDir..."
if (-not (Test-Path $PortableDir)) { New-Item -ItemType Directory -Path $PortableDir -Force | Out-Null }
$robocopyArgs = @($BuildDir, $PortableDir, "/E", "/COPY:DAT", "/R:3", "/W:5", "/NDL", "/NFL", "/NJH")
$rc = Start-Process -NoNewWindow -Wait -PassThru -FilePath "robocopy" -ArgumentList $robocopyArgs
$exitCode = $rc.ExitCode
if ($exitCode -ge 8) {
    Write-Host "[WARN] robocopy exit code $exitCode — some non-critical files may be missing"
} else {
    Write-Host "[INFO] robocopy completed (code $exitCode)."
}

# Verify final installation
$finalPy = Join-Path $PortableDir "python.exe"
if (-not (Test-Path $finalPy)) {
    Write-Host "[WARN] Copy failed entirely. Portable Python not available."
    return
}

& $finalPy -c "import fastapi, uvicorn; print('OK')" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Portable Python ready — fastapi/uvicorn verified."
} else {
    Write-Host "[WARN] Portable Python validation failed (missing packages). Will rely on PYTHONPATH fallback."
}

# Strip __pycache__ and .pyc to prevent WiX light.exe from choking on missing cache files
Get-ChildItem -Path $PortableDir -Recurse -Directory -Filter __pycache__ -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path $PortableDir -Recurse -Filter *.pyc -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue

# Cleanup
if (Test-Path $BuildDir) { Remove-Item -Recurse -Force $BuildDir -ErrorAction SilentlyContinue }
if (Test-Path $EmbedZip) { Remove-Item -Force $EmbedZip -ErrorAction SilentlyContinue }
if (Test-Path $GetPipScript) { Remove-Item -Force $GetPipScript -ErrorAction SilentlyContinue }
