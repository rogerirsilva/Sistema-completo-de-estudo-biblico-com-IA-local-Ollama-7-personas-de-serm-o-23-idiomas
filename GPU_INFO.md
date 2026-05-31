# 🎮 Guia de Aceleração por GPU - Sistema Bíblico

## ✅ Status Atual

**O sistema JÁ ESTÁ OTIMIZADO para usar GPU automaticamente!**

### Como funciona

```
┌─────────────────┐
│  Streamlit App  │  ← Você está aqui (código Python)
│    (app.py)     │
└────────┬────────┘
         │ HTTP Request (requests.post)
         ↓
┌─────────────────┐
│  Ollama Server  │  ← GPU é usada AQUI automaticamente
│  (localhost)    │  
└────────┬────────┘
         │ Detecta GPU disponível
         ↓
┌─────────────────┐
│   GPU/CPU       │  ← NVIDIA CUDA | AMD ROCm | Apple Metal
│   Hardware      │
└─────────────────┘
```

## 🚀 Como garantir melhor performance

### 1️⃣ Verificar se você tem GPU dedicada

Execute o arquivo criado:
```bash
check_gpu.bat
```

### 2️⃣ NVIDIA GPU (GeForce/RTX/Quadro)

**Requisitos:**
- Drivers NVIDIA atualizados ([Download](https://www.nvidia.com/download/index.aspx))
- CUDA Toolkit (opcional - Ollama já inclui)

**Verificar se está usando GPU:**
```bash
# Abra outro terminal PowerShell
nvidia-smi

# Durante geração de perguntas/sermões, você verá:
# GPU utilization: 90-100%
# Memory usage: aumentando
```

### 3️⃣ AMD GPU (Radeon)

**Requisitos:**
- Drivers AMD Adrenalin atualizados
- ROCm (para Linux) ou drivers Windows

**Suporte limitado no Windows** - NVIDIA é mais otimizado para LLMs

### 4️⃣ Sem GPU dedicada (Intel/AMD integrada)

**O sistema funciona normalmente, mas mais lento:**
- CPU faz todo processamento
- Geração de 50 perguntas: ~8-10 minutos (vs 2-3 minutos com GPU)
- Sem necessidade de configuração extra

## 📊 Performance Comparativa

| Hardware | 10 perguntas | 50 perguntas | Status |
|----------|--------------|--------------|--------|
| CPU Intel i5/i7 | 2-3 min | 8-10 min | ✅ Funciona |
| GPU NVIDIA GTX 1660+ | 30-45s | 2-3 min | ⚡ Rápido |
| GPU NVIDIA RTX 3060+ | 20-30s | 1.5-2 min | 🚀 Muito rápido |
| Apple M1/M2/M3 | 25-35s | 2-2.5 min | ⚡ Rápido (Metal) |

## 🔧 Configurações Atuais do Código

**O código app.py NÃO PRECISA de alterações porque:**

```python
# ✅ JÁ OTIMIZADO - Ollama gerencia GPU automaticamente
ok, result = query_ollama(
    selected_model, 
    prompt, 
    max_tokens=max_tokens,
    timeout=dynamic_timeout,
    auto_continue=True,
    lang_code=lang_code,
    show_progress=True
)
```

### Por que não precisa mexer no código?

1. **Ollama Server** detecta GPU na inicialização
2. **Modelos são carregados** na VRAM da GPU automaticamente
3. **Inferência acontece** na GPU sem configuração
4. **Cliente Python** apenas faz HTTP requests (não vê GPU)

## 🐛 Troubleshooting

### GPU não está sendo usada?

**1. Verificar instalação do Ollama:**
```bash
ollama --version
# Se não reconhecer, reinstale: https://ollama.ai
```

**2. Verificar modelos instalados:**
```bash
ollama list
```

**3. Testar GPU manualmente:**
```bash
# Rodar modelo diretamente
ollama run llama3 "teste rápido"

# Abrir outro terminal e verificar GPU
nvidia-smi
# Deve mostrar uso de GPU > 0%
```

**4. Reinstalar Ollama (com GPU support):**
- Desinstale: Painel de Controle → Ollama
- Baixe versão mais recente: https://ollama.ai/download
- Instale (detectará GPU automaticamente)
- Reinicie o computador

### GPU sendo usada mas ainda lento?

**Possíveis causas:**

1. **Modelo muito grande para VRAM:**
   - Llama 3 70B precisa de ~40GB VRAM
   - Llama 3 8B precisa de ~8GB VRAM
   - **Solução:** Use modelos menores (llama3, mistral, phi)

2. **VRAM compartilhada:**
   - GPU está sendo usada por outros apps (jogos, Chrome, etc)
   - **Solução:** Feche apps pesados antes de gerar perguntas

3. **Drivers desatualizados:**
   - **Solução:** Atualize drivers da GPU

## 📈 Monitorar Performance em Tempo Real

### Durante geração de perguntas (Windows):

1. **Abra Task Manager** (Ctrl + Shift + Esc)
2. Vá em **Performance** → **GPU**
3. Clique em "Gerar Perguntas" no sistema
4. Observe GPU usage subir para 80-100%

### Linux/Mac:

```bash
# Monitorar GPU NVIDIA
watch -n 1 nvidia-smi

# Monitorar CPU (se sem GPU)
htop
```

## 🎯 Recomendações Finais

### ✅ O que FAZER:

1. ✅ Mantenha drivers da GPU atualizados
2. ✅ Use modelos otimizados (llama3, mistral)
3. ✅ Feche apps pesados durante geração
4. ✅ Deixe Ollama gerenciar GPU automaticamente

### ❌ O que NÃO fazer:

1. ❌ Não modifique o código Python para GPU (já otimizado)
2. ❌ Não tente carregar modelos manualmente na GPU
3. ❌ Não use modelos muito grandes para sua VRAM
4. ❌ Não instale CUDA/ROCm manualmente (Ollama já tem)

## 🆘 Suporte

**GPU não detectada após seguir tudo?**

Execute e envie o log:
```bash
check_gpu.bat > gpu_log.txt
```

**Compartilhe:**
- Modelo da GPU
- Versão do driver
- Versão do Ollama
- Arquivo gpu_log.txt
