# Sistema de Estudo Biblico e Assistente Teologico

## Estrutura de arquivos
- `requirements.txt`: dependencias pip para Streamlit, requests, LangChain e Ollama.
- `setup_database.py`: baixa os livros e versiculos da API `https://www.abibliadigital.com.br/api` e gera `bible_data.json` para uso offline.
- `app.py`: aplicacao web responsiva em Streamlit com abas de Exegese, Sermoes, Devocional e Chat guiado por prompts.
- `bible_data.json`: cache local da Biblia (gerado pelo script de setup).
- `Dados_Json/`: pasta opcional com JSONs (AA, ACF, NVI) que o app pode importar automaticamente sem baixar do GitHub.
- `DOCUMENTATION.md`: este arquivo, com instrucoes completas.

## Pre requisitos
1. **Python 3.10+**: instale via https://www.python.org/downloads/ e verifique com `python --version`.
2. **pip**: ja vem com Python moderno, mas confirme com `pip --version`.
3. **Ollama**: instale de https://ollama.com/ e certifique-se de rodar `ollama run` ou `ollama serve` no computador local.
4. **Dependencias do projeto**:
   ```sh
   pip install -r requirements.txt
   ```
5. **Modelos Ollama** (exemplos):
   ```sh
   ollama pull llama3
   ollama pull mistral
   ollama models
   ```
   Use o nome mostrado em `ollama models` no seletor de modelo da barra lateral do app.

## Setup offline da Biblia
1. Garanta que o diretorio raiz contenha o script `setup_database.py` e esteja conectado a internet para baixar a Biblia.
2. Rode:
   ```sh
   python setup_database.py --versions nvi almeida
   ```
   - `--versions` aceita uma lista de abreviaturas suportadas (ex: `nvi`, `almeida`).
   - `--output` permite trocar o nome do arquivo destino.
   - `--force` sobrescreve `bible_data.json` mesmo quando ja existe.
3. O script consulta `/books` para saber cada livro e depois `/verses/{versao}/{livro}/{capitulo}` para coletar os versiculos.
4. O arquivo resultante `bible_data.json` e o unico cache utilizado pelo frontend e deve permanecer no mesmo diretorio do `app.py`.

## Importando diretamente do GitHub
Os repositórios `thiagobodruk/biblia` e `mrk214/bible-data-pt-por` já expõem os JSONs com as versões em português (NVI, ACF e AA) dentro da pasta `json/`. Cada arquivo aninha a lista de livros com chapitros como arrays de strings, por isso o conversor agora reconhece esse layout.
Execute `python import_github_data.py --repo <owner/repo> --ref <branch> --versions nvi acf aa` para baixar o ZIP mais recente e converter o conteúdo para o formato padronizado (o valor padrão aponta para `mrk214/bible-data-pt-por`).
O script usa `https://codeload.github.com/<owner>/<repo>/zip/<ref>` e converte as pastas `json/<versao>` em versões dentro do JSON. Se quiser baixar apenas um subconjunto, informe as versões em `--versions`.
- `--replace` apaga as versões anteriores antes de escrever o arquivo final; sem esse flag, o script mescla as novas versões com o que já existe. Use `--force` para ignorar o prompt de sobrescrita.
- Se o GitHub estiver indisponível, use a aba "Importar Dados" dentro do app para carregar um ZIP ou JSON manualmente.

### Estrutura do JSON gerado
```json
{
  "generated_on": 1691452800.123,
  "versions": {
    "nvi": {
      "version": "nvi",
      "books": {
        "gn": {
          "name": "Genesis",
          "abbrev": "gn",
          "order": 1,
          "chapters": {
            "1": {
              "chapter_title": 1,
              "verses": {
                "1": "No principio Deus criou os ceus e a terra.",
                "2": "..."
              }
            }
          }
        }
      }
    }
  }
}
```
- `versions`: cada versao tem seus livros organizados pelo identificador (ex: `gn`, `ex`).
- `chapters`: chaves como strings, cada valor contem o mapa `verses` em que a chave e o numero e o valor e o texto.

## Executando a aplicacao Streamlit
1. Confirme que `bible_data.json` existe e que o Ollama esta rodando (`ollama serve` ou `ollama run <modelo>`).
2. Inicie o app:
   ```sh
   streamlit run app.py
   ```
3. No navegador aberto pelo Streamlit:
   - Use a barra lateral para selecionar a versao da Biblia e o modelo Ollama.
   - Verifique o `Status Ollama` (Online/Offline) para saber se a conexao teve sucesso.
   - Cada aba exige que um versiculo base seja escolhido para proibir alucinacoes e garantir RAG.
   - O modelo recebe prompts no formato: `Com base estritamente no texto biblico a seguir: {texto}`.

  ## Importando via Streamlit
  - A aba **Importar Dados** permite fazer o download direto ou usar arquivos locais.
    - Preencha `Repositório GitHub` e `Branch ou tag`, defina as versões desejadas (por exemplo `nvi,almeida`) e clique em `Baixar e converter do GitHub`.
    - Se o repo estiver inacessível, carregue um ZIP (que contenha `json/<versao>/`) ou um JSON simples. Use `Nome da versão para JSON simples` quando o arquivo não informar qual versão representa.
    - O checkbox `Manter versões existentes` controla se as novas entradas serão adicionadas ao `bible_data.json` ou se substituem o conteúdo anterior.
    - O app recarrega automaticamente assim que a importação termina, e os dados aparecem nas abas principais.
    - Se os arquivos `aa.json`, `acf.json` e `nvi.json` estiverem em `Dados_Json/`, o app tentará carregá-los automaticamente quando o download do GitHub falhar.

## Comandos adicionais Ollama
- Listar: `ollama models`
- Baixar modelos mais leves (ex):
  ```sh
  ollama pull llama3
  ollama pull mistral
  ollama pull llama2
  ```
- Iniciar servidor em background (Windows PowerShell):
  ```powershell
  ollama serve
  ```
  Deixe essa janela aberta ao usar o Streamlit.

## Notas e manutencao
- Caso o Ollama esteja offline, o app exibira mensagens de erro amigaveis em cada funcionalidade.
- Sempre que quiser adicionar outra versao da Biblia, execute novamente `setup_database.py` com a lista desejada e use `--force` se quiser substituir os dados atuais.
- O endpoint `https://www.abibliadigital.com.br/api` tem limites de taxa; se ocorrer erro 429 o script tentara novamente com pequenos atrasos.
- O Streamlit usa o cache `@st.cache_data` para evitar recarregar `bible_data.json` a cada interacao.
