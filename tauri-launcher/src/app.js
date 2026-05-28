(() => {
  const API = "http://127.0.0.1:8000";
  const SUPPORT_PAYPAL_URL = "https://www.paypal.com/donate/?business=9SNHLWN6MUJAQ&no_recurring=0&item_name=Feito+com+dedicacao.+Se+puder,+apoie+o+tempo+e+os+custos+de+criacao+deste+projeto.&currency_code=BRL";
  const SUPPORT_PICKPAY_KEY = "";
  const STORAGE_KEYS = {
    study: "study_history",
    sermon: "sermon_history",
    devotional: "devotional_history",
    chat: "chat_history",
    questions: "questions_history",
  };
  const OT_CUTOFF = 39;

  const SERMON_STYLES = [
    { value: "Analitico-Essencia", label: "Analitico-Essencia", subtitle: "O Investigador" },
    { value: "Expositivo-Teologico", label: "Expositivo-Teologico", subtitle: "O Professor" },
    { value: "Narrativo-Imersivo", label: "Narrativo-Imersivo", subtitle: "O Storyteller" },
    { value: "Devocional-Pratico", label: "Devocional-Pratico", subtitle: "O Mentor" },
    { value: "Cristocentrico-Tipologico", label: "Cristocentrico-Tipologico", subtitle: "O Revelador" },
    { value: "Profetico-Confrontador", label: "Profetico-Confrontador", subtitle: "O Atalaia" },
    { value: "Apologetico-Filosofico", label: "Apologetico-Filosofico", subtitle: "O Defensor" },
  ];

  const SERMON_STYLES_I18N = {
    en: {
      "Analitico-Essencia": { label: "Analytical-Essence", subtitle: "The Investigator" },
      "Expositivo-Teologico": { label: "Expository-Theological", subtitle: "The Teacher" },
      "Narrativo-Imersivo": { label: "Narrative-Immersive", subtitle: "The Storyteller" },
      "Devocional-Pratico": { label: "Devotional-Practical", subtitle: "The Mentor" },
      "Cristocentrico-Tipologico": { label: "Christocentric-Typological", subtitle: "The Revealer" },
      "Profetico-Confrontador": { label: "Prophetic-Confrontational", subtitle: "The Watchman" },
      "Apologetico-Filosofico": { label: "Apologetic-Philosophical", subtitle: "The Defender" },
    },
    ar: {
      "Analitico-Essencia": { label: "تحليلي-الجوهر", subtitle: "الباحث" },
      "Expositivo-Teologico": { label: "تفسيري-لاهوتي", subtitle: "المعلم" },
      "Narrativo-Imersivo": { label: "سردي-غامر", subtitle: "الراوي" },
      "Devocional-Pratico": { label: "تعبدي-عملي", subtitle: "المرشد" },
      "Cristocentrico-Tipologico": { label: "متمحور حول المسيح-نمطي", subtitle: "الكاشف" },
      "Profetico-Confrontador": { label: "نبوي-مواجه", subtitle: "الحارس" },
      "Apologetico-Filosofico": { label: "دفاعي-فلسفي", subtitle: "المدافع" },
    },
  };

  const MODEL_SUGGESTIONS = [
    "llama3.2:1b",
    "llama3.2:3b",
    "llama3.1:8b",
    "qwen2.5:7b",
    "qwen2.5-coder:7b",
    "mistral:7b",
    "gemma2:9b",
    "phi4",
    "deepseek-r1:8b",
  ];

  const state = {
    online: false,
    languages: [],
    uiTranslations: {},
    models: [],
    versions: [],
    books: [],
    selectedBook: null,
    chapterData: null,
    importSources: [],
    activeTab: "reading",
    histories: {
      study: loadHistory(STORAGE_KEYS.study),
      sermon: loadHistory(STORAGE_KEYS.sermon),
      devotional: loadHistory(STORAGE_KEYS.devotional),
      chat: loadHistory(STORAGE_KEYS.chat),
      questions: loadHistory(STORAGE_KEYS.questions),
    },
  };

  document.title = "Biblical Study AI";
  document.body.innerHTML = `
    <div class="shell">
      <aside class="sidebar">
        <div class="brand">
          <div class="brand-badge">B</div>
          <div>
            <div class="brand-title">Biblical Study AI</div>
            <div class="brand-subtitle">FastAPI + Tauri</div>
          </div>
        </div>

        <div class="status-row">
          <div id="apiStatus" class="status warn">Conectando...</div>
          <button id="refreshButton" class="ghost-button">Recarregar</button>
        </div>

        <div class="panel-group" id="settingsPanel">
          <div class="panel-header">
            <div class="panel-title">Configuracoes</div>
            <button id="settingsToggle" class="ghost-button panel-toggle" type="button" aria-expanded="true">▲</button>
          </div>
          <div id="settingsBody" class="panel-body">
            <label class="field-label" for="langSelect">Idioma</label>
            <select id="langSelect" class="field"></select>

            <label class="field-label" for="versionSelect">Versao</label>
            <select id="versionSelect" class="field"></select>

            <label class="field-label" for="modelSelect">Modelo Ollama</label>
            <div class="button-row">
              <button id="modelRefresh" class="ghost-button" type="button">Atualizar modelos</button>
            </div>
            <select id="modelSelect" class="field"></select>
            <div id="modelInfo" class="helper-text">Modelos carregados: 0</div>

            <label class="field-label" for="chapterInput">Capitulo</label>
            <input id="chapterInput" class="field" type="number" min="1" value="1" />

            <label class="field-label" for="verseInput">Versiculos base</label>
            <input id="verseInput" class="field" type="text" placeholder="1,2,3 ou 1-5" />

            <button id="loadChapterButton" class="primary-button">Carregar Capitulo</button>
            <div class="helper-text">O backend local sobe automaticamente com o launcher.</div>
          </div>
        </div>

        <div class="panel-group" id="supportPanel">
          <div class="panel-header">
            <div class="panel-title" id="supportTitle">Apoie o projeto</div>
          </div>
          <div class="panel-body">
            <div id="supportText" class="helper-text">Se este sistema te ajuda, considere apoiar o desenvolvimento.</div>
            <div class="button-row">
              <button id="supportPaypal" class="ghost-button" type="button">Doar via PayPal</button>
              <button id="supportPickpay" class="ghost-button" type="button">Copiar chave PicPay</button>
            </div>
            <div id="supportKeyHint" class="helper-text"></div>
          </div>
        </div>

      </aside>

      <main class="main">
        <header class="topbar">
          <div>
            <div class="page-title">Painel de Estudo Biblico</div>
            <div id="pageSubtitle" class="page-subtitle">Exegese, Sermoes (7 Personas), Devocional e Chat teologico local com Ollama.</div>
          </div>
          <div class="topbar-meta">
            <span id="versionBadge" class="badge">Versao: -</span>
            <span id="bookBadge" class="badge">Livro: -</span>
          </div>
        </header>

        <nav class="tabs">
          <button class="tab active" data-tab="reading">Leitura</button>
          <button class="tab" data-tab="sermon">Sermoes</button>
          <button class="tab" data-tab="devotional">Devocional</button>
          <button class="tab" data-tab="chat">Chat</button>
          <button class="tab" data-tab="questions">Perguntas</button>
          <button class="tab" data-tab="history">Historico</button>
          <button class="tab" data-tab="import">Importar</button>
        </nav>

        <section id="reading" class="tab-panel active">
          <div class="grid-two">
            <section class="card">
              <div class="card-title">Texto Biblico</div>
              <label class="field-label" for="readingBookSelect">Livro</label>
              <select id="readingBookSelect" class="field"></select>
              <div id="chapterText" class="scroll-box muted-box">Selecione um livro e carregue o capitulo.</div>
            </section>

            <section class="card">
              <div class="card-title">Leitura e Exegese</div>
              <label class="field-label" for="studyCompare">Modo</label>
              <label class="check-row"><input id="studyCompare" type="checkbox" /> Comparar com outras versoes</label>

              <label class="field-label" for="studyRequest">Pedido</label>
              <textarea id="studyRequest" class="textarea" rows="5">Explique o contexto historico e teologico, destaque palavras-chave e a aplicacao pastoral do texto.</textarea>

              <div class="button-row">
                <button id="studyButton" class="primary-button">Gerar Exegese</button>
                <button id="studyCopyButton" class="ghost-button">Copiar resultado</button>
              </div>

              <div class="output-title">Resposta</div>
              <div id="studyOutput" class="scroll-box muted-box">Aguardando solicitaÃ§Ã£o...</div>
            </section>
          </div>

          <section class="card">
            <div class="card-title">Historico de Estudos</div>
            <div class="filters-row">
              <input id="studySearch" class="field" type="text" placeholder="Buscar no historico" />
              <select id="studySort" class="field">
                <option value="recent">Mais recente</option>
                <option value="oldest">Mais antigo</option>
              </select>
              <button id="studyClear" class="ghost-button">Limpar historico</button>
            </div>
            <div id="studyHistory"></div>
          </section>
        </section>

        <section id="sermon" class="tab-panel">
          <div class="grid-two">
            <section class="card">
              <div class="card-title">Gerador de Sermoes</div>
              <div class="field-grid two-up">
                <div>
                  <label class="field-label" for="sermonScope">Escopo</label>
                  <select id="sermonScope" class="field">
                    <option value="specific">Livro especifico</option>
                    <option value="selected">Livros selecionados</option>
                    <option value="whole">Toda a Biblia</option>
                  </select>
                </div>
                <div>
                  <label class="field-label" for="sermonStyle">Estilo</label>
                  <select id="sermonStyle" class="field"></select>
                </div>
              </div>

              <label class="field-label" for="sermonBook">Livro para contexto</label>
              <select id="sermonBook" class="field"></select>

              <div class="field-grid two-up">
                <div>
                  <label class="field-label" for="sermonTheme">Tema</label>
                  <input id="sermonTheme" class="field" type="text" placeholder="Fe, esperanÃ§a, santidade..." />
                </div>
                <div>
                  <label class="field-label" for="sermonAudience">Publico</label>
                  <input id="sermonAudience" class="field" type="text" placeholder="Jovens, igreja local, lideres..." />
                </div>
              </div>

              <label class="field-label" for="sermonNotes">Notas extras</label>
              <textarea id="sermonNotes" class="textarea" rows="4" placeholder="Contexto do pregador, enfoque, objetivo..."></textarea>

              <div class="button-row">
                <button id="sermonButton" class="primary-button">Gerar Sermao</button>
                <button id="sermonCopyButton" class="ghost-button">Copiar resultado</button>
              </div>
              <div class="output-title">Resultado</div>
              <div id="sermonOutput" class="scroll-box muted-box">Aguardando geracao...</div>
            </section>

            <section class="card">
              <div class="card-title">Historico de Sermoes</div>
              <div class="filters-row">
                <input id="sermonSearch" class="field" type="text" placeholder="Buscar sermoes" />
                <select id="sermonSort" class="field">
                  <option value="recent">Mais recente</option>
                  <option value="oldest">Mais antigo</option>
                </select>
                <button id="sermonClear" class="ghost-button">Limpar historico</button>
              </div>
              <div id="sermonHistory"></div>
            </section>
          </div>
        </section>

        <section id="devotional" class="tab-panel">
          <div class="grid-two">
            <section class="card">
              <div class="card-title">Devocional & Meditacao</div>
              <div class="field-grid two-up">
                <div>
                  <label class="field-label" for="devScope">Escopo</label>
                  <select id="devScope" class="field">
                    <option value="specific">Livro especifico</option>
                    <option value="selected">Livros selecionados</option>
                    <option value="whole">Toda a Biblia</option>
                  </select>
                </div>
                <div>
                  <label class="field-label" for="devFeeling">Tema / sentimento</label>
                  <input id="devFeeling" class="field" type="text" value="Gratidao" />
                </div>
              </div>

              <label class="field-label" for="devBook">Livro para contexto</label>
              <select id="devBook" class="field"></select>

              <div class="button-row">
                <button id="devButton" class="primary-button">Gerar Devocional</button>
                <button id="devCopyButton" class="ghost-button">Copiar resultado</button>
              </div>
              <div class="output-title">Resultado</div>
              <div id="devOutput" class="scroll-box muted-box">Aguardando geracao...</div>
            </section>

            <section class="card">
              <div class="card-title">Historico de Devocionais</div>
              <div class="filters-row">
                <input id="devSearch" class="field" type="text" placeholder="Buscar devocionais" />
                <select id="devSort" class="field">
                  <option value="recent">Mais recente</option>
                  <option value="oldest">Mais antigo</option>
                </select>
                <button id="devClear" class="ghost-button">Limpar historico</button>
              </div>
              <div id="devHistory"></div>
            </section>
          </div>
        </section>

        <section id="chat" class="tab-panel">
          <div class="grid-two">
            <section class="card">
              <div class="card-title">Chat Teologico</div>
              <div class="field-grid two-up">
                <div>
                  <label class="field-label" for="chatScope">Escopo</label>
                  <select id="chatScope" class="field">
                    <option value="specific">Versiculo especifico</option>
                    <option value="selected">Livros selecionados</option>
                    <option value="whole">Toda a Biblia</option>
                  </select>
                </div>
                <div>
                  <label class="field-label" for="chatBook">Livro para contexto</label>
                  <select id="chatBook" class="field"></select>
                </div>
              </div>

              <label class="field-label" for="chatQuestion">Pergunta</label>
              <textarea id="chatQuestion" class="textarea" rows="5" placeholder="Digite sua duvida biblica..."></textarea>

              <div class="button-row">
                <button id="chatButton" class="primary-button">Enviar Pergunta</button>
                <button id="chatCopyButton" class="ghost-button">Copiar resposta</button>
              </div>
              <div class="output-title">Resposta</div>
              <div id="chatOutput" class="scroll-box muted-box">Aguardando pergunta...</div>
            </section>

            <section class="card">
              <div class="card-title">Historico do Chat</div>
              <div class="filters-row">
                <input id="chatSearch" class="field" type="text" placeholder="Buscar conversas" />
                <select id="chatSort" class="field">
                  <option value="recent">Mais recente</option>
                  <option value="oldest">Mais antigo</option>
                </select>
                <button id="chatClear" class="ghost-button">Limpar historico</button>
              </div>
              <div id="chatHistory"></div>
            </section>
          </div>
        </section>

        <section id="questions" class="tab-panel">
          <div class="grid-two">
            <section class="card">
              <div class="card-title">Gerador de Perguntas Biblicas</div>
              <div class="field-grid two-up">
                <div>
                  <label class="field-label" for="questionsScope">Escopo</label>
                  <select id="questionsScope" class="field">
                    <option value="specific">Livro especifico</option>
                    <option value="selected">Livros selecionados</option>
                    <option value="whole">Bibia toda</option>
                  </select>
                </div>
                <div>
                  <label class="field-label" for="questionsCount">Quantidade</label>
                  <input id="questionsCount" class="field" type="number" min="1" max="50" value="10" />
                </div>
              </div>

              <label class="field-label" for="questionsBook">Livro para contexto</label>
              <select id="questionsBook" class="field"></select>

              <label class="field-label" for="questionsMode">Modo</label>
              <select id="questionsMode" class="field">
                <option value="with">Com respostas</option>
                <option value="only">Somente perguntas</option>
              </select>

              <div class="button-row">
                <button id="questionsButton" class="primary-button">Gerar Perguntas</button>
                <button id="questionsCopyButton" class="ghost-button">Copiar resultado</button>
              </div>
              <div class="output-title">Resultado</div>
              <div id="questionsOutput" class="scroll-box muted-box">Aguardando geracao...</div>
            </section>

            <section class="card">
              <div class="card-title">Historico de Perguntas</div>
              <div class="filters-row">
                <input id="questionsSearch" class="field" type="text" placeholder="Buscar perguntas" />
                <select id="questionsSort" class="field">
                  <option value="recent">Mais recente</option>
                  <option value="oldest">Mais antigo</option>
                </select>
                <button id="questionsClear" class="ghost-button">Limpar historico</button>
              </div>
              <div id="questionsHistory"></div>
            </section>
          </div>
        </section>

        <section id="history" class="tab-panel">
          <section class="card">
            <div class="card-title">Historico Consolidado</div>
            <div id="historySummary" class="summary-grid"></div>
          </section>
          <section class="card">
            <div class="card-title">Todos os Registros</div>
            <div id="allHistory"></div>
          </section>
        </section>

        <section id="import" class="tab-panel">
          <div class="grid-two">
            <section class="card">
              <div class="card-title">Fontes Locais</div>
              <div class="helper-text">O backend carrega direto de Dados_Json, entao esta aba mostra os arquivos disponiveis e permite recarregar o catalogo.</div>
              <div class="button-row">
                <button id="importRefresh" class="primary-button">Recarregar catalogo</button>
              </div>
              <div id="importSources" class="scroll-box muted-box"></div>
            </section>

            <section class="card">
              <div class="card-title">Ajuda de Importacao</div>
              <div class="scroll-box muted-box">
                <p>1. Coloque os arquivos JSON em Dados_Json/idioma/.</p>
                <p>2. Use um nome de versao consistente, por exemplo NVI.json ou AA.json.</p>
                <p>3. Clique em Recarregar catalogo para atualizar a lista local.</p>
                <p>4. O backend usa estes arquivos direto, entao nao existe mais uma importacao separada no fluxo nativo.</p>
              </div>
            </section>
          </div>
        </section>
      </main>
    </div>
  `;

  document.head.insertAdjacentHTML(
    "beforeend",
    `
      <style>
        :root {
          --bg: #07111f;
          --bg2: #0b1c2d;
          --panel: rgba(10, 19, 33, 0.92);
          --card: rgba(12, 23, 39, 0.96);
          --line: rgba(148, 163, 184, 0.2);
          --fg: #e5eefc;
          --muted: #9fb2cc;
          --accent: #67d5ff;
          --accent2: #a78bfa;
          --ok: #22c55e;
          --warn: #f59e0b;
          --danger: #fb7185;
        }
        * { box-sizing: border-box; }
        html, body { margin: 0; min-height: 100%; background: radial-gradient(circle at top left, #13243a, var(--bg)); color: var(--fg); font-family: "Segoe UI", "Noto Sans", sans-serif; }
        body::before {
          content: "";
          position: fixed;
          inset: 0;
          pointer-events: none;
          background: linear-gradient(135deg, rgba(103, 213, 255, 0.08), transparent 40%), linear-gradient(315deg, rgba(167, 139, 250, 0.08), transparent 38%);
        }
        .shell { position: relative; z-index: 1; display: grid; grid-template-columns: 320px 1fr; min-height: 100vh; }
        .sidebar { background: rgba(4, 10, 18, 0.72); border-right: 1px solid var(--line); padding: 20px; display: flex; flex-direction: column; gap: 16px; }
        .brand { display: flex; gap: 12px; align-items: center; }
        .brand-badge { width: 44px; height: 44px; border-radius: 14px; display: grid; place-items: center; font-weight: 700; color: #00111d; background: linear-gradient(135deg, var(--accent), #d8fbff); box-shadow: 0 12px 30px rgba(103, 213, 255, 0.3); }
        .brand-title { font-size: 18px; font-weight: 700; }
        .brand-subtitle { color: var(--muted); font-size: 12px; }
        .status-row, .button-row, .filters-row, .topbar-meta, .field-grid, .summary-grid { display: flex; gap: 10px; flex-wrap: wrap; }
        .status { padding: 9px 12px; border-radius: 999px; border: 1px solid var(--line); font-size: 13px; }
        .status.ok { color: #d1fae5; border-color: rgba(34, 197, 94, 0.45); background: rgba(34, 197, 94, 0.12); }
        .status.warn { color: #fde68a; border-color: rgba(245, 158, 11, 0.45); background: rgba(245, 158, 11, 0.12); }
        .ghost-button, .primary-button, .tab { border: 0; border-radius: 12px; cursor: pointer; transition: transform .15s ease, opacity .15s ease, background .15s ease; }
        .ghost-button:hover, .primary-button:hover, .tab:hover { transform: translateY(-1px); }
        .ghost-button { background: rgba(148, 163, 184, 0.08); color: var(--fg); padding: 10px 14px; border: 1px solid var(--line); }
        .primary-button { background: linear-gradient(135deg, var(--accent), var(--accent2)); color: #03111e; font-weight: 700; padding: 11px 16px; }
        .panel-group { background: var(--panel); border: 1px solid var(--line); border-radius: 18px; padding: 14px; display: flex; flex-direction: column; gap: 8px; }
        .panel-header { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
        .panel-toggle { min-width: 36px; padding: 6px 10px; }
        .panel-body { display: flex; flex-direction: column; gap: 8px; }
        .panel-group.collapsed .panel-body { display: none; }
        .panel-group.grow { flex: 1; min-height: 0; }
        .panel-title { color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .12em; }
        .field, .textarea { width: 100%; background: rgba(6, 13, 24, 0.95); color: var(--fg); border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; font-size: 14px; }
        .textarea { resize: vertical; min-height: 110px; }
        .field.multi { min-height: 220px; }
        .field-label { color: var(--muted); font-size: 12px; margin-top: 4px; margin-bottom: 6px; display: block; }
        .helper-text { color: var(--muted); font-size: 12px; line-height: 1.4; }
        .book-list { display: grid; gap: 8px; overflow: auto; padding-right: 4px; }
        .book-item { padding: 10px 12px; border-radius: 12px; border: 1px solid var(--line); background: rgba(255,255,255,0.03); cursor: pointer; color: #dbeafe; }
        .book-item.active { background: linear-gradient(135deg, rgba(103, 213, 255, 0.18), rgba(167, 139, 250, 0.18)); border-color: rgba(103, 213, 255, 0.4); }
        .main { padding: 20px; display: flex; flex-direction: column; gap: 16px; min-width: 0; }
        .topbar { display: flex; justify-content: space-between; gap: 16px; align-items: flex-start; padding: 18px 20px; border-radius: 20px; background: rgba(10, 19, 33, 0.75); border: 1px solid var(--line); box-shadow: 0 20px 40px rgba(0,0,0,0.25); }
        .page-title { font-size: 22px; font-weight: 800; }
        .page-subtitle { color: var(--muted); font-size: 13px; margin-top: 4px; }
        .badge { padding: 9px 12px; border-radius: 999px; background: rgba(255,255,255,0.05); border: 1px solid var(--line); color: var(--muted); font-size: 12px; }
        .tabs { display: flex; gap: 8px; flex-wrap: wrap; }
        .tab { padding: 11px 14px; color: var(--fg); background: rgba(148, 163, 184, 0.07); border: 1px solid var(--line); }
        .tab.active { background: linear-gradient(135deg, var(--accent), var(--accent2)); color: #05131f; font-weight: 700; }
        .tab-panel { display: none; gap: 16px; flex-direction: column; }
        .tab-panel.active { display: flex; }
        .grid-two { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); gap: 16px; }
        .card { background: var(--card); border: 1px solid var(--line); border-radius: 18px; padding: 16px; min-width: 0; box-shadow: 0 20px 40px rgba(0,0,0,0.15); }
        .card-title { font-size: 16px; font-weight: 700; margin-bottom: 12px; }
        .scroll-box { max-height: 520px; overflow: auto; white-space: pre-wrap; line-height: 1.8; padding: 16px; border-radius: 14px; border: 1px solid var(--line); font-size: 15px; transition: all 0.2s ease; }
        .muted-box { background: rgba(5, 13, 24, 0.8); color: #dbeafe; }
        .output-title { margin-top: 10px; margin-bottom: 8px; color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .12em; }
        .check-row { display: inline-flex; gap: 8px; align-items: center; font-size: 14px; color: #dbeafe; margin-bottom: 10px; }
        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
        .summary-card { border: 1px solid var(--line); border-radius: 14px; padding: 14px; background: rgba(255,255,255,0.03); }
        .summary-card strong { display: block; font-size: 20px; margin-bottom: 6px; }
        .record-list { display: grid; gap: 12px; }
        .record { border: 1px solid var(--line); border-radius: 16px; padding: 14px; background: rgba(255,255,255,0.03); }
        .record-head { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; align-items: center; }
        .record-title { font-weight: 700; font-size: 15px; }
        .record-meta { color: var(--muted); font-size: 12px; margin-top: 4px; }
        .record-body { margin-top: 10px; white-space: pre-wrap; line-height: 1.7; color: #dbeafe; }
        .record-actions { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
        .record-actions button { padding: 9px 12px; }
        .empty-state { color: var(--muted); border: 1px dashed var(--line); border-radius: 14px; padding: 14px; }
        @media (max-width: 1100px) {
          .shell { grid-template-columns: 1fr; }
          .sidebar { border-right: 0; border-bottom: 1px solid var(--line); }
          .grid-two { grid-template-columns: 1fr; }
        }
      </style>
    `
  );

  const refs = {
    apiStatus: byId("apiStatus"),
    refreshButton: byId("refreshButton"),
    settingsToggle: byId("settingsToggle"),
    settingsBody: byId("settingsBody"),
    langSelect: byId("langSelect"),
    versionSelect: byId("versionSelect"),
    modelRefresh: byId("modelRefresh"),
    modelSelect: byId("modelSelect"),
    modelInfo: byId("modelInfo"),
    chapterInput: byId("chapterInput"),
    verseInput: byId("verseInput"),
    loadChapterButton: byId("loadChapterButton"),
    readingBookSelect: byId("readingBookSelect"),
    versionBadge: byId("versionBadge"),
    bookBadge: byId("bookBadge"),
    pageSubtitle: byId("pageSubtitle"),
    chapterText: byId("chapterText"),
    studyCompare: byId("studyCompare"),
    studyRequest: byId("studyRequest"),
    studyButton: byId("studyButton"),
    studyCopyButton: byId("studyCopyButton"),
    studyOutput: byId("studyOutput"),
    studySearch: byId("studySearch"),
    studySort: byId("studySort"),
    studyClear: byId("studyClear"),
    studyHistory: byId("studyHistory"),
    sermonScope: byId("sermonScope"),
    sermonStyle: byId("sermonStyle"),
    sermonBook: byId("sermonBook"),
    sermonTheme: byId("sermonTheme"),
    sermonAudience: byId("sermonAudience"),
    sermonNotes: byId("sermonNotes"),
    sermonButton: byId("sermonButton"),
    sermonCopyButton: byId("sermonCopyButton"),
    sermonOutput: byId("sermonOutput"),
    sermonSearch: byId("sermonSearch"),
    sermonSort: byId("sermonSort"),
    sermonClear: byId("sermonClear"),
    sermonHistory: byId("sermonHistory"),
    devScope: byId("devScope"),
    devBook: byId("devBook"),
    devFeeling: byId("devFeeling"),
    devButton: byId("devButton"),
    devCopyButton: byId("devCopyButton"),
    devOutput: byId("devOutput"),
    devSearch: byId("devSearch"),
    devSort: byId("devSort"),
    devClear: byId("devClear"),
    devHistory: byId("devHistory"),
    chatScope: byId("chatScope"),
    chatBook: byId("chatBook"),
    chatQuestion: byId("chatQuestion"),
    chatButton: byId("chatButton"),
    chatCopyButton: byId("chatCopyButton"),
    chatOutput: byId("chatOutput"),
    chatSearch: byId("chatSearch"),
    chatSort: byId("chatSort"),
    chatClear: byId("chatClear"),
    chatHistory: byId("chatHistory"),
    questionsScope: byId("questionsScope"),
    questionsBook: byId("questionsBook"),
    questionsCount: byId("questionsCount"),
    questionsMode: byId("questionsMode"),
    questionsButton: byId("questionsButton"),
    questionsCopyButton: byId("questionsCopyButton"),
    questionsOutput: byId("questionsOutput"),
    questionsSearch: byId("questionsSearch"),
    questionsSort: byId("questionsSort"),
    questionsClear: byId("questionsClear"),
    questionsHistory: byId("questionsHistory"),
    historySummary: byId("historySummary"),
    allHistory: byId("allHistory"),
    importRefresh: byId("importRefresh"),
    importSources: byId("importSources"),
    supportTitle: byId("supportTitle"),
    supportText: byId("supportText"),
    supportPaypal: byId("supportPaypal"),
    supportPickpay: byId("supportPickpay"),
    supportKeyHint: byId("supportKeyHint"),
  };

  function byId(id) {
    return document.getElementById(id);
  }

  function getValue(ref, fallback = "") {
    if (!ref || typeof ref.value !== "string") {
      return fallback;
    }
    return ref.value;
  }

  function getTranslation(path, fallback) {
    const keys = String(path || "").split(".");
    let current = state.uiTranslations;
    for (const key of keys) {
      if (!current || typeof current !== "object" || !(key in current)) {
        return fallback;
      }
      current = current[key];
    }
    return typeof current === "string" && current.trim() ? current : fallback;
  }

  async function loadUiTranslations(lang) {
    const langCode = (lang || getValue(refs.langSelect, "pt") || "pt").toLowerCase();
    try {
      const data = await apiGet(`/api/meta/translation?lang=${encodeURIComponent(langCode)}`);
      state.uiTranslations = data.items && typeof data.items === "object" ? data.items : {};
    } catch (_) {
      state.uiTranslations = {};
    }
  }

  function setLabelText(forId, text) {
    const label = document.querySelector(`label[for="${forId}"]`);
    if (label) {
      label.textContent = text;
    }
  }

  function setSelectOptionText(selectRef, value, text) {
    if (!selectRef) {
      return;
    }
    const option = selectRef.querySelector(`option[value="${value}"]`);
    if (option && text) {
      option.textContent = text;
    }
  }

  function setCardTitleByChild(childRef, text) {
    if (!childRef || !text) {
      return;
    }
    const card = childRef.closest(".card");
    const title = card ? card.querySelector(".card-title") : null;
    if (title) {
      title.textContent = text;
    }
  }

  function stripDecorators(text) {
    return String(text || "").replace(/^[^\p{L}\p{N}]+/u, "").trim();
  }

  function setOutputTitle(outputRef, text) {
    if (!outputRef || !text) {
      return;
    }
    const title = outputRef.previousElementSibling;
    if (title && title.classList.contains("output-title")) {
      title.textContent = text;
    }
  }

  function updateWaitingText(ref, message) {
    if (!ref || !message) {
      return;
    }
    const current = String(ref.textContent || "").trim();
    const knownDefaults = [
      "Aguardando solicitacao...",
      "Aguardando solicitacao…",
      "Aguardando geracao...",
      "Aguardando pergunta...",
      "Awaiting request...",
      "Awaiting generation...",
      "Awaiting question...",
    ];
    if (!current || knownDefaults.includes(current)) {
      ref.textContent = message;
    }
  }

  function localizedSermonStyles() {
    const lang = (getValue(refs.langSelect, "pt") || "pt").toLowerCase();
    const map = SERMON_STYLES_I18N[lang] || SERMON_STYLES_I18N.en;
    return SERMON_STYLES.map((item) => {
      const translated = map[item.value];
      return {
        ...item,
        label: translated?.label || item.label,
        subtitle: translated?.subtitle || item.subtitle,
      };
    });
  }

  function applyUiTranslations() {
    document.title = getTranslation("menu.reading", "Biblical Study AI");

    const tabs = {
      reading: getTranslation("menu.reading", "Leitura"),
      sermon: getTranslation("menu.sermon_gen", "Sermoes"),
      devotional: getTranslation("menu.devotional", "Devocional"),
      chat: getTranslation("menu.chat", "Chat"),
      questions: getTranslation("menu.questions_gen", "Perguntas"),
      history: getTranslation("menu.history", "Historico"),
      import: getTranslation("menu.import", "Importar"),
    };
    Object.entries(tabs).forEach(([tabName, text]) => {
      const tab = document.querySelector(`.tab[data-tab="${tabName}"]`);
      if (tab) {
        tab.textContent = String(text || "").replace(/^[^\p{L}\p{N}]+/u, "").trim() || tab.textContent;
      }
    });

    setLabelText("langSelect", getTranslation("labels.language_selector", "Idioma"));
    setLabelText("versionSelect", getTranslation("labels.bible_version", "Versao"));
    setLabelText("modelSelect", getTranslation("labels.ollama_model", "Modelo Ollama"));
    setLabelText("chapterInput", getTranslation("labels.chapter_selector", "Capitulo"));
    setLabelText("verseInput", getTranslation("labels.verses", "Versiculos base"));
    setLabelText("readingBookSelect", getTranslation("labels.book_selector", "Livro"));
    setLabelText("sermonBook", getTranslation("labels.book_selector", "Livro para contexto"));
    setLabelText("devBook", getTranslation("labels.book_selector", "Livro para contexto"));
    setLabelText("chatBook", getTranslation("labels.book_selector", "Livro para contexto"));
    setLabelText("questionsBook", getTranslation("labels.book_selector", "Livro para contexto"));
    setLabelText("sermonScope", getTranslation("labels.scope", "Escopo"));
    setLabelText("devScope", getTranslation("labels.scope", "Escopo"));
    setLabelText("chatScope", getTranslation("labels.scope", "Escopo"));
    setLabelText("questionsScope", getTranslation("labels.scope", "Escopo"));
    setLabelText("studyRequest", getTranslation("labels.extra_notes", "Pedido"));
    setLabelText("chatQuestion", getTranslation("labels.your_question", "Pergunta"));
    setLabelText("sermonStyle", getTranslation("labels.generation_mode", "Estilo"));
    setLabelText("devFeeling", getTranslation("labels.theme_or_feeling", "Tema / sentimento"));

    refs.refreshButton.textContent = getTranslation("buttons.clear_cache", "Recarregar").replace("🔄 ", "");
    refs.modelRefresh.textContent = getTranslation("buttons.import_versions", "Atualizar modelos").replace("🔄 ", "");
    refs.loadChapterButton.textContent = getTranslation("labels.reading_page", "Carregar Capitulo");
    refs.studyButton.textContent = getTranslation("buttons.generate_explanation", "Gerar Exegese").replace("✨ ", "");
    refs.sermonButton.textContent = getTranslation("buttons.generate_sermon", "Gerar Sermao").replace("✨ ", "");
    refs.devButton.textContent = getTranslation("buttons.generate_devotional", "Gerar Devocional").replace("✨ ", "");
    refs.chatButton.textContent = getTranslation("buttons.send_question", "Enviar Pergunta").replace("✨ ", "");
    refs.questionsButton.textContent = getTranslation("menu.questions_gen", "Gerar Perguntas").replace(/^[^\p{L}\p{N}]+/u, "").trim();
    refs.studyCopyButton.textContent = getTranslation("buttons.copy", "Copiar").replace("📋 ", "");
    refs.sermonCopyButton.textContent = getTranslation("buttons.copy_sermon", "Copiar resultado").replace("📋 ", "");
    refs.devCopyButton.textContent = getTranslation("buttons.copy_devotional", "Copiar resultado").replace("📋 ", "");
    refs.chatCopyButton.textContent = getTranslation("buttons.copy_conversation", "Copiar resposta").replace("📋 ", "");
    refs.questionsCopyButton.textContent = getTranslation("buttons.copy", "Copiar resultado").replace("📋 ", "");
    refs.importRefresh.textContent = getTranslation("buttons.import_versions", "Recarregar catalogo").replace("🔄 ", "");

    refs.modelInfo.textContent = `${getTranslation("labels.ollama_model", "Modelo Ollama")}: ${state.models.length}`;
    refs.verseInput.placeholder = getTranslation("labels.verses", "1,2,3 ou 1-5");
    refs.studySearch.placeholder = getTranslation("labels.search_history", getTranslation("labels.search_placeholder", "Buscar no historico")).replace("🔍 ", "");
    refs.sermonSearch.placeholder = getTranslation("labels.search_sermons_placeholder", "Buscar sermoes");
    refs.devSearch.placeholder = getTranslation("labels.search_devotionals_placeholder", "Buscar devocionais");
    refs.chatSearch.placeholder = getTranslation("labels.search_conversations_placeholder", "Buscar conversas");
    refs.questionsSearch.placeholder = getTranslation("labels.search_placeholder", "Buscar perguntas");
    refs.chatQuestion.placeholder = getTranslation("labels.your_question", "Digite sua duvida biblica...");

    refs.studyClear.textContent = getTranslation("buttons.clear_history", "Limpar historico").replace("🗑️ ", "");
    refs.sermonClear.textContent = getTranslation("buttons.clear_history", "Limpar historico").replace("🗑️ ", "");
    refs.devClear.textContent = getTranslation("buttons.clear_history", "Limpar historico").replace("🗑️ ", "");
    refs.chatClear.textContent = getTranslation("buttons.clear_history", "Limpar historico").replace("🗑️ ", "");
    refs.questionsClear.textContent = getTranslation("buttons.clear_history", "Limpar historico").replace("🗑️ ", "");

    const mostRecentLabel = getTranslation("labels.most_recent_plural", getTranslation("labels.most_recent", "Mais recente"));
    const oldestLabel = getTranslation("labels.oldest_plural", getTranslation("labels.oldest", "Mais antigo"));
    [refs.studySort, refs.sermonSort, refs.devSort, refs.chatSort, refs.questionsSort].forEach((sortRef) => {
      setSelectOptionText(sortRef, "recent", mostRecentLabel);
      setSelectOptionText(sortRef, "oldest", oldestLabel);
    });

    const scopeSpecific = getTranslation("labels.specific_book", "Livro especifico");
    const scopeSelected = getTranslation("labels.multiple_books", "Livros selecionados");
    const scopeWhole = getTranslation("labels.whole_bible", getTranslation("labels.entire_bible", "Toda a Biblia"));
    [refs.sermonScope, refs.devScope, refs.chatScope, refs.questionsScope].forEach((scopeRef) => {
      setSelectOptionText(scopeRef, "specific", scopeSpecific);
      setSelectOptionText(scopeRef, "selected", scopeSelected);
      setSelectOptionText(scopeRef, "whole", scopeWhole);
    });

    setSelectOptionText(refs.questionsMode, "with", getTranslation("labels.with_answers", "Com respostas"));
    setSelectOptionText(refs.questionsMode, "only", getTranslation("labels.only_questions", "Somente perguntas"));

    setCardTitleByChild(refs.sermonScope, stripDecorators(getTranslation("headers.sermon_generator", "Gerador de Sermoes")));
    setCardTitleByChild(refs.studyHistory, stripDecorators(getTranslation("headers.bible_studies_history", "Historico de Estudos")));
    setCardTitleByChild(refs.sermonHistory, stripDecorators(getTranslation("headers.sermons_history", "Historico de Sermoes")));
    setCardTitleByChild(refs.devHistory, stripDecorators(getTranslation("headers.devotionals_history", "Historico de Devocionais")));
    setCardTitleByChild(refs.chatHistory, stripDecorators(getTranslation("headers.conversations_history", "Historico do Chat")));
    setCardTitleByChild(refs.questionsHistory, stripDecorators(getTranslation("menu.questions_hist", "Historico de Perguntas")));
    setCardTitleByChild(refs.historySummary, stripDecorators(getTranslation("menu.history", "Historico Consolidado")));
    setCardTitleByChild(refs.allHistory, stripDecorators(getTranslation("labels.search_history", "Todos os Registros")));

    const uiLang = (getValue(refs.langSelect, "pt") || "pt").toLowerCase();
    if (uiLang === "en") {
      refs.supportTitle.textContent = "Support the project";
      refs.supportText.textContent = "If this app helps you, consider supporting its development.";
      refs.supportPaypal.textContent = "Donate via PayPal";
      refs.supportPickpay.textContent = "Copy PicPay key";
      refs.supportKeyHint.textContent = SUPPORT_PICKPAY_KEY ? "PicPay key available for copy." : "PicPay key not configured yet.";
    } else if (uiLang === "ar") {
      refs.supportTitle.textContent = "ادعم المشروع";
      refs.supportText.textContent = "إذا كان هذا التطبيق مفيدا لك، ففكر في دعم تطويره.";
      refs.supportPaypal.textContent = "تبرع عبر PayPal";
      refs.supportPickpay.textContent = "نسخ مفتاح PicPay";
      refs.supportKeyHint.textContent = SUPPORT_PICKPAY_KEY ? "مفتاح PicPay متاح للنسخ." : "مفتاح PicPay غير مضبوط بعد.";
    } else {
      refs.supportTitle.textContent = "Apoie o projeto";
      refs.supportText.textContent = "Se este sistema te ajuda, considere apoiar o desenvolvimento.";
      refs.supportPaypal.textContent = "Doar via PayPal";
      refs.supportPickpay.textContent = "Copiar chave PicPay";
      refs.supportKeyHint.textContent = SUPPORT_PICKPAY_KEY ? "Chave PicPay pronta para copia." : "Chave PicPay ainda nao configurada.";
    }

    refs.supportPickpay.disabled = !SUPPORT_PICKPAY_KEY;

    setOutputTitle(refs.studyOutput, stripDecorators(getTranslation("formatting.answer_label", "Resposta")));
    setOutputTitle(refs.sermonOutput, stripDecorators(getTranslation("formatting.explanation_label", "Resultado")));
    setOutputTitle(refs.devOutput, stripDecorators(getTranslation("formatting.explanation_label", "Resultado")));
    setOutputTitle(refs.chatOutput, stripDecorators(getTranslation("formatting.answer_label", "Resposta")));
    setOutputTitle(refs.questionsOutput, stripDecorators(getTranslation("formatting.explanation_label", "Resultado")));

    updateWaitingText(refs.studyOutput, getTranslation("messages.select_book_chapter", "Aguardando solicitacao..."));
    updateWaitingText(refs.sermonOutput, getTranslation("messages.generating_sermon", "Aguardando geracao..."));
    updateWaitingText(refs.devOutput, getTranslation("messages.generating_devotional", "Aguardando geracao..."));
    updateWaitingText(refs.chatOutput, getTranslation("messages.write_question_first", "Aguardando pergunta..."));
    updateWaitingText(refs.questionsOutput, getTranslation("messages.generating_questions", "Aguardando geracao..."));
  }

  function pickPreferredModel(models) {
    if (!Array.isArray(models) || !models.length) {
      return "";
    }

    const localModel = models.find((name) => !String(name).toLowerCase().includes("cloud"));
    return localModel || models[0];
  }

  function loadHistory(key) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : [];
    } catch (_) {
      return [];
    }
  }

  function saveHistory(key, items) {
    localStorage.setItem(key, JSON.stringify(items));
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function formatTime(timestamp) {
    return new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" }).format(new Date(timestamp));
  }

  function setStatus(message, ok) {
    refs.apiStatus.textContent = message;
    refs.apiStatus.className = ok ? "status ok" : "status warn";
  }

  function isRtl(lang) {
    return ["ar", "fa", "he", "ur"].includes(lang);
  }

  function updateDirection() {
    const lang = getValue(refs.langSelect, "pt") || "pt";
    const rtl = isRtl(lang);
    const dir = rtl ? "rtl" : "ltr";
    const align = rtl ? "right" : "left";
    
    // Apply to main output boxes
    [refs.chapterText, refs.studyOutput, refs.sermonOutput, refs.devOutput, refs.chatOutput, refs.questionsOutput].forEach(el => {
      if (el) {
        el.style.direction = dir;
        el.style.textAlign = align;
      }
    });
    
    // Apply to history and inputs
    document.querySelectorAll(".record-body, .textarea, .field:not(select)").forEach(el => {
      el.style.direction = dir;
      el.style.textAlign = align;
    });

    document.querySelectorAll(".book-item").forEach(el => {
      el.style.textAlign = align;
    });
  }

  function setActiveTab(tabName) {
    state.activeTab = tabName;
    document.querySelectorAll(".tab").forEach((button) => {
      button.classList.toggle("active", button.dataset.tab === tabName);
    });
    document.querySelectorAll(".tab-panel").forEach((panel) => {
      panel.classList.toggle("active", panel.id === tabName);
    });
  }

  function apiGet(path) {
    return fetch(`${API}${path}`, { cache: "no-store" }).then(async (response) => {
      if (!response.ok) {
        let detail = `HTTP ${response.status}`;
        try {
          const payload = await response.json();
          detail = payload.detail || detail;
        } catch (_) {
        }
        throw new Error(detail);
      }
      return response.json();
    });
  }

  function apiPost(path, body) {
    return fetch(`${API}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(async (response) => {
      if (!response.ok) {
        let detail = `HTTP ${response.status}`;
        try {
          const payload = await response.json();
          detail = payload.detail || detail;
        } catch (_) {
        }
        throw new Error(detail);
      }
      return response.json();
    });
  }

  function multiSelectValues(selectElement) {
    if (!selectElement) {
      return [];
    }
    return Array.from(selectElement.selectedOptions).map((option) => option.value);
  }

  function parseVerseSelection(raw) {
    const cleaned = String(raw || "").replace(/\s+/g, "");
    if (!cleaned) {
      return [];
    }
    const result = new Set();
    for (const part of cleaned.split(",")) {
      if (!part) {
        continue;
      }
      if (part.includes("-")) {
        const [startText, endText] = part.split("-");
        const start = Number.parseInt(startText, 10);
        const end = Number.parseInt(endText, 10);
        if (Number.isInteger(start) && Number.isInteger(end) && start > 0 && end >= start) {
          for (let index = start; index <= end; index += 1) {
            result.add(String(index));
          }
        }
      } else {
        const verse = Number.parseInt(part, 10);
        if (Number.isInteger(verse) && verse > 0) {
          result.add(String(verse));
        }
      }
    }
    return Array.from(result);
  }

  function buildVerseText(verses, selection) {
    const orderedKeys = selection && selection.length ? selection : Object.keys(verses || {}).sort((left, right) => Number(left) - Number(right));
    return orderedKeys
      .map((verseKey) => {
        const verseText = verses?.[verseKey];
        return verseText ? `${verseKey}. ${verseText}` : null;
      })
      .filter(Boolean)
      .join("\n");
  }

  async function loadLanguages() {
    if (!refs.langSelect) {
      return;
    }

    const previousSelection = getValue(refs.langSelect);
    const data = await apiGet("/api/meta/languages");
    state.languages = data.items || [];
    refs.langSelect.innerHTML = state.languages
      .map((item) => `<option value="${escapeHtml(item.code)}">${escapeHtml(item.name)} (${escapeHtml(item.code)})</option>`)
      .join("");

    const codes = state.languages.map((item) => item.code);
    if (previousSelection && codes.includes(previousSelection)) {
      refs.langSelect.value = previousSelection;
    } else if (codes.includes("pt")) {
      refs.langSelect.value = "pt";
    } else if (state.languages.length) {
      refs.langSelect.value = state.languages[0].code;
    }
  }

  async function loadOllamaModels() {
    if (!refs.modelSelect || !refs.modelInfo) {
      return;
    }

    const previousModel = String(getValue(refs.modelSelect) || "").trim();
    try {
      const data = await apiGet("/api/ai/models");
      state.models = Array.isArray(data.items) ? data.items : [];
    } catch (_) {
      state.models = [];
    }

    const combinedModels = Array.from(new Set([...state.models, ...MODEL_SUGGESTIONS]));

    refs.modelSelect.innerHTML = combinedModels
      .map((model) => {
        const isDetected = state.models.includes(model);
        const label = isDetected ? model : `${model} (sugestao)`;
        return `<option value="${escapeHtml(model)}">${escapeHtml(label)}</option>`;
      })
      .join("");

    refs.modelInfo.textContent = `Modelos detectados no Ollama: ${state.models.length}`;

    if (previousModel) {
      refs.modelSelect.value = combinedModels.includes(previousModel) ? previousModel : "";
      return;
    }

    const preferredModel = pickPreferredModel(state.models.length ? state.models : combinedModels);
    if (preferredModel) {
      refs.modelSelect.value = preferredModel;
    }
  }

  async function loadVersions() {
    if (!refs.versionSelect) {
      return;
    }

    const lang = getValue(refs.langSelect, "pt") || "pt";
    const previousSelection = getValue(refs.versionSelect);
    const data = await apiGet(`/api/bible/versions?lang=${encodeURIComponent(lang)}`);
    state.versions = data.versions || [];
    refs.versionSelect.innerHTML = state.versions
      .map((version) => `<option value="${escapeHtml(version)}">${escapeHtml(version)}</option>`)
      .join("");

    if (previousSelection && state.versions.includes(previousSelection)) {
      refs.versionSelect.value = previousSelection;
    } else if (state.versions.length) {
      refs.versionSelect.value = state.versions[0];
    }
  }

  function renderBookOptions() {
    const options = state.books
      .map((book) => `<option value="${escapeHtml(book.key)}">${escapeHtml(book.name)}</option>`)
      .join("");
    const bookSelectors = [refs.readingBookSelect, refs.sermonBook, refs.devBook, refs.chatBook, refs.questionsBook];
    bookSelectors.forEach((selectElement) => {
      if (!selectElement) {
        return;
      }
      const previous = getValue(selectElement);
      selectElement.innerHTML = options;
      if (previous && state.books.some((book) => book.key === previous)) {
        selectElement.value = previous;
      } else if (state.selectedBook) {
        selectElement.value = state.selectedBook;
      }
    });

    // Populate sermon styles
    refs.sermonStyle.innerHTML = localizedSermonStyles()
      .map(s => `<option value="${escapeHtml(s.value)}">${escapeHtml(s.label)} (${escapeHtml(s.subtitle)})</option>`)
      .join("");

    updateScopeControls();
  }

  function toggleSettingsPanel() {
    const panel = byId("settingsPanel");
    if (!panel || !refs.settingsToggle) {
      return;
    }
    const collapsed = panel.classList.toggle("collapsed");
    refs.settingsToggle.textContent = collapsed ? "▼" : "▲";
    refs.settingsToggle.setAttribute("aria-expanded", String(!collapsed));
  }

  function updateScopeControls() {
    [refs.readingBookSelect, refs.sermonBook, refs.devBook, refs.chatBook, refs.questionsBook].forEach((selectElement) => {
      if (!selectElement || getValue(selectElement)) {
        return;
      }
      if (state.selectedBook) {
        selectElement.value = state.selectedBook;
      }
    });
  }

  function getScopeBookKeys(scope, selectedBook, maxBooks) {
    if (scope === "specific") {
      return [selectedBook || state.selectedBook].filter(Boolean);
    }

    if (scope === "selected") {
      return [selectedBook || state.selectedBook].filter(Boolean);
    }

    const total = Math.max(2, maxBooks || 6);
    const otCount = Math.ceil(total / 2);
    const ntCount = Math.floor(total / 2);
    const otKeys = state.books.slice(0, OT_CUTOFF).slice(0, otCount).map((book) => book.key);
    const ntKeys = state.books.slice(OT_CUTOFF).slice(0, ntCount).map((book) => book.key);
    const keys = [...otKeys, ...ntKeys].filter(Boolean);
    return keys.length ? keys : [state.selectedBook].filter(Boolean);
  }

  function renderBookList() {
    // Lista lateral removida. Selecao de livro agora e por dropdown em cada aba.
  }

  function updateBadges() {
    refs.versionBadge.textContent = `Versao: ${refs.versionSelect.value || "-"}`;
    const selectedBook = state.books.find((book) => book.key === state.selectedBook);
    refs.bookBadge.textContent = `Livro: ${selectedBook ? selectedBook.name : "-"}`;
  }

  async function loadBooks() {
    const lang = getValue(refs.langSelect, "pt") || "pt";
    const version = getValue(refs.versionSelect);
    const previousBook = getValue(refs.readingBookSelect) || state.selectedBook;
    if (!version) {
      state.books = [];
      state.selectedBook = null;
      renderBookList();
      renderBookOptions();
      return;
    }
    const data = await apiGet(`/api/bible/books?lang=${encodeURIComponent(lang)}&version=${encodeURIComponent(version)}`);
    state.books = data.items || [];
    const hasPreviousBook = previousBook && state.books.some((book) => book.key === previousBook);
    state.selectedBook = hasPreviousBook ? previousBook : (state.books.length ? state.books[0].key : null);
    if (refs.readingBookSelect && state.selectedBook) {
      refs.readingBookSelect.value = state.selectedBook;
    }
    renderBookList();
    renderBookOptions();
    updateBadges();
  }

  async function ensureValidBibleSelection() {
    if (!state.versions.length) {
      await loadVersions();
    }

    if (!state.versions.length) {
      refs.versionSelect.innerHTML = "";
      state.books = [];
      state.selectedBook = null;
      renderBookList();
      renderBookOptions();
      return false;
    }

    let version = getValue(refs.versionSelect);
    let versionAdjusted = false;
    if (!version || !state.versions.includes(version)) {
      refs.versionSelect.value = state.versions[0];
      version = refs.versionSelect.value;
      versionAdjusted = true;
    }

    if (versionAdjusted || !state.books.length) {
      await loadBooks();
    }

    const hasSelectedBook = state.selectedBook && state.books.some((book) => book.key === state.selectedBook);
    if (!hasSelectedBook) {
      state.selectedBook = state.books.length ? state.books[0].key : null;
      renderBookList();
      updateBadges();
    }

    return Boolean(version && state.selectedBook);
  }

  async function loadChapter(retryOnMismatch = true) {
    state.selectedBook = getValue(refs.readingBookSelect) || state.selectedBook;
    const ready = await ensureValidBibleSelection();
    if (!ready || !state.selectedBook) {
      refs.chapterText.textContent = "Nenhum livro selecionado.";
      return;
    }

    const lang = getValue(refs.langSelect, "pt") || "pt";
    const version = getValue(refs.versionSelect);
    if (!version) {
      refs.chapterText.textContent = "Nenhuma versao selecionada para este idioma.";
      return;
    }

    const chapter = Number.parseInt(getValue(refs.chapterInput, "1") || "1", 10) || 1;
    let data;
    try {
      data = await apiGet(
        `/api/bible/chapter?lang=${encodeURIComponent(lang)}&version=${encodeURIComponent(version)}&book=${encodeURIComponent(state.selectedBook)}&chapter=${encodeURIComponent(chapter)}`
      );
    } catch (error) {
      const canRetry = retryOnMismatch && /Versao nao encontrada|Livro nao encontrado/i.test(String(error?.message || ""));
      if (canRetry) {
        await loadVersions();
        await loadBooks();
        return loadChapter(false);
      }
      throw error;
    }
    state.chapterData = data;
    const verses = data.verses || {};
    const selectedVerses = parseVerseSelection(getValue(refs.verseInput));
    const text = buildVerseText(verses, selectedVerses);
    refs.chapterText.textContent = text || "Capitulo vazio.";
    refs.studyOutput.textContent = getTranslation("messages.select_book_chapter", "Aguardando solicitacao...");
    updateBadges();
    updateDirection();
    return data;
  }

  async function collectChapterText(bookKey, chapterNumber) {
    const lang = getValue(refs.langSelect, "pt") || "pt";
    const version = getValue(refs.versionSelect);
    const chapter = Number.parseInt(String(chapterNumber || 1), 10) || 1;
    const data = await apiGet(
      `/api/bible/chapter?lang=${encodeURIComponent(lang)}&version=${encodeURIComponent(version)}&book=${encodeURIComponent(bookKey)}&chapter=${encodeURIComponent(chapter)}`
    );
    const verses = data.verses || {};
    return {
      reference: `${data.book} ${data.chapter}`,
      text: buildVerseText(verses),
    };
  }

  async function collectSelectedBooksContext(bookKeys, maxBooks, chapterMode, currentBookKey = state.selectedBook) {
    const selected = (bookKeys || []).slice(0, maxBooks);
    const chunks = [];
    for (const bookKey of selected) {
      const chapterNumber = chapterMode === "current" && bookKey === currentBookKey ? getValue(refs.chapterInput, "1") : 1;
      try {
        const chunk = await collectChapterText(bookKey, chapterNumber);
        if (chunk.text) {
          chunks.push(`**${chunk.reference}**\n${chunk.text}`);
        }
      } catch (_) {
      }
    }
    return chunks.join("\n\n");
  }

  async function collectComparisonContext() {
    if (!state.selectedBook || !state.versions.length) {
      return "";
    }
    const lang = getValue(refs.langSelect, "pt") || "pt";
    const chapter = Number.parseInt(getValue(refs.chapterInput, "1") || "1", 10) || 1;
    const chunks = [];
    for (const version of state.versions) {
      try {
        const data = await apiGet(
          `/api/bible/chapter?lang=${encodeURIComponent(lang)}&version=${encodeURIComponent(version)}&book=${encodeURIComponent(state.selectedBook)}&chapter=${encodeURIComponent(chapter)}`
        );
        const verses = data.verses || {};
        const text = buildVerseText(verses, parseVerseSelection(getValue(refs.verseInput)));
        if (text) {
          chunks.push(`**${version}**\n${text}`);
        }
      } catch (_) {
      }
    }
    return chunks.join("\n\n");
  }

  function buildStudyRequest(compareMode) {
    if (compareMode) {
      return [
        "Compare as diferentes traducoes do mesmo texto biblico.",
        "Analise diferencas de vocabulario, escolhas de traducao e possiveis impactos teologicos.",
        "Entregue uma resposta clara, equilibrada e pastoral.",
      ].join(" ");
    }
    return String(refs.studyRequest.value || "").trim() || "Explique o contexto historico e teologico do texto e aplique-o de forma pastoral.";
  }

  function buildSermonRequest() {
    const style = refs.sermonStyle.value;
    const theme = String(refs.sermonTheme.value || "").trim() || "Tema a ser desenvolvido do texto";
    const audience = String(refs.sermonAudience.value || "").trim() || "Igreja geral";
    const notes = String(refs.sermonNotes.value || "").trim() || "Nenhuma nota adicional";
    const styleMap = {
      "Analitico-Essencia": "Tom serio e investigativo. Persona: O Investigador. Foco em motivacoes ocultas, racionalidade espiritual, contraste entre aparencia e essencia, e profundidade psicologica do texto.",
      "Expositivo-Teologico": "Tom academico e didatico. Persona: O Professor. Explique o contexto historico-geografico, as palavras-chave no original (se possivel), a doutrina sistematica e a hermeneutica precisa.",
      "Narrativo-Imersivo": "Tom cinematografico e emocional. Persona: O Storyteller. Reconte a cena com atmosfera, descreva os sentimentos dos personagens, o conflito e leve ao clÃ­max da mensagem de forma envolvente.",
      "Devocional-Pratico": "Tom empatico e direto. Persona: O Mentor. Traga conforto, aplicacao para o dia a dia, passos concretos para a vida crista e encorajamento constante.",
      "Cristocentrico-Tipologico": "Tom adorador e reverente. Persona: O Revelador. Conecte cada sombra do Antigo Testamento Ã  luz do Novo Testamento, focando em Cristo, na cruz e na redencao final.",
      "Profetico-Confrontador": "Tom urgente e firme. Persona: O Atalaia. Confronte o pecado com autoridade, chame ao arrependimento, destaque a santidade de Deus e a necessidade de mudanca imediata.",
      "Apologetico-Filosofico": "Tom racional e persuasivo. Persona: O Defensor. Responda a objecoes intelectuais, use logica e filosofia crista para sustentar a fe e demonstrar a superioridade da cosmovisao biblica.",
    };
    return [
      `Voce e um pregador experiente. Escreva um sermao completo seguindo esta orientacao: ${styleMap[style] || "tom pastoral equilibrado"}.`,
      `Tema central: ${theme}.`,
      `Publico-alvo: ${audience}.`,
      `Notas e enfoques especificos: ${notes}.`,
      "Estrutura obrigatoria: Titulo criativo, Introducao impactante, 3 pontos de desenvolvimento com base no texto, Aplicacao pratica detalhada e Conclusao com apelo/convite.",
      "Importante: Seja fiel ao texto biblico fornecido no contexto, nao invente fatos istoricos e mantenha um linguajar digno.",
    ].join("\n");
  }

  function buildDevotionalRequest() {
    const feeling = String(refs.devFeeling.value || "").trim() || "Gratidao";
    return [
      `Crie um devocional breve sobre ${feeling}.`,
      "Estrutura: Leitura, Reflexao e Oracao.",
      "A linguagem deve ser simples, calorosa e pratica.",
      "Termine a oracao com Amem.",
    ].join(" ");
  }

  function buildChatRequest(question) {
    return [
      `O usuario pergunta: ${question}.`,
      "Responda com base no texto biblico, seja didatico e cuidadoso.",
      "Evite inventar informacoes e destaque aplicacoes praticas.",
    ].join(" ");
  }

  function buildQuestionsRequest(count, withAnswers) {
    const modeText = withAnswers ? "com respostas curtas e diretas" : "somente perguntas";
    return [
      `Gere exatamente ${count} perguntas biblicas ${modeText}.`,
      "As perguntas devem explorar curiosidades, contexto historico, personagens e ensinamentos.",
      withAnswers ? "Mantenha as respostas em 1 ou 2 frases." : "Nao adicione respostas.",
      "Use numeracao clara e texto objetivo.",
    ].join(" ");
  }

  async function callGenerate(kind, reference, context, request, options = {}) {
    const lang = getValue(refs.langSelect, "pt") || "pt";
    const model = String(getValue(refs.modelSelect) || "").trim() || null;
    const payload = {
      kind,
      reference,
      context,
      request,
      language: lang,
      model,
      temperature: options.temperature ?? 0.2,
      max_tokens: options.maxTokens ?? 1800,
      timeout_sec: options.timeoutSec ?? 180,
    };
    const data = await apiPost("/api/ai/generate", payload);
    return data.response || "";
  }

  function addHistory(type, entry) {
    state.histories[type].unshift(entry);
    saveHistory(STORAGE_KEYS[type], state.histories[type]);
    renderHistory(type);
    renderSummary();
  }

  function historyDomRefs(type) {
    const alias = type === "devotional" ? "dev" : type;
    return {
      search: byId(`${alias}Search`),
      sort: byId(`${alias}Sort`),
      clear: byId(`${alias}Clear`),
      container: byId(`${alias}History`),
    };
  }

  function historyItems(type) {
    const { search, sort } = historyDomRefs(type);
    const query = String(getValue(search) || "").trim().toLowerCase();
    const sortMode = getValue(sort, "recent");
    let items = state.histories[type].slice();
    if (query) {
      items = items.filter((item) => {
        const haystack = [item.reference, item.title, item.question, item.request, item.response, item.context, item.theme, item.feeling].filter(Boolean).join(" ").toLowerCase();
        return haystack.includes(query);
      });
    }
    if (sortMode === "oldest") {
      items = items.reverse();
    }
    return items;
  }

  function renderHistory(type) {
    const { container } = historyDomRefs(type);
    if (!container) {
      return;
    }
    const items = historyItems(type);
    if (!items.length) {
      container.innerHTML = `<div class="empty-state">${escapeHtml(getTranslation("messages.no_search_results", "Nenhum registro encontrado."))}</div>`;
      return;
    }
    container.innerHTML = `<div class="record-list">${items
      .map((item, index) => renderRecord(type, item, index))
      .join("")}</div>`;
    container.querySelectorAll("[data-action=copy]").forEach((button) => button.addEventListener("click", () => copyText(button.dataset.text || "")));
    container.querySelectorAll("[data-action=pdf]").forEach((button) => button.addEventListener("click", () => exportPdfFromRecord(type, Number(button.dataset.index))));
    container.querySelectorAll("[data-action=delete]").forEach((button) => button.addEventListener("click", () => deleteHistoryEntry(type, Number(button.dataset.index))));
    updateDirection();
  }

  function renderRecord(type, item, index) {
    const title = item.title || item.reference || item.question || "Registro";
    const metaParts = [formatTime(item.timestamp)];
    if (item.version) metaParts.push(`${getTranslation("captions.version", "Versao:").replace(/^[^\p{L}\p{N}]+/u, "").trim()} ${item.version}`);
    if (item.model) metaParts.push(`${getTranslation("captions.model", "Modelo:").replace(/^[^\p{L}\p{N}]+/u, "").trim()} ${item.model}`);
    const scopeLabels = {
      specific: getTranslation("labels.specific_book", "Livro especifico"),
      selected: getTranslation("labels.multiple_books", "Livros selecionados"),
      whole: getTranslation("labels.whole_bible", getTranslation("labels.entire_bible", "Toda a Biblia")),
    };
    const scopeText = item.scope ? scopeLabels[item.scope] || item.scope : "";
    if (scopeText) metaParts.push(`${getTranslation("labels.scope_colon", "Escopo:").replace(/^[^\p{L}\p{N}]+/u, "").trim()} ${scopeText}`);
    const body = item.response || item.answer || item.content || item.text || "";
    return `
      <article class="record">
        <div class="record-head">
          <div>
            <div class="record-title">${escapeHtml(title)}</div>
            <div class="record-meta">${escapeHtml(metaParts.join(" | "))}</div>
          </div>
        </div>
        ${item.context ? `<div class="record-body"><strong>${escapeHtml(getTranslation("formatting.context_label", "Contexto:").replace(/^[^\\p{L}\\p{N}]+/u, "").replace(/:$/, ""))}</strong>\n${escapeHtml(item.context)}</div>` : ""}
        ${body ? `<div class="record-body"><strong>${escapeHtml(getTranslation("formatting.explanation_label", "Conteudo:").replace(/^[^\\p{L}\\p{N}]+/u, "").replace(/:$/, ""))}</strong>\n${escapeHtml(body)}</div>` : ""}
        <div class="record-actions">
          <button class="ghost-button" data-action="copy" data-text="${escapeHtml(buildCopyText(type, item))}">${escapeHtml(getTranslation("buttons.copy", "Copiar").replace(/^[^\\p{L}\\p{N}]+/u, "").trim())}</button>
          <button class="ghost-button" data-action="pdf" data-index="${index}">${escapeHtml(getTranslation("buttons.generate_pdf", "PDF").replace(/^[^\\p{L}\\p{N}]+/u, "").trim() || "PDF")}</button>
          <button class="ghost-button" data-action="delete" data-index="${index}">${escapeHtml(getTranslation("buttons.delete", "Excluir").replace(/^[^\\p{L}\\p{N}]+/u, "").trim())}</button>
        </div>
      </article>
    `;
  }

  function buildCopyText(type, item) {
    const parts = [];
    parts.push(item.title || item.reference || item.question || "Registro");
    if (item.context) {
      parts.push(getTranslation("formatting.context_label", "Contexto:"));
      parts.push(item.context);
    }
    if (item.response) {
      parts.push(getTranslation("formatting.answer_label", "Resposta:"));
      parts.push(item.response);
    } else if (item.answer) {
      parts.push(getTranslation("formatting.answer_label", "Resposta:"));
      parts.push(item.answer);
    }
    return parts.join("\n\n");
  }

  async function copyText(text) {
    await navigator.clipboard.writeText(text);
  }

  function openExternal(url) {
    if (!url) {
      return;
    }
    try {
      window.open(url, "_blank", "noopener,noreferrer");
    } catch (_) {
      window.location.href = url;
    }
  }

  async function exportPdfFromRecord(type, index) {
    const items = historyItems(type);
    const item = items[index];
    if (!item) {
      return;
    }
    const title = item.title || item.reference || item.question || "Registro";
    const scopeLabels = {
      specific: getTranslation("labels.specific_book", "Livro especifico"),
      selected: getTranslation("labels.multiple_books", "Livros selecionados"),
      whole: getTranslation("labels.whole_bible", getTranslation("labels.entire_bible", "Toda a Biblia")),
    };
    const scopeSubtitle = item.scope ? scopeLabels[item.scope] || item.scope : "";
    const sections = [];
    if (item.context) {
      sections.push({ heading: stripDecorators(getTranslation("formatting.context_label", "Contexto")), body: item.context });
    }
    if (item.response) {
      sections.push({ heading: stripDecorators(getTranslation("formatting.explanation_label", "Resultado")), body: item.response });
    } else if (item.answer) {
      sections.push({ heading: stripDecorators(getTranslation("formatting.answer_label", "Resultado")), body: item.answer });
    }
    if (item.question) {
      sections.push({ heading: stripDecorators(getTranslation("formatting.question_label", "Pergunta")), body: item.question });
    }
    const response = await fetch(`${API}/api/export/pdf`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        subtitle: item.reference || scopeSubtitle || "Biblical Study AI",
        sections,
        footer: `Gerado em ${formatTime(Date.now())}`,
      }),
    });
    if (!response.ok) {
      throw new Error(`Falha ao gerar PDF: HTTP ${response.status}`);
    }
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `${title.replace(/[^a-z0-9]+/gi, "_").replace(/^_|_$/g, "") || "export"}.pdf`;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  }

  function deleteHistoryEntry(type, index) {
    const items = historyItems(type);
    const item = items[index];
    if (!item) {
      return;
    }
    const originalIndex = state.histories[type].findIndex((entry) => entry.timestamp === item.timestamp && (entry.reference || "") === (item.reference || ""));
    if (originalIndex >= 0) {
      state.histories[type].splice(originalIndex, 1);
      saveHistory(STORAGE_KEYS[type], state.histories[type]);
      renderHistory(type);
      renderSummary();
    }
  }

  function renderSummary() {
    refs.historySummary.innerHTML = Object.entries(state.histories)
      .map(([type, items]) => {
        const labels = {
          study: getTranslation("menu.reading", "Estudos").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          sermon: getTranslation("menu.sermon_gen", "Sermoes").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          devotional: getTranslation("menu.devotional", "Devocionais").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          chat: getTranslation("menu.chat", "Chats").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          questions: getTranslation("menu.questions_gen", "Perguntas").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
        };
        return `<div class="summary-card"><strong>${items.length}</strong>${labels[type]}</div>`;
      })
      .join("");

    const allItems = Object.entries(state.histories)
      .flatMap(([type, items]) => items.map((item) => ({ ...item, kind: type })))
      .sort((left, right) => right.timestamp - left.timestamp);

    if (!allItems.length) {
      refs.allHistory.innerHTML = `<div class="empty-state">${escapeHtml(getTranslation("messages.no_studies_yet", "Ainda nao ha registros."))}</div>`;
      return;
    }

    refs.allHistory.innerHTML = `<div class="record-list">${allItems
      .map((item) => {
        const title = item.title || item.reference || item.question || "Registro";
        const kindLabel = {
          study: getTranslation("menu.reading", "Estudo").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          sermon: getTranslation("menu.sermon_gen", "Sermao").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          devotional: getTranslation("menu.devotional", "Devocional").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          chat: getTranslation("menu.chat", "Chat").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          questions: getTranslation("menu.questions_gen", "Perguntas").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
        }[item.kind] || item.kind;
        const body = item.response || item.answer || item.content || item.text || "";
        return `
          <article class="record">
            <div class="record-head">
              <div>
                <div class="record-title">${escapeHtml(kindLabel)} - ${escapeHtml(title)}</div>
                <div class="record-meta">${escapeHtml(formatTime(item.timestamp))}</div>
              </div>
            </div>
            ${item.context ? `<div class="record-body"><strong>${escapeHtml(getTranslation("formatting.context_label", "Contexto:").replace(/^[^\\p{L}\\p{N}]+/u, "").replace(/:$/, ""))}</strong>\n${escapeHtml(item.context)}</div>` : ""}
            ${body ? `<div class="record-body"><strong>${escapeHtml(getTranslation("formatting.explanation_label", "Conteudo:").replace(/^[^\\p{L}\\p{N}]+/u, "").replace(/:$/, ""))}</strong>\n${escapeHtml(body)}</div>` : ""}
          </article>
        `;
      })
      .join("")}</div>`;
    updateDirection();
  }

  async function loadImportSources() {
    const lang = getValue(refs.langSelect, "pt") || "pt";
    const data = await apiGet(`/api/meta/import-sources?lang=${encodeURIComponent(lang)}`);
    state.importSources = data.items || [];
    if (!state.importSources.length) {
      refs.importSources.innerHTML = `<div class="empty-state">Nenhum arquivo JSON encontrado para este idioma.</div>`;
      return;
    }
    refs.importSources.innerHTML = state.importSources
      .map((item) => `<div class="record"><div class="record-title">${escapeHtml(item.version)}</div><div class="record-meta">${escapeHtml(item.name)} | ${escapeHtml(String(item.size))} bytes | ${escapeHtml(item.modified)}</div></div>`)
      .join("");
  }

  async function handleStudyGenerate() {
    refs.studyButton.disabled = true;
    refs.studyOutput.textContent = getTranslation("messages.generating_explanation", "Gerando...");
    try {
      const compareMode = refs.studyCompare.checked && state.versions.length > 1;
      const context = compareMode ? await collectComparisonContext() : await collectChapterContext();
      if (!context) {
        refs.studyOutput.textContent = "Nenhum contexto encontrado.";
        return;
      }
      const request = buildStudyRequest(compareMode);
      const reference = compareMode
        ? `${state.selectedBook ? state.selectedBook : "Biblia"} ${getValue(refs.chapterInput, "1") || 1} - comparacao`
        : `${state.selectedBook ? state.selectedBook : "Biblia"} ${getValue(refs.chapterInput, "1") || 1}`;
      const response = await callGenerate("study", reference, context, request, {
        temperature: 0.2,
        maxTokens: compareMode ? 2000 : 1500,
        timeoutSec: compareMode ? 240 : 180,
      });
      refs.studyOutput.textContent = response;
      updateDirection();
      addHistory("study", {
        timestamp: Date.now(),
        title: compareMode ? "Comparacao de versoes" : "Estudo biblico",
        reference,
        context,
        response,
        version: refs.versionSelect.value,
        model: String(getValue(refs.modelSelect) || "").trim(),
        scope: compareMode ? "Comparacao" : "Capitulo",
      });
    } catch (error) {
      refs.studyOutput.textContent = `Erro: ${error.message}`;
    } finally {
      refs.studyButton.disabled = false;
    }
  }

  async function collectChapterContext() {
    if (!state.chapterData) {
      await loadChapter();
    }
    if (!state.chapterData) {
      return "";
    }
    const verses = state.chapterData.verses || {};
    const selected = parseVerseSelection(getValue(refs.verseInput));
    const text = buildVerseText(verses, selected);
    return text || buildVerseText(verses);
  }

  async function handleSermonGenerate() {
    refs.sermonButton.disabled = true;
    refs.sermonOutput.textContent = getTranslation("messages.generating_sermon", "Gerando...");
    try {
      const scope = getValue(refs.sermonScope, "specific");
      const selectedBook = getValue(refs.sermonBook) || state.selectedBook;
      const scopeKeys = getScopeBookKeys(scope, selectedBook, scope === "selected" ? 8 : 10);
      const context =
        scope === "specific"
          ? await collectSelectedBooksContext([selectedBook].filter(Boolean), 1, "current", selectedBook)
          : await collectSelectedBooksContext(scopeKeys, scope === "selected" ? 8 : 10, "first", selectedBook);
      if (!context) {
        refs.sermonOutput.textContent = "Nenhum contexto encontrado para o sermao.";
        return;
      }
      const request = buildSermonRequest();
      const reference = `${getValue(refs.sermonTheme, "Sermao") || "Sermao"} - ${getValue(refs.versionSelect, "-")}`;
      const response = await callGenerate("sermon", reference, context, request, { temperature: 0.35, maxTokens: 2600, timeoutSec: 360 });
      refs.sermonOutput.textContent = response;
      updateDirection();
      addHistory("sermon", {
        timestamp: Date.now(),
        title: getValue(refs.sermonTheme, "Sermao") || "Sermao",
        reference,
        context,
        response,
        theme: getValue(refs.sermonTheme),
        audience: getValue(refs.sermonAudience),
        version: getValue(refs.versionSelect),
        model: String(getValue(refs.modelSelect) || "").trim(),
        scope,
      });
    } catch (error) {
      refs.sermonOutput.textContent = `Erro: ${error.message}`;
    } finally {
      refs.sermonButton.disabled = false;
    }
  }

  async function handleDevotionalGenerate() {
    refs.devButton.disabled = true;
    refs.devOutput.textContent = getTranslation("messages.generating_devotional", "Gerando...");
    try {
      const scope = getValue(refs.devScope, "specific");
      const selectedBook = getValue(refs.devBook) || state.selectedBook;
      const scopeKeys = getScopeBookKeys(scope, selectedBook, scope === "selected" ? 8 : 10);
      const context =
        scope === "specific"
          ? await collectSelectedBooksContext([selectedBook].filter(Boolean), 1, "current", selectedBook)
          : await collectSelectedBooksContext(scopeKeys, scope === "selected" ? 8 : 10, "first", selectedBook);
      if (!context) {
        refs.devOutput.textContent = "Nenhum contexto encontrado para o devocional.";
        return;
      }
      const request = buildDevotionalRequest();
      const reference = getValue(refs.devFeeling, "Devocional") || "Devocional";
      const response = await callGenerate("devotional", reference, context, request, { temperature: 0.18, maxTokens: 1200, timeoutSec: 240 });
      refs.devOutput.textContent = response;
      updateDirection();
      addHistory("devotional", {
        timestamp: Date.now(),
        title: reference,
        reference,
        context,
        response,
        feeling: getValue(refs.devFeeling),
        version: getValue(refs.versionSelect),
        model: String(getValue(refs.modelSelect) || "").trim(),
        scope,
      });
    } catch (error) {
      refs.devOutput.textContent = `Erro: ${error.message}`;
    } finally {
      refs.devButton.disabled = false;
    }
  }

  async function handleChatGenerate() {
    refs.chatButton.disabled = true;
    refs.chatOutput.textContent = getTranslation("messages.generating_answer", "Gerando...");
    try {
      const question = String(getValue(refs.chatQuestion) || "").trim();
      if (!question) {
        refs.chatOutput.textContent = "Escreva uma pergunta primeiro.";
        return;
      }
      const scope = getValue(refs.chatScope, "specific");
      const selectedBook = getValue(refs.chatBook) || state.selectedBook;
      const scopeKeys = getScopeBookKeys(scope, selectedBook, scope === "selected" ? 8 : 10);
      const context =
        scope === "specific"
          ? await collectSelectedBooksContext([selectedBook].filter(Boolean), 1, "current", selectedBook)
          : await collectSelectedBooksContext(scopeKeys, scope === "selected" ? 8 : 10, "first", selectedBook);
      if (!context) {
        refs.chatOutput.textContent = "Nenhum contexto encontrado para o chat.";
        return;
      }
      const request = buildChatRequest(question);
      const reference = `Chat - ${getValue(refs.versionSelect, "-")}`;
      const response = await callGenerate("chat", reference, context, request, { temperature: 0.22, maxTokens: 1400, timeoutSec: 240 });
      refs.chatOutput.textContent = response;
      updateDirection();
      addHistory("chat", {
        timestamp: Date.now(),
        title: "Chat teologico",
        reference,
        context,
        question,
        answer: response,
        version: getValue(refs.versionSelect),
        model: String(getValue(refs.modelSelect) || "").trim(),
        scope,
      });
    } catch (error) {
      refs.chatOutput.textContent = `Erro: ${error.message}`;
    } finally {
      refs.chatButton.disabled = false;
    }
  }

  async function handleQuestionsGenerate() {
    refs.questionsButton.disabled = true;
    refs.questionsOutput.textContent = getTranslation("messages.generating_questions", "Gerando...");
    try {
      const count = Number.parseInt(getValue(refs.questionsCount, "10") || "10", 10) || 10;
      const withAnswers = getValue(refs.questionsMode, "with") === "with";
      const scope = getValue(refs.questionsScope, "specific");
      const selectedBook = getValue(refs.questionsBook) || state.selectedBook;
      const scopeKeys = getScopeBookKeys(scope, selectedBook, scope === "selected" ? 8 : 10);
      const context =
        scope === "specific"
          ? await collectSelectedBooksContext([selectedBook].filter(Boolean), 1, "current", selectedBook)
          : await collectSelectedBooksContext(scopeKeys, scope === "selected" ? 8 : 10, "first", selectedBook);
      if (!context) {
        refs.questionsOutput.textContent = "Nenhum contexto encontrado para perguntas.";
        return;
      }
      const request = buildQuestionsRequest(count, withAnswers);
      const reference = `Perguntas - ${getValue(refs.versionSelect, "-")}`;
      const response = await callGenerate("questions", reference, context, request, {
        temperature: 0.22,
        maxTokens: Math.min(count * (withAnswers ? 80 : 50) + 800, 8000),
        timeoutSec: Math.max(180, count * (withAnswers ? 10 : 4)),
      });
      refs.questionsOutput.textContent = response;
      updateDirection();
      addHistory("questions", {
        timestamp: Date.now(),
        title: withAnswers ? "Perguntas com respostas" : "Perguntas sem respostas",
        reference,
        context,
        response,
        questionsCount: count,
        withAnswers,
        version: getValue(refs.versionSelect),
        model: String(getValue(refs.modelSelect) || "").trim(),
        scope,
      });
    } catch (error) {
      refs.questionsOutput.textContent = `Erro: ${error.message}`;
    } finally {
      refs.questionsButton.disabled = false;
    }
  }

  function renderAllHistories() {
    renderHistory("study");
    renderHistory("sermon");
    renderHistory("devotional");
    renderHistory("chat");
    renderHistory("questions");
    renderSummary();
  }

  function bindHistoryControls() {
    ["study", "sermon", "devotional", "chat", "questions"].forEach((type) => {
      const { search, sort, clear } = historyDomRefs(type);
      if (!search || !sort || !clear) {
        return;
      }

      search.addEventListener("input", () => renderHistory(type));
      sort.addEventListener("change", () => renderHistory(type));
      clear.addEventListener("click", () => {
        state.histories[type] = [];
        saveHistory(STORAGE_KEYS[type], []);
        renderHistory(type);
        renderSummary();
      });
    });
  }

  async function loadImportSourcesAndMeta() {
    await loadUiTranslations(getValue(refs.langSelect, "pt") || "pt");
    applyUiTranslations();
    await loadLanguages();
    await loadUiTranslations(getValue(refs.langSelect, "pt") || "pt");
    applyUiTranslations();
    await loadOllamaModels();
    await loadVersions();
    await loadBooks();
    await loadChapter();
    await loadImportSources();
  }

  async function refreshEverything() {
    setStatus("Atualizando dados...", false);
    try {
      await loadUiTranslations(getValue(refs.langSelect, "pt") || "pt");
      applyUiTranslations();
      await loadOllamaModels();
      await loadVersions();
      await loadBooks();
      await loadChapter();
      await loadImportSources();
      setStatus("API online em http://localhost:8000", true);
      state.online = true;
    } catch (error) {
      setStatus(`Erro: ${error.message}`, false);
    }
  }

  async function bootstrap() {
    try {
      for (let attempt = 0; attempt < 90; attempt += 1) {
        try {
          await apiGet("/health");
          state.online = true;
          break;
        } catch (_) {
          await new Promise((resolve) => setTimeout(resolve, 1200));
        }
      }

      if (!state.online) {
        setStatus("API nao respondeu. Verifique o backend.", false);
        return;
      }

      setStatus("API online em http://localhost:8000", true);
      await loadImportSourcesAndMeta();
      renderAllHistories();
      bindHistoryControls();
      bindEvents();
      updateBadges();
      updateDirection();
      setActiveTab("reading");
    } catch (error) {
      setStatus(`Erro ao iniciar: ${error.message}`, false);
    }
  }

  function bindEvents() {
    document.querySelectorAll(".tab").forEach((button) => {
      button.addEventListener("click", () => setActiveTab(button.dataset.tab));
    });

    refs.refreshButton.addEventListener("click", refreshEverything);
    if (refs.settingsToggle) {
      refs.settingsToggle.addEventListener("click", toggleSettingsPanel);
    }
    if (refs.modelRefresh) {
      refs.modelRefresh.addEventListener("click", loadOllamaModels);
    }
    if (refs.modelSelect) {
      refs.modelSelect.addEventListener("change", () => {
        const selected = getValue(refs.modelSelect);
        if (selected) {
          refs.modelSelect.value = selected;
        }
      });
    }
    refs.importRefresh.addEventListener("click", loadImportSources);
    refs.langSelect.addEventListener("change", async () => {
      try {
        await loadUiTranslations(getValue(refs.langSelect, "pt") || "pt");
        applyUiTranslations();
        await loadVersions();
        await loadBooks();
        await loadChapter();
        await loadImportSources();
        renderAllHistories();
        updateBadges();
      } catch (error) {
        refs.chapterText.textContent = `Erro: ${error.message}`;
      } finally {
        updateDirection();
      }
    });
    refs.versionSelect.addEventListener("change", async () => {
      try {
        await loadBooks();
        await loadChapter();
        updateBadges();
      } catch (error) {
        refs.chapterText.textContent = `Erro: ${error.message}`;
      }
    });
    if (refs.readingBookSelect) {
      refs.readingBookSelect.addEventListener("change", async () => {
        state.selectedBook = getValue(refs.readingBookSelect) || state.selectedBook;
        updateScopeControls();
        updateBadges();
        try {
          await loadChapter();
        } catch (error) {
          refs.chapterText.textContent = `Erro: ${error.message}`;
        }
      });
    }
    [refs.sermonScope, refs.devScope, refs.chatScope, refs.questionsScope].forEach((scopeRef) => {
      if (scopeRef) {
        scopeRef.addEventListener("change", updateScopeControls);
      }
    });
    refs.loadChapterButton.addEventListener("click", loadChapter);
    refs.chapterInput.addEventListener("change", loadChapter);
    refs.verseInput.addEventListener("change", loadChapter);
    refs.studyButton.addEventListener("click", handleStudyGenerate);
    refs.sermonButton.addEventListener("click", handleSermonGenerate);
    refs.devButton.addEventListener("click", handleDevotionalGenerate);
    refs.chatButton.addEventListener("click", handleChatGenerate);
    refs.questionsButton.addEventListener("click", handleQuestionsGenerate);
    refs.studyCopyButton.addEventListener("click", () => copyText(refs.studyOutput.textContent || ""));
    refs.sermonCopyButton.addEventListener("click", () => copyText(refs.sermonOutput.textContent || ""));
    refs.devCopyButton.addEventListener("click", () => copyText(refs.devOutput.textContent || ""));
    refs.chatCopyButton.addEventListener("click", () => copyText(refs.chatOutput.textContent || ""));
    refs.questionsCopyButton.addEventListener("click", () => copyText(refs.questionsOutput.textContent || ""));

    if (refs.supportPaypal) {
      refs.supportPaypal.addEventListener("click", () => openExternal(SUPPORT_PAYPAL_URL));
    }
    if (refs.supportPickpay) {
      refs.supportPickpay.addEventListener("click", async () => {
        if (!SUPPORT_PICKPAY_KEY) {
          setStatus("Chave PicPay nao configurada.", false);
          return;
        }
        await copyText(SUPPORT_PICKPAY_KEY);
        setStatus("Chave PicPay copiada.", true);
      });
    }
  }

  bootstrap();
})();

