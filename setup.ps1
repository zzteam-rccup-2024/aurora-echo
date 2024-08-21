$OS = Get-CimInstance Win32_OperatingSystem | Select-Object -ExpandProperty Caption

if ($OS -notlike "*Windows*") {
    Write-Host "This script is designed for Windows."
    exit 1
}

# Install PortAudio on Windows, if needed
$portAudioPath = "C:\Program Files\PortAudio"
if (Test-Path $portAudioPath) {
    Write-Host "PortAudio is already installed."
} else {
    Write-Host "Please manually install PortAudio for Windows."
}

# Install Python dependencies
pip install -r requirements.txt
pip install uvicorn
pip install 'httpx[socks]'
python -m spacy download en_core_web_sm

# Check URL accessibility
try {
    $response = Invoke-WebRequest -Uri "https://aurora-echo.zzdev.org" -Method Head -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "URL is accessible. You can open the client by visiting https://aurora-echo.zzdev.org."
    }
} catch {
    Write-Host "URL is not accessible. Please use python -m http.server -d ./data/client to serve the client."
}

Write-Host "Setup complete. You can now run the server by executing 'uvicorn main:app --reload' in the release directory."
