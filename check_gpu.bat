@echo off
chcp 65001 > nul
echo ========================================
echo 🎮 VERIFICAÇÃO DE GPU PARA OLLAMA
echo ========================================
echo.

echo 📊 Verificando GPUs disponíveis...
echo.

REM Verificar NVIDIA GPU
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv 2>nul
if %errorlevel% equ 0 (
    echo.
    echo ✅ GPU NVIDIA detectada!
    echo 💡 Ollama usará CUDA automaticamente
    echo.
    echo 📈 Uso atual da GPU:
    nvidia-smi --query-gpu=utilization.gpu,utilization.memory --format=csv
) else (
    echo ⚠️ GPU NVIDIA não detectada
)

echo.
echo ========================================
echo 🔧 STATUS DO OLLAMA
echo ========================================
echo.

REM Verificar se Ollama está rodando
curl -s http://127.0.0.1:11434/api/version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama está ONLINE
    echo.
    echo 📋 Modelos instalados:
    ollama list
) else (
    echo ❌ Ollama está OFFLINE
    echo 💡 Inicie com: start_app.bat
)

echo.
echo ========================================
echo 💡 DICAS DE PERFORMANCE
echo ========================================
echo.
echo • GPU NVIDIA: Instale drivers NVIDIA + CUDA Toolkit
echo • GPU AMD: Instale drivers AMD + ROCm
echo • Sem GPU: Ollama usa CPU (mais lento mas funciona)
echo.
echo Para melhor performance com GPU:
echo 1. Instale drivers da GPU atualizados
echo 2. Baixe Ollama do site oficial (já vem com suporte GPU)
echo 3. Reinicie o computador após instalar drivers
echo.

pause
