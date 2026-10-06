@echo off
setlocal
set "CONTATTO_PACKAGE=%~dp0"
powershell.exe -NoProfile -Command "& { $ErrorActionPreference='Stop'; $package=$env:CONTATTO_PACKAGE; $base=Join-Path $env:LOCALAPPDATA 'Contatto'; $runtime=Join-Path $base 'Runtime-44.5.1'; $exe=Join-Path $runtime 'Contatto.exe'; $source=Join-Path $package 'app.asar'; if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash -ne 'a144d4c86f18b49f606395dc51a428284391a5e76efdab23d896de35789dfe3e') {throw 'Il pacchetto dell’app non e integro. Scaricalo nuovamente da GitHub.'}; if (-not (Test-Path -LiteralPath $exe)) { Write-Host 'Prima apertura: scarico i componenti ufficiali di Windows (151 MB). Attendi...'; New-Item -ItemType Directory -Force -Path $base | Out-Null; $zip=Join-Path $base 'electron-44.5.1.zip'; [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -UseBasicParsing -Uri 'https://github.com/electron/electron/releases/download/v44.5.1/electron-v44.5.1-win32-x64.zip' -OutFile $zip; if ((Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash -ne '9b382492dcfee91f8f9e92c91f7972550a1b95d2299cac72279dab33a600d7db') {throw 'Verifica del runtime non riuscita. Il programma non verra avviato.'}; Expand-Archive -LiteralPath $zip -DestinationPath $runtime -Force; Rename-Item -LiteralPath (Join-Path $runtime 'electron.exe') -NewName 'Contatto.exe'; } Copy-Item -LiteralPath $source -Destination (Join-Path $runtime 'resources\app.asar') -Force; try { $shell=New-Object -ComObject WScript.Shell; $shortcut=$shell.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'Contatto.lnk')); $shortcut.TargetPath=$exe; $shortcut.WorkingDirectory=$runtime; $shortcut.Save(); } catch {Write-Host 'Programma pronto. Collegamento Desktop non creato.'}; Write-Host 'Avvio Contatto...'; Start-Process -FilePath $exe -WorkingDirectory $runtime; }"
if errorlevel 1 (
 echo Avvio non riuscito. Leggi il messaggio sopra e comunica l errore.
 pause
 exit /b 1
)
endlocal
