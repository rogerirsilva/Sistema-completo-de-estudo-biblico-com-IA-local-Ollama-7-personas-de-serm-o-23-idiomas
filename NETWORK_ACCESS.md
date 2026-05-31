# 🌐 Acesso pela Rede Local

## 📱 Acessar de Outros Dispositivos

O sistema está configurado para ser acessado por qualquer dispositivo conectado à mesma rede Wi-Fi ou cabo.

### ✅ Pré-requisitos

1. **Todos os dispositivos devem estar na mesma rede**
   - Mesma rede Wi-Fi
   - Ou conectados ao mesmo roteador

2. **Firewall do Windows**
   - A porta 8501 precisa estar liberada
   - O script de configuração pode ajudar com isso

### 🚀 Como Usar

#### 1️⃣ No Computador Principal

Execute o aplicativo normalmente:

```bash
start_app.bat
```

O script vai mostrar **dois endereços**:

```
ACESSO LOCAL:
  http://localhost:8501

ACESSO NA REDE:
  http://192.168.1.100:8501
```

#### 2️⃣ Em Outros Dispositivos

**No celular, tablet ou outro computador:**

1. Abra o navegador
2. Digite o endereço da REDE (exemplo: `http://192.168.1.100:8501`)
3. Pronto! O sistema estará acessível

### 📲 Dispositivos Compatíveis

- ✅ **Smartphones** (Android/iOS)
- ✅ **Tablets** (Android/iOS/Windows)
- ✅ **Computadores** (Windows/Mac/Linux)
- ✅ **Smart TVs** com navegador
- ✅ Qualquer dispositivo com navegador web

### 🔧 Configurar Firewall (Se Necessário)

Se outros dispositivos não conseguirem conectar, libere a porta no Firewall:

#### Opção 1: Script Automático

Execute como **Administrador**:

```bash
configure_firewall.bat
```

#### Opção 2: Manual

1. Abra o **Firewall do Windows**
2. Clique em **Configurações Avançadas**
3. **Regras de Entrada** → **Nova Regra**
4. Tipo: **Porta**
5. Protocolo: **TCP**
6. Porta específica: **8501**
7. Ação: **Permitir conexão**
8. Nome: **Streamlit Bible Study**

### 🔍 Descobrir o IP da Máquina

Se precisar verificar o IP manualmente:

```bash
ipconfig
```

Procure por **IPv4** na seção do adaptador de rede ativo:

```
Adaptador Ethernet:
   IPv4: 192.168.1.100  ← Este é seu IP
```

### 📶 Criar QR Code (Opcional)

Para facilitar o acesso do celular, crie um QR Code:

1. Acesse: https://www.qr-code-generator.com/
2. Cole o endereço: `http://192.168.1.100:8501`
3. Gere o QR Code
4. Escaneie com a câmera do celular

### 🌐 Diferenças de Acesso

| Recurso | Acesso Local | Acesso Rede |
|---------|-------------|-------------|
| **Velocidade** | Muito rápida | Rápida |
| **Dependência** | Nenhuma | Rede Wi-Fi |
| **Dispositivos** | Só o host | Todos na rede |
| **IA (Ollama)** | ✅ Funciona | ✅ Funciona |
| **ChromaDB** | ✅ Funciona | ✅ Funciona |
| **PDF Export** | ✅ Funciona | ✅ Funciona |

### ⚠️ Importante

#### Dados Compartilhados
- **Históricos salvos:** Todos os dispositivos veem os mesmos históricos
- **ChromaDB:** O banco de dados é o mesmo para todos
- **Edições simultâneas:** Evite editar o mesmo estudo ao mesmo tempo

#### Segurança
- ✅ Acesso limitado à **rede local** apenas
- ❌ **NÃO** está acessível pela internet
- ✅ Outros dispositivos **não podem** modificar arquivos do sistema
- ✅ Apenas visualizam e interagem com a aplicação

### 🎯 Casos de Uso

#### 📖 Estudo em Grupo
- Professor no computador
- Alunos acompanham pelo celular
- Todos veem as mesmas análises

#### ⛪ Apresentação na Igreja
- Computador conectado ao projetor
- Tablet para controlar remotamente
- Celular como backup

#### 👨‍👩‍👧 Família
- Pai/mãe controla no computador
- Filhos acompanham no tablet
- Todos participam do estudo

#### 📱 Mobilidade
- Inicie no computador
- Continue no celular em outro cômodo
- Volte ao computador quando quiser

### 🔒 Privacidade

**O que outros podem fazer:**
- ✅ Ver estudos salvos
- ✅ Gerar novos estudos
- ✅ Exportar PDFs
- ✅ Usar todas as funcionalidades

**O que outros NÃO podem fazer:**
- ❌ Acessar arquivos do computador
- ❌ Ver outras pastas/documentos
- ❌ Modificar o código
- ❌ Acessar pela internet (só rede local)

### 🆘 Solução de Problemas

#### Problema: "Não consigo acessar de outro dispositivo"

**Checklist:**
1. ✅ Ambos dispositivos na mesma rede?
2. ✅ IP está correto?
3. ✅ Porta 8501 está no endereço?
4. ✅ Firewall liberado?
5. ✅ Aplicação rodando no computador?

**Teste de conexão:**
```bash
# No outro dispositivo, no navegador:
ping 192.168.1.100
```

#### Problema: "Conexão lenta"

**Soluções:**
- Use cabo ethernet no computador principal
- Aproxime-se do roteador Wi-Fi
- Feche outros programas pesados
- Reinicie o roteador

#### Problema: "Firewall bloqueando"

```bash
# Execute como Administrador
configure_firewall.bat
```

Ou desative temporariamente o Firewall para testar.

### 💡 Dicas

1. **Bookmark no celular:** Salve o endereço nos favoritos
2. **Tela inicial:** Adicione à tela inicial do smartphone
3. **Modo paisagem:** Use o celular deitado para melhor visualização
4. **Zoom:** Use pinça para aumentar/diminuir texto
5. **Fullscreen:** Pressione F11 no navegador para tela cheia

### 🚀 Acesso Avançado

#### Porta Customizada

Edite `start_app.bat` e mude `8501` para outra porta:

```bat
streamlit run app.py --server.address 0.0.0.0 --server.port 8080
```

#### IP Fixo

Configure IP fixo no roteador para o computador:
1. Acesse configurações do roteador (geralmente 192.168.1.1)
2. DHCP → Reserva de endereço
3. Associe o MAC do computador a um IP fixo

#### Túnel para Internet (Avançado)

⚠️ **Cuidado:** Expõe seu sistema à internet

```bash
# Instalar ngrok
# Depois:
ngrok http 8501
```

Use apenas se realmente necessário e entender os riscos de segurança.

### 📊 Monitoramento

#### Ver Dispositivos Conectados

O Streamlit não mostra isso nativamente, mas você pode:

```bash
# Ver conexões na porta 8501
netstat -an | findstr :8501
```

#### Logs de Acesso

Os logs do Streamlit mostram todas as conexões no terminal onde foi iniciado.

### ✨ Conclusão

Agora seu sistema de estudo bíblico está acessível de qualquer dispositivo na sua rede! 

📱 Perfeito para estudos em família, grupos de estudo, ou simplesmente para ter flexibilidade de acessar de onde estiver em casa.

---

**Dúvidas?** Consulte a [documentação oficial do Streamlit](https://docs.streamlit.io/library/advanced-features/configuration#server).
