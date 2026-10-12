$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot
$sourceDirectory = Join-Path $repositoryRoot "tex"
$exportDirectory = Join-Path $repositoryRoot "dist\sources"
$preamble = Join-Path $sourceDirectory "preamble.tex"
New-Item -ItemType Directory -Force -Path $exportDirectory | Out-Null

$sources = Get-ChildItem -LiteralPath $sourceDirectory -Filter "*.tex" |
    Where-Object { $_.Name -ne "preamble.tex" }
foreach ($source in $sources) {
    Copy-Item -LiteralPath $source.FullName -Destination (Join-Path $exportDirectory $source.Name)
    $projectFiles = @($source.FullName, $preamble)
    # Preserve the figures/ directory used by LaTeX's graphicspath.
    if ([IO.File]::ReadAllText($source.FullName) -match '\\includegraphics') {
        $projectFiles += Join-Path $sourceDirectory "figures"
    }
    Compress-Archive -LiteralPath $projectFiles -DestinationPath (Join-Path $exportDirectory "$($source.BaseName).zip") -Force
}
Write-Host "Exported $($sources.Count) TeX sources and project archives."
