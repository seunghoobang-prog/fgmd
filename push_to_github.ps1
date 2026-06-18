# Run after: gh auth login
$env:Path = "C:\Program Files\Git\cmd;C:\Program Files\GitHub CLI;" + $env:Path
Set-Location $PSScriptRoot

gh auth status
if ($LASTEXITCODE -ne 0) {
    Write-Host "Run: gh auth login" -ForegroundColor Yellow
    exit 1
}

gh repo create fgmd --public --source=. --remote=origin --push
if ($LASTEXITCODE -ne 0) {
    git remote add origin https://github.com/$(gh api user -q .login)/fgmd.git 2>$null
    git push -u origin main
}