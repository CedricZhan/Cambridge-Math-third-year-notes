# Run only after the owner explicitly asks to upload announcements.
param([string]$Message = "Publish manual announcements")
$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repositoryRoot
try {
    $staged = & git diff --cached --name-only
    if ($LASTEXITCODE -ne 0) { throw "Cannot inspect Git staging area." }
    if ($staged) { throw "There are already staged changes. Review them before publishing." }

    # Publish only announcement data and its rendered homepage.
    & git diff --quiet -- dist/index.html dist/posts.json
    $diffStatus = $LASTEXITCODE
    $untracked = & git ls-files --others --exclude-standard -- dist/posts.json
    if ($LASTEXITCODE -ne 0 -or $diffStatus -gt 1) { throw "Cannot inspect announcement changes." }
    if ($diffStatus -eq 0 -and !$untracked) { throw "No announcement changes to publish." }
    & git diff --check -- dist/index.html dist/posts.json
    if ($LASTEXITCODE -ne 0) { throw "Fix whitespace errors before publishing." }
    & git add -- dist/index.html dist/posts.json
    if ($LASTEXITCODE -ne 0) { throw "Could not stage announcements." }
    & git commit -m $Message
    if ($LASTEXITCODE -ne 0) { throw "Could not commit announcements." }
    & git push
    if ($LASTEXITCODE -ne 0) { throw "Push failed. The commit is saved locally; retry git push after resolving the error." }
}
finally {
    Pop-Location
}
