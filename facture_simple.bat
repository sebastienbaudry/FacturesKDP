@echo off
cls
echo ========================================
echo     GENERATEUR DE FACTURES KDP v3.1
echo ========================================
echo.

REM --- Configuration ---
REM Modifiez le nom du fichier ci-dessous si nécessaire.
set FICHIER_KDP=KDP_Payments_b69ceb68-b7bc-4bec-ac3f-04ad517ff769.xlsx

REM Vérifie si le script Python existe
if not exist "kdp_invoice_generator.py" (
    echo ERREUR: Le script 'kdp_invoice_generator.py' est introuvable.
    pause
    exit /b 1
)

echo Script Python trouve.
echo.

:SAISIE_ANNEE
set /p ANNEE="Entrez l'annee (ex: 2025) ou laissez vide pour le mois precedent: "
echo.

:SAISIE_MOIS
set /p MOIS="Entrez le mois (1-12) ou laissez vide pour le mois precedent: "
echo.

:SAISIE_FORMAT
set /p FORMAT="Entrez le format (docx, pdf, both) [defaut: both]: "
if /i not "%FORMAT%"=="docx" if /i not "%FORMAT%"=="pdf" if /i not "%FORMAT%"=="both" set "FORMAT=both"
echo.

echo --- Lancement de la generation ---
echo Annee: %ANNEE%
echo Mois: %MOIS%
echo Format: %FORMAT%
echo.
echo Appuyez sur une touche pour continuer...
pause >nul
echo Generation en cours...
echo.

REM Construit les arguments optionnels
set ANNEE_ARG=
if not "%ANNEE%"=="" set ANNEE_ARG=--annee %ANNEE%

set MOIS_ARG=
if not "%MOIS%"=="" set MOIS_ARG=--mois %MOIS%

REM Exécute le script Python
python kdp_invoice_generator.py "%FICHIER_KDP%" %ANNEE_ARG% %MOIS_ARG% --format %FORMAT%

if errorlevel 1 (
    echo.
    echo --------------------------------------------
    echo ^>^> ERREUR lors de la generation.
    echo ^>^> Verifiez les messages ci-dessus.
    echo ^>^> Assurez-vous que les dependances sont installees :
    echo ^>^> pip install pandas openpyxl python-docx fpdf2
    echo --------------------------------------------
) else (
    echo.
    echo --------------------------------------------
    echo ^>^> SUCCES: La facture a ete generee.
    echo ^>^> Verifiez le dossier de sortie configure dans config.json.
    echo --------------------------------------------
)

echo.
pause