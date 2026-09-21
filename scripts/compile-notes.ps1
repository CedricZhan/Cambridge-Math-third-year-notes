$ErrorActionPreference = "Stop"

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$sourceDirectory = Join-Path $repositoryRoot "tex"
$outputDirectory = Join-Path $repositoryRoot "dist\pdfs"

New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null

$sources = Get-ChildItem -LiteralPath $sourceDirectory -Filter "*.tex" |
    Where-Object { $_.Name -ne "preamble.tex" } |
    Sort-Object Name

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

Get-ChildItem -LiteralPath $outputDirectory -File |
    Where-Object { $_.Extension -in ".aux", ".log", ".out" } |
    Remove-Item -Force

Write-Host "Compiled $($sources.Count) notes into $outputDirectory"
