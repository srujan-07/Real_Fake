# Git setup script for Windows
# Run this to prepare your repository for deployment

Write-Host "`n=== Setting up Git Repository ===" -ForegroundColor Cyan

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "`n1. Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "   ✅ Git initialized" -ForegroundColor Green
} else {
    Write-Host "   ✅ Git already initialized" -ForegroundColor Green
}

# Add all files
Write-Host "`n2. Adding files to git..." -ForegroundColor Yellow
git add .
Write-Host "   ✅ Files staged" -ForegroundColor Green

# Create initial commit
Write-Host "`n3. Creating commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Real_Fake CTF Challenge ready for deployment"
Write-Host "   ✅ Commit created" -ForegroundColor Green

# Instructions for GitHub
Write-Host "`n=== Next Steps ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create a new repository on GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Run these commands (replace YOUR_USERNAME):" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/real-fake-ctf.git" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Deploy on Render:" -ForegroundColor White
Write-Host "   • Go to https://render.com" -ForegroundColor Gray
Write-Host "   • Click 'New +' → 'Blueprint'" -ForegroundColor Gray
Write-Host "   • Connect your GitHub repo" -ForegroundColor Gray
Write-Host "   • Click 'Apply'" -ForegroundColor Gray
Write-Host ""
Write-Host "Done! Your CTF will be live in minutes. 🚀" -ForegroundColor Green
Write-Host ""
