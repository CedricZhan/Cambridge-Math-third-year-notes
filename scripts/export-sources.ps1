$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot
$sourceDirectory = Join-Path $repositoryRoot "tex"
$exportDirectory = Join-Path $repositoryRoot "dist\sources"
New-Item -ItemType Directory -Force -Path $exportDirectory | Out-Null

$sources = Get-ChildItem -LiteralPath $sourceDirectory -Filter "*.tex" |
    Where-Object { $_.Name -ne "preamble.tex" }
foreach ($source in $sources) {
    Copy-Item -LiteralPath $source.FullName -Destination (Join-Path $exportDirectory $source.Name)
}
Write-Host "Exported $($sources.Count) TeX sources."
