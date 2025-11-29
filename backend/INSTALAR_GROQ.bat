@echo off
echo ========================================
echo Instalando Groq para LangChain
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Uninstall Anthropic
echo Desinstalando Anthropic...
pip uninstall -y langchain-anthropic

REM Install Groq
echo.
echo Instalando Groq...
pip install langchain-groq==0.2.1

REM Update other packages
echo.
echo Actualizando paquetes...
pip install --upgrade langchain langchain-core langchain-community

echo.
echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo IMPORTANTE: Actualiza tu archivo .env
echo Cambia ANTHROPIC_API_KEY por GROQ_API_KEY
echo.
echo Obten tu API key en: https://console.groq.com/keys
echo.
pause
