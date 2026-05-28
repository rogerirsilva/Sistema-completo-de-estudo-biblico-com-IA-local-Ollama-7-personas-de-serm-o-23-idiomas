# Upload Rapido para GitHub

## Repositorio alvo

- Usuario: rogerirsilva
- Repositorio: Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas
- URL: https://github.com/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas.git

---

## Fluxo recomendado

1. Inicializar Git local (se necessario)
2. Commitar alteracoes de codigo e documentacao
3. Subir para branch main
4. Publicar instalador via GitHub Releases

---

## Publicar instalador para download

Use GitHub Releases para distribuir instaladores.

Por que:

- Evita inflar o historico do Git com binarios
- Facilita download por usuarios finais
- Permite controle por versao

Limite pratico:

- Asset de Release suporta arquivos grandes (ate 2 GiB por arquivo)

Gerar instalador:

```bash
tauri_build_installers.bat
```

Artefatos esperados:

```text
tauri-launcher/src-tauri/target/release/bundle/
```

Depois:

1. Crie tag (ex.: v2.1.0)
2. Crie Release no GitHub
3. Anexe .msi/.exe
4. Publique notas da versao

---

## Comandos Git basicos

```bash
git init
git branch -M main
git remote add origin https://github.com/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas.git
git add .
git commit -m "feat: atualiza interface Tauri, i18n e docs"
git push -u origin main
```

---

## Autenticacao GitHub

GitHub exige token pessoal para push HTTPS.

- URL: https://github.com/settings/tokens
- Permissao minima: repo

---

## Observacoes

- Nao commitar .venv, caches e build de target
- Nao commitar instalador na arvore principal
- Manter binarios apenas na Release
