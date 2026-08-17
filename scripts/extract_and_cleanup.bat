@echo off
setlocal

:: Get the directory where the batch file is located
set "TARGET_DIR=%~dp0"
:: Remove trailing backslash if present
if "%TARGET_DIR:~-1%"=="\" set "TARGET_DIR=%TARGET_DIR:~0,-1%"

echo Starting extraction of files into "new media" folder...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command "& { $targetDir = '%TARGET_DIR%'; $target = Join-Path -Path $targetDir -ChildPath 'new media'; if (-not (Test-Path $target)) { New-Item -ItemType Directory -Force -Path $target | Out-Null }; $files = Get-ChildItem -Path $targetDir -File -Recurse -Force | Where-Object { $_.DirectoryName -ne $targetDir -and $_.FullName -notlike ($target + '\*') }; foreach ($file in $files) { $destination = Join-Path -Path $target -ChildPath $file.Name; $count = 1; while (Test-Path -Path $destination) { $newName = '{0}_{1}{2}' -f $file.BaseName, $count, $file.Extension; $destination = Join-Path -Path $target -ChildPath $newName; $count++; }; Move-Item -LiteralPath $file.FullName -Destination $destination; }; Get-ChildItem -Path $targetDir -Recurse -Directory -Force | Where-Object { $_.FullName -notlike ($target + '*') } | Sort-Object -Property @{Expression={$_.FullName.Length};Descending=$true} | Where-Object { @(Get-ChildItem -LiteralPath $_.FullName -Force).Count -eq 0 } | Remove-Item -Force; Write-Host 'Done!'; }"

echo.
pause
