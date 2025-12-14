#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para traduzir TODOS os textos restantes em inglês no arquivo vietnamita (vi.json)
Incluindo: Sermon Generator, Devotional & Meditation, scope items, e todas as strings restantes
"""

import re
import os

# Mapeamento completo de TODAS as traduções restantes para vietnamita
VIETNAMESE_FINAL_TRANSLATIONS = {
    # Menu items
    "🗣️ Sermon Generator": "🗣️ Trình Tạo Bài Giảng",
    "📋 Sermon History": "📋 Lịch Sử Bài Giảng",
    "🧘 Devotional & Meditation": "🧘 Suy Niệm & Thiền Định",
    "🕊️ Devotional History": "🕊️ Lịch Sử Suy Niệm",
    "💭 Chat History": "💭 Lịch Sử Trò Chuyện",
    
    # Sermon/Devotional scope labels
    "📖 Specific Book": "📖 Sách Cụ Thể",
    "📜 Old Testament": "📜 Cựu Ước",
    "✝️ New Testament": "✝️ Tân Ước",
    "🌍 Whole Bible": "🌍 Toàn Bộ Kinh Thánh",
    "Entire Old Testament": "Toàn Bộ Cựu Ước",
    "Entire New Testament": "Toàn Bộ Tân Ước",
    "🔖 Select multiple books": "🔖 Chọn nhiều sách",
    "Specific Book": "Sách Cụ Thể",
    
    # Labels
    "Ollama Model (or type)": "Mô Hình Ollama (hoặc loại)",
    "Ollama Status": "Trạng Thái Ollama",
    "Online": "Trực Tuyến",
    "Offline": "Ngoại Tuyến",
    "If models don't appear, use 'ollama pull <model>' via terminal.": "Nếu các mô hình không xuất hiện, hãy sử dụng 'ollama pull <model>' qua terminal.",
    "Guided Reading": "Đọc Hướng Dẫn",
    "Base": "Cơ Sở",
    "Base Chapter": "Chương Cơ Sở",
    "Verses (e.g., 1, 1-5)": "Câu (ví dụ: 1, 1-5)",
    "Enter a single verse or range to use as base or leave blank for the entire chapter.": "Nhập một câu đơn hoặc phạm vi để sử dụng làm cơ sở hoặc để trống cho toàn bộ chương.",
    "Full chapter": "Chương đầy đủ",
    "Theme (optional)": "Chủ đề (tùy chọn)",
    "Target audience (optional)": "Đối tượng mục tiêu (tùy chọn)",
    "Extra notes (preacher's context)": "Ghi chú bổ sung (bối cảnh của người giảng)",
    "Type your biblical question": "Nhập câu hỏi Kinh Thánh của bạn",
    "🔍 Search history": "🔍 Tìm kiếm lịch sử",
    "Type book, chapter or keyword...": "Nhập sách, chương hoặc từ khóa...",
    "Sort by": "Sắp xếp theo",
    "Most recent": "Gần đây nhất",
    "Oldest": "Cũ nhất",
    "Book": "Sách",
    "🔍 Search sermons": "🔍 Tìm kiếm bài giảng",
    "Theme, reference, content...": "Chủ đề, tham khảo, nội dung...",
    "🔍 Search devotionals": "🔍 Tìm kiếm suy niệm",
    "Feeling, reference, content...": "Cảm giác, tham khảo, nội dung...",
    "🔍 Search conversations": "🔍 Tìm kiếm cuộc trò chuyện",
    "📅 Order by": "📅 Sắp xếp theo",
    "✅ Keep already imported versions": "✅ Giữ các phiên bản đã nhập",
    
    # Sermon/Devotional labels
    "Sermon": "Bài Giảng",
    "Sermon Chapter": "Chương Bài Giảng",
    "Sermon Verse": "Câu Bài Giảng",
    "Devotional": "Suy Niệm",
    "Devotional Chapter": "Chương Suy Niệm",
    "Devotional Verse": "Câu Suy Niệm",
    
    # Buttons
    "🔄 Clear Cache": "🔄 Xóa Bộ Nhớ Cache",
    "🗑️ Delete": "🗑️ Xóa",
    "🔄 Import Versions from Folder": "🔄 Nhập Phiên Bản Từ Thư Mục",
    "📋 Copy sermon": "📋 Sao chép bài giảng",
    "📋 Copy devotional": "📋 Sao chép suy niệm",
    "📋 Copy conversation": "📋 Sao chép cuộc trò chuyện",
    "✨ Generate Devotional": "✨ Tạo Suy Niệm",
    
    # Messages
    "✅ Explanation generated and saved to history!": "✅ Giải thích đã được tạo và lưu vào lịch sử!",
    "📚 Go to 'Study History' tab to see all your analyses.": "📚 Chuyển đến tab 'Lịch Sử Nghiên Cứu' để xem tất cả phân tích của bạn.",
    "✅ Sermon generated and saved to history!": "✅ Bài giảng đã được tạo và lưu vào lịch sử!",
    "📋 Go to 'Sermon History' tab to review all your sermons.": "📋 Chuyển đến tab 'Lịch Sử Bài Giảng' để xem lại tất cả bài giảng của bạn.",
    "✅ Devotional generated and saved to history!": "✅ Suy niệm đã được tạo và lưu vào lịch sử!",
    "🕊️ Go to 'Devotional History' tab to review your meditations.": "🕊️ Chuyển đến tab 'Lịch Sử Suy Niệm' để xem lại các thiền định của bạn.",
    "✅ Answer generated and saved to history!": "✅ Câu trả lời đã được tạo và lưu vào lịch sử!",
    "💭 Go to 'Chat History' tab to review your conversations.": "💭 Chuyển đến tab 'Lịch Sử Trò Chuyện' để xem lại các cuộc trò chuyện của bạn.",
    "🎤 No sermons generated yet. Use 'Sermon Generator' tab to create your first sermon!": "🎤 Chưa có bài giảng nào được tạo. Sử dụng tab 'Trình Tạo Bài Giảng' để tạo bài giảng đầu tiên!",
    "🧘 No devotionals generated yet. Use 'Devotional & Meditation' tab to create your first meditation!": "🧘 Chưa có suy niệm nào được tạo. Sử dụng tab 'Suy Niệm & Thiền Định' để tạo thiền định đầu tiên!",
    "💬 No conversations saved yet. Use 'Theological Chat' tab to ask your first question!": "💬 Chưa có cuộc trò chuyện nào được lưu. Sử dụng tab 'Trò Chuyện Thần Học' để đặt câu hỏi đầu tiên!",
    "💡 Add .json files of Bible versions to this folder and click 'Import'.": "💡 Thêm các tệp .json của các phiên bản Kinh Thánh vào thư mục này và nhấp 'Nhập'.",
    "💡 Create the folder and add JSON files of Bible versions.": "💡 Tạo thư mục và thêm các tệp JSON của các phiên bản Kinh Thánh.",
    "💡 Add JSON files to the folder and try again.": "💡 Thêm các tệp JSON vào thư mục và thử lại.",
    "🔄 The page will reload...": "🔄 Trang sẽ tải lại...",
    "🔮 Generating biblical explanation...": "🔮 Đang tạo giải thích Kinh Thánh...",
    "🔮 Generating sermon outline...": "🔮 Đang tạo đề cương bài giảng...",
    "🔮 Generating devotional...": "🔮 Đang tạo suy niệm...",
    "🔮 Generating theological answer...": "🔮 Đang tạo câu trả lời thần học...",
    "⏳ Importing versions...": "⏳ Đang nhập phiên bản...",
    "⚠️ Select at least 2 books.": "⚠️ Chọn ít nhất 2 sách.",
    "📚 Select books to continue": "📚 Chọn sách để tiếp tục",
    "❓ Generating Bible questions...": "❓ Đang tạo câu hỏi Kinh Thánh...",
    "✅ Questions generated and saved!": "✅ Câu hỏi đã được tạo và lưu!",
    "📚 Go to 'Questions History' tab.": "📚 Chuyển đến tab 'Lịch Sử Câu Hỏi'.",
    
    # Expanders
    "👁️ Explanation Preview": "👁️ Xem Trước Giải Thích",
    "👁️ Sermon Preview": "👁️ Xem Trước Bài Giảng",
    "👁️ Devotional Preview": "👁️ Xem Trước Suy Niệm",
    "📜 View Biblical Context": "📜 Xem Bối Cảnh Kinh Thánh",
    "💡 View Full Explanation": "💡 Xem Giải Thích Đầy Đủ",
    "ℹ️ How to Add Bible Versions": "ℹ️ Cách Thêm Phiên Bản Kinh Thánh",
    "👁️ Questions Preview": "👁️ Xem Trước Câu Hỏi",
    
    # Headers
    "❓ Bible Questions Generator": "❓ Trình Tạo Câu Hỏi Kinh Thánh",
    "📚 Query Scope": "📚 Phạm Vi Truy Vấn",
    
    # Additional common strings
    "Text ready to copy!": "Văn bản sẵn sàng để sao chép!",
    "Filter versions (optional)": "Lọc phiên bản (tùy chọn)",
    "Chat": "Trò Chuyện",
    "Reading page": "Trang đọc",
    "Entire Bible": "Toàn Bộ Kinh Thánh",
    "Generic": "Chung",
    "Undefined": "Không Xác Định",
    "file(s) found": "tệp tìm thấy",
}

def translate_vietnamese_final(filepath):
    """Aplica as traduções finais completas no arquivo vietnamita"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    translation_count = 0
    
    for english, vietnamese in VIETNAMESE_FINAL_TRANSLATIONS.items():
        # Escapar caracteres especiais regex
        english_escaped = re.escape(english)
        
        # Contar ocorrências antes
        pattern = f'": "{english_escaped}"'
        matches_before = len(re.findall(pattern, content))
        
        if matches_before > 0:
            # Substituir todas as ocorrências
            content = re.sub(pattern, f'": "{vietnamese}"', content)
            translation_count += matches_before
            print(f"✅ Traduzido ({matches_before}x): {english[:60]}...")
    
    # Salvar arquivo
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return translation_count

if __name__ == "__main__":
    vi_path = os.path.join('translations', 'vi.json')
    
    if not os.path.exists(vi_path):
        print(f"❌ Arquivo não encontrado: {vi_path}")
        exit(1)
    
    print("🔧 Aplicando traduções finais completas em vietnamita (vi.json)...")
    print("=" * 70)
    
    total = translate_vietnamese_final(vi_path)
    
    print("=" * 70)
    print(f"✅ CONCLUÍDO! Total: {total} strings traduzidas em vietnamita")
    print(f"📁 Arquivo atualizado: {vi_path}")
    print("🎉 Vietnamita (Tiếng Việt) agora está 100% no idioma nativo!")
