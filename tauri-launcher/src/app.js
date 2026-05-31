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
  const PREF_KEYS = {
    model: "preferred_model",
    language: "preferred_language",
    version: "preferred_version",
    savePrefs: "save_preferences_enabled",
  };

  const STRIP_PREFIX_RE = /^[^A-Za-zÀ-ÿ0-9]+/;
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
    pt: {
      "Analitico-Essencia": { label: "Analítico-Essência", subtitle: "O Investigador" },
      "Expositivo-Teologico": { label: "Expositivo-Teológico", subtitle: "O Professor" },
      "Narrativo-Imersivo": { label: "Narrativo-Imersivo", subtitle: "O Storyteller" },
      "Devocional-Pratico": { label: "Devocional-Prático", subtitle: "O Mentor" },
      "Cristocentrico-Tipologico": { label: "Cristocêntrico-Tipológico", subtitle: "O Revelador" },
      "Profetico-Confrontador": { label: "Profético-Confrontador", subtitle: "O Atalaia" },
      "Apologetico-Filosofico": { label: "Apologético-Filosófico", subtitle: "O Defensor" },
    },
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
    selectedBooks: [],
    chapterData: null,
    readProgress: {},
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
          <div style="display:flex;align-items:flex-start;justify-content:space-between">
            <div class="brand">
              <div class="brand-badge">B</div>
              <div>
                <div id="brandTitle" class="brand-title">Biblia de Estudos com IA</div>
              </div>
            </div>
          </div>

        <div class="status-row">
          <div id="apiStatus" class="status warn">Conectando…</div>
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
            <button id="modelHelpBtn" class="help-btn" type="button">?</button>
            <div id="modelHelpContent" class="help-content" style="display:none;margin-top:6px;padding:8px;background:var(--bg2);border-radius:6px;font-size:13px;line-height:1.5"></div>
            <div id="modelInfo" class="helper-text">Models loaded: 0</div>
            <label class="toggle-row save-prefs-row">
              <input type="checkbox" id="savePrefsCheck" />
              <span class="toggle-slider"></span>
              <span id="savePrefsLabel" class="toggle-label">Salvar preferencias ao sair</span>
            </label>
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

      <button id="sidebarToggle" class="sidebar-toggle">◀</button>

      <main class="main">
        <header class="topbar">
          <div>
            <div id="pageTitle" class="page-title">Painel de Estudo Biblico</div>
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
          <button class="tab" data-tab="about">Sobre</button>
          <button class="tab" data-tab="import" style="display:none">Importar</button>
        </nav>

        <section id="reading" class="tab-panel active">
          <div class="grid-two">
            <section class="card">
              <div class="card-title">Texto Biblico</div>
              <div class="field-grid four-up field-compact">
                <div>
                  <label class="field-label" for="readingBookSelect">Livro</label>
                  <select id="readingBookSelect" class="field"></select>
                </div>
                <div>
                  <label class="field-label" for="readingChapterSelect">Cap.</label>
                  <input id="readingChapterSelect" class="field" type="text" list="readingChapterList" placeholder="1" />
                  <datalist id="readingChapterList"></datalist>
                </div>
                <div>
                  <label class="field-label" for="readingVerseRange">Vers.</label>
                  <input id="readingVerseRange" class="field" type="text" placeholder="e.g. 1-15,19" />
                </div>
                <div class="btn-wrap">
                  <label class="field-label">&nbsp;</label>
                  <button id="loadReadingChapterBtn" class="primary-button">Carregar</button>
                </div>
              </div>
              <div class="filters-row" style="margin-top:8px;align-items:center;gap:8px;flex-wrap:wrap">
                <span class="color-palette" id="colorPalette"></span>
                <button id="markChapterReadBtn" class="ghost-button" style="font-size:12px">✓ Marcar</button>
                <button id="unmarkChapterReadBtn" class="ghost-button" style="font-size:12px">✗ Desmarcar</button>
                <label class="toggle-row">
                  <input id="hideReadVerses" type="checkbox" /> <span id="hideReadLabel">Ocultar lidos</span>
                </label>
                <span id="readingProgress" class="helper-text" style="margin:0;font-size:12px"></span>
              </div>
              <div id="chapterText" class="scroll-box muted-box">Selecione um livro e carregue o capitulo.</div>
            </section>

            <section class="card">
              <div class="card-title">Leitura e Exegese</div>
              <label class="field-label" for="studyCompare" id="studyCompareLabel">Modo</label>
              <label class="check-row"><input id="studyCompare" type="checkbox" /> <span id="studyCompareText">Comparar com outras versoes</span></label>

              <div id="studyReference" class="helper-text" style="margin-bottom:4px;font-size:13px;color:var(--accent);font-weight:600">Baseado em: —</div>
              <label class="field-label" for="studyRequest">Pedido</label>
              <textarea id="studyRequest" class="textarea" rows="5">Explain the historical and theological context of the text, highlight keywords and the pastoral application of the text.</textarea>

              <div class="button-row">
                <button id="studyButton" class="primary-button">Gerar Exegese</button>
                <button id="studyCopyButton" class="ghost-button">Copiar resultado</button>
              </div>

              <div class="output-title">Resposta</div>
              <div id="studyOutput" class="scroll-box muted-box">Aguardando solicitacao...</div>
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

              <div class="field-grid two-up field-compact">
                <div>
                  <label class="field-label" for="sermonBook">Livro</label>
                  <select id="sermonBook" class="field"></select>
                </div>
                <div>
                  <label class="field-label" for="sermonChapter">Cap.</label>
                  <input id="sermonChapter" class="field" type="text" list="sermonChapterList" placeholder="1" />
                  <datalist id="sermonChapterList"></datalist>
                </div>
              </div>

              <div class="field-grid two-up">
                <div>
                  <label class="field-label" for="sermonTheme">Tema</label>
                  <input id="sermonTheme" class="field" type="text" placeholder="Faith, hope, holiness..." />
                </div>
                <div>
                  <label class="field-label" for="sermonAudience">Publico</label>
                  <input id="sermonAudience" class="field" type="text" placeholder="Youth, local church, leaders..." />
                </div>
              </div>

              <label class="field-label" for="sermonNotes">Notas extras</label>
              <textarea id="sermonNotes" class="textarea" rows="4" placeholder="Preacher context, focus, goal..."></textarea>

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
                  <input id="devFeeling" class="field" type="text" value="Gratitude" />
                </div>
              </div>

              <div class="field-grid two-up field-compact">
                <div>
                  <label class="field-label" for="devBook">Livro</label>
                  <select id="devBook" class="field"></select>
                </div>
                <div>
                  <label class="field-label" for="devChapter">Cap.</label>
                  <input id="devChapter" class="field" type="text" list="devChapterList" placeholder="1" />
                  <datalist id="devChapterList"></datalist>
                </div>
              </div>

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
              <div class="field-grid three-up field-compact">
                <div>
                  <label class="field-label" for="chatScope">Escopo</label>
                  <select id="chatScope" class="field">
                    <option value="specific">Versículo específico</option>
                    <option value="selected">Livros selecionados</option>
                    <option value="whole">Toda a Biblia</option>
                  </select>
                </div>
                <div>
                  <label class="field-label" for="chatBook">Livro</label>
                  <select id="chatBook" class="field"></select>
                </div>
                <div>
                  <label class="field-label" for="chatChapter">Cap.</label>
                  <input id="chatChapter" class="field" type="text" list="chatChapterList" placeholder="1" />
                  <datalist id="chatChapterList"></datalist>
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
                    <option value="whole">Bíblia toda</option>
                  </select>
                </div>
                <div>
                  <label class="field-label" for="questionsCount">Quantidade</label>
                  <input id="questionsCount" class="field" type="number" min="1" max="50" value="10" />
                </div>
              </div>

              <div class="field-grid two-up field-compact">
                <div>
                  <label class="field-label" for="questionsBook">Livro</label>
                  <select id="questionsBook" class="field"></select>
                </div>
                <div>
                  <label class="field-label" for="questionsChapter">Cap.</label>
                  <input id="questionsChapter" class="field" type="text" list="questionsChapterList" placeholder="1" />
                  <datalist id="questionsChapterList"></datalist>
                </div>
              </div>

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

        <section id="import" class="tab-panel" style="display:none">
          <div class="grid-two">
            <section class="card">
              <div class="card-title">Fontes Locais</div>
              <div id="importHelper" class="helper-text">O backend carrega direto de Dados_Json, entao esta aba mostra os arquivos disponiveis e permite recarregar o catalogo.</div>
              <div class="button-row">
                <button id="importRefresh" class="primary-button">Recarregar catalogo</button>
              </div>
              <div id="importSources" class="scroll-box muted-box"></div>
            </section>

            <section class="card">
              <div id="importHelpTitle" class="card-title">Ajuda de Importacao</div>
              <div id="importHelpContent" class="scroll-box muted-box">
                <p id="importHelp1">1. Coloque os arquivos JSON em Dados_Json/idioma/.</p>
                <p id="importHelp2">2. Use um nome de versao consistente, por exemplo NVI.json ou AA.json.</p>
                <p id="importHelp3">3. Clique em Recarregar catalogo para atualizar a lista local.</p>
                <p id="importHelp4">4. O backend usa estes arquivos direto, entao nao existe mais uma importacao separada no fluxo nativo.</p>
              </div>
            </section>
          </div>
        </section>

        <section id="about" class="tab-panel">
          <div class="about-hero">
            <div class="about-icon">
              <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="var(--accent)" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
            </div>
            <h1 class="about-title" data-i18n="about.title">Bible Study Panel</h1>
            <p class="about-subtitle" data-i18n="about.subtitle">Exegese, Sermoes, Devocional e Chat Teologico com IA local</p>
          </div>

          <div class="about-grid">
            <div class="about-card">
              <h2 data-i18n="about.dedication_title">Dedicatória</h2>
              <p data-i18n="about.dedication_text">Este aplicativo foi feito por alguém que não entende muito de programação, mas deu o melhor de si. Sou um pequeno programador e suporte de TI que não pode viajar para pregar o evangelho, mas espero que através desta ferramenta seja possível ajudar muitos irmãos a meditar e entender a Palavra de Deus.</p>
              <p data-i18n="about.church">Membro da Nova Igreja Batista, Cidade de Manaus, Amazonas, onde aprendi que a Palavra de Deus é muito importante para cada um de nós.</p>
            </div>

            <div class="about-card about-card-highlight">
              <h2 data-i18n="about.encouragement_title">Encorajamento</h2>
              <blockquote>
                <p data-i18n="about.verse_phil">"Posso todas as coisas naquele que me fortalece."</p>
                <cite data-i18n="about.verse_ref">— Filipenses 4:13</cite>
              </blockquote>
              <blockquote>
                <p data-i18n="about.verse_john">"Eu vim para que tenham vida, e a tenham com abundância."</p>
                <cite data-i18n="about.verse_john_ref">— João 10:10</cite>
              </blockquote>
              <p data-i18n="about.encouragement_body">Lembre-se: esta vida é passageira. O nosso alvo é Cristo, e Ele é o único que tem vida — vida com abundância. Que esta ferramenta seja uma luz para aqueles que buscam a verdade.</p>
              <p data-i18n="about.purpose">Para os que não podem andar com uma Bíblia física nas mãos, para os que não têm liberdade de expressão, saibam que a Palavra de Deus nunca volta vazia.</p>
            </div>

            <div class="about-card">
              <h2 data-i18n="about.translation_title">Traduções</h2>
              <p data-i18n="about.translation_note">Se em algum lugar a tradução não ficou boa, pedimos desculpas. Estamos sempre buscando melhorar. Caso encontre algum bug ou texto mal traduzido, por favor, informe no GitHub.</p>
            </div>

            <div class="about-card">
              <h2 data-i18n="about.links_title">Links</h2>
              <p><a href="https://github.com/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas/issues" target="_blank" rel="noopener" data-i18n="about.github_link">GitHub - Reportar bugs / Sugerir melhorias</a></p>
              <p><a href="https://github.com/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas" target="_blank" rel="noopener" data-i18n="about.download_link">Distribuicao gratuita oficial — Download</a></p>
            </div>

            <div class="about-card about-card-footer">
              <p data-i18n="about.thanks">Que Deus abençoe sua leitura e meditation na Palavra. Soli Deo Gloria.</p>
            </div>
          </div>
        </section>
      </main>
    </div>
    <div id="splashOverlay" class="splash-overlay">
      <div class="splash-content">
        <div class="splash-logo-ring"></div>
        <div class="splash-logo">B</div>
        <div class="splash-title">Biblical Study AI</div>
        <div class="splash-status" id="splashStatus">Conectando...</div>
        <div class="splash-bar-track"><div class="splash-bar-fill" id="splashBar"></div></div>
        <div class="splash-verse" id="splashVerse"></div>
      </div>
    </div>
  `;

  document.head.insertAdjacentHTML(
    "beforeend",
    `
            <style>
        /* 1  Paleta Premium Noite Sagrada  */
        :root {
          --bg: #0a0e1a;
          --bg2: #131a2e;
          --panel: rgba(14, 20, 38, 0.88);
          --card: rgba(17, 24, 39, 0.82);
          --line: rgba(148, 163, 184, 0.12);
          --fg: #f8fafc;
          --muted: #cbd5e1;
          --accent: #67d5ff;
          --accent2: #a78bfa;
          --ok: #22c55e;
          --warn: #f59e0b;
          --danger: #fb7185;
          --persona-1: #67d5ff;
          --persona-2: #a78bfa;
          --persona-3: #f472b6;
          --persona-4: #34d399;
          --persona-5: #fbbf24;
          --persona-6: #fb923c;
          --persona-7: #818cf8;
          --shadow-card: 0 4px 16px rgba(0,0,0,0.3);
          --shadow-elevated: 0 8px 28px rgba(0,0,0,0.45);
        }
        * { box-sizing: border-box; }
        html, body {
          margin: 0; min-height: 100%;
          background: radial-gradient(circle at top left, #0d1324, var(--bg));
          color: var(--fg);
          font-family: "Inter", "Segoe UI", "Noto Sans", sans-serif;
          font-size: 14px;
          line-height: 1.6;
        }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(148,163,184,0.2); border-radius: 99px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(148,163,184,0.35); }
        * { scrollbar-width: thin; scrollbar-color: rgba(148,163,184,0.2) transparent; }
        body::before {
          content: "";
          position: fixed;
          inset: 0;
          pointer-events: none;
          background: linear-gradient(135deg, rgba(103, 213, 255, 0.06), transparent 45%), linear-gradient(315deg, rgba(167, 139, 250, 0.06), transparent 42%), radial-gradient(ellipse at 70% 20%, rgba(103, 213, 255, 0.03), transparent 60%);
        }
        .shell { position: relative; z-index: 1; display: grid; grid-template-columns: 320px 1fr; min-height: 100vh; transition: grid-template-columns 0.35s ease; }
        .sidebar {
          background: rgba(10, 14, 26, 0.78);
          backdrop-filter: blur(14px);
          -webkit-backdrop-filter: blur(14px);
          border-right: 1px solid rgba(255,255,255,0.06);
          padding: 20px;
          display: flex; flex-direction: column; gap: 16px;
          transition: width 0.35s ease, padding 0.35s ease, visibility 0.35s ease, border 0.35s ease;
        }
        .brand { display: flex; gap: 12px; align-items: center; }
        .brand-badge {
          width: 44px; height: 44px; border-radius: 14px;
          display: grid; place-items: center; font-weight: 800;
          color: #00111d;
          background: linear-gradient(135deg, var(--accent), #d8fbff);
          box-shadow: 0 8px 24px rgba(103, 213, 255, 0.35);
        }
        .brand-title {
          font-size: 18px; font-weight: 800;
          letter-spacing: 0.05em;
          background: linear-gradient(135deg, var(--fg), var(--accent));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }
        .brand-subtitle { color: var(--muted); font-size: 12px; }
        .status-row, .button-row, .filters-row, .topbar-meta, .field-grid, .summary-grid { display: flex; gap: 10px; flex-wrap: wrap; }
        .status {
          padding: 9px 12px; border-radius: 999px; border: 1px solid var(--line); font-size: 13px;
          display: flex; align-items: center; gap: 6px;
        }
        .status.ok {
          color: #d1fae5; border-color: rgba(34, 197, 94, 0.4); background: rgba(34, 197, 94, 0.1);
        }
        .status.ok::before {
          content: ""; width: 8px; height: 8px; border-radius: 50%;
          background: var(--ok);
          box-shadow: 0 0 8px rgba(34,197,94,0.6);
          animation: pulse-dot 2s ease-in-out infinite;
        }
        .status.warn {
          color: #fde68a; border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.1);
        }
        .status.warn::before {
          content: ""; width: 8px; height: 8px; border-radius: 50%;
          background: var(--warn);
          box-shadow: 0 0 8px rgba(245,158,11,0.5);
        }
        @keyframes pulse-dot {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.5; transform: scale(0.85); }
        }
        .ghost-button, .primary-button, .tab {
          border: 0; border-radius: 12px; cursor: pointer;
          transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease, background 0.2s ease;
        }
        .ghost-button:hover, .primary-button:hover, .tab:hover { transform: translateY(-2px); }
        .ghost-button:hover { box-shadow: 0 4px 14px rgba(0,0,0,0.25); }
        .ghost-button {
          background: rgba(148, 163, 184, 0.06); color: var(--fg);
          padding: 10px 14px; border: 1px solid var(--line);
          backdrop-filter: blur(4px);
        }
        .help-btn {
          background: rgba(148, 163, 184, 0.1); color: var(--fg);
          border: 1px solid var(--line); border-radius: 50%;
          width: 22px; height: 22px; font-size: 12px;
          cursor: pointer; display: inline-flex; align-items: center; justify-content: center;
          margin-left: 4px; vertical-align: middle;
          transition: background 0.2s, color 0.2s, transform 0.2s;
        }
        .help-btn:hover { background: var(--accent); color: #03111e; transform: scale(1.15); }
        .primary-button {
          background: linear-gradient(135deg, var(--accent), var(--accent2));
          color: #03111e; font-weight: 700; padding: 11px 16px;
          box-shadow: inset 0 1px 0 rgba(255,255,255,0.2), 0 4px 14px rgba(103,213,255,0.2);
          transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease;
        }
        .primary-button:hover {
          box-shadow: inset 0 1px 0 rgba(255,255,255,0.25), 0 6px 20px rgba(103,213,255,0.3);
          transform: translateY(-2px);
        }
        .primary-button:active { transform: translateY(0); }
        .panel-group {
          background: var(--panel);
          backdrop-filter: blur(8px);
          border: 1px solid rgba(255,255,255,0.06);
          border-radius: 18px; padding: 14px;
          display: flex; flex-direction: column; gap: 8px;
        }
        .panel-header { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
        .panel-toggle { min-width: 36px; padding: 6px 10px; }
        .panel-body { display: flex; flex-direction: column; gap: 8px; }
        .panel-group.collapsed .panel-body { display: none; }
        .panel-group.grow { flex: 1; min-height: 0; }
        .panel-title { color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .12em; font-weight: 600; }
        .field, .textarea {
          width: 100%;
          background: rgba(6, 13, 24, 0.85);
          color: var(--fg);
          border: 1px solid rgba(148, 163, 184, 0.15);
          border-radius: 12px; padding: 10px 12px; font-size: 14px;
          transition: border-color 0.2s, box-shadow 0.2s;
        }
        .field:focus, .textarea:focus {
          outline: none;
          border-color: var(--accent);
          box-shadow: 0 0 0 3px rgba(103, 213, 255, 0.12);
        }
        .textarea { resize: vertical; min-height: 110px; }
        .field.multi { min-height: 220px; }
        .field-label {
          color: var(--muted); font-size: 12px; margin-top: 4px; margin-bottom: 6px; display: block;
          font-weight: 500; letter-spacing: 0.03em;
        }
        .helper-text { color: var(--muted); font-size: 12px; line-height: 1.4; }
        .book-list { display: grid; gap: 8px; overflow: auto; padding-right: 4px; }
        .book-item {
          padding: 10px 12px; border-radius: 12px;
          border: 1px solid rgba(148,163,184,0.1);
          background: rgba(255,255,255,0.02);
          cursor: pointer; color: #e2e8f0;
          transition: background 0.2s, border-color 0.2s, transform 0.15s;
        }
        .book-item::before { content: "\U0001F4D6"; margin-right: 8px; font-size: 13px; }
        .book-item:hover {
          background: rgba(148,163,184,0.06);
          border-color: rgba(148,163,184,0.2);
          transform: translateX(2px);
        }
        .book-item.active {
          background: linear-gradient(135deg, rgba(103, 213, 255, 0.15), rgba(167, 139, 250, 0.15));
          border-color: rgba(103, 213, 255, 0.3);
        }
        .main { padding: 20px; display: flex; flex-direction: column; gap: 16px; min-width: 0; }
        .topbar {
          display: flex; justify-content: space-between; gap: 16px; align-items: flex-start;
          padding: 18px 20px; border-radius: 20px;
          background: rgba(17, 24, 39, 0.72);
          backdrop-filter: blur(12px);
          border: 1px solid rgba(255,255,255,0.06);
          box-shadow: 0 8px 24px rgba(0,0,0,0.3);
          position: relative;
        }
        .topbar::before {
          content: "";
          position: absolute; top: 0; left: 20px; right: 20px; height: 1px;
          background: linear-gradient(90deg, transparent, rgba(103, 213, 255, 0.4), rgba(167, 139, 250, 0.4), transparent);
          pointer-events: none;
        }
        .page-title { font-size: 22px; font-weight: 800; letter-spacing: -0.02em; }
        .page-subtitle { color: var(--muted); font-size: 13px; margin-top: 4px; }
        .badge { padding: 9px 12px; border-radius: 999px; background: rgba(255,255,255,0.04); border: 1px solid var(--line); color: var(--muted); font-size: 12px; }
        .tabs { display: flex; gap: 8px; flex-wrap: wrap; }
        .tab {
          padding: 11px 14px; color: var(--fg); font-size: 13px;
          background: rgba(148, 163, 184, 0.06);
          border: 1px solid rgba(148,163,184,0.1);
          backdrop-filter: blur(4px);
        }
        .tab:hover {
          background: rgba(148, 163, 184, 0.12);
          border-color: rgba(148,163,184,0.2);
        }
        .tab.active {
          background: linear-gradient(135deg, var(--accent), var(--accent2));
          color: #05131f; font-weight: 700; border-color: transparent;
          box-shadow: 0 4px 16px rgba(103,213,255,0.2);
        }
        .tab-panel { display: none; gap: 16px; flex-direction: column; }
        .tab-panel.active { display: flex; }
        .grid-two { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); gap: 16px; }
        .card {
          background: rgba(17, 24, 39, 0.78);
          backdrop-filter: blur(12px);
          border: 1px solid rgba(255,255,255,0.06);
          border-radius: 18px; padding: 16px; min-width: 0;
          box-shadow: var(--shadow-card);
          transition: box-shadow 0.3s ease, transform 0.2s ease;
        }
        .card:hover { box-shadow: var(--shadow-elevated); }
        .card-title { font-size: 16px; font-weight: 700; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.1em; }
        .scroll-box {
          max-height: 520px; overflow: auto; white-space: pre-wrap; line-height: 1.8;
          padding: 16px; border-radius: 14px;
          border: 1px solid rgba(255,255,255,0.06);
          font-size: 15px;
          background: rgba(5, 13, 24, 0.6);
          backdrop-filter: blur(4px);
        }
        .muted-box { background: rgba(5, 13, 24, 0.6); color: #e2e8f0; }
        .output-title { margin-top: 10px; margin-bottom: 8px; color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .12em; font-weight: 600; }
        .check-row { display: inline-flex; gap: 8px; align-items: center; font-size: 14px; color: #e2e8f0; margin-bottom: 10px; }
        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
        .summary-card {
          border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 14px;
          background: rgba(255,255,255,0.02);
          backdrop-filter: blur(4px);
        }
        .summary-card:hover { background: rgba(255,255,255,0.04); }
        .summary-card strong { display: block; font-size: 20px; margin-bottom: 6px; }
        .record-list { display: grid; gap: 12px; }
        .record {
          border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 14px;
          background: rgba(255,255,255,0.02);
          backdrop-filter: blur(4px);
        }
        .record:hover { background: rgba(255,255,255,0.04); border-color: rgba(255,255,255,0.1); }
        .record-head { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; align-items: center; }
        .record-title { font-weight: 700; font-size: 15px; }
        .record-meta { color: var(--muted); font-size: 12px; margin-top: 4px; }
        .record-body { margin-top: 10px; white-space: pre-wrap; line-height: 1.7; color: #e2e8f0; }
        .record-actions { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
        .record-actions button { padding: 9px 12px; }
        .empty-state { color: var(--muted); border: 1px dashed rgba(148,163,184,0.2); border-radius: 14px; padding: 14px; }
        .field-grid.three-up { display: grid; grid-template-columns: repeat(3, 1fr); }
        .field-grid.four-up { display: grid; grid-template-columns: repeat(4, 1fr); }
        .field-compact input, .field-compact select { max-width: 130px; }
        .field-compact input { min-width: 70px; width: 100%; }
        .color-palette { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
        .color-btn {
          width: 22px; height: 22px; border-radius: 50%; border: 2px solid transparent;
          cursor: pointer; flex-shrink: 0; padding: 0;
          transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), border-color 0.2s;
        }
        .color-btn:hover { transform: scale(1.25); }
        .color-btn.active { border-color: var(--accent); box-shadow: 0 0 10px var(--accent); }
        .verse-row { display: flex; align-items: flex-start; gap: 8px; padding: 6px 10px; border-radius: 10px; margin: 3px 0; transition: background 0.2s; cursor: pointer; }
        .verse-row:hover { background: rgba(148, 163, 184, 0.08) !important; }
        .verse-row .verse-num { font-weight: 700; flex-shrink: 0; min-width: 2em; color: var(--accent); font-size: 0.9em; transition: color .2s; }
        .verse-row:hover .verse-num { color: #fff; }
        .verse-row .verse-text { flex: 1; line-height: 1.6; }
        .verse-row input[type=checkbox] { margin-top: 4px; flex-shrink: 0; accent-color: var(--accent); }
        .sidebar-toggle {
          position: fixed; top: 50%; left: 312px; z-index: 999;
          transform: translateY(-50%);
          background: rgba(10,14,26,0.9);
          backdrop-filter: blur(8px);
          border: 1px solid rgba(255,255,255,0.08);
          color: var(--muted); font-size: 16px; cursor: pointer;
          padding: 6px 10px; border-radius: 10px; line-height: 1;
          transition: transform 0.2s, background 0.2s, left 0.35s ease;
        }
        .sidebar-toggle:hover { background: rgba(148,163,184,0.2); color: var(--fg); transform: translateY(-50%) scale(1.1); }
        .shell.collapsed .sidebar-toggle { left: 10px; }
        .shell.collapsed { grid-template-columns: 0 1fr; }
        .shell.collapsed .sidebar { width: 0; min-width: 0; padding: 0; overflow: hidden; visibility: hidden; border: none; }
        .field-grid { gap: 6px; }
        #readingChapterSelect { max-width: 85px; }
        #readingVerseRange { max-width: 120px; }
        .field-grid .btn-wrap { display: flex; flex-direction: column; }
        .field-grid .btn-wrap .primary-button { width: 100%; white-space: nowrap; }
        #chapterText { margin-top: 10px; }
        .toggle-row { display: inline-flex; align-items: center; gap: 6px; cursor: pointer; font-size: 12px; color: var(--muted); user-select: none; }
        .toggle-row:hover { color: var(--fg); }
        .toggle-row input { appearance: none; -webkit-appearance: none; width: 34px; height: 20px; background: rgba(148,163,184,0.12); border: 1px solid rgba(148,163,184,0.15); border-radius: 10px; cursor: pointer; position: relative; transition: all .25s; flex-shrink: 0; }
        .toggle-row input::after { content: ""; position: absolute; top: 2px; left: 2px; width: 14px; height: 14px; border-radius: 50%; background: var(--muted); transition: all .25s cubic-bezier(0.34, 1.56, 0.64, 1); }
        .toggle-row input:checked { background: var(--accent); border-color: var(--accent); }
        .toggle-row input:checked::after { left: 16px; background: #03111e; }
        .card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          cursor: pointer;
          user-select: none;
          padding: 4px 0;
          margin-bottom: 12px;
          font-size: 16px;
          font-weight: 700;
          color: var(--fg);
          border-bottom: 1px solid rgba(255,255,255,0.06);
          letter-spacing: 0.05em;
        }
        .card-header .card-title {
          margin-bottom: 0;
          font-size: inherit;
          text-transform: none;
          letter-spacing: 0;
        }
        .card-header:hover .card-title { color: var(--accent); }
        .card-header::after {
          content: "\u25BC";
          font-size: 14px;
          color: var(--muted);
          transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
          flex-shrink: 0;
          margin-left: 12px;
        }
        .card-header:hover::after { color: var(--accent); }
        .card-header.collapsed::after { transform: rotate(-180deg); }
        .card-content {
          overflow: hidden;
          max-height: 2000px;
          transition: max-height 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .card-content.collapsed { max-height: 0; padding: 0; margin: 0; }
        .book-multi-select {
          display: none;
          max-height: 240px;
          overflow: auto;
          border: 1px solid rgba(255,255,255,0.06);
          border-radius: 12px;
          padding: 8px;
          background: rgba(5, 13, 24, 0.7);
          margin-bottom: 10px;
          backdrop-filter: blur(4px);
        }
        .book-multi-select.visible { display: block; }
        .book-multi-select .book-item {
          padding: 7px 10px;
          border-radius: 8px;
          cursor: pointer;
          color: #e2e8f0;
          font-size: 13px;
        }
        .book-multi-select .book-item:hover { background: rgba(148,163,184,0.12); }
        .book-section-title {
          font-size: 12px;
          font-weight: 700;
          color: var(--accent);
          margin: 8px 0 4px;
          padding: 0 4px;
          text-transform: uppercase;
          letter-spacing: .08em;
        }
        .book-section-title:first-child { margin-top: 0; }
        .book-multi-select .book-item.selected {
          background: linear-gradient(135deg, rgba(103, 213, 255, 0.18), rgba(167, 139, 250, 0.18));
          color: var(--accent);
        }
        select.field:disabled, input.field:disabled, textarea.field:disabled, .field:disabled {
          opacity: 0.35;
          cursor: not-allowed;
        }
        .about-hero { text-align: center; padding: 32px 16px 24px; }
        .about-icon { margin-bottom: 12px; opacity: 0.85; filter: drop-shadow(0 4px 12px rgba(103,213,255,0.2)); }
        .about-title {
          font-size: 28px; font-weight: 800; margin: 0 0 6px;
          background: linear-gradient(135deg, var(--accent), var(--accent2));
          -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
          letter-spacing: -0.02em;
        }
        .about-subtitle { color: var(--muted); font-size: 14px; margin: 0; }
        .about-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
        .about-card {
          background: rgba(17, 24, 39, 0.78);
          backdrop-filter: blur(12px);
          border: 1px solid rgba(255,255,255,0.06);
          border-radius: 18px; padding: 20px;
          box-shadow: var(--shadow-card);
        }
        .about-card:hover { box-shadow: var(--shadow-elevated); }
        .about-card h2 { font-size: 16px; font-weight: 700; margin: 0 0 12px; color: var(--accent); letter-spacing: 0.08em; text-transform: uppercase; }
        .about-card p { font-size: 14px; line-height: 1.7; color: #e2e8f0; margin: 0 0 10px; }
        .about-card p:last-child { margin-bottom: 0; }
        .about-card blockquote { margin: 12px 0; padding: 12px 16px; border-left: 3px solid var(--accent2); background: rgba(167,139,250,0.08); border-radius: 0 14px 14px 0; }
        .about-card blockquote p { font-style: italic; font-size: 15px; margin: 0 0 4px; color: #e2d9ff; }
        .about-card blockquote cite { font-size: 12px; color: var(--muted); font-style: normal; }
        .about-card-highlight { border-color: rgba(167,139,250,0.25); background: linear-gradient(135deg, rgba(17,24,39,0.78), rgba(167,139,250,0.06)); }
        .about-card-footer { grid-column: 1 / -1; text-align: center; border-color: rgba(103,213,255,0.18); }
        .about-card-footer p { font-size: 16px; color: var(--accent); font-weight: 600; }
        .about-card a { color: var(--accent2); text-decoration: none; }
        .about-card a:hover { text-decoration: underline; }
        @media (max-width: 1100px) {
          .shell { grid-template-columns: 1fr; }
          .sidebar { border-right: 0; border-bottom: 1px solid var(--line); }
          .grid-two { grid-template-columns: 1fr; }
        }
        @media (max-width: 800px) { .about-grid { grid-template-columns: 1fr; } }
        @media (max-width: 600px) {
          .field-grid.three-up { display: grid; grid-template-columns: 1fr; }
          .field-grid.four-up { display: grid; grid-template-columns: 1fr; }
        }
        .splash-overlay {
          position: fixed; inset: 0; z-index: 9999;
          background: radial-gradient(ellipse at center, #0f1729 0%, #070b15 100%);
          display: flex; align-items: center; justify-content: center;
          transition: opacity 0.8s ease, visibility 0.8s ease;
        }
        .splash-overlay.hidden { opacity: 0; visibility: hidden; pointer-events: none; }
        .splash-content {
          text-align: center; position: relative;
          animation: splash-fade-in 1s ease-out;
        }
        @keyframes splash-fade-in { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .splash-logo {
          width: 80px; height: 80px; margin: 0 auto 20px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border-radius: 24px; display: flex; align-items: center; justify-content: center;
          font-size: 36px; font-weight: 800; color: #fff; position: relative;
          box-shadow: 0 0 40px rgba(102, 126, 234, 0.3);
          animation: splash-logo-glow 2s ease-in-out infinite;
        }
        @keyframes splash-logo-glow { 0%, 100% { box-shadow: 0 0 40px rgba(102, 126, 234, 0.3); } 50% { box-shadow: 0 0 80px rgba(102, 126, 234, 0.6); } }
        .splash-logo-ring {
          position: absolute; width: 110px; height: 110px; top: 50%; left: 50%; margin: -55px 0 0 -55px;
          border: 2px solid transparent; border-top-color: #667eea; border-right-color: #764ba2;
          border-radius: 50%; animation: splash-spin 1.2s cubic-bezier(0.6, 0, 0.4, 1) infinite;
        }
        @keyframes splash-spin { to { transform: rotate(360deg); } }
        .splash-title {
          font-size: 22px; font-weight: 700; color: #f1f5f9; margin-bottom: 4px;
          letter-spacing: -0.3px;
        }
        .splash-status {
          font-size: 14px; color: #94a3b8; margin: 12px 0;
          transition: opacity 0.3s ease;
        }
        .splash-bar-track {
          width: 220px; height: 3px; margin: 0 auto; border-radius: 4px;
          background: rgba(148, 163, 184, 0.15); overflow: hidden;
        }
        .splash-bar-fill {
          height: 100%; width: 0%; border-radius: 4px;
          background: linear-gradient(90deg, #667eea, #764ba2);
          transition: width 0.6s ease;
        }
        .splash-verse {
          margin-top: 20px; font-size: 12px; color: #64748b; font-style: italic;
          max-width: 300px; line-height: 1.5; min-height: 36px;
          transition: opacity 0.8s ease;
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
    modelHelpBtn: byId("modelHelpBtn"),
    modelHelpContent: byId("modelHelpContent"),
    savePrefsCheck: byId("savePrefsCheck"),
    savePrefsLabel: byId("savePrefsLabel"),
    savePrefsCheck: byId("savePrefsCheck"),
    savePrefsLabel: byId("savePrefsLabel"),
    readingBookSelect: byId("readingBookSelect"),
    readingChapterSelect: byId("readingChapterSelect"),
    readingChapterList: byId("readingChapterList"),
    readingVerseRange: byId("readingVerseRange"),
    colorPalette: byId("colorPalette"),
    markChapterReadBtn: byId("markChapterReadBtn"),
    unmarkChapterReadBtn: byId("unmarkChapterReadBtn"),
    hideReadVerses: byId("hideReadVerses"),
    readingProgress: byId("readingProgress"),
    sidebarToggle: byId("sidebarToggle"),
    loadReadingChapterBtn: byId("loadReadingChapterBtn"),
    versionBadge: byId("versionBadge"),
    bookBadge: byId("bookBadge"),
    pageSubtitle: byId("pageSubtitle"),
    chapterText: byId("chapterText"),
    studyReference: byId("studyReference"),
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
    sermonChapter: byId("sermonChapter"),
    sermonChapterList: byId("sermonChapterList"),
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
    devChapter: byId("devChapter"),
    devChapterList: byId("devChapterList"),
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
    chatChapter: byId("chatChapter"),
    chatChapterList: byId("chatChapterList"),
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
    questionsChapter: byId("questionsChapter"),
    questionsChapterList: byId("questionsChapterList"),
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
      if (!data.items || typeof data.items !== "object") {
        console.warn("loadUiTranslations: data.items is not an object", data);
      }
    } catch (err) {
      console.warn("loadUiTranslations: API error", err);
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
    ref.textContent = message;
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
    document.title = getTranslation("labels.app_title", "Bible Study with AI");

    const brandTitle = byId("brandTitle");
    if (brandTitle) brandTitle.textContent = getTranslation("labels.app_title", "Bible Study with AI");

    const pageTitle = byId("pageTitle");
    if (pageTitle) pageTitle.textContent = getTranslation("labels.page_title", "Bible Study Panel");

    const pageSubtitle = byId("pageSubtitle");
    if (pageSubtitle) pageSubtitle.textContent = getTranslation("labels.page_subtitle", "Exegesis, Sermons (7 Personas), Devotional and Theological Chat locally with Ollama.");

    const tabs = {
      reading: getTranslation("menu.reading", "Reading"),
      sermon: getTranslation("menu.sermon_gen", "Sermons"),
      devotional: getTranslation("menu.devotional", "Devotional"),
      chat: getTranslation("menu.chat", "Chat"),
      questions: getTranslation("menu.questions_gen", "Questions"),
      history: getTranslation("menu.history", "History"),
      about: getTranslation("menu.about", "About"),
      import: getTranslation("menu.import", "Import"),
    };
    Object.entries(tabs).forEach(([tabName, text]) => {
      const tab = document.querySelector(`.tab[data-tab="${tabName}"]`);
      if (tab) {
        tab.textContent = String(text || "").replace(/^[^\p{L}\p{N}]+/u, "").trim() || tab.textContent;
      }
    });

    setLabelText("langSelect", getTranslation("labels.language_selector", "Language"));
    setLabelText("versionSelect", getTranslation("labels.bible_version", "Version"));
    setLabelText("modelSelect", getTranslation("labels.ollama_model", "Ollama Model"));
    setLabelText("readingBookSelect", getTranslation("labels.book_selector", "Book"));
    setLabelText("sermonBook", getTranslation("labels.book_selector", "Book for context"));
    setLabelText("devBook", getTranslation("labels.book_selector", "Book for context"));
    setLabelText("chatBook", getTranslation("labels.book_selector", "Book for context"));
    setLabelText("questionsBook", getTranslation("labels.book_selector", "Book for context"));
    setLabelText("sermonScope", getTranslation("labels.scope", "Scope"));
    setLabelText("devScope", getTranslation("labels.scope", "Scope"));
    setLabelText("chatScope", getTranslation("labels.scope", "Scope"));
    setLabelText("questionsScope", getTranslation("labels.scope", "Scope"));
    setLabelText("studyRequest", getTranslation("labels.extra_notes", "Request"));
    setLabelText("chatQuestion", getTranslation("labels.your_question", "Question"));
    setLabelText("sermonStyle", getTranslation("labels.generation_mode", "Style"));
    setLabelText("questionsMode", getTranslation("labels.generation_mode", "Mode"));
    setLabelText("devFeeling", getTranslation("labels.theme_or_feeling", "Theme / feeling"));

    refs.refreshButton.textContent = getTranslation("buttons.clear_cache", "Reload").replace("🔄 ", "");
    refs.modelRefresh.textContent = getTranslation("buttons.import_versions", "Update models").replace("🔄 ", "");
    if (refs.loadReadingChapterBtn) refs.loadReadingChapterBtn.textContent = getTranslation("labels.reading_page", "Load Chapter");
    refs.studyButton.textContent = getTranslation("buttons.generate_explanation", "Generate Explanation").replace("✨ ", "");
    refs.sermonButton.textContent = getTranslation("buttons.generate_sermon", "Generate Sermon").replace("✨ ", "");
    refs.devButton.textContent = getTranslation("buttons.generate_devotional", "Generate Devotional").replace("✨ ", "");
    refs.chatButton.textContent = getTranslation("buttons.send_question", "Send Question").replace("✨ ", "");
    refs.questionsButton.textContent = getTranslation("menu.questions_gen", "Generate Questions").replace(/^[^\p{L}\p{N}]+/u, "").trim();
    refs.studyCopyButton.textContent = getTranslation("buttons.copy", "Copy").replace("📋 ", "");
    refs.sermonCopyButton.textContent = getTranslation("buttons.copy_sermon", "Copy result").replace("📋 ", "");
    refs.devCopyButton.textContent = getTranslation("buttons.copy_devotional", "Copy result").replace("📋 ", "");
    refs.chatCopyButton.textContent = getTranslation("buttons.copy_conversation", "Copy answer").replace("📋 ", "");
    refs.questionsCopyButton.textContent = getTranslation("buttons.copy", "Copy result").replace("📋 ", "");
    refs.importRefresh.textContent = getTranslation("buttons.reload_catalog", "Reload Catalog").replace("🔄 ", "");

    refs.modelInfo.textContent = `${getTranslation("labels.ollama_model", "Ollama Model")}: ${state.models.length}`;
    refs.studySearch.placeholder = getTranslation("labels.search_history", getTranslation("labels.search_placeholder", "Search history")).replace("🔍 ", "");
    refs.sermonSearch.placeholder = getTranslation("labels.search_sermons_placeholder", "Search sermons");
    refs.devSearch.placeholder = getTranslation("labels.search_devotionals_placeholder", "Search devotionals");
    refs.chatSearch.placeholder = getTranslation("labels.search_conversations_placeholder", "Search conversations");
    refs.questionsSearch.placeholder = getTranslation("labels.search_placeholder", "Search questions");
    refs.chatQuestion.placeholder = getTranslation("labels.your_question", "Type your Bible question...");

    refs.studyClear.textContent = getTranslation("buttons.clear_history", "Clear history").replace("🗑️ ", "");
    refs.sermonClear.textContent = getTranslation("buttons.clear_history", "Clear history").replace("🗑️ ", "");
    refs.devClear.textContent = getTranslation("buttons.clear_history", "Clear history").replace("🗑️ ", "");
    refs.chatClear.textContent = getTranslation("buttons.clear_history", "Clear history").replace("🗑️ ", "");
    refs.questionsClear.textContent = getTranslation("buttons.clear_history", "Clear history").replace("🗑️ ", "");

    const mostRecentLabel = getTranslation("labels.most_recent_plural", getTranslation("labels.most_recent", "Most recent"));
    const oldestLabel = getTranslation("labels.oldest_plural", getTranslation("labels.oldest", "Oldest"));
    [refs.studySort, refs.sermonSort, refs.devSort, refs.chatSort, refs.questionsSort].forEach((sortRef) => {
      setSelectOptionText(sortRef, "recent", mostRecentLabel);
      setSelectOptionText(sortRef, "oldest", oldestLabel);
    });

    const scopeSpecific = getTranslation("labels.specific_book", "Specific Book");
    const scopeSelected = getTranslation("labels.multiple_books", "Selected Books");
    const scopeWhole = getTranslation("labels.whole_bible", getTranslation("labels.entire_bible", "Whole Bible"));
    [refs.sermonScope, refs.devScope, refs.chatScope, refs.questionsScope].forEach((scopeRef) => {
      setSelectOptionText(scopeRef, "specific", scopeSpecific);
      setSelectOptionText(scopeRef, "selected", scopeSelected);
      setSelectOptionText(scopeRef, "whole", scopeWhole);
    });

    setSelectOptionText(refs.questionsMode, "with", getTranslation("labels.with_answers", "With answers"));
    setSelectOptionText(refs.questionsMode, "only", getTranslation("labels.only_questions", "Only questions"));

    setCardTitleByChild(refs.sermonScope, stripDecorators(getTranslation("headers.sermon_generator", "Sermon Generator")));
    setCardTitleByChild(refs.studyHistory, stripDecorators(getTranslation("headers.bible_studies_history", "Study History")));
    setCardTitleByChild(refs.sermonHistory, stripDecorators(getTranslation("headers.sermons_history", "Sermon History")));
    setCardTitleByChild(refs.devHistory, stripDecorators(getTranslation("headers.devotionals_history", "Devotional History")));
    setCardTitleByChild(refs.chatHistory, stripDecorators(getTranslation("headers.conversations_history", "Chat History")));
    setCardTitleByChild(refs.questionsHistory, stripDecorators(getTranslation("menu.questions_hist", "Questions History")));
    setCardTitleByChild(refs.historySummary, stripDecorators(getTranslation("menu.history", "Consolidated History")));
    setCardTitleByChild(refs.allHistory, stripDecorators(getTranslation("labels.search_history", "All Records")));

    // === Missing card title translations ===
    setCardTitleByChild(refs.readingBookSelect, stripDecorators(getTranslation("headers.bible_text", "Bible Text")));
    setCardTitleByChild(refs.studyCompare, stripDecorators(getTranslation("headers.reading_exegesis", "Reading and Exegesis")));
    setCardTitleByChild(refs.devFeeling, stripDecorators(getTranslation("headers.devotional_meditation", "Devotional & Meditation")));
    setCardTitleByChild(refs.chatQuestion, stripDecorators(getTranslation("headers.theological_chat", "Theological Chat")));
    setCardTitleByChild(refs.questionsCount, stripDecorators(getTranslation("headers.questions_generator", "Bible Questions Generator")));
    setCardTitleByChild(refs.importRefresh, stripDecorators(getTranslation("headers.local_sources", "Local Sources")));
    const importHelpTitle = byId("importHelpTitle");
    if (importHelpTitle) importHelpTitle.textContent = stripDecorators(getTranslation("headers.import_help", "Import Help"));

    // === Missing field label translations ===
    setLabelText("readingVerseRange", getTranslation("labels.verse_label", "V."));
    setLabelText("sermonChapter", getTranslation("labels.chapter_short", "Ch."));
    setLabelText("sermonTheme", getTranslation("labels.theme", "Theme"));
    setLabelText("sermonAudience", getTranslation("labels.audience", "Audience"));
    setLabelText("sermonNotes", getTranslation("labels.extra_notes", "Extra notes"));
    setLabelText("devChapter", getTranslation("labels.chapter_short", "Ch."));
    setLabelText("chatChapter", getTranslation("labels.chapter_short", "Ch."));
    setLabelText("questionsChapter", getTranslation("labels.chapter_short", "Ch."));
    setLabelText("questionsCount", getTranslation("labels.questions_count_label", "Quantity"));

    // === Missing placeholder translations ===
    const placeholderPairs = [
      { ref: refs.readingChapterSelect, key: "labels.chapter_number", fallback: "1" },
      { ref: refs.readingVerseRange, key: "labels.verse_example", fallback: "e.g. 1-15,19" },
      { ref: refs.sermonChapter, key: "labels.chapter_number", fallback: "1" },
      { ref: refs.sermonTheme, key: "labels.theme_placeholder", fallback: "Faith, hope, holiness..." },
      { ref: refs.sermonAudience, key: "labels.audience_placeholder", fallback: "Youth, local church, leaders..." },
      { ref: refs.sermonNotes, key: "labels.extra_notes_placeholder", fallback: "Preacher context, focus, goal..." },
      { ref: refs.devChapter, key: "labels.chapter_number", fallback: "1" },
      { ref: refs.chatChapter, key: "labels.chapter_number", fallback: "1" },
      { ref: refs.questionsChapter, key: "labels.chapter_number", fallback: "1" },
    ];
    placeholderPairs.forEach(({ ref, key, fallback }) => {
      if (ref) ref.placeholder = getTranslation(key, fallback);
    });

    // === Settings and misc labels ===
    const settingsTitle = document.querySelector("#settingsPanel .panel-title");
    if (settingsTitle) settingsTitle.textContent = getTranslation("labels.settings", "Settings");
    if (refs.savePrefsLabel) refs.savePrefsLabel.textContent = getTranslation("labels.save_prefs", "Save preferences on exit");

    const hideReadLabel = byId("hideReadLabel");
    if (hideReadLabel) hideReadLabel.textContent = getTranslation("labels.hide_read", "Hide read");

    const studyCompareText = byId("studyCompareText");
    if (studyCompareText) studyCompareText.textContent = getTranslation("labels.compare_versions", "Compare with other versions");

    const studyCompareLabel = byId("studyCompareLabel");
    if (studyCompareLabel) studyCompareLabel.textContent = getTranslation("labels.mode_label", "Mode");

    const chapterText = byId("chapterText");
    if (chapterText && (chapterText.textContent === "Select a book and load the chapter." || !chapterText.textContent.trim())) {
      chapterText.textContent = getTranslation("labels.select_book_chapter", "Select a book and load the chapter.");
    }

    // Model info: override the previous line to use "Models detected" prefix
    refs.modelInfo.textContent = `${getTranslation("labels.models_detected", "Models detected in Ollama:")} ${state.models.length}`;
    if (refs.modelHelpBtn) refs.modelHelpBtn.title = getTranslation("messages.model_help_title", "Recommended models");

    // === Import tab translations ===
    const importHelper = byId("importHelper");
    if (importHelper) importHelper.textContent = getTranslation("labels.import_helper", "The backend loads directly from Dados_Json, so this tab shows available files and allows reloading the catalog.");

    // Import help content - translate each paragraph
    const importHelpPairs = [
      { id: "importHelp1", key: "labels.import_help_1", fallback: "1. Place JSON files in Dados_Json/language/." },
      { id: "importHelp2", key: "labels.import_help_2", fallback: "2. Use a consistent version name, e.g. NVI.json or AA.json." },
      { id: "importHelp3", key: "labels.import_help_3", fallback: "3. Click Reload Catalog to update the local list." },
      { id: "importHelp4", key: "labels.import_help_4", fallback: "4. The backend uses these files directly, so there is no separate import in the native flow." },
    ];
    importHelpPairs.forEach(({ id, key, fallback }) => {
      const el = byId(id);
      if (el) el.textContent = getTranslation(key, fallback);
    });

    // Set default study request text if empty or still showing old default
    const OLD_DEFAULTS = [
      "Explain the historical and theological context of the text, highlight keywords and the pastoral application of the text.",
      "Explain the historical and theological context of the text and apply it pastorally.",
      "Explique o contexto historico e teologico, destaque palavras-chave e a aplicacao pastoral do texto.",
      "Explique o contexto historico e teologico do texto e aplique-o de forma pastoral."
    ];
    const srVal = String(refs.studyRequest?.value || "").trim();
    if (!srVal || OLD_DEFAULTS.includes(srVal)) {
      refs.studyRequest.value = getTranslation("prompts.explain_context", "Explain the historical and theological context of the text and apply it pastorally.");
    }

    // New reading tab labels
    setLabelText("readingChapterSelect", getTranslation("labels.chapter_selector", "Chapter"));

    if (refs.markChapterReadBtn) refs.markChapterReadBtn.textContent = getTranslation("buttons.mark_read", "Mark chapter");
    if (refs.unmarkChapterReadBtn) refs.unmarkChapterReadBtn.textContent = getTranslation("buttons.unmark_read", "Unmark chapter");

    refs.supportTitle.textContent = getTranslation("messages.support_title", "Support the project");
    refs.supportText.textContent = getTranslation("messages.support_desc", "If this system helps you, consider supporting its development.");
    refs.supportPaypal.textContent = getTranslation("messages.support_paypal", "Donate via PayPal");
    refs.supportPickpay.textContent = getTranslation("messages.support_picpay", "Copy PicPay key");
    refs.supportKeyHint.textContent = SUPPORT_PICKPAY_KEY
      ? getTranslation("messages.support_picpay_ready", "PicPay key ready to copy.")
      : getTranslation("messages.support_picpay_missing", "PicPay key not yet configured.");

    refs.supportPickpay.disabled = !SUPPORT_PICKPAY_KEY;

    setOutputTitle(refs.studyOutput, stripDecorators(getTranslation("formatting.answer_label", "Answer")));
    setOutputTitle(refs.sermonOutput, stripDecorators(getTranslation("formatting.explanation_label", "Result")));
    setOutputTitle(refs.devOutput, stripDecorators(getTranslation("formatting.explanation_label", "Result")));
    setOutputTitle(refs.chatOutput, stripDecorators(getTranslation("formatting.answer_label", "Answer")));
    setOutputTitle(refs.questionsOutput, stripDecorators(getTranslation("formatting.explanation_label", "Result")));

    updateWaitingText(refs.studyOutput, getTranslation("messages.select_book_chapter", "Awaiting request..."));
    updateWaitingText(refs.sermonOutput, getTranslation("messages.generating_sermon", "Awaiting generation..."));
    updateWaitingText(refs.devOutput, getTranslation("messages.generating_devotional", "Awaiting generation..."));
    updateWaitingText(refs.chatOutput, getTranslation("messages.write_question_first", "Awaiting question..."));
    updateWaitingText(refs.questionsOutput, getTranslation("messages.generating_questions", "Awaiting generation..."));

    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      const fallback = el.textContent.trim();
      if (key) {
        el.textContent = getTranslation(key, fallback);
      }
    });
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
    const locale = (getValue(refs.langSelect, "pt") || "pt").toLowerCase() === "en" ? "en-US" : "pt-BR";
    return new Intl.DateTimeFormat(locale, { dateStyle: "short", timeStyle: "short" }).format(new Date(timestamp));
  }

  const SPLASH_VERSES = [
    { pt: '"Lâmpada para os meus pés é a tua palavra e luz para o meu caminho." — Salmo 119:105', en: '"Your word is a lamp to my feet and a light to my path." — Psalm 119:105' },
    { pt: '"Não temas, porque eu sou contigo." — Isaías 41:10', en: '"Fear not, for I am with you." — Isaiah 41:10' },
    { pt: '"Tudo posso naquele que me fortalece." — Filipenses 4:13', en: '"I can do all things through him who strengthens me." — Philippians 4:13' },
    { pt: '"O Senhor é o meu pastor; nada me faltará." — Salmo 23:1', en: '"The Lord is my shepherd; I shall not want." — Psalm 23:1' },
    { pt: '"Espera no Senhor, anima-te, e ele fortalecerá o teu coração." — Salmo 27:14', en: '"Wait for the Lord; be strong, and let your heart take courage." — Psalm 27:14' },
    { pt: '"Portanto, vede prudentemente como andais, não como néscios, mas como sábios." — Efésios 5:15', en: '"Look carefully then how you walk, not as unwise but as wise." — Ephesians 5:15' },
    { pt: '"Examinais as Escrituras, porque julgais ter nelas a vida eterna." — João 5:39', en: '"You search the Scriptures because you think that in them you have eternal life." — John 5:39' },
    { pt: '"A minha graça te basta, porque o meu poder se aperfeiçoa na fraqueza." — 2 Coríntios 12:9', en: '"My grace is sufficient for you, for my power is made perfect in weakness." — 2 Corinthians 12:9' },
    { pt: '"Bem-aventurado aquele que lê e os que ouvem as palavras desta profecia." — Apocalipse 1:3', en: '"Blessed is the one who reads aloud the words of this prophecy." — Revelation 1:3' },
    { pt: '"Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito." — João 3:16', en: '"For God so loved the world, that he gave his only Son." — John 3:16' },
  ];

  function updateSplash(message, progress) {
    const el = byId("splashStatus");
    const bar = byId("splashBar");
    const verse = byId("splashVerse");
    if (el) el.textContent = message;
    if (bar && progress != null) bar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
    if (verse && !verse.dataset.active) {
      verse.dataset.active = "1";
      const lang = (getValue(refs.langSelect, "pt") || "pt").toLowerCase();
      const isEn = lang === "en";
      let idx = 0;
      verse.textContent = SPLASH_VERSES[idx][isEn ? "en" : "pt"];
      setInterval(() => {
        idx = (idx + 1) % SPLASH_VERSES.length;
        verse.style.opacity = "0";
        setTimeout(() => {
          verse.textContent = SPLASH_VERSES[idx][isEn ? "en" : "pt"];
          verse.style.opacity = "1";
        }, 400);
      }, 6000);
    }
  }

  function hideSplash() {
    const el = byId("splashOverlay");
    if (el) el.classList.add("hidden");
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

    const previousSelection = getValue(refs.langSelect) || localStorage.getItem(PREF_KEYS.language);
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
    if (!refs.modelSelect || !refs.modelInfo) return;

    const previousModel = (String(getValue(refs.modelSelect) || "").trim()) || localStorage.getItem(PREF_KEYS.model) || "";
    const modelMsg = getTranslation("messages.loading_models", "Loading Ollama models...");
    setStatus(modelMsg, false);
    updateSplash("Carregando modelos de IA...", 40);
    let ollamaOk = false;
    try {
      const data = await apiGet("/api/ai/models");
      state.models = Array.isArray(data?.ollama?.items) ? data.ollama.items : [];
      ollamaOk = data?.ollama?.online === true;
    } catch (_) {
      state.models = [];
    }

    refs.modelSelect.innerHTML = state.models
      .map((model) => `<option value="${escapeHtml(model)}">${escapeHtml(model)}</option>`)
      .join("");

    const modelsPrefix = getTranslation("labels.models_detected", "Ollama models:");
    refs.modelInfo.textContent = ollamaOk
      ? `${modelsPrefix} ${state.models.length}`
      : getTranslation("messages.no_connector", "Ollama offline");

    setStatus(getTranslation("messages.api_online", "API online at http://localhost:8000"), true);

    if (previousModel) {
      refs.modelSelect.value = state.models.includes(previousModel) ? previousModel : "";
      return;
    }

    const preferredModel = pickPreferredModel(state.models.length ? state.models : state.models);
    if (preferredModel) {
      refs.modelSelect.value = preferredModel;
    }
  }

  async function loadVersions() {
    if (!refs.versionSelect) {
      return;
    }

    const lang = getValue(refs.langSelect, "pt") || "pt";
    const previousSelection = getValue(refs.versionSelect) || localStorage.getItem(PREF_KEYS.version);
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
    // Update disabled state based on scope
    updateDisabledFields();
  }

  function updateDisabledFields() {
    const pairs = [
      { scope: refs.sermonScope, book: refs.sermonBook, chapter: refs.sermonChapter, multiId: 'sermonBooksMulti' },
      { scope: refs.devScope, book: refs.devBook, chapter: refs.devChapter, multiId: 'devBooksMulti' },
      { scope: refs.chatScope, book: refs.chatBook, chapter: refs.chatChapter, multiId: 'chatBooksMulti' },
      { scope: refs.questionsScope, book: refs.questionsBook, chapter: refs.questionsChapter, multiId: 'questionsBooksMulti' },
    ];
    pairs.forEach(({ scope, book, chapter, multiId }) => {
      if (!scope) return;
      const isWhole = getValue(scope) === "whole";
      const isSelected = getValue(scope) === "selected";
      const disabled = isWhole || isSelected;
      if (book) book.disabled = disabled;
      if (chapter) chapter.disabled = disabled;
      const multiEl = byId(multiId);
      if (multiEl) {
        if (isSelected) {
          multiEl.classList.add("visible");
          renderBookMultiSelect(multiId, scope);
        } else {
          multiEl.classList.remove("visible");
        }
      }
    });
  }

  function getScopeBookKeys(scope, selectedBook, maxBooks) {
    if (scope === "specific") {
      return [selectedBook || state.selectedBook].filter(Boolean);
    }

    if (scope === "selected") {
      if (state.selectedBooks && state.selectedBooks.length > 0) {
        return state.selectedBooks;
      }
      return [selectedBook || state.selectedBook].filter(Boolean);
    }

    // "whole" - sample representative books across both testaments
    const otBooks = state.books.filter((b) => b.key && b.name && state.books.indexOf(b) < OT_CUTOFF);
    const ntBooks = state.books.filter((b) => b.key && b.name && state.books.indexOf(b) >= OT_CUTOFF);
    const otCount = Math.min(otBooks.length, 20);
    const ntCount = Math.min(ntBooks.length, 20);
    // Evenly sample across each testament
    const stepOT = otBooks.length / otCount;
    const stepNT = ntBooks.length / ntCount;
    const keys = [];
    for (let i = 0; i < otCount; i++) {
      keys.push(otBooks[Math.floor(i * stepOT)].key);
    }
    for (let i = 0; i < ntCount; i++) {
      keys.push(ntBooks[Math.floor(i * stepNT)].key);
    }
    return keys.length ? keys : [state.selectedBook].filter(Boolean);
  }

  function renderBookList() {
    // Lista lateral removida. Selecao de livro agora e por dropdown em cada aba.
  }

  // --- Collapsible cards ---
  function toggleCard(header) {
    const card = header.closest('.card');
    if (!card) return;
    const content = card.querySelector('.card-content');
    if (!content) return;
    header.classList.toggle('collapsed');
    content.classList.toggle('collapsed');
  }

  function initCollapsibleCards() {
    document.querySelectorAll('.card').forEach(card => {
      const title = card.querySelector('.card-title');
      if (!title) return;
      const header = document.createElement('div');
      header.className = 'card-header';
      title.parentNode.insertBefore(header, title);
      header.appendChild(title);
      const content = document.createElement('div');
      content.className = 'card-content';
      const children = [...card.children];
      const idx = children.indexOf(header) + 1;
      for (let i = idx; i < children.length; i++) {
        content.appendChild(children[i]);
      }
      card.appendChild(content);
      header.addEventListener('click', () => toggleCard(header));
    });
  }

  // --- Multi-book selection ---
  function renderBookMultiSelect(containerId, scopeRef) {
    const scope = getValue(scopeRef);
    const container = byId(containerId);
    if (!container) return;
    if (scope !== "selected") {
      container.classList.remove("visible");
      return;
    }
    container.classList.add("visible");
    container.innerHTML = "";

    const otBooks = state.books.filter(b => b.key && b.name && state.books.indexOf(b) < OT_CUTOFF);
    const ntBooks = state.books.filter(b => b.key && b.name && state.books.indexOf(b) >= OT_CUTOFF);

    function appendSection(title, books) {
      if (!books.length) return;
      const heading = document.createElement('div');
      heading.className = 'book-section-title';
      heading.textContent = title;
      container.appendChild(heading);
      books.forEach(book => {
        const item = document.createElement('div');
        item.className = 'book-item' + (state.selectedBooks.includes(book.key) ? ' selected' : '');
        item.textContent = book.name;
        item.addEventListener('click', () => {
          const idx = state.selectedBooks.indexOf(book.key);
          if (idx === -1) {
            state.selectedBooks.push(book.key);
          } else {
            state.selectedBooks.splice(idx, 1);
          }
          renderBookMultiSelect(containerId, scopeRef);
        });
        container.appendChild(item);
      });
    }

    appendSection(getTranslation('labels.ot', 'Old Testament'), otBooks);
    appendSection(getTranslation('labels.nt', 'New Testament'), ntBooks);
  }



  function disableScopeFields(scopeRef, bookRef, chapterRef, multiContainerId) {
    const scope = getValue(scopeRef);
    const isWhole = scope === "whole";
    const isSelected = scope === "selected";
    if (bookRef) bookRef.disabled = isWhole;
    if (chapterRef) chapterRef.disabled = isWhole;
    const multiContainer = byId(multiContainerId);
    if (multiContainer) {
      multiContainer.style.display = isSelected ? "block" : "none";
    }
  }

  function updateBadges() {
    const versionLabel = getTranslation("labels.version_prefix", "Version");
    const bookLabel = getTranslation("labels.book_prefix", "Book");
    refs.versionBadge.textContent = `${versionLabel}: ${refs.versionSelect.value || "-"}`;
    const selectedBook = state.books.find((book) => book.key === state.selectedBook);
    refs.bookBadge.textContent = `${bookLabel}: ${selectedBook ? selectedBook.name : "-"}`;
  }

  async function loadBackendPrefs() {
    if (!refs.savePrefsCheck || !refs.savePrefsCheck.checked) {
      return;
    }
    try {
      const data = await apiGet("/api/preferences");
      if (data.language) {
        refs.langSelect.value = data.language;
        localStorage.setItem(PREF_KEYS.language, data.language);
      }
      if (data.version) {
        refs.versionSelect.value = data.version;
        localStorage.setItem(PREF_KEYS.version, data.version);
      }
      if (data.model) {
        refs.modelSelect.value = data.model;
        localStorage.setItem(PREF_KEYS.model, data.model);
      }
    } catch (_) {}
  }

  async function saveBackendPrefs() {
    if (!refs.savePrefsCheck || !refs.savePrefsCheck.checked) {
      return;
    }
    const prefs = {
      language: refs.langSelect.value || "pt",
      version: refs.versionSelect.value || "",
      model: refs.modelSelect.value || "",
    };
    try {
      await apiPost("/api/preferences", prefs);
    } catch (_) {}
  }

  async function loadBackendPrefs() {
    try {
      const data = await apiGet("/api/preferences");
      if (data.language) {
        refs.langSelect.value = data.language;
        localStorage.setItem(PREF_KEYS.language, data.language);
      }
      if (data.version) {
        refs.versionSelect.value = data.version;
        localStorage.setItem(PREF_KEYS.version, data.version);
      }
      if (data.model) {
        refs.modelSelect.value = data.model;
        localStorage.setItem(PREF_KEYS.model, data.model);
      }
    } catch (_) {}
  }

  async function saveBackendPrefs() {
    const prefs = {
      language: refs.langSelect.value || "pt",
      version: refs.versionSelect.value || "",
      model: refs.modelSelect.value || "",
    };
    try {
      await apiPost("/api/preferences", prefs);
    } catch (_) {}
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
    populateChapterList();
    updateBadges();
    // Re-render multi-book selects if containers already exist (post-bootstrap)
    const multiIds = ['sermonBooksMulti', 'devBooksMulti', 'chatBooksMulti', 'questionsBooksMulti'];
    if (byId(multiIds[0])) {
      multiIds.forEach(id => {
        const container = byId(id);
        if (container) {
          const panel = container.closest('.tab-panel');
          if (panel) {
            const scopeSelect = panel.querySelector('select[id$="Scope"]');
            if (scopeSelect) {
              renderBookMultiSelect(id, scopeSelect);
            }
          }
        }
      });
      updateDisabledFields();
    }
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

  function getBookChapterCount(bookKey) {
    const book = state.books.find((b) => b.key === bookKey);
    return book ? (book.chapters || 1) : 1;
  }

  function populateChapterListFor(bookSelect, listRef, inputRef) {
    const bookKey = getValue(bookSelect) || state.selectedBook;
    const count = bookKey ? getBookChapterCount(bookKey) : 1;
    const datalistHtml = Array.from({ length: count }, (_, i) => `<option value="${i + 1}">`).join("");
    if (listRef) listRef.innerHTML = datalistHtml;
    if (inputRef) inputRef.setAttribute("placeholder", `1-${count}`);
  }

  function populateChapterList() {
    populateChapterListFor(refs.readingBookSelect, refs.readingChapterList, refs.readingChapterSelect);
    populateChapterListFor(refs.sermonBook, refs.sermonChapterList, refs.sermonChapter);
    populateChapterListFor(refs.devBook, refs.devChapterList, refs.devChapter);
    populateChapterListFor(refs.chatBook, refs.chatChapterList, refs.chatChapter);
    populateChapterListFor(refs.questionsBook, refs.questionsChapterList, refs.questionsChapter);
  }

  function loadReadProgress() {
    try {
      const raw = localStorage.getItem("bible_read_progress");
      state.readProgress = raw ? JSON.parse(raw) : {};
    } catch (_) {
      state.readProgress = {};
    }
  }

  function saveReadProgress() {
    try {
      localStorage.setItem("bible_read_progress", JSON.stringify(state.readProgress));
    } catch (_) {}
  }

  function getReadStateKey(bookKey, chapter) {
    return `${bookKey}_${chapter}`;
  }

  const READ_COLORS = [
    { name: "Azul", css: "rgba(59,130,246,0.25)" },
    { name: "Verde", css: "rgba(16,185,129,0.25)" },
    { name: "Roxo", css: "rgba(139,92,246,0.25)" },
    { name: "Ambar", css: "rgba(245,158,11,0.25)" },
    { name: "Rosa", css: "rgba(236,72,153,0.20)" },
    { name: "Ciano", css: "rgba(6,182,212,0.25)" },
  ];

  function getDefaultReadColor() {
    return READ_COLORS[0].css;
  }

  function getReadVerses(bookKey, chapter) {
    const key = getReadStateKey(bookKey, chapter);
    return state.readProgress[key] || { verses: [], color: getDefaultReadColor() };
  }

  function toggleReadVerse(bookKey, chapter, verseNum) {
    const key = getReadStateKey(bookKey, chapter);
    if (!state.readProgress[key]) {
      state.readProgress[key] = { verses: [], color: getDefaultReadColor() };
    }
    const idx = state.readProgress[key].verses.indexOf(String(verseNum));
    if (idx >= 0) {
      state.readProgress[key].verses.splice(idx, 1);
    } else {
      state.readProgress[key].verses.push(String(verseNum));
    }
    saveReadProgress();
    renderReadProgress();
  }

  function markChapterRead(bookKey, chapter, totalVerses, mark) {
    const key = getReadStateKey(bookKey, chapter);
    const color = state.readProgress[key]?.color || getDefaultReadColor();
    if (mark) {
      state.readProgress[key] = { verses: Array.from({ length: totalVerses }, (_, i) => String(i + 1)), color };
    } else {
      delete state.readProgress[key];
    }
    saveReadProgress();
    renderReadProgress();
    renderVerseList();
    renderColorPalette();
  }

  function renderReadProgress() {
    if (!refs.readingProgress) return;
    const bookKey = getValue(refs.readingBookSelect) || state.selectedBook;
    const chapter = getValue(refs.readingChapterSelect, "1") || "1";
    const rv = getReadVerses(bookKey, chapter);
    const total = state.chapterData ? Object.keys(state.chapterData.verses || {}).length : 0;
    const count = rv.verses.length;
    refs.readingProgress.textContent = total > 0 ? getTranslation('messages.verses_read', '%d/%d verses read').replace('%d', count).replace('%d', total) : "";
  }

  function renderColorPalette() {
    if (!refs.colorPalette) return;
    const bookKey = state.selectedBook;
    const chapter = getValue(refs.readingChapterSelect, "1") || "1";
    const rv = getReadVerses(bookKey, chapter);
    const currentColor = rv.color || getDefaultReadColor();
    refs.colorPalette.innerHTML = READ_COLORS.map((c) =>
      `<button class="color-btn${c.css === currentColor ? " active" : ""}" data-color="${c.css}" title="${getTranslation('messages.color_' + c.name.toLowerCase(), c.name)}" style="background:${c.css}"></button>`
    ).join("");
  }

  function setActiveColor(color) {
    if (!refs.colorPalette) return;
    const bookKey = state.selectedBook;
    const chapter = getValue(refs.readingChapterSelect, "1") || "1";
    const key = getReadStateKey(bookKey, chapter);
    if (!state.readProgress[key]) {
      state.readProgress[key] = { verses: [], color };
    } else {
      state.readProgress[key].color = color;
    }
    saveReadProgress();
    renderVerseList();
    renderColorPalette();
  }

  function initColorPalette() {
    if (!refs.colorPalette) return;
    renderColorPalette();
    refs.colorPalette.addEventListener("click", (e) => {
      const btn = e.target.closest(".color-btn");
      if (!btn) return;
      setActiveColor(btn.dataset.color);
    });
  }

  function initSidebarToggle() {
    if (!refs.sidebarToggle) return;
    const shell = document.querySelector(".shell");
    const saved = localStorage.getItem("sidebar_collapsed");
    if (saved === "true" && shell) {
      shell.classList.add("collapsed");
      refs.sidebarToggle.textContent = "▶";
    }
    refs.sidebarToggle.addEventListener("click", () => {
      if (!shell) return;
      shell.classList.toggle("collapsed");
      const isCollapsed = shell.classList.contains("collapsed");
      refs.sidebarToggle.textContent = isCollapsed ? "▶" : "◀";
      localStorage.setItem("sidebar_collapsed", isCollapsed);
    });
  }

  function renderVerseList() {
    if (!state.chapterData || !refs.chapterText) return;
    const verses = state.chapterData.verses || {};
    const bookKey = state.selectedBook;
    const chapter = getValue(refs.readingChapterSelect, "1") || "1";
    const rv = getReadVerses(bookKey, chapter);
    const readColor = rv.color || getDefaultReadColor();
    const selected = parseVerseSelection(getValue(refs.readingVerseRange));
    const hideRead = refs.hideReadVerses ? refs.hideReadVerses.checked : false;

    const keys = Object.keys(verses).sort((a, b) => Number(a) - Number(b));
    let html = "";
    for (const vKey of keys) {
      if (selected.length && !selected.includes(vKey)) continue;
      const isRead = rv.verses.includes(vKey);
      if (hideRead && isRead) continue;
      const bgColor = isRead ? readColor : "transparent";
      const mark = isRead ? "✓" : "";
      html += `<div class="verse-row" data-verse="${vKey}" style="background:${bgColor}">
        <span class="verse-num">${mark ? `<span style="color:var(--ok);margin-right:4px">${mark}</span>` : ""}${vKey}</span>
        <span class="verse-text">${escapeHtml(verses[vKey])}</span>
      </div>`;
    }
    refs.chapterText.innerHTML = html || `<div class='empty-state'>${escapeHtml(getTranslation("messages.no_verses_found", "No verses found."))}</div>`;

    refs.chapterText.querySelectorAll(".verse-row").forEach((row) => {
      row.addEventListener("click", (e) => {
        if (e.target.closest(".verse-num") || e.target.closest(".verse-text")) {
          toggleReadVerse(bookKey, chapter, row.dataset.verse);
          renderVerseList();
        }
      });
    });
    renderReadProgress();
    updateStudyReference();
  }

  async function loadChapter(retryOnMismatch = true) {
    state.selectedBook = getValue(refs.readingBookSelect) || state.selectedBook;
    const ready = await ensureValidBibleSelection();
    if (!ready || !state.selectedBook) {
      if (refs.chapterText) refs.chapterText.innerHTML = `<div class='empty-state'>${escapeHtml(getTranslation("messages.no_book_selected", "No book selected."))}</div>`;
      return;
    }

    const lang = getValue(refs.langSelect, "pt") || "pt";
    const version = getValue(refs.versionSelect);
    if (!version) {
      if (refs.chapterText) refs.chapterText.innerHTML = `<div class='empty-state'>${escapeHtml(getTranslation("messages.no_version_language", "No version selected for this language."))}</div>`;
      return;
    }

    populateChapterList();
    const chapter = Number.parseInt(getValue(refs.readingChapterSelect, "1") || "1", 10) || 1;
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

    refs.studyOutput.textContent = getTranslation("messages.select_book_chapter", "Awaiting request...");
    updateBadges();
    updateDirection();
    renderVerseList();
    renderColorPalette();
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

  async function collectSelectedBooksContext(bookKeys, maxBooks, chapterNumber = 1) {
    const selected = (bookKeys || []).slice(0, maxBooks);
    const results = [];
    // Process in parallel batches of 12 to avoid hammering the API
    for (let i = 0; i < selected.length; i += 12) {
      const batch = selected.slice(i, i + 12);
      const batchResults = await Promise.allSettled(
        batch.map((bookKey) => collectChapterText(bookKey, chapterNumber))
      );
      for (const res of batchResults) {
        if (res.status === "fulfilled" && res.value && res.value.text) {
          results.push(`**${res.value.reference}**\n${res.value.text}`);
        }
      }
    }
    return results.join("\n\n");
  }

  async function collectComparisonContext() {
    if (!state.selectedBook || !state.versions.length) {
      return "";
    }
    const lang = getValue(refs.langSelect, "pt") || "pt";
    const chapter = Number.parseInt(getValue(refs.readingChapterSelect, "1") || "1", 10) || 1;
    const chunks = [];
    for (const version of state.versions) {
      try {
        const data = await apiGet(
          `/api/bible/chapter?lang=${encodeURIComponent(lang)}&version=${encodeURIComponent(version)}&book=${encodeURIComponent(state.selectedBook)}&chapter=${encodeURIComponent(chapter)}`
        );
        const verses = data.verses || {};
        const text = buildVerseText(verses);
        if (text) {
          chunks.push(`**${version}**\n${text}`);
        }
      } catch (_) {
      }
    }
    return chunks.join("\n\n");
  }

  function updateStudyReference() {
    if (!refs.studyReference) return;
    const book = state.selectedBook || getValue(refs.readingBookSelect) || "—";
    const chapter = getValue(refs.readingChapterSelect, "1") || "1";
    const verses = String(getValue(refs.readingVerseRange) || "").trim();
    let ref = `${book} ${chapter}`;
    if (verses) ref += `:${verses}`;
    const baseOn = getTranslation("labels.base_on", "Based on");
    refs.studyReference.textContent = `${baseOn}: ${ref}`;
  }

  function buildStudyRequest(compareMode) {
    if (compareMode) {
      return [
        "Compare as diferentes traducoes do mesmo texto biblico.",
        "Analise diferencas de vocabulario, escolhas de traducao e possiveis impactos teologicos.",
        "Entregue uma resposta clara, equilibrada e pastoral.",
      ].join(" ");
    }
    return String(refs.studyRequest.value || "").trim() || getTranslation("prompts.explain_context", "Explain the historical and theological context of the text and apply it pastorally.");
  }

  function buildSermonRequest() {
    const style = refs.sermonStyle.value;
    const theme = String(refs.sermonTheme.value || "").trim() || getTranslation("prompts.default_theme", "Theme to be developed from the text");
    const audience = String(refs.sermonAudience.value || "").trim() || getTranslation("prompts.default_audience", "General church");
    const notes = String(refs.sermonNotes.value || "").trim() || getTranslation("prompts.default_notes", "No additional notes");
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
    const feeling = String(refs.devFeeling.value || "").trim() || "Gratitude";
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
        const haystack = [item.reference, item.title, item.question, item.request, item.response, item.theme, item.feeling].filter(Boolean).join(" ").toLowerCase();
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
      container.innerHTML = `<div class="empty-state">${escapeHtml(getTranslation("messages.no_search_results", "No records found."))}</div>`;
      return;
    }
    container.innerHTML = `<div class="record-list">${items
      .map((item, index) => renderRecord(type, item, index))
      .join("")}</div>`;
    container.querySelectorAll("[data-action=copy]").forEach((button) => button.addEventListener("click", () => copyText(button.dataset.text || "")));
    container.querySelectorAll("[data-action=pdf]").forEach((button) => button.addEventListener("click", () => exportPdfFromRecord(type, Number(button.dataset.index))));
    container.querySelectorAll("[data-action=delete]").forEach((button) => button.addEventListener("click", () => deleteHistoryEntry(type, Number(button.dataset.index))));
    container.querySelectorAll(".record-head").forEach((head) => {
      head.addEventListener("click", () => {
        const record = head.closest(".record");
        if (!record) return;
        const collapsed = record.classList.toggle("collapsed");
        record.querySelectorAll(".record-body, .record-actions").forEach((el) => {
          el.style.display = collapsed ? "none" : "";
        });
      });
    });
    updateDirection();
  }

  function renderRecord(type, item, index) {
    const title = item.title || item.reference || item.question || getTranslation("messages.record_default", "Record");
    const metaParts = [formatTime(item.timestamp)];
    if (item.version) metaParts.push(`${getTranslation("captions.version", "Version:").replace(STRIP_PREFIX_RE, "").trim()} ${item.version}`);
    if (item.model) metaParts.push(`${getTranslation("captions.model", "Model:").replace(STRIP_PREFIX_RE, "").trim()} ${item.model}`);
    const scopeLabels = {
      specific: getTranslation("labels.specific_book", "Specific Book"),
      selected: getTranslation("labels.multiple_books", "Selected Books"),
      whole: getTranslation("labels.whole_bible", getTranslation("labels.entire_bible", "Whole Bible")),
    };
    const scopeText = item.scope ? scopeLabels[item.scope] || item.scope : "";
    if (scopeText) metaParts.push(`${getTranslation("labels.scope_colon", "Scope:").replace(STRIP_PREFIX_RE, "").trim()} ${scopeText}`);
    const body = item.response || item.answer || item.content || item.text || "";
return `
  <article class="record collapsed">
        <div class="record-head">
          <div>
            <div class="record-title">${escapeHtml(title)}</div>
            <div class="record-meta">${escapeHtml(metaParts.join(" | "))}</div>
          </div>
        </div>
        ${body ? `<div class="record-body"><strong>${escapeHtml(getTranslation("formatting.explanation_label", "Content:").replace(STRIP_PREFIX_RE, "").replace(/:$/, ""))}</strong>\n${escapeHtml(body)}</div>` : ""}
        <div class="record-actions">
          <button class="ghost-button" data-action="copy" data-text="${escapeHtml(buildCopyText(type, item))}">${escapeHtml(getTranslation("buttons.copy", "Copy").replace(STRIP_PREFIX_RE, "").trim())}</button>
          <button class="ghost-button" data-action="pdf" data-index="${index}">${escapeHtml(getTranslation("buttons.generate_pdf", "PDF").replace(STRIP_PREFIX_RE, "").trim() || "PDF")}</button>
          <button class="ghost-button" data-action="delete" data-index="${index}">${escapeHtml(getTranslation("buttons.delete", "Delete").replace(STRIP_PREFIX_RE, "").trim())}</button>
        </div>
      </article>
    `;
  }

  function buildCopyText(type, item) {
    const parts = [];
    parts.push(item.title || item.reference || item.question || getTranslation("messages.record_default", "Record"));
    if (item.response) {
      parts.push(getTranslation("formatting.answer_label", "Answer:"));
      parts.push(item.response);
    } else if (item.answer) {
      parts.push(getTranslation("formatting.answer_label", "Answer:"));
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
    const title = item.title || item.reference || item.question || getTranslation("messages.record_default", "Record");
    const scopeLabels = {
      specific: getTranslation("labels.specific_book", "Specific Book"),
      selected: getTranslation("labels.multiple_books", "Selected Books"),
      whole: getTranslation("labels.whole_bible", getTranslation("labels.entire_bible", "Whole Bible")),
    };
    const scopeSubtitle = item.scope ? scopeLabels[item.scope] || item.scope : "";
    const sections = [];
    if (item.context) {
      sections.push({ heading: stripDecorators(getTranslation("formatting.context_label", "Context")), body: item.context });
    }
    if (item.response) {
      sections.push({ heading: stripDecorators(getTranslation("formatting.explanation_label", "Result")), body: item.response });
    } else if (item.answer) {
      sections.push({ heading: stripDecorators(getTranslation("formatting.answer_label", "Result")), body: item.answer });
    }
    if (item.question) {
      sections.push({ heading: stripDecorators(getTranslation("formatting.question_label", "Question")), body: item.question });
    }
    const response = await fetch(`${API}/api/export/pdf`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        subtitle: item.reference || scopeSubtitle || "Biblical Study AI",
        sections,
        footer: `${getTranslation("messages.pdf_generated", "Generated on")} ${formatTime(Date.now())}`,
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
          study: getTranslation("menu.reading", "Studies").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          sermon: getTranslation("menu.sermon_gen", "Sermons").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          devotional: getTranslation("menu.devotional", "Devotionals").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          chat: getTranslation("menu.chat", "Chats").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          questions: getTranslation("menu.questions_gen", "Questions").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
        };
        return `<div class="summary-card"><strong>${items.length}</strong>${labels[type]}</div>`;
      })
      .join("");

    const allItems = Object.entries(state.histories)
      .flatMap(([type, items]) => items.map((item) => ({ ...item, kind: type })))
      .sort((left, right) => right.timestamp - left.timestamp);

    if (!allItems.length) {
      refs.allHistory.innerHTML = `<div class="empty-state">${escapeHtml(getTranslation("messages.no_studies_yet", "No records yet."))}</div>`;
      return;
    }

    refs.allHistory.innerHTML = `<div class="record-list">${allItems
      .map((item) => {
        const title = item.title || item.reference || item.question || getTranslation("messages.record_default", "Record");
        const kindLabel = {
          study: getTranslation("menu.reading", "Study").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          sermon: getTranslation("menu.sermon_gen", "Sermon").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          devotional: getTranslation("menu.devotional", "Devotional").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          chat: getTranslation("menu.chat", "Chat").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
          questions: getTranslation("menu.questions_gen", "Questions").replace(/^[^\p{L}\p{N}]+/u, "").trim(),
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
            ${body ? `<div class="record-body"><strong>${escapeHtml(getTranslation("formatting.explanation_label", "Content:").replace(/^[^\p{L}\p{N}]+/u, "").replace(/:$/, ""))}</strong>\n${escapeHtml(body)}</div>` : ""}
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
      refs.importSources.innerHTML = `<div class="empty-state">${escapeHtml(getTranslation("messages.no_json_found", "No JSON files found for this language."))}</div>`;
      return;
    }
    refs.importSources.innerHTML = state.importSources
      .map((item) => `<div class="record"><div class="record-title">${escapeHtml(item.version)}</div><div class="record-meta">${escapeHtml(item.name)} | ${escapeHtml(String(item.size))} bytes | ${escapeHtml(item.modified)}</div></div>`)
      .join("");
  }

  async function handleStudyGenerate() {
    refs.studyButton.disabled = true;
    refs.studyOutput.textContent = getTranslation("messages.generating_explanation", "Generating...");
    try {
      const compareMode = refs.studyCompare.checked && state.versions.length > 1;
      const context = compareMode ? await collectComparisonContext() : await collectChapterContext();
      if (!context) {
        refs.studyOutput.textContent = getTranslation("messages.no_context", "No context found.");
        return;
      }
      const request = buildStudyRequest(compareMode);
      const chapterRef = getValue(refs.readingChapterSelect, "1") || "1";
      const verses = String(getValue(refs.readingVerseRange) || "").trim();
      const refSuffix = verses ? `:${verses}` : "";
      const reference = compareMode
        ? `${state.selectedBook ? state.selectedBook : getTranslation("messages.bible_default", "Bible")} ${chapterRef}${refSuffix} - ${getTranslation("messages.history_comparison", "Version comparison").toLowerCase()}`
        : `${state.selectedBook ? state.selectedBook : getTranslation("messages.bible_default", "Bible")} ${chapterRef}${refSuffix}`;
      const response = await callGenerate("study", reference, context, request, {
        temperature: 0.2,
        maxTokens: compareMode ? 2000 : 1500,
        timeoutSec: compareMode ? 240 : 180,
      });
      refs.studyOutput.textContent = response;
      updateDirection();
      addHistory("study", {
        timestamp: Date.now(),
        title: compareMode ? getTranslation("messages.history_comparison", "Version comparison") : getTranslation("messages.history_study", "Bible study"),
        reference,
        response,
        version: refs.versionSelect.value,
        model: String(getValue(refs.modelSelect) || "").trim(),
        scope: compareMode ? getTranslation("labels.compare", "Comparison") : getTranslation("labels.chapter_selector", "Chapter"),
      });
    } catch (error) {
      refs.studyOutput.textContent = `${getTranslation("messages.error_prefix", "Error")}: ${error.message}`;
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
    const range = String(getValue(refs.readingVerseRange) || "").trim();
    const selected = range ? parseVerseSelection(range) : [];
    const text = selected.length ? buildVerseText(verses, selected) : buildVerseText(verses);
    return text;
  }

  async function handleSermonGenerate() {
    refs.sermonButton.disabled = true;
    refs.sermonOutput.textContent = getTranslation("messages.generating_sermon", "Generating...");
    try {
      const scope = getValue(refs.sermonScope, "specific");
      const selectedBook = getValue(refs.sermonBook) || state.selectedBook;
      const scopeKeys = getScopeBookKeys(scope, selectedBook, state.books.length);
      const chapterNum = Number.parseInt(getValue(refs.sermonChapter, "1") || "1", 10) || 1;
      const context =
        scope === "specific"
          ? await collectSelectedBooksContext([selectedBook].filter(Boolean), 1, chapterNum)
          : await collectSelectedBooksContext(scopeKeys, state.books.length, scope === "selected" ? chapterNum : 1);
      if (!context) {
        refs.sermonOutput.textContent = getTranslation("messages.no_context_sermon", "No context found for sermon.");
        return;
      }
      const request = buildSermonRequest();
      const defaultSermao = getTranslation("messages.history_sermon", "Sermon");
      const reference = `${getValue(refs.sermonTheme, defaultSermao) || defaultSermao} - ${getValue(refs.versionSelect, "-")}`;
      const response = await callGenerate("sermon", reference, context, request, { temperature: 0.35, maxTokens: 2600, timeoutSec: 360 });
      refs.sermonOutput.textContent = response;
      updateDirection();
      addHistory("sermon", {
        timestamp: Date.now(),
        title: getValue(refs.sermonTheme, defaultSermao) || defaultSermao,
        reference,
        response,
        theme: getValue(refs.sermonTheme),
        audience: getValue(refs.sermonAudience),
        version: getValue(refs.versionSelect),
        model: String(getValue(refs.modelSelect) || "").trim(),
        scope,
      });
    } catch (error) {
      refs.sermonOutput.textContent = `${getTranslation("messages.error_prefix", "Error")}: ${error.message}`;
    } finally {
      refs.sermonButton.disabled = false;
    }
  }

  async function handleDevotionalGenerate() {
    refs.devButton.disabled = true;
    refs.devOutput.textContent = getTranslation("messages.generating_devotional", "Generating...");
    try {
      const scope = getValue(refs.devScope, "specific");
      const selectedBook = getValue(refs.devBook) || state.selectedBook;
      const scopeKeys = getScopeBookKeys(scope, selectedBook, state.books.length);
      const chapterNum = Number.parseInt(getValue(refs.devChapter, "1") || "1", 10) || 1;
      const context =
        scope === "specific"
          ? await collectSelectedBooksContext([selectedBook].filter(Boolean), 1, chapterNum)
          : await collectSelectedBooksContext(scopeKeys, state.books.length, scope === "selected" ? chapterNum : 1);
      if (!context) {
        refs.devOutput.textContent = getTranslation("messages.no_context_devotional", "No context found for devotional.");
        return;
      }
      const request = buildDevotionalRequest();
      const defaultDev = getTranslation("messages.history_devotional", "Devotional");
      const reference = getValue(refs.devFeeling, defaultDev) || defaultDev;
      const response = await callGenerate("devotional", reference, context, request, { temperature: 0.18, maxTokens: 1200, timeoutSec: 240 });
      refs.devOutput.textContent = response;
      updateDirection();
      addHistory("devotional", {
        timestamp: Date.now(),
        title: reference,
        reference,
        response,
        feeling: getValue(refs.devFeeling),
        version: getValue(refs.versionSelect),
        model: String(getValue(refs.modelSelect) || "").trim(),
        scope,
      });
    } catch (error) {
      refs.devOutput.textContent = `${getTranslation("messages.error_prefix", "Error")}: ${error.message}`;
    } finally {
      refs.devButton.disabled = false;
    }
  }

  async function handleChatGenerate() {
    refs.chatButton.disabled = true;
    refs.chatOutput.textContent = getTranslation("messages.generating_answer", "Generating...");
    try {
      const question = String(getValue(refs.chatQuestion) || "").trim();
      if (!question) {
        refs.chatOutput.textContent = getTranslation("messages.write_question_first", "Write a question first.");
        return;
      }
      const scope = getValue(refs.chatScope, "specific");
      const selectedBook = getValue(refs.chatBook) || state.selectedBook;
      const scopeKeys = getScopeBookKeys(scope, selectedBook, state.books.length);
      const chapterNum = Number.parseInt(getValue(refs.chatChapter, "1") || "1", 10) || 1;
      const context =
        scope === "specific"
          ? await collectSelectedBooksContext([selectedBook].filter(Boolean), 1, chapterNum)
          : await collectSelectedBooksContext(scopeKeys, state.books.length, scope === "selected" ? chapterNum : 1);
      if (!context) {
        refs.chatOutput.textContent = getTranslation("messages.no_context_chat", "No context found for chat.");
        return;
      }
      const request = buildChatRequest(question);
      const reference = `${getTranslation("messages.history_chat_teologico", "Theological chat")} - ${getValue(refs.versionSelect, "-")}`;
      const response = await callGenerate("chat", reference, context, request, { temperature: 0.22, maxTokens: 1400, timeoutSec: 240 });
      refs.chatOutput.textContent = response;
      updateDirection();
      addHistory("chat", {
        timestamp: Date.now(),
        title: getTranslation("messages.history_chat_teologico", "Theological chat"),
        reference,
        question,
        answer: response,
        version: getValue(refs.versionSelect),
        model: String(getValue(refs.modelSelect) || "").trim(),
        scope,
      });
    } catch (error) {
      refs.chatOutput.textContent = `${getTranslation("messages.error_prefix", "Error")}: ${error.message}`;
    } finally {
      refs.chatButton.disabled = false;
    }
  }

  async function handleQuestionsGenerate() {
    refs.questionsButton.disabled = true;
    refs.questionsOutput.textContent = getTranslation("messages.generating_questions", "Generating...");
    try {
      const count = Number.parseInt(getValue(refs.questionsCount, "10") || "10", 10) || 10;
      const withAnswers = getValue(refs.questionsMode, "with") === "with";
      const scope = getValue(refs.questionsScope, "specific");
      const selectedBook = getValue(refs.questionsBook) || state.selectedBook;
      const scopeKeys = getScopeBookKeys(scope, selectedBook, state.books.length);
      const chapterNum = Number.parseInt(getValue(refs.questionsChapter, "1") || "1", 10) || 1;
      const context =
        scope === "specific"
          ? await collectSelectedBooksContext([selectedBook].filter(Boolean), 1, chapterNum)
          : await collectSelectedBooksContext(scopeKeys, state.books.length, scope === "selected" ? chapterNum : 1);
      if (!context) {
        refs.questionsOutput.textContent = getTranslation("messages.no_context_questions", "No context found for questions.");
        return;
      }
      const request = buildQuestionsRequest(count, withAnswers);
      const reference = `${getTranslation("messages.history_questions_with", "Questions")} - ${getValue(refs.versionSelect, "-")}`;
      const response = await callGenerate("questions", reference, context, request, {
        temperature: 0.22,
        maxTokens: Math.min(count * (withAnswers ? 80 : 50) + 800, 8000),
        timeoutSec: Math.max(180, count * (withAnswers ? 10 : 4)),
      });
      refs.questionsOutput.textContent = response;
      updateDirection();
      addHistory("questions", {
        timestamp: Date.now(),
        title: withAnswers ? getTranslation("messages.history_questions_with", "Questions with answers") : getTranslation("messages.history_questions_without", "Questions without answers"),
        reference,
        response,
        questionsCount: count,
        withAnswers,
        version: getValue(refs.versionSelect),
        model: String(getValue(refs.modelSelect) || "").trim(),
        scope,
      });
    } catch (error) {
      refs.questionsOutput.textContent = `${getTranslation("messages.error_prefix", "Error")}: ${error.message}`;
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
    if (refs.savePrefsCheck) {
      const savedFlag = localStorage.getItem(PREF_KEYS.savePrefs);
      refs.savePrefsCheck.checked = savedFlag === "true";
    }
    await loadBackendPrefs();
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
    setStatus(getTranslation("messages.refreshing_data", "Updating data..."), false);
    try {
      await loadBackendPrefs();
      await loadUiTranslations(getValue(refs.langSelect, "pt") || "pt");
      applyUiTranslations();
      await loadOllamaModels();
      await loadVersions();
      await loadBooks();
      await loadChapter();
      await loadImportSources();
      setStatus(getTranslation("messages.api_online", "API online at http://localhost:8000"), true);
      state.online = true;
    } catch (error) {
      setStatus(`${getTranslation("messages.error_prefix", "Error")}: ${error.message}`, false);
    }
  }

  function createMultiBookContainers() {
    const pairs = [
      { scopeId: 'sermonScope', containerId: 'sermonBooksMulti', afterId: 'sermonStyle' },
      { scopeId: 'devScope', containerId: 'devBooksMulti', afterId: 'devFeeling' },
      { scopeId: 'chatScope', containerId: 'chatBooksMulti', afterId: 'chatChapter' },
      { scopeId: 'questionsScope', containerId: 'questionsBooksMulti', afterId: 'questionsChapter' },
    ];
    pairs.forEach(({ scopeId, containerId, afterId }) => {
      if (byId(containerId)) return;
      const afterEl = byId(afterId);
      if (!afterEl) return;
      const container = document.createElement('div');
      container.id = containerId;
      container.className = 'book-multi-select';
      afterEl.parentNode.insertBefore(container, afterEl.nextSibling);
    });
  }

  async function bootstrap() {
    try {
      let attempt = 0;
      updateSplash("Iniciando servidor...", 5);
      while (true) {
        try {
          await apiGet("/health");
          state.online = true;
          updateSplash("Servidor conectado!", 25);
          break;
        } catch (_) {
          attempt++;
          const progress = Math.min(22, 5 + attempt * 0.6);
          updateSplash("Conectando ao servidor...", progress);
          if (window.__TAURI__ && attempt % 5 === 0) {
            try {
              const log = await window.__TAURI__.invoke("read_log");
              const lines = log.split("\n").filter(Boolean);
              if (lines.length > 0) {
                const last = lines[lines.length - 1];
                const clean = last.replace(/\[[^\]]*\]\s*/g, "").replace(/\x1B\[[0-9;]*[a-zA-Z]/g, "").trim();
                updateSplash(clean, progress);
              }
            } catch (_) {}
          }
          await new Promise((resolve) => setTimeout(resolve, 1200));
        }
      }

      updateSplash("Carregando recursos...", 30);
      await loadImportSourcesAndMeta();
      updateSplash("Preparando interface...", 75);
      loadReadProgress();
      renderAllHistories();
      updateStudyReference();
      bindHistoryControls();
      initCollapsibleCards();
      createMultiBookContainers();
      // Render multi-book selects for any already-selected scope
      ['sermonBooksMulti', 'devBooksMulti', 'chatBooksMulti', 'questionsBooksMulti'].forEach(id => {
        const container = byId(id);
        if (container) {
          const panel = container.closest('.tab-panel');
          if (panel) {
            const scopeSelect = panel.querySelector('select[id$="Scope"]');
            if (scopeSelect) {
              renderBookMultiSelect(id, scopeSelect);
            }
          }
        }
      });
      updateDisabledFields();
      bindEvents();
      updateBadges();
      updateDirection();
      setStatus(getTranslation("messages.api_online", "API online at http://localhost:8000"), true);
      updateSplash("Pronto!", 100);
      setTimeout(hideSplash, 600);
      if (!localStorage.getItem("bible_study_visited")) {
        localStorage.setItem("bible_study_visited", "1");
        setActiveTab("about");
      } else {
        setActiveTab("reading");
      }
    } catch (error) {
      setStatus(`${getTranslation("messages.bootstrap_error", "Error starting up")}: ${error.message}`, false);
      updateSplash(`Erro: ${error.message}`, 0);
      setTimeout(hideSplash, 2000);
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
    if (refs.modelHelpBtn && refs.modelHelpContent) {
      refs.modelHelpBtn.addEventListener("click", () => {
        const visible = refs.modelHelpContent.style.display !== "none";
        refs.modelHelpContent.style.display = visible ? "none" : "block";
        if (!visible) {
          refs.modelHelpContent.innerHTML = getTranslation("messages.model_help_text", "For computers with dedicated GPU: llama3.1:8b, mistral:7b, gemma2:9b, phi4, deepseek-r1:8b\nFor computers without dedicated GPU (CPU only): llama3.2:1b, llama3.2:3b, qwen2.5:7b, qwen2.5-coder:7b");
        }
      });
    }
    if (refs.modelSelect) {
      refs.modelSelect.addEventListener("change", () => {
        const selected = getValue(refs.modelSelect);
        if (selected) {
          refs.modelSelect.value = selected;
          localStorage.setItem(PREF_KEYS.model, selected);
          saveBackendPrefs();
        }
      });
    }
    if (refs.savePrefsCheck) {
      refs.savePrefsCheck.addEventListener("change", () => {
        localStorage.setItem(PREF_KEYS.savePrefs, refs.savePrefsCheck.checked ? "true" : "false");
        if (refs.savePrefsCheck.checked) {
          saveBackendPrefs();
        }
      });
    }
    refs.importRefresh.addEventListener("click", loadImportSources);
    refs.langSelect.addEventListener("change", async () => {
      localStorage.setItem(PREF_KEYS.language, refs.langSelect.value);
      try {
        await loadUiTranslations(getValue(refs.langSelect, "pt") || "pt");
        applyUiTranslations();
        await loadVersions();
        await loadBooks();
        await loadChapter();
        await loadImportSources();
        renderAllHistories();
        updateBadges();
        saveBackendPrefs();
      } catch (error) {
        if (refs.chapterText) refs.chapterText.innerHTML = `<div class='empty-state'>${escapeHtml(getTranslation("messages.error_prefix", "Error"))}: ${escapeHtml(error.message)}</div>`;
      } finally {
        updateDirection();
      }
    });
    refs.versionSelect.addEventListener("change", async () => {
      localStorage.setItem(PREF_KEYS.version, refs.versionSelect.value);
      try {
        await loadBooks();
        await loadChapter();
        updateBadges();
        saveBackendPrefs();
      } catch (error) {
        if (refs.chapterText) refs.chapterText.innerHTML = `<div class='empty-state'>${escapeHtml(getTranslation("messages.error_prefix", "Error"))}: ${escapeHtml(error.message)}</div>`;
      }
    });
    if (refs.readingBookSelect) {
      refs.readingBookSelect.addEventListener("change", async () => {
        state.selectedBook = getValue(refs.readingBookSelect) || state.selectedBook;
        updateScopeControls();
        updateBadges();
        populateChapterList();
        try {
          await loadChapter();
        } catch (error) {
          if (refs.chapterText) refs.chapterText.innerHTML = `<div class='empty-state'>${escapeHtml(getTranslation("messages.error_prefix", "Error"))}: ${escapeHtml(error.message)}</div>`;
        }
      });
    }
    // Sync chapter list when book changes on any tab
    [refs.sermonBook, refs.devBook, refs.chatBook, refs.questionsBook].forEach((sel) => {
      if (sel) {
        sel.addEventListener("change", populateChapterList);
      }
    });
    [refs.sermonScope, refs.devScope, refs.chatScope, refs.questionsScope].forEach((scopeRef) => {
      if (scopeRef) {
        scopeRef.addEventListener("change", () => {
          updateScopeControls();
          updateDisabledFields();
        });
      }
    });
    // Reading tab events
    initSidebarToggle();
    if (refs.loadReadingChapterBtn) {
      refs.loadReadingChapterBtn.addEventListener("click", loadChapter);
    }
    if (refs.readingChapterSelect) {
      refs.readingChapterSelect.addEventListener("change", loadChapter);
    }
    if (refs.readingVerseRange) {
      refs.readingVerseRange.addEventListener("change", renderVerseList);
    }
    if (refs.markChapterReadBtn) {
      refs.markChapterReadBtn.addEventListener("click", () => {
        const bookKey = state.selectedBook;
        const chapter = getValue(refs.readingChapterSelect, "1") || "1";
        const verses = state.chapterData ? state.chapterData.verses || {} : {};
        const total = Object.keys(verses).length;
        markChapterRead(bookKey, chapter, total, true);
        renderVerseList();
      });
    }
    if (refs.unmarkChapterReadBtn) {
      refs.unmarkChapterReadBtn.addEventListener("click", () => {
        const bookKey = state.selectedBook;
        const chapter = getValue(refs.readingChapterSelect, "1") || "1";
        markChapterRead(bookKey, chapter, 0, false);
        renderVerseList();
      });
    }
    if (refs.hideReadVerses) {
      refs.hideReadVerses.addEventListener("change", renderVerseList);
    }
    initColorPalette();
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
          setStatus(getTranslation("messages.picpay_not_configured", "PicPay key not configured."), false);
          return;
        }
        await copyText(SUPPORT_PICKPAY_KEY);
        setStatus(getTranslation("messages.picpay_copied", "PicPay key copied."), true);
      });
    }
  }

  bootstrap();
})();

