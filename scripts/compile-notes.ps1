$ErrorActionPreference = "Stop"

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$sourceDirectory = Join-Path $repositoryRoot "tex"
$outputDirectory = Join-Path $repositoryRoot "dist\pdfs"
$indexPath = Join-Path $repositoryRoot "dist\index.html"
$timestampPattern = '<time id="last-compiled"[^>]*>[^<]*</time>'
$indexHtml = [System.IO.File]::ReadAllText($indexPath)
if ([regex]::Matches($indexHtml, $timestampPattern).Count -ne 1) {
    throw "Expected exactly one last-compiled timestamp in $indexPath."
}

New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null

$sources = Get-ChildItem -LiteralPath $sourceDirectory -Filter "*.tex" |
    Where-Object { $_.Name -ne "preamble.tex" } |
    Sort-Object Name

if ($sources.Count -eq 0) {
    throw "No lecture notes found in $sourceDirectory."
}

Push-Location $sourceDirectory
try {
    foreach ($source in $sources) {
        Write-Host "Compiling $($source.Name)..."
        & pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$outputDirectory" $source.Name
        if ($LASTEXITCODE -ne 0) {
            throw "LaTeX compilation failed for $($source.Name)."
        }
    }
}
finally {
    Pop-Location
}

$londonZone = [TimeZoneInfo]::FindSystemTimeZoneById("GMT Standard Time")
$compiledAt = [TimeZoneInfo]::ConvertTime([DateTimeOffset]::UtcNow, $londonZone)
$zoneLabel = if ($londonZone.IsDaylightSavingTime($compiledAt)) { "BST" } else { "GMT" }
$isoTime = $compiledAt.ToString("yyyy-MM-dd'T'HH:mm:sszzz", [Globalization.CultureInfo]::InvariantCulture)
$displayTime = $compiledAt.ToString("d MMMM yyyy, HH:mm", [Globalization.CultureInfo]::InvariantCulture)
$timestamp = '<time id="last-compiled" datetime="' + $isoTime + '">' + $displayTime + ' (' + $zoneLabel + ')</time>'
$indexHtml = [regex]::Replace($indexHtml, $timestampPattern, $timestamp)
[System.IO.File]::WriteAllText($indexPath, $indexHtml, [System.Text.UTF8Encoding]::new($false))

Get-ChildItem -LiteralPath $outputDirectory -File |
    Where-Object { $_.Extension -in ".aux", ".log", ".out" } |
    Remove-Item -Force

Write-Host "Compiled $($sources.Count) notes into $outputDirectory"
