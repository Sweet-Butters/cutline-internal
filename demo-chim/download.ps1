<#
.SYNOPSIS
Restores the original and human edit to their demo-chim project paths.
.PARAMETER Python
Python with yt-dlp installed. Defaults to the internal repository's Windows venv.
.PARAMETER DryRun
Lists the public source, destination and planned action without downloading or writing.
.EXAMPLE
.\download.ps1 -DryRun
.EXAMPLE
.\download.ps1 -Python 'C:\Tools\Python\python.exe'
#>
[CmdletBinding()]
param(
    [string]$Python,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
if (!$Python) {
    $Python = Join-Path (Split-Path $PSScriptRoot -Parent) '.venv/Scripts/python.exe'
}
$media = @(
    @{ Path = 'sources/original.mp4'; Url = 'https://www.youtube.com/watch?v=wnXAkjgVELc' }
    @{ Path = 'reference/human_edit.mp4'; Url = 'https://www.youtube.com/watch?v=GVHagGsmLck' }
)
$format = 'bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/bv*[height<=720]+ba/b[height<=720]'

foreach ($item in $media) {
    $target = Join-Path $PSScriptRoot $item.Path
    if (Test-Path -LiteralPath $target -PathType Leaf) {
        Write-Output "Keep existing $target"
        if ($DryRun) { Write-Output "Source: $($item.Url)" }
        continue
    }
    if ($DryRun) {
        Write-Output "Would download $($item.Url) to $target (up to 720p, MP4)"
        continue
    }

    $directory = [IO.Path]::GetDirectoryName($target)
    [void][IO.Directory]::CreateDirectory($directory)
    $staging = Join-Path $directory ([guid]::NewGuid().ToString('N') + '.part')
    [void][IO.Directory]::CreateDirectory($staging)
    try {
        $arguments = @(
            '-m', 'yt_dlp', '--ignore-config', '--no-overwrites', '--no-playlist',
            '--quiet', '--no-warnings', '--no-cache-dir', '--js-runtimes', 'node',
            '--remote-components', 'ejs:github', '-f', $format,
            '--merge-output-format', 'mp4', '--remux-video', 'mp4',
            '-P', $staging, '-o', 'video.%(ext)s', '--', $item.Url
        )
        Write-Output "Downloading $($item.Path)"
        $pythonCommand = Get-Command $Python -CommandType Application,ExternalScript | Select-Object -First 1
        $exitCode = & {
            # Windows PowerShell treats redirected native stderr as error records.
            $ErrorActionPreference = 'Continue'
            & $pythonCommand @arguments *> $null
            $LASTEXITCODE
        }
        if ($exitCode -ne 0) {
            throw "yt-dlp failed for $($item.Path) (exit $exitCode). Check yt-dlp, Node, ffmpeg, and source availability."
        }
        $finished = Join-Path $staging 'video.mp4'
        try {
            [IO.File]::Move($finished, $target)
            Write-Output "Restored $target"
        } catch [IO.IOException] {
            if (!(Test-Path -LiteralPath $target -PathType Leaf)) { throw }
            Write-Output "Keep existing $target"
        }
    } finally {
        $resolved = (Resolve-Path -LiteralPath $staging).ProviderPath
        if ([IO.Path]::GetDirectoryName($resolved) -eq $directory -and [IO.Path]::GetFileName($resolved) -match '^[a-f0-9]{32}\.part$') {
            Remove-Item -LiteralPath $resolved -Recurse -Force
        }
    }
}
