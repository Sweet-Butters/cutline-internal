<#
.SYNOPSIS
Restores and verifies the media listed in the demo's private GitHub release manifest.
.PARAMETER ProjectRoot
Destination demo directory. Defaults to the folder containing this script and its manifest.
.PARAMETER DryRun
Checks existing files and lists missing downloads without contacting GitHub or writing files.
.EXAMPLE
.\restore-github.ps1 -DryRun
#>
[CmdletBinding()]
param([string]$ProjectRoot, [switch]$DryRun)

$ErrorActionPreference = 'Stop'
if (!$ProjectRoot) { $ProjectRoot = $PSScriptRoot }
$root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($ProjectRoot)
$manifest = Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $PSScriptRoot 'media-manifest.json') | ConvertFrom-Json
if ($manifest.version -ne 1 -or $manifest.repository -notmatch '^[\w.-]+/[\w.-]+$' -or
    $manifest.release -notmatch '^[a-z0-9][a-z0-9._-]*$' -or !$manifest.files) {
    throw 'Invalid media release manifest.'
}

function Confirm-Media($path, $entry) {
    $file = Get-Item -Force -LiteralPath $path
    if ($file.PSIsContainer -or ($file.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        throw "Expected a regular file at $path."
    }
    if ($file.Length -ne $entry.bytes -or (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ne $entry.sha256) {
        throw "Size or SHA-256 mismatch for $path. Expected $($entry.bytes) bytes and $($entry.sha256)."
    }
}

$missing = @()
$seen = @{}
foreach ($entry in $manifest.files) {
    # Each release file lives directly inside one of the project's media directories.
    if ($entry.path -cnotmatch '^(sources|reference|\.cutline-cache)/[a-zA-Z0-9][a-zA-Z0-9._-]*\.(mp4|webm)$' -or
        $entry.asset -notmatch '^[a-z0-9][a-z0-9._-]*$' -or $entry.sha256 -notmatch '^[a-f0-9]{64}$' -or
        $entry.bytes -notmatch '^[1-9][0-9]*$' -or $seen.ContainsKey($entry.path)) {
        throw 'Invalid or duplicate media manifest entry.'
    }
    $seen[$entry.path] = $true
    $target = Join-Path $root $entry.path
    $directory = [IO.Path]::GetDirectoryName($target)
    $parent = Get-Item -Force -LiteralPath $directory -ErrorAction SilentlyContinue
    if ($parent -and (!$parent.PSIsContainer -or ($parent.Attributes -band [IO.FileAttributes]::ReparsePoint))) {
        throw "Expected a regular project directory at $directory."
    }
    if (Get-Item -Force -LiteralPath $target -ErrorAction SilentlyContinue) {
        Confirm-Media $target $entry
        Write-Output "Verified existing $($entry.path)"
    } else {
        $missing += $entry
        if ($DryRun) { Write-Output "Would restore $($entry.path) ($($entry.bytes) bytes)" }
    }
}
if ($DryRun -or !$missing.Count) { return }

$gh = Get-Command gh -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
if (!$gh) { throw 'Install GitHub CLI (gh) and sign in with access to the private release.' }
foreach ($entry in $missing) {
    $target = Join-Path $root $entry.path
    $directory = [IO.Path]::GetDirectoryName($target)
    [void][IO.Directory]::CreateDirectory($directory)
    $staged = Join-Path $directory ([Guid]::NewGuid().ToString('N') + '.part')
    try {
        Write-Output "Downloading $($entry.asset)"
        $exitCode = & {
            # Windows PowerShell promotes redirected native stderr to error records.
            $ErrorActionPreference = 'Continue'
            & $gh release download $manifest.release --repo $manifest.repository --pattern $entry.asset --output $staged *> $null
            $LASTEXITCODE
        }
        if ($exitCode -ne 0) { throw "gh download failed for $($entry.asset) (exit $exitCode). Check gh auth status and private release access." }
        Confirm-Media $staged $entry
        try {
            [IO.File]::Move($staged, $target)
            Write-Output "Restored $($entry.path)"
        } catch [IO.IOException] {
            if (![IO.File]::Exists($target)) { throw }
            Confirm-Media $target $entry
            Write-Output "Verified concurrently restored $($entry.path)"
        }
    } finally {
        if ([IO.File]::Exists($staged)) { [IO.File]::Delete($staged) }
    }
}
