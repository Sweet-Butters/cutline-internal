$ErrorActionPreference='Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$env:TEMP="$PWD\tmp"
$env:TMP=$env:TEMP
$timer=[Diagnostics.Stopwatch]::StartNew()
& .\.venv\Scripts\python.exe -m yt_dlp --ignore-config --cache-dir .cache/yt-dlp --js-runtimes node --remote-components ejs:github --no-playlist -f 'bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/bv*[height<=720]+ba/b[height<=720]' --merge-output-format mp4 --write-info-json -o 'project/reference/human_edit.%(ext)s' 'https://www.youtube.com/watch?v=GVHagGsmLck' *> logs/download.log
$code=$LASTEXITCODE
@{exit_code=$code;seconds=$timer.Elapsed.TotalSeconds} | ConvertTo-Json | Set-Content logs/download-timing.json
Get-Content logs/download.log -Tail 20
exit $code

