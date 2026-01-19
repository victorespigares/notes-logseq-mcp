#!/bin/bash

# Script de inicio rápido para Notes-Logseq MCP Server

echo "🚀 Iniciando Notes-Logseq MCP Server..."
echo ""

# Verificar que existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment no encontrado"
    echo "Por favor crea el entorno virtual primero:"
    echo "  python3.10 -m venv venv  # o python3.13"
    echo "  venv/bin/pip install -r requirements.txt"
    exit 1
fi

echo "✓ Virtual environment encontrado"
echo "✓ Python: $(venv/bin/python --version)"

# Verificar que existe config.json
if [ ! -f "config.json" ]; then
    echo "❌ Error: config.json no encontrado"
    echo "Por favor crea config.json con tu configuración"
    exit 1
fi

echo "✓ config.json encontrado"

# Verificar dependencias
if ! venv/bin/python -c "import mcp" 2>/dev/null; then
    echo "⚠️  Dependencias no instaladas. Instalando..."
    venv/bin/pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error instalando dependencias"
        exit 1
    fi
    echo "✓ Dependencias instaladas"
else
    echo "✓ Dependencias verificadas"
fi

# Verificar Ollama (opcional)
if command -v ollama &> /dev/null; then
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✓ Ollama está corriendo"
    else
        echo "⚠️  Ollama instalado pero no está corriendo"
        echo "   Ejecuta: ollama serve"
    fi
else
    echo "ℹ️  Ollama no instalado (opcional para modelos locales)"
fi

echo ""
echo "🎯 Iniciando servidor MCP..."
echo "   Presiona Ctrl+C para detener"
echo ""

# Iniciar el servidor
venv/bin/python -m src.server config.json
