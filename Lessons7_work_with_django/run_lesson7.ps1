# Запускайте з цієї папки (де лежить manage.py). Інакше на :8000 буде «чужий» Django.
Set-Location $PSScriptRoot
$port = 8000
Write-Host ""
Write-Host "  Якщо тут лише admin у 404 — на $port вже інший runserver. Зупиніть його (Ctrl+C)." -ForegroundColor Yellow
Write-Host "  Перевірка: http://127.0.0.1:$port/lesson7-alive/" -ForegroundColor Cyan
Write-Host "  JSON:      http://127.0.0.1:$port/core/cbv/" -ForegroundColor Cyan
Write-Host ""
py -3 manage.py runserver $port
