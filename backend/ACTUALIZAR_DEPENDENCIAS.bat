@echo off
echo ========================================
echo Actualizando Dependencias
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Uninstall old versions
echo Desinstalando versiones antiguas...
pip uninstall -y langchain langchain-anthropic langchain-community langchain-core pydantic pydantic-settings

REM Install new versions
echo.
echo Instalando nuevas versiones compatibles...
pip install -r requirements.txt

echo.
echo ========================================
echo Actualizacion completada!
echo ========================================
echo.
echo Ahora puedes ejecutar: python main.py
pause
