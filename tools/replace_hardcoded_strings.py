"""
Script para substituir todas as strings hardcoded restantes no app.py
"""
import re

# Ler o arquivo
with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Dicionário de substituições
replacements = {
    # Devocional
    '"Tema ou sentimento a meditar"': 't(trans, "labels.theme_or_feeling", "Tema ou sentimento a meditar")',
    '"Selecione um versiculo ou escopo para ancorar a meditacao."': 't(trans, "messages.select_verse_meditation", "Selecione um versiculo ou escopo para ancorar a meditacao.")',
    '"Ollama esta offline. Ligue o servidor e tente novamente."': 't(trans, "messages.ollama_offline_retry", "Ollama esta offline. Ligue o servidor e tente novamente.")',
    '"🕊️ Criando devocional..."': 't(trans, "messages.generating_devotional", "🕊️ Criando devocional...")',
    '"✅ Devocional gerado e salvo no histórico!"': 't(trans, "messages.devotional_saved", "✅ Devocional gerado e salvo no histórico!")',
    '"🕊️ Acesse a aba \'Histórico Devocionais\' para revisar suas meditações."': 't(trans, "messages.check_devotional_tab", "🕊️ Acesse a aba \'Histórico Devocionais\' para revisar suas meditações.")',
    '"👁️ Prévia do Devocional"': 't(trans, "expanders.devotional_preview", "👁️ Prévia do Devocional")',
    '"✨ Gerar Devocional"': 't(trans, "buttons.generate_devotional", "✨ Gerar Devocional")',
    
    # Chat Teológico
    '"Chat Teologico"': 't(trans, "headers.theological_chat", "Chat Teologico")',
    '"Importe uma versao para poder dialogar com o chat teologico."': 't(trans, "messages.import_version_chat", "Importe uma versao para poder dialogar com o chat teologico.")',
    '"Digite sua duvida biblica"': 't(trans, "labels.your_question", "Digite sua dúvida bíblica")',
    '"✨ Enviar Pergunta"': 't(trans, "buttons.send_question", "✨ Enviar Pergunta")',
    '"Selecione um versiculo para que a IA utilize como autoridade."': 't(trans, "messages.select_verse_authority", "Selecione um versiculo para que a IA utilize como autoridade.")',
    '"Escreva a pergunta antes de enviar."': 't(trans, "messages.write_question_first", "Escreva a pergunta antes de enviar.")',
    '"Ollama esta offline. Por favor inicie o servidor."': 't(trans, "messages.ollama_offline_start", "Ollama esta offline. Por favor inicie o servidor.")',
    '"💬 Processando sua pergunta..."': 't(trans, "messages.generating_answer", "💬 Processando sua pergunta...")',
    '"✅ Resposta gerada e salva no histórico!"': 't(trans, "messages.answer_saved", "✅ Resposta gerada e salva no histórico!")',
    '"💭 Acesse a aba \'Histórico Chat\' para revisar suas conversas."': 't(trans, "messages.check_chat_tab", "💭 Acesse a aba \'Histórico Chat\' para revisar suas conversas.")',
    
    # Histórico de Sermões
    '"📋 Histórico de Sermões"': 't(trans, "headers.sermons_history", "📋 Histórico de Sermões")',
    '"🎤 Nenhum sermão gerado ainda. Use a aba \'Gerador Sermoes\' para criar seu primeiro sermão!"': 't(trans, "messages.no_sermons_yet", "🎤 Nenhum sermão gerado ainda. Use a aba \'Gerador Sermoes\' para criar seu primeiro sermão!")',
    '"🔍 Buscar sermões"': 't(trans, "labels.search_sermons", "🔍 Buscar sermões")',
    '"Tema, referência, conteúdo..."': 't(trans, "labels.search_sermons_placeholder", "Tema, referência, conteúdo...")',
    '"📅 Ordenar por"': 't(trans, "labels.order_by", "📅 Ordenar por")',
    '"Mais recentes"': 't(trans, "labels.most_recent_plural", "Mais recentes")',
    '"Mais antigos"': 't(trans, "labels.oldest_plural", "Mais antigos")',
    
    # Histórico de Devocionais
    '"🕊️ Histórico de Devocionais"': 't(trans, "headers.devotionals_history", "🕊️ Histórico de Devocionais")',
    '"🧘 Nenhum devocional gerado ainda. Use a aba \'Devocional & Meditacao\' para criar sua primeira meditação!"': 't(trans, "messages.no_devotionals_yet", "🧘 Nenhum devocional gerado ainda. Use a aba \'Devocional & Meditacao\' para criar sua primeira meditação!")',
    '"🔍 Buscar devocionais"': 't(trans, "labels.search_devotionals", "🔍 Buscar devocionais")',
    '"Sentimento, referência, conteúdo..."': 't(trans, "labels.search_devotionals_placeholder", "Sentimento, referência, conteúdo...")',
    
    # Histórico de Conversas
    '"💭 Histórico de Conversas"': 't(trans, "headers.conversations_history", "💭 Histórico de Conversas")',
    '"💬 Nenhuma conversa salva ainda. Use a aba \'Chat Teologico\' para fazer sua primeira pergunta!"': 't(trans, "messages.no_conversations_yet", "💬 Nenhuma conversa salva ainda. Use a aba \'Chat Teologico\' para fazer sua primeira pergunta!")',
    '"🔍 Buscar conversas"': 't(trans, "labels.search_conversations", "🔍 Buscar conversas")',
    '"Pergunta, resposta, referência..."': 't(trans, "labels.search_conversations_placeholder", "Pergunta, resposta, referência...")',
    
    # Import Data
    '"💡 Adicione arquivos .json de versões bíblicas nesta pasta e clique em \'Importar\'."': 't(trans, "messages.add_json_files", "💡 Adicione arquivos .json de versões bíblicas nesta pasta e clique em \'Importar\'.")',
    '"✅ Manter versões já importadas"': 't(trans, "labels.keep_existing", "✅ Manter versões já importadas")',
    '"Mesclar com versões existentes ao invés de substituir"': 't(trans, "labels.keep_existing_help", "Mesclar com versões existentes ao invés de substituir")',
    '"🔄 Importar Versões da Pasta"': 't(trans, "buttons.import_versions", "🔄 Importar Versões da Pasta")',
    '"💡 Crie a pasta e adicione arquivos JSON de versões bíblicas."': 't(trans, "messages.create_folder_add_json", "💡 Crie a pasta e adicione arquivos JSON de versões bíblicas.")',
    '"💡 Adicione arquivos JSON na pasta e tente novamente."': 't(trans, "messages.add_json_retry", "💡 Adicione arquivos JSON na pasta e tente novamente.")',
    '"🔄 A página será recarregada..."': 't(trans, "messages.page_will_reload", "🔄 A página será recarregada...")',
    '"ℹ️ Como Adicionar Versões Bíblicas"': 't(trans, "expanders.how_to_add_versions", "ℹ️ Como Adicionar Versões Bíblicas")',
}

# Aplicar substituições
for old, new in replacements.items():
    content = content.replace(old, new)

# Salvar o arquivo
with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Todas as strings hardcoded foram substituídas!")
print(f"Total de substituições: {len(replacements)}")
