@ECHO OFF
SETLOCAL EnableDelayedExpansion
SET $Echo=FOR %%I IN (1 2) DO IF %%I==2 (SETLOCAL EnableDelayedExpansion ^& FOR %%A IN (^^^!Text:""^^^^^=^^^^^"^^^!) DO ENDLOCAL ^& ENDLOCAL ^& ECHO %%~A) ELSE SETLOCAL DisableDelayedExpansion ^& SET Text=

SETLOCAL DisableDelayedExpansion

                        

echo.
echo.
echo Downloading Latest Update . . .
powershell (New-Object System.Net.WebClient).Downloadfile('https://github.com/LIL-JABA/valchecker/archive/refs/heads/main.zip', 'valchecker-latest.zip') 
echo Extracting Files
powershell.exe Expand-Archive -Path valchecker-latest.zip -Force 
echo Replacing Files
xcopy /s "valchecker-latest/valchecker-main" "*" /Y
echo Cleaning Up Temp Files !
powershell Remove-Item -Path valchecker-latest.zip -Force
powershell Remove-Item -Path valchecker-latest -Force -Recurse
echo Successfully Updated ! You may Now Run The Program.

ENDLOCAL

PAUSE
ENDLOCAL & EXIT /B